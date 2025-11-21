import threading

from api import create_routes
from database import Database
from led_matrix_controller import LEDMatrixController
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from state_manager import StateManager

WEBSERVER_DIR = "webapp"

led_matrix_controller = LEDMatrixController()
state_manager = StateManager(Database(), led_matrix_controller)

routes = [
    Mount("/api", routes=create_routes(state_manager)),
    Mount("/", app=StaticFiles(directory=WEBSERVER_DIR, html=True), name=WEBSERVER_DIR),
]

app = Starlette(routes=routes)

threading.Thread(target=led_matrix_controller.run).start()
