from application.config import settings
from application.server import ApiServer
from presentation.api.routers.file_router import FileRouter

media_manager_app = ApiServer(
    name=settings.NAME,
    routers=[FileRouter().api_router],
    start_callbacks=[],
    stop_callbacks=[],
).app
