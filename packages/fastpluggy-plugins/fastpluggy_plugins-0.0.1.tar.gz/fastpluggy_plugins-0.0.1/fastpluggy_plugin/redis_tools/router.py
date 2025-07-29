# redis_browser.py

import redis
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse

from fastpluggy.core.dependency import get_templates

from .redis_connector import RedisConnection, get_redis_connection

# Create router
redis_router = APIRouter()


# Define routes
@redis_router.get("/", response_class=HTMLResponse, name="redis_browser")
async def redis_browser(request: Request, templates=Depends(get_templates)):
    return templates.TemplateResponse("redis_tools/browser.html.j2", {
        "request": request,
        "base_plugin_url": str(request.url_for("redis_browser"))[:-1]
    })

@redis_router.get("/databases")
async def get_databases(redis_conn: RedisConnection = Depends(get_redis_connection)):
    """Get a list of all available Redis databases."""
    return redis_conn.get_databases()

@redis_router.post("/databases/{db_index}")
async def select_database(db_index: int, redis_conn: RedisConnection = Depends(get_redis_connection)):
    """Select a Redis database."""
    success = redis_conn.select_db(db_index)
    return {"success": success, "db_index": db_index}

@redis_router.get("/keys")
async def get_keys(
    pattern: str = "*", 
    db: int = Query(None, description="Database index to use"),
):
    redis_conn: RedisConnection = get_redis_connection(db=db)

    return redis_conn.get_keys(pattern)

@redis_router.get("/keys/{key}")
async def get_key(
    key: str, 
    db: int = Query(None, description="Database index to use"),
):
    redis_conn: RedisConnection = get_redis_connection(db=db)

    return redis_conn.get_key_details(key)

@redis_router.delete("/keys/{key}")
async def delete_key(
    key: str, 
    db: int = Query(None, description="Database index to use"),
):
    redis_conn: RedisConnection = get_redis_connection(db=db)
    success = redis_conn.delete_key(key)
    return {"success": success}

@redis_router.post("/flush-db")
async def flush_db(
    db: int = Query(None, description="Database index to use"),
):
    redis_conn: RedisConnection = get_redis_connection(db=db)
    success = redis_conn.flush_db()
    return {"success": success}
