from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from mrkutil.pagination.sqlalchemy import apaginate


class BaseManager:
    MODEL = None

    def __init__(self, session: AsyncSession):
        if not self.MODEL:
            raise Exception("Please setup the current DB Model.")
        self.db = session

    async def get_all(self):
        return select(self.MODEL)

    async def get_single(self, filters={}):
        query = await self.get_filtered(filters=filters)
        obj = await self.db.scalars(query)
        return obj.first()

    async def create(self, obj_dict):
        obj = self.MODEL(**obj_dict)
        self.db.add(obj)
        await self.db.commit()
        return await self.get_single({"id": obj.id})

    async def update(self, obj: MODEL, obj_dict):
        for key, value in obj_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        await self.db.commit()
        return await self.get_single({"id": obj.id})

    async def delete(self, obj):
        self.db.delete(obj)
        await self.db.commit()
        return True

    async def get_filtered(self, filters):
        pk = filters.get("id")
        filter_options = (self.MODEL.id == pk if pk else True,)
        filtered = await self.get_all()
        filtered = filtered.filter(*filter_options)
        return filtered

    async def get_paginated(
        self, filters, page, size, direction, sort_by
    ):
        query = await self.get_filtered(filters)
        paginated_query = await apaginate(
            query=query,
            session=self.db,
            page_number=page,
            page_size=size,
            direction=direction,
            sort_by=sort_by,
            format_to_dict=False,
        )
        return paginated_query
