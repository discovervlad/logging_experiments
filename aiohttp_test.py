from aiohttp import web
from aiohttp.web_log import AccessLogger
import logging

from aiohttp_request_id_logging import (
    setup_logging_request_id_prefix,
    request_id_middleware,
    RequestIdContextAccessLogger)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-14s %(levelname)s: %(requestIdPrefix)s%(message)s')

setup_logging_request_id_prefix()

@web.middleware
async def request_logger(request, handler):
    logger.info(f"Request Text: {await request.text()}")
    response = await handler(request)
    logger.info(f"Response Text: {response.text}")
    return response

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application(middlewares=[request_id_middleware(), request_logger])
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app, access_log_class=RequestIdContextAccessLogger,
    access_log_format=AccessLogger.LOG_FORMAT.replace(' %t ', ' ') + ' %Tf')
