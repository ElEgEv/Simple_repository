from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse

import src.core.repository
from src.utils.custom_logging import setup_logging
from config import Config

from src.routers.user_router import router as user_router
from src.routers.user_auto_router import router as user_auto_router
from src.routers.brand_router import router as brand_router
from src.routers.model_router import router as model_router
from src.routers.generation_router import router as generation_router
from src.routers.engine_router import router as engine_router
from src.routers.gas_station_operator_router import router as gas_station_operator_router
from src.routers.gas_station_router import router as gas_station_router
from src.routers.favorite_route_router import router as favorite_route_router
from src.routers.map_router import router as map_router


app = FastAPI(
    title="Mobile gas station API", 
    description="Данная API предназначена для работы информационно-поискового картографического сервиса", 
    version="1.0.1",
)

favicon_path = './favicon.ico'
config = Config()
log = setup_logging()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/public", StaticFiles(directory=Path("./public")), name="public")

# common section
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")

@app.get("/hello")
def hello_from_api():
    return {"message" : "Hello!"}


# routers section
app.include_router(user_router)

app.include_router(user_auto_router)

app.include_router(brand_router)

app.include_router(model_router)

app.include_router(generation_router)

app.include_router(engine_router)

app.include_router(gas_station_operator_router)

app.include_router(gas_station_router)

app.include_router(favorite_route_router)

app.include_router(map_router)


if __name__ == "__main__":
    import logging
    import uvicorn
    import yaml

    uvicorn_log_config = 'logging.yaml'

    with open(uvicorn_log_config, 'r') as f:
        uvicorn_config = yaml.safe_load(f.read())
        logging.config.dictConfig(uvicorn_config)

    if config.__getattr__("DEBUG") == "TRUE":
        reload = True
    elif config.__getattr__("DEBUG") == "FALSE":
        reload = False
    else:
        raise Exception("Not init debug mode in env file")
    
    uvicorn.run("main:app", 
                host=config.__getattr__("HOST"), 
                port=int(config.__getattr__("SERVER_PORT")),
                # log_config=uvicorn_log_config,
                # reload=reload
            )