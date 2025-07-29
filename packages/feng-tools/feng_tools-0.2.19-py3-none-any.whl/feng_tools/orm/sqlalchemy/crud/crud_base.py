from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Sequence
from datetime import datetime, date, time
from sqlalchemy import select, update, delete, and_, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func, false
from sqlalchemy.orm import InstrumentedAttribute

T = TypeVar('T', bound='Model')


class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        增强版通用CRUD工具类

        :param model: SQLAlchemy模型类（继承自Model基类）
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[T]:
        """根据主键ID获取单条记录（自动过滤已删除记录）"""
        result = await db.execute(
            select(self.model).where(
                and_(
                    self.model.id == id,
                    self.model.deleted == false()
                )
            )
        )
        return result.scalars().first()

    async def get_by_where(
        self,
        db: AsyncSession,
        *whereclause: Any,
        order_by: Optional[Any] = None
    ) -> Optional[T]:
        """
        根据条件查询单条记录

        :param whereclause: SQLAlchemy 条件表达式
        :param order_by: 排序条件
        :return: 符合条件的第一条记录
        """
        query = select(self.model).where(
            and_(
                *whereclause,
                self.model.deleted == false()
            )
        )

        if order_by is not None:
            query = query.order_by(order_by)

        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_field(
        self,
        db: AsyncSession,
        field: Union[str, InstrumentedAttribute],
        value: Any,
        case_sensitive: bool = True
    ) -> Optional[T]:
        """
        根据字段值查询单条记录

        :param field: 字段名或SQLAlchemy字段对象
        :param value: 字段值
        :param case_sensitive: 是否区分大小写（仅对字符串字段有效）
        """
        field_obj = getattr(self.model, field) if isinstance(field, str) else field

        if isinstance(value, str) and not case_sensitive:
            condition = func.lower(field_obj) == func.lower(value)
        else:
            condition = field_obj == value

        return await self.get_by_where(db, condition)

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        where_clause: Optional[list] = None,
        order_by: Optional[Any] = None
    ) -> List[T]:
        """
        获取多条记录（支持分页、条件过滤和排序）

        :param skip: 跳过的记录数
        :param limit: 返回的最大记录数
        :param where_clause: 过滤条件列表
        :param order_by: 排序条件
        """
        query = select(self.model).where(self.model.deleted == false())

        if where_clause:
            query = query.where(and_(*where_clause))

        if order_by is not None:
            query = query.order_by(order_by)
        else:
            # 默认排序：按order_num降序，id降序
            query = query.order_by(
                self.model.order_num.desc(),
                self.model.id.desc()
            )

        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: Union[Dict[str, Any], T]) -> T:
        """创建单条记录"""
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.to_dict()

        # 移除可能存在的id字段（自增主键）
        create_data.pop("id", None)

        db_obj = self.model(**create_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_bulk(
        self,
        db: AsyncSession,
        objs_in: List[Union[Dict[str, Any], T]],
        *,
        commit: bool = True
    ) -> List[T]:
        """
        批量创建记录

        :param objs_in: 要创建的记录列表（字典或模型实例）
        :param commit: 是否立即提交事务
        :return: 创建的模型实例列表
        """
        db_objs = []
        for obj_in in objs_in:
            if isinstance(obj_in, dict):
                create_data = obj_in.copy()
            else:
                create_data = obj_in.to_dict()

            create_data.pop("id", None)
            db_obj = self.model(**create_data)
            db.add(db_obj)
            db_objs.append(db_obj)

        if commit:
            await db.commit()
            for db_obj in db_objs:
                await db.refresh(db_obj)

        return db_objs

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: T,
        obj_in: Union[Dict[str, Any], T],
        exclude_unset: bool = False
    ) -> T:
        """更新单条记录"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.to_dict(exclude_unset=exclude_unset)

        # 移除不能更新的字段
        update_data.pop("id", None)
        update_data.pop("created_at", None)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_bulk(
        self,
        db: AsyncSession,
        objs_in: List[Union[Dict[str, Any], T]],
        *,
        commit: bool = True
    ) -> List[T]:
        """
        批量更新记录

        :param objs_in: 要更新的记录列表（必须包含id字段）
        :param commit: 是否立即提交事务
        :return: 更新后的模型实例列表
        """
        updated_objs = []
        for obj_in in objs_in:
            if isinstance(obj_in, dict):
                update_data = obj_in.copy()
            else:
                update_data = obj_in.to_dict()

            obj_id = update_data.get("id")
            if not obj_id:
                raise ValueError("批量更新记录必须包含id字段")

            db_obj = await self.get(db, id=obj_id)
            if not db_obj:
                raise ValueError(f"{self.model.__name__} ID {obj_id} 不存在")

            # 移除不能更新的字段
            update_data.pop("id", None)
            update_data.pop("created_at", None)

            for field in update_data:
                setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            updated_objs.append(db_obj)

        if commit:
            await db.commit()
            for db_obj in updated_objs:
                await db.refresh(db_obj)

        return updated_objs

    async def save(
        self,
        db: AsyncSession,
        obj_in: Union[Dict[str, Any], T],
        *,
        commit: bool = True
    ) -> T:
        """
        智能保存（根据主键ID自动判断是新增还是更新）

        :param obj_in: 要保存的数据（字典或模型实例）
        :param commit: 是否立即提交事务
        :return: 保存后的模型实例
        """
        if isinstance(obj_in, dict):
            data = obj_in.copy()
        else:
            data = obj_in.to_dict()

        obj_id = data.get("id")

        if obj_id:
            # 存在ID，执行更新操作
            db_obj = await self.get(db, id=obj_id)
            if db_obj:
                return await self.update(db, db_obj=db_obj, obj_in=data, commit=commit)

        # 不存在ID或找不到对应记录，执行新增操作
        return await self.create(db, obj_in=data, commit=commit)

    async def save_bulk(
        self,
        db: AsyncSession,
        objs_in: List[Union[Dict[str, Any], T]],
        *,
        commit: bool = True
    ) -> List[T]:
        """
        批量智能保存（自动判断新增或更新）

        :param objs_in: 要保存的记录列表
        :param commit: 是否立即提交事务
        :return: 保存后的模型实例列表
        """
        saved_objs = []
        for obj_in in objs_in:
            saved_obj = await self.save(db, obj_in=obj_in, commit=False)
            saved_objs.append(saved_obj)

        if commit:
            await db.commit()
            for db_obj in saved_objs:
                await db.refresh(db_obj)

        return saved_objs

    async def remove(self, db: AsyncSession, *, id: int) -> T:
        """软删除单条记录"""
        db_obj = await self.get(db, id)
        if not db_obj:
            raise ValueError(f"{self.model.__name__} ID {id} 不存在")

        db_obj.deleted = True
        db_obj.deleted_at = func.now()
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def remove_bulk(
        self,
        db: AsyncSession,
        ids: List[int],
        *,
        commit: bool = True
    ) -> List[T]:
        """批量软删除记录"""
        removed_objs = []
        for obj_id in ids:
            db_obj = await self.get(db, id=obj_id)
            if db_obj:
                db_obj.deleted = True
                db_obj.deleted_at = func.now()
                db.add(db_obj)
                removed_objs.append(db_obj)

        if commit:
            await db.commit()

        return removed_objs

    async def hard_remove(self, db: AsyncSession, *, id: int) -> None:
        """硬删除单条记录"""
        await db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await db.commit()

    async def hard_remove_bulk(
        self,
        db: AsyncSession,
        ids: List[int],
        *,
        commit: bool = True
    ) -> None:
        """批量硬删除记录"""
        await db.execute(
            delete(self.model).where(self.model.id.in_(ids))
        )
        if commit:
            await db.commit()

    async def toggle_enable(self, db: AsyncSession, *, id: int) -> T:
        """切换启用状态"""
        db_obj = await self.get(db, id)
        if not db_obj:
            raise ValueError(f"{self.model.__name__} ID {id} 不存在")

        db_obj.is_enable = not db_obj.is_enable
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def count(
        self,
        db: AsyncSession,
        whereclause: Optional[list] = None
    ) -> int:
        """统计记录数量（可带条件）"""
        query = select(func.count()).select_from(self.model).where(
            self.model.deleted == false()
        )

        if whereclause:
            query = query.where(and_(*whereclause))

        result = await db.execute(query)
        return result.scalar_one()

    async def exists(self, db: AsyncSession, *, id: int) -> bool:
        """检查记录是否存在"""
        result = await db.execute(
            select(self.model.id).where(
                and_(
                    self.model.id == id,
                    self.model.deleted == false()
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_where(
        self,
        db: AsyncSession,
        *whereclause: Any
    ) -> bool:
        """根据条件检查记录是否存在"""
        query = select(self.model.id).where(
            and_(
                *whereclause,
                self.model.deleted == false()
            )
        ).limit(1)

        result = await db.execute(query)
        return result.scalar_one_or_none() is not None