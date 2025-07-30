from __future__ import annotations

import uuid
from typing import TypeVar, Type, Generic, Optional, List, Dict, Literal, Union, Sequence, Any, Iterable
from sqlalchemy import select, delete, update, and_, func, desc, inspect, or_, asc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, InstrumentedAttribute, selectinload, RelationshipProperty, Load

from rb_commons.http.exceptions import NotFoundException
from rb_commons.orm.exceptions import DatabaseException, InternalException

ModelType = TypeVar('ModelType', bound=declarative_base())

class Q:
    """Boolean logic container that can be combined with `&`, `|`, and `~`."""

    def __init__(self, **lookups: Any) -> None:
        self.lookups: Dict[str, Any] = lookups
        self.children: List[Q] = []
        self._operator: str = "AND"
        self.negated: bool = False

    def _combine(self, other: "Q", operator: str) -> "Q":
        combined = Q()
        combined.children = [self, other]
        combined._operator = operator
        return combined

    def __or__(self, other: "Q") -> "Q":
        return self._combine(other, "OR")

    def __and__(self, other: "Q") -> "Q":
        return self._combine(other, "AND")

    def __invert__(self) -> "Q":
        clone = Q()
        clone.lookups = self.lookups.copy()
        clone.children = list(self.children)
        clone._operator = self._operator
        clone.negated = not self.negated
        return clone

    def __repr__(self) -> str:
        if self.lookups:
            base = f"Q({self.lookups})"
        else:
            base = "Q()"
        if self.children:
            base += f" {self._operator} {self.children}"
        if self.negated:
            base = f"NOT({base})"
        return base

def with_transaction_error_handling(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as e:
            await self.session.rollback()
            raise InternalException(f"Constraint violation: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(f"Database error: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise InternalException(f"Unexpected error: {str(e)}") from e
    return wrapper

class BaseManager(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
        self.filters: List[Any] = []
        self._filtered: bool = False
        self._limit: Optional[int] = None
        self._order_by: List[Any] = []

    async def _smart_commit(self, instance: Optional[ModelType] = None) -> Optional[ModelType]:
        if not self.session.in_transaction():
            await self.session.commit()
        if instance is not None:
            await self.session.refresh(instance)
            return instance
        return None

    def _parse_lookup(self, lookup: str, value: Any):
        parts = lookup.split("__")
        operator = "eq"
        if parts[-1] in {"eq", "ne", "gt", "lt", "gte", "lte", "in", "contains", "null"}:
            operator = parts.pop()

        current: Union[Type[ModelType], InstrumentedAttribute] = self.model
        # walk relationships
        for field in parts:
            attr = getattr(current, field, None)
            if attr is None:
                raise ValueError(f"Invalid filter field: {'.'.join(parts)}")
            if hasattr(attr, "property") and isinstance(attr.property, RelationshipProperty):
                current = attr.property.mapper.class_
            else:
                current = attr

        if operator == "eq":
            return current == value
        if operator == "ne":
            return current != value
        if operator == "gt":
            return current > value
        if operator == "lt":
            return current < value
        if operator == "gte":
            return current >= value
        if operator == "lte":
            return current <= value
        if operator == "in":
            if not isinstance(value, (list, tuple, set)):
                raise ValueError(f"{lookup}__in requires an iterable")
            return current.in_(value)
        if operator == "contains":
            return current.ilike(f"%{value}%")
        if operator == "null":
            return current.is_(None) if value else current.isnot(None)
        raise ValueError(f"Unsupported operator in lookup: {lookup}")

    def _q_to_expr(self, q: Q):
        clauses: List[Any] = [self._parse_lookup(k, v) for k, v in q.lookups.items()]
        for child in q.children:
            clauses.append(self._q_to_expr(child))
        combined = (
            True
            if not clauses
            else (or_(*clauses) if q._operator == "OR" else and_(*clauses))
        )
        return ~combined if q.negated else combined

    def _loader_from_path(self, path: str) -> Load:
        """
        Turn 'attributes.attribute.attribute_group' into
        selectinload(Product.attributes)
            .selectinload(Attribute.attribute)
            .selectinload(ProductAttributeGroup.attribute_group)
        """
        parts = path.split(".")
        current_model = self.model
        loader = None

        for segment in parts:
            attr = getattr(current_model, segment, None)
            if attr is None or not hasattr(attr, "property"):
                raise ValueError(f"Invalid relationship path: {path!r}")

            loader = selectinload(attr) if loader is None else loader.selectinload(attr)
            current_model = attr.property.mapper.class_  # step down the graph

        return loader

    def order_by(self, *columns: Any):
        """Collect ORDER BY clauses.
        """
        for col in columns:
            if isinstance(col, str):
                descending = col.startswith("-")
                field_name = col.lstrip("+-")
                sa_col = getattr(self.model, field_name, None)
                if sa_col is None:
                    raise ValueError(f"Invalid order_by field '{field_name}' for {self.model.__name__}")
                self._order_by.append(sa_col.desc() if descending else sa_col.asc())
            else:
                self._order_by.append(col)

        return self

    def filter(self, *expressions: Any, **lookups: Any) -> "BaseManager[ModelType]":
        """Add **AND** constraints (default behaviour).

        * `expressions` can be raw SQLAlchemy clauses **or** `Q` objects.
        * `lookups` are Django‑style keyword filters.
        """
        self._filtered = True
        for expr in expressions:
            self.filters.append(self._q_to_expr(expr) if isinstance(expr, Q) else expr)
        for k, v in lookups.items():
            self.filters.append(self._parse_lookup(k, v))
        return self

    def or_filter(self, *expressions: Any, **lookups: Any) -> "BaseManager[ModelType]":
        """Add one OR group (shortcut for `filter(Q() | Q())`)."""
        or_clauses: List[Any] = []
        for expr in expressions:
            or_clauses.append(self._q_to_expr(expr) if isinstance(expr, Q) else expr)
        for k, v in lookups.items():
            or_clauses.append(self._parse_lookup(k, v))
        if or_clauses:
            self._filtered = True
            self.filters.append(or_(*or_clauses))
        return self

    def limit(self, value: int) -> "BaseManager[ModelType]":
        self._limit = value
        return self

    def _apply_eager_loading(self, stmt, load_all_relations: bool = False):
        if not load_all_relations:
            return stmt
        opts: List[Any] = []
        visited: set[Any] = set()

        def recurse(model, loader=None):
            mapper = inspect(model)
            if mapper in visited:
                return
            visited.add(mapper)
            for rel in mapper.relationships:
                attr = getattr(model, rel.key)
                this_loader = selectinload(attr) if loader is None else loader.selectinload(attr)
                opts.append(this_loader)
                recurse(rel.mapper.class_, this_loader)

        recurse(self.model)
        return stmt.options(*opts)

    async def _execute_query(self, stmt, load_all_relations: bool):
        stmt = self._apply_eager_loading(stmt, load_all_relations)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return list({obj.id: obj for obj in rows}.values())

    def _reset_state(self):
        self.filters.clear()
        self._filtered = False
        self._limit = None

    async def all(self, load_all_relations: bool = False):
        stmt = select(self.model)
        if self.filters:
            stmt = stmt.filter(and_(*self.filters))
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        if self._limit:
            stmt = stmt.limit(self._limit)
        try:
            return await self._execute_query(stmt, load_all_relations)
        finally:
            self._reset_state()

    async def first(self, load_relations: Optional[Sequence[str]] = None):
        self._ensure_filtered()
        stmt = select(self.model).filter(and_(*self.filters))
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))
        result = await self.session.execute(stmt)
        self._reset_state()
        return result.scalars().first()


    async def last(self, load_relations: Optional[Sequence[str]] = None):
        self._ensure_filtered()
        stmt = select(self.model).filter(and_(*self.filters))
        order = self._order_by or [self.model.id.desc()]
        stmt = stmt.order_by(*order[::-1])  # reverse for LAST
        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))
        result = await self.session.execute(stmt)
        self._reset_state()
        return result.scalars().first()

    async def count(self) -> int | None:
        self._ensure_filtered()

        stmt = select(func.count(self.model.id)).select_from(self.model)
        if self.filters:
            stmt = stmt.where(and_(*self.filters))

        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def paginate(self, limit=10, offset=0, load_all_relations=False):
        self._ensure_filtered()
        stmt = select(self.model).filter(and_(*self.filters))
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        stmt = stmt.limit(limit).offset(offset)
        try:
            return await self._execute_query(stmt, load_all_relations)
        finally:
            self._reset_state()

    @with_transaction_error_handling
    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return await self._smart_commit(obj)

    @with_transaction_error_handling
    async def save(self, instance: ModelType):
        self.session.add(instance)
        await self.session.flush()
        return await self._smart_commit(instance)

    @with_transaction_error_handling
    async def lazy_save(self, instance: ModelType, load_relations: Sequence[str] = None) -> Optional[ModelType]:
        self.session.add(instance)
        await self.session.flush()
        await self._smart_commit(instance)

        if load_relations is None:
            mapper = inspect(self.model)
            load_relations = [rel.key for rel in mapper.relationships]

        if not load_relations:
            return instance

        stmt = select(self.model).filter_by(id=instance.id)

        for rel in load_relations:
            stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)
        loaded_instance = result.scalar_one_or_none()

        if loaded_instance is None:
            raise NotFoundException(
                message="Object saved but could not be retrieved with relationships",
                status=404,
                code="0001",
            )

        return loaded_instance

    @with_transaction_error_handling
    async def update(self, instance: ModelType, **fields):
        if not fields:
            raise InternalException("No fields provided for update")
        for k, v in fields.items():
            setattr(instance, k, v)
        self.session.add(instance)
        await self._smart_commit()
        return instance

    @with_transaction_error_handling
    async def update_by_filters(self, filters: Dict[str, Any], **fields):
        if not fields:
            raise InternalException("No fields provided for update")
        stmt = update(self.model).filter_by(**filters).values(**fields)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get(**filters)

    @with_transaction_error_handling
    async def delete(self, instance: Optional[ModelType] = None):
        if instance is not None:
            await self.session.delete(instance)
            await self.session.commit()
            return True
        self._ensure_filtered()
        stmt = delete(self.model).where(and_(*self.filters))
        await self.session.execute(stmt)
        await self.session.commit()
        self._reset_state()
        return True

    @with_transaction_error_handling
    async def bulk_save(self, instances: Iterable[ModelType]):
        if not instances:
            return
        self.session.add_all(list(instances))
        await self.session.flush()
        if not self.session.in_transaction():
            await self.session.commit()

    @with_transaction_error_handling
    async def bulk_delete(self):
        self._ensure_filtered()
        stmt = delete(self.model).where(and_(*self.filters))
        result = await self.session.execute(stmt)
        await self._smart_commit()
        self._reset_state()
        return result.rowcount

    async def get(
            self,
            pk: Union[str, int, uuid.UUID],
            load_relations: Optional[Sequence[str]] = None,
    ):
        stmt = select(self.model).filter_by(id=pk)
        if load_relations:
            for rel in load_relations:
                loader = (
                    self._loader_from_path(rel) if "." in rel
                    else selectinload(getattr(self.model, rel))
                )
                stmt = stmt.options(loader)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            raise NotFoundException("Object does not exist", 404, "0001")
        return instance

    async def is_exists(self):
        self._ensure_filtered()

        stmt = select(self.model).filter(and_(*self.filters))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def has_relation(self, relation_name: str):
        relationship = getattr(self.model, relation_name)
        subquery = (
            select(1)
            .select_from(relationship.property.mapper.class_)
            .where(relationship.property.primaryjoin)
            .exists()
        )
        self.filters.append(subquery)
        self._filtered = True
        return self

    def sort_by(self, tokens: Sequence[str]) -> "BaseManager[ModelType]":
        """
        Dynamically apply ORDER BY clauses based on a list of "field" or "-field" tokens.
        """
        model = self.model

        for tok in tokens:
            if not tok:
                continue
            direction = desc if tok.startswith("-") else asc
            name = tok.lstrip("-")
            col = getattr(model, name, None)
            if col is None:
                raise InternalException(f"Cannot sort by unknown field '{name}'")

            self._order_by.append(direction(col))

        return self

    def model_to_dict(self, instance: ModelType, exclude: set[str] | None = None):
        exclude = exclude or set()
        return {
            col.key: getattr(instance, col.key)
            for col in inspect(instance).mapper.column_attrs
            if col.key not in exclude
        }

    def _ensure_filtered(self):
        if not self._filtered:
            raise RuntimeError("You must call `filter()` before this operation.")

