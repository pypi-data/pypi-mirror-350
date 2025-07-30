from typing import Dict, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Osdental.Exception.ControlledException import DatabaseException
from Osdental.Shared.Utils.DataUtils import DataUtils
from Osdental.Shared.Code import Code
from Osdental.Shared.Message import Message

class Connection:

    _instances: Dict[str, 'Connection'] = {}

    def __new__(cls, db_url: str):
        if db_url not in cls._instances:
            cls._instances[db_url] = super(Connection, cls).__new__(cls)
        return cls._instances[db_url]

    def __init__(self, db_url: str):
        if not hasattr(self, 'initialized'):
            self.engine = create_async_engine(
                db_url,
                pool_size=20,          
                max_overflow=40,       
                pool_timeout=30,       
                pool_recycle=3600     
            )
            self.session_factory = sessionmaker(
                bind=self.engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )
            self.initialized = True

    async def get_session(self) -> AsyncSession:
        return self.session_factory()

    async def execute_query_return_first_value(self, query:str, params:Dict[str,str] = None) -> str:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                value = result.scalar()
                return DataUtils.normalize_uuid_value(value)

    async def execute_query_return_data(self, query:str, params:Dict[str,str] = None, fetchone=False) -> List[Dict[str,str]] | Dict[str,str]:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                keys = result.keys()
                if fetchone:
                    row = result.fetchone()
                    return DataUtils.normalize_uuids_dict(dict(zip(keys, row))) if row else {}
                
                rows = result.fetchall()
                return [DataUtils.normalize_uuids_dict(dict(zip(keys, row))) for row in rows] if rows else []

    async def execute_query_return_message(self, query:str, params:Dict[str,str] = None, code:str = Code.PROCESS_SUCCESS_CODE) -> str:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                row = result.fetchone() 
                if not row:
                    raise DatabaseException(message=Message.NO_RESULTS_FOUND_MSG, error=Message.NO_RESULTS_FOUND_MSG)
                
                if row.STATUS_CODE != code:
                    raise DatabaseException(message=row.STATUS_MESSAGE, error=row.STATUS_MESSAGE, status_code=row.STATUS_CODE)

                return row.STATUS_MESSAGE
                
    async def execute_query(self, query:str, params:Dict[str,str] = None, code:str = None) -> None | Dict[str,str]:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                if code:
                    row = result.fetchone()
                    if not row:
                        raise DatabaseException(message=Message.NO_RESULTS_FOUND_MSG, error=Message.NO_RESULTS_FOUND_MSG)

                    if row.STATUS_CODE != code:
                        raise DatabaseException(message=row.STATUS_MESSAGE, error=row.STATUS_MESSAGE, status_code=row.STATUS_CODE)

                    return DataUtils.normalize_uuids_dict(dict(zip(result.keys(), row)))
                
                return None

    
    async def close_engine(self) -> None:
        """Dispose of the engine and remove instance."""
        if self.engine:
            await self.engine.dispose() 
        
        if self.db_url in self._instances:
            del self._instances[self.db_url]