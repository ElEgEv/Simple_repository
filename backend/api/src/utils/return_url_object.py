from fastapi.responses import FileResponse, JSONResponse
# from src.database.models import Images
from config import Config
config = Config()
    
def return_simple_url_object(image_url: str) -> str:
    return (f"http://{config.__getattr__('HOST')}:{config.__getattr__('SERVER_PORT')}/{image_url}")
