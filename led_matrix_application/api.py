import os

from database import Database
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route

db = Database()


async def get_state(_):
    state = db.get_state()
    return JSONResponse(state)


async def patch_state(request):
    state = await request.json()
    db.patch_state(state)
    return JSONResponse(db.get_state())


async def get_images(_):
    stripped_list = []
    for file in os.listdir("images"):
        if not file.startswith("."):
            stripped_list.append(file)
    return JSONResponse({"images": stripped_list})


async def get_image(request):
    return FileResponse(f"images/{request.path_params['image']}")


async def post_image(request):
    form = await request.form()
    image = form.get("image")
    with open(f"images/{image.filename}", "wb") as buffer:
        buffer.write(await image.read())
    return JSONResponse({"image": image.filename})


async def delete_image(request):
    image = request.path_params["image"]
    try:
        os.remove(f"images/{image}")
        return JSONResponse({"image": image})
    except FileNotFoundError:
        return JSONResponse({"error": "Image not found"}, status_code=404)


routes = [
    Route("/state", endpoint=get_state, methods=["GET"]),
    Route("/state", endpoint=patch_state, methods=["PATCH"]),
    Route("/images", endpoint=get_images, methods=["GET"]),
    Route("/image/{image}", endpoint=get_image, methods=["GET"]),
    Route("/image", endpoint=post_image, methods=["POST"]),
    Route("/image/{image}", endpoint=delete_image, methods=["DELETE"]),
]
