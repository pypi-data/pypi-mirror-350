from typing import Optional, Dict, Any
import json
from datetime import datetime, timezone
import asyncio
import aiosqlite

DB_PATH = "bot.db"


class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    async def initialize(self):
        if not self._initialized:
            self.connection = await aiosqlite.connect(DB_PATH)
            await self._create_tables()
            self._initialized = True

    async def _create_tables(self):
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS api_message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                type TEXT NOT NULL,
                api_id TEXT NOT NULL,
                cache_data TEXT,             -- e.g., 'manga', 'chapter', 'page', 'post',
                current_page INTEGER DEFAULT 0,
                last_api_update TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
        """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS general_message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                type TEXT NOT NULL,
                cache_data TEXT,            -- e.g., 'general', 'warning', 'debug', 'admin', 'system', 'scrapper'
                current_page INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
        """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mugen_uuid INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
        """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS mangas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kitsu_id INTEGER,
                kuma_url TEXT 
                manga_id TEXT NOT NULL,
                type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
        """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS readlist (
                manga_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT,
                score INTEGER,
                review TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            );
        """
        )
        await self.connection.commit()

    async def close(self):
        if self._initialized:
            await self.connection.close()
            self._initialized = False

    # API Message Operations
    async def insert_api_message(
        self,
        message_id: str,
        channel_id: str,
        user_id: str,
        message_type: str,
        api_id: str,
        cache_data: Optional[Dict[str, Any]] = None,
        current_page: int = 0,
    ) -> int:
        cache_json = json.dumps(cache_data) if cache_data else None
        cursor = await self.connection.execute(
            """
            INSERT INTO api_message (
                message_id, channel_id, user_id, type, api_id, cache_data, current_page
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message_id,
                channel_id,
                user_id,
                message_type,
                api_id,
                cache_json,
                current_page,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def get_api_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        async with self.connection.execute(
            "SELECT * FROM api_message WHERE message_id = ?", (message_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return self._row_to_dict_api_message(row)
            return None

    async def update_api_message_cache(
        self,
        message_id: str,
        cache_data: Optional[Dict[str, Any]] = None,
        current_page: Optional[int] = None,
        update_api_timestamp: bool = True,
    ) -> bool:
        now = datetime.now(timezone.utc).isoformat()

        query: str
        params: tuple[Any, ...]

        if cache_data is not None and current_page is not None:
            cache_json = json.dumps(cache_data)
            query = """
                UPDATE api_message 
                SET cache_data = ?, current_page = ?, updated_at = ?, last_api_update = ?
                WHERE message_id = ?
            """
            params = (
                cache_json,
                current_page,
                now,
                now if update_api_timestamp else None,
                message_id,
            )
        elif cache_data is not None:
            cache_json = json.dumps(cache_data)
            query = """
                UPDATE api_message 
                SET cache_data = ?, updated_at = ?, last_api_update = ?
                WHERE message_id = ?
            """
            params = (
                cache_json,
                now,
                now if update_api_timestamp else None,
                message_id,
            )
        elif current_page is not None:
            query = """
                UPDATE api_message 
                SET current_page = ?, updated_at = ?, last_api_update = ?
                WHERE message_id = ?
            """
            params = (
                current_page,
                now,
                now if update_api_timestamp else None,
                message_id,
            )
        else:
            # Se ambos são None, apenas atualiza o timestamp se necessário
            if update_api_timestamp:
                query = """
                    UPDATE api_message 
                    SET updated_at = ?, last_api_update = ?
                    WHERE message_id = ?
                """
                params = (now, now, message_id)
            else:
                return False  # Nada para atualizar

        cursor = await self.connection.execute(query, params)
        await self.connection.commit()
        return cursor.rowcount > 0

    async def delete_api_message(self, message_id: str) -> bool:
        cursor = await self.connection.execute(
            "DELETE FROM api_message WHERE message_id = ?", (message_id,)
        )
        await self.connection.commit()
        return cursor.rowcount > 0

    # General Message Operations
    async def insert_general_message(
        self,
        message_id: str,
        channel_id: str,
        user_id: str,
        message_type: str,
        cache_data: Optional[Dict[str, Any]] = None,
        current_page: int = 0,
    ) -> int:
        cache_json = json.dumps(cache_data) if cache_data else None
        cursor = await self.connection.execute(
            """
            INSERT INTO general_message (
                message_id, channel_id, user_id, type, cache_data, current_page
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (message_id, channel_id, user_id, message_type, cache_json, current_page),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def get_general_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        async with self.connection.execute(
            "SELECT * FROM general_message WHERE message_id = ?", (message_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return self._row_to_dict_general_message(row)
            return None

    async def update_general_message(
        self,
        message_id: str,
        cache_data: Optional[Dict[str, Any]] = None,
        current_page: Optional[int] = None,
    ) -> bool:
        now = datetime.now(timezone.utc).isoformat()

        query: str
        params: tuple[Any, ...]

        if cache_data is not None and current_page is not None:
            cache_json = json.dumps(cache_data)
            query = """
                UPDATE general_message 
                SET cache_data = ?, current_page = ?, updated_at = ?
                WHERE message_id = ?
            """
            params = (cache_json, current_page, now, message_id)
        elif cache_data is not None:
            cache_json = json.dumps(cache_data)
            query = """
                UPDATE general_message 
                SET cache_data = ?, updated_at = ?
                WHERE message_id = ?
            """
            params = (cache_json, now, message_id)
        elif current_page is not None:
            query = """
                UPDATE general_message 
                SET current_page = ?, updated_at = ?
                WHERE message_id = ?
            """
            params = (current_page, now, message_id)
        else:
            return False

        cursor = await self.connection.execute(query, params)
        await self.connection.commit()
        return cursor.rowcount > 0

    async def delete_general_message(self, message_id: str) -> bool:
        cursor = await self.connection.execute(
            "DELETE FROM general_message WHERE message_id = ?", (message_id,)
        )
        await self.connection.commit()
        return cursor.rowcount > 0

    # Utility Methods
    def _row_to_dict_api_message(self, row) -> Dict[str, Any]:
        return {
            "id": row[0],
            "message_id": row[1],
            "channel_id": row[2],
            "user_id": row[3],
            "type": row[4],
            "api_id": row[5],
            "cache_data": json.loads(row[6]) if row[6] else None,
            "current_page": row[7],
            "last_api_update": row[8],
            "created_at": row[9],
            "updated_at": row[10],
        }

    def _row_to_dict_general_message(self, row) -> Dict[str, Any]:
        return {
            "id": row[0],
            "message_id": row[1],
            "channel_id": row[2],
            "user_id": row[3],
            "type": row[4],
            "cache_data": json.loads(row[5]) if row[5] else None,
            "current_page": row[6],
            "created_at": row[7],
            "updated_at": row[8],
        }


# Example usage
async def main():
    db_manager = DBManager()
    await db_manager.initialize()

    try:
        # API Message example
        api_msg_id = await db_manager.insert_api_message(
            message_id="msg123",
            channel_id="channel456",
            user_id="user789",
            message_type="manga",
            api_id="manga123",
            cache_data={"title": "One Piece", "chapter": 1050},
            current_page=1,
        )
        print(f"Inserted API message with ID: {api_msg_id}")

        # General Message example
        general_msg_id = await db_manager.insert_general_message(
            message_id="msg456",
            channel_id="channel789",
            user_id="user123",
            message_type="warning",
            cache_data={"text": "This is a warning message"},
            current_page=0,
        )
        print(f"Inserted General message with ID: {general_msg_id}")

        # Fetch and print messages
        api_msg = await db_manager.get_api_message("msg123")
        print("API Message:", api_msg)

        general_msg = await db_manager.get_general_message("msg456")
        print("General Message:", general_msg)

    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
