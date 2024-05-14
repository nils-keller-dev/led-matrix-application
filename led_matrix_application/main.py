from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from controller import led_matrix_controller
from api import routes as api_routes
import threading
from database import Database

WEBSERVER_DIR = "webapp"
routes = [
    Mount("/api", routes=api_routes),
    Mount("/", app=StaticFiles(directory=WEBSERVER_DIR, html=True), name=WEBSERVER_DIR),
]
 
app = Starlette(routes=routes)

db = Database()
led_matrix_controller.update_state(db.get_state())
threading.Thread(target=led_matrix_controller.run).start()