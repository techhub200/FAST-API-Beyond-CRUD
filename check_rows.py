from src.config import engine
from sqlalchemy import text

conn = engine.connect()
print(conn.execute(text('SELECT count(*) FROM auth_user')).scalar())
print(conn.execute(text('SELECT "User_id", "Username", email FROM auth_user ORDER BY "User_id" DESC LIMIT 5')).fetchall())
conn.close()
