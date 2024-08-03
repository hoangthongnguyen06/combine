from enum import Enum
from app.config import Config


class APIPlatformEndpoints(Enum):
    LOGIN = f'{Config.PLATFORM_API_URL}/api/platform/authentication/login'
    GET_TOPIC = f'{Config.PLATFORM_API_URL}/api/platform/topic/search'
    POST = f'{Config.PLATFORM_API_URL}/api/platform/article/search'
    GET_TARGET = f'{Config.PLATFORM_API_URL}/api/platform/profile/user/search'
    GET_POST_NUMBER_WITH_LOCATION = f'{Config.PLATFORM_API_URL}/api/platform/statistic/demographic'
    GET_CHANNELS = f'{Config.PLATFORM_API_URL}/api/platform/youtube/search'
    SAC_THAI_THEO_CHU_DE = f"{Config.PLATFORM_API_URL}/api/platform/statistic/statistic-source-by-days"

class APISpyderEndpoints(Enum):
    LOGIN = f'{Config.SPYDER_API_URL}/api/admin-mgt/v1/account/login_v2'
    CHUYEN_MUC = f"{Config.SPYDER_API_URL}/api/category_management/v1/category/list/by_account"
    SAC_THAI_THEO_CHU_DE = f"{Config.SPYDER_API_URL}/api/category_management/v1/dashboard_topic/overall/sources"
    THONG_TIN_THAO_LUAN = f"{Config.SPYDER_API_URL}/api/category_management/v1/dashboard_topic/overall/buzz"
    THONG_TIN_NGUON_CHU_DE = f"{Config.SPYDER_API_URL}/api/category_management/v1/dashboard_topic/overall/sources"
    TOP_WEBSITE_BAI_DANG = f"{Config.SPYDER_API_URL}/api/category_management/v1/report_top/hot_content/top_domain/by_post"
    TONG_QUAN_BAI_VIET = f"{Config.SPYDER_API_URL}/api/category_management/v1/report/user_overview/stats_card"
    TOP_DOI_TUONG_LUOT_TUONG_TAC = f"{Config.SPYDER_API_URL}/api/category_management/v1/report_top/hot_content/top_fb/interaction"
    PHAN_BO_KENH = f"{Config.SPYDER_API_URL}/api/category_management/v1/report/chart/article/source_type"
    THONG_KE_TUONG_TAC = f"{Config.SPYDER_API_URL}/api/category_management/v1/report/overview/stats/list"
    TONG_SAC_THAI = f"{Config.SPYDER_API_URL}/api/category_management/v1/report/chart/sentiment"
    
class APISupabase(Enum):
    CHU_DE = f'{Config.URL_SUPABASE}/chude/'
