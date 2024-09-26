import logging
import datetime

from aiohttp.typedefs import Handler

# from keystone_scim.util import ThreadSafeSingleton
from keystone_scim.util.config import Config
# from keystone_scim.util.exc import UnauthorizedRequest
# from keystone_scim.store import BaseStore, RDBMSStore
from keystone_scim.store import mysql_store

from aiohttp import web


CONFIG = Config()
LOGGER = logging.getLogger(__name__)

db_engine = mysql_store.MySqlStore("logs")

@web.middleware
async def save_request(request: web.Request, handler: Handler):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_data = {
        "timestamp": str(timestamp),
        "method": str(request.method),
        "path": str(request.path),
        "headers": str(dict(request.headers)),
        "query_params": str(dict(request.query)),
        "body": await request.text(),
    }
    
    await db_engine.create_request_log(request_data)
           
    # with open("request.log", "a") as file:
    #     file.write(str(request_data) + "\n")
        
    return await handler(request)
