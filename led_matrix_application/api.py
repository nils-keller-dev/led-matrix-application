from starlette.routing import Route
from starlette.responses import JSONResponse
from database import Database

db = Database()

async def get_state():
    state = db.get_state()
    return JSONResponse(state)

async def patch_state(request):
    state = await request.json()
    db.patch_state(state)
    return JSONResponse(db.get_state())

routes = [
    Route("/state", endpoint=get_state, methods=["GET"]),
    Route("/state", endpoint=patch_state, methods=["PATCH"]),
]