import asyncio
import websockets
import json
from datetime import datetime
import aiofiles
import aiosqlite
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

WEBSOCKET_SERVER = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8765))

DB_PATH = os.getenv("SQLITE_DB_PATH", "logs/log_db.sqlite3")
LOG_FILE = "logs/server.log"
os.makedirs("logs", exist_ok=True)


async def save_to_file(log_data: str):
    async with aiofiles.open(LOG_FILE, mode='a') as f:
        await f.write(log_data + '\n')


async def save_to_db(conn, json_data: dict):
    await conn.execute('''
        INSERT INTO logs (timestamp, service, level, message)
        VALUES (?, ?, ?, ?)
    ''', (
        json_data.get('timestamp'),
        json_data.get('service'),
        json_data.get('level'),
        json_data.get('message')
    ))
    await conn.commit()


async def init_db(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            service TEXT,
            level TEXT,
            message TEXT
        )
    ''')
    await conn.commit()


async def log_handler(websocket, db_conn):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                data['timestamp'] = datetime.now().isoformat()

                await save_to_file(json.dumps(data))
                await save_to_db(db_conn, data)

                logger.info(f"✅ \t- {data.get('service')} - {data.get('message')}")
            except Exception as e:
                logger.error(f"❌ \tError handling message: {e}")
    except websockets.ConnectionClosed:
        logger.warning("❌ \tClient disconnected.")


async def main():
    async with aiosqlite.connect(DB_PATH) as db_conn:
        await init_db(db_conn)
        async with websockets.serve(lambda ws: log_handler(ws, db_conn), WEBSOCKET_SERVER, WEBSOCKET_PORT):
            print(f"🟢 \tLogging server started at ws://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}")
            await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
