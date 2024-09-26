import logging
import datetime

from aiohttp.typedefs import Handler

from keystone_scim.util import ThreadSafeSingleton
from keystone_scim.util.config import Config
from keystone_scim.util.exc import UnauthorizedRequest

from aiohttp import web


CONFIG = Config()
LOGGER = logging.getLogger(__name__)


@web.middleware
async def save_request(request: web.Request, handler: Handler):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_data = {
        "timestamp": timestamp,
        "method": request.method,
        "path": request.path,
        "headers": dict(request.headers),
        "query_params": dict(request.query),
        "body": await request.text(),
    }
    with open("request.log", "a") as file:
        file.write(str(request_data) + "\n")
    return await handler(request)
