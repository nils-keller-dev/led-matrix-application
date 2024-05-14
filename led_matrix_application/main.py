from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from led_matrix_controller import LEDMatrixController
from api import routes as api_routes

led_matrix_controller = LEDMatrixController()
led_matrix_controller.fill(0, 255, 0)

WEBSERVER_DIR = "webapp"
routes = [
    Mount("/api", routes=api_routes),
    Mount("/", app=StaticFiles(directory=WEBSERVER_DIR, html=True), name=WEBSERVER_DIR),
]

app = Starlette(routes=routes)