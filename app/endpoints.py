from enum import Enum
from app.config import Config

class APIPlatformEndpoints(Enum):
    LOGIN = f'{Config.PLATFORM_API_URL}/api/platform/authentication/login'
    GET_TOPIC = f'{Config.PLATFORM_API_URL}/api/platform/topic/search'
    POST = f'{Config.PLATFORM_API_URL}/api/platform/article/search'
    GET_TARGET = F'{Config.PLATFORM_API_URL}/api/platform/profile/user/search'
    GET_POST_NUMBER_WITH_LOCATION = F'{Config.PLATFORM_API_URL}/api/platform/statistic/demographic'
    
class APISiderEndpoints(Enum):
    LOGIN = f''