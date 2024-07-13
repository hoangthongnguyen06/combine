from enum import Enum
from app.config import Config

class APIPlatformEndpoints(Enum):
    LOGIN = f'{Config.PLATFORM_API_URL}/api/platform/authentication/login'