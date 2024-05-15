from database import Database
from starlette.responses import JSONResponse
from starlette.routing import Route

db = Database()


async def get_state(request):
    state = db.get_state()
    return JSONResponse(state)


async def patch_state(request):
    state = await request.json()
    db.patch_state(state)
    return JSONResponse(db.get_state())


async def get_images(request):
    return JSONResponse({"images": ["http://example.com/image.png"]})


routes = [
    Route("/state", endpoint=get_state, methods=["GET"]),
    Route("/state", endpoint=patch_state, methods=["PATCH"]),
    Route("/images", endpoint=get_images, methods=["GET"]),
]
