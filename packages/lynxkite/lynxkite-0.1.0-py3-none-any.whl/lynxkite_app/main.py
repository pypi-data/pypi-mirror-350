"""The FastAPI server for serving the LynxKite application."""

import shutil
import pydantic
import fastapi
import importlib
import pathlib
import pkgutil
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
import starlette
from lynxkite.core import ops
from lynxkite.core import workspace
from . import crdt


def detect_plugins():
    plugins = {}
    for _, name, _ in pkgutil.iter_modules():
        if name.startswith("lynxkite_"):
            print(f"Importing {name}")
            plugins[name] = importlib.import_module(name)
    if not plugins:
        print("No LynxKite plugins found. Be sure to install some!")
    return plugins


lynxkite_plugins = detect_plugins()
ops.save_catalogs("plugins loaded")

app = fastapi.FastAPI(lifespan=crdt.lifespan)
app.include_router(crdt.router)
app.add_middleware(GZipMiddleware)


@app.get("/api/catalog")
def get_catalog(workspace: str):
    ops.load_user_scripts(workspace)
    return {k: {op.name: op.model_dump() for op in v.values()} for k, v in ops.CATALOGS.items()}


class SaveRequest(workspace.BaseConfig):
    path: str
    ws: workspace.Workspace


data_path = pathlib.Path()


def save(req: SaveRequest):
    path = data_path / req.path
    assert path.is_relative_to(data_path), f"Path '{path}' is invalid"
    req.ws.save(path)


@app.post("/api/save")
async def save_and_execute(req: SaveRequest):
    save(req)
    if req.ws.has_executor():
        await req.ws.execute()
        save(req)
    return req.ws


@app.post("/api/delete")
async def delete_workspace(req: dict):
    json_path: pathlib.Path = data_path / req["path"]
    crdt_path: pathlib.Path = data_path / ".crdt" / f"{req['path']}.crdt"
    assert json_path.is_relative_to(data_path), f"Path '{json_path}' is invalid"
    json_path.unlink()
    crdt_path.unlink()


@app.get("/api/load")
def load(path: str):
    path = data_path / path
    assert path.is_relative_to(data_path), f"Path '{path}' is invalid"
    if not path.exists():
        return workspace.Workspace()
    return workspace.Workspace.load(path)


class DirectoryEntry(pydantic.BaseModel):
    name: str
    type: str


def _get_path_type(path: pathlib.Path) -> str:
    if path.is_dir():
        return "directory"
    elif path.suffixes[-2:] == [".lynxkite", ".json"]:
        return "workspace"
    else:
        return "file"


@app.get("/api/dir/list")
def list_dir(path: str):
    path = data_path / path
    assert path.is_relative_to(data_path), f"Path '{path}' is invalid"
    return sorted(
        [
            DirectoryEntry(
                name=str(p.relative_to(data_path)),
                type=_get_path_type(p),
            )
            for p in path.iterdir()
            if not p.name.startswith(".")
        ],
        key=lambda x: (x.type != "directory", x.name.lower()),
    )


@app.post("/api/dir/mkdir")
def make_dir(req: dict):
    path = data_path / req["path"]
    assert path.is_relative_to(data_path), f"Path '{path}' is invalid"
    assert not path.exists(), f"{path} already exists"
    path.mkdir()


@app.post("/api/dir/delete")
def delete_dir(req: dict):
    path: pathlib.Path = data_path / req["path"]
    assert all([path.is_relative_to(data_path), path.exists(), path.is_dir()]), (
        f"Path '{path}' is invalid"
    )
    shutil.rmtree(path)


@app.get("/api/service/{module_path:path}")
async def service_get(req: fastapi.Request, module_path: str):
    """Executors can provide extra HTTP APIs through the /api/service endpoint."""
    module = lynxkite_plugins[module_path.split("/")[0]]
    return await module.api_service_get(req)


@app.post("/api/service/{module_path:path}")
async def service_post(req: fastapi.Request, module_path: str):
    """Executors can provide extra HTTP APIs through the /api/service endpoint."""
    module = lynxkite_plugins[module_path.split("/")[0]]
    return await module.api_service_post(req)


@app.post("/api/upload")
async def upload(req: fastapi.Request):
    """Receives file uploads and stores them in DATA_PATH."""
    form = await req.form()
    for file in form.values():
        file_path = data_path / "uploads" / file.filename
        assert file_path.is_relative_to(data_path), f"Path '{file_path}' is invalid"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"status": "ok"}


@app.post("/api/execute_workspace")
async def execute_workspace(name: str):
    """Trigger and await the execution of a workspace."""
    room = await crdt.ws_websocket_server.get_room(name)
    ws_pyd = workspace.Workspace.model_validate(room.ws.to_py())
    await crdt.execute(name, room.ws, ws_pyd)


class SPAStaticFiles(StaticFiles):
    """Route everything to index.html. https://stackoverflow.com/a/73552966/3318517"""

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (
            fastapi.HTTPException,
            starlette.exceptions.HTTPException,
        ) as ex:
            if ex.status_code == 404:
                return await super().get_response(".", scope)
            else:
                raise ex


static_dir = SPAStaticFiles(packages=[("lynxkite_app", "web_assets")], html=True)
app.mount("/", static_dir, name="web_assets")
