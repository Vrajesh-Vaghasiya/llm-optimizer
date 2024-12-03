import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if env.bool('DJANGO_READ_DOT_ENV_FILE', default=True):
    env_file = str(os.path.join(BASE_DIR, '.env'))
    if os.path.exists(env_file):
        env.read_env(env_file)

WAFERMAP_DB_CONNECTION_NAME = env('WAFERMAP_DB_CONNECTION_NAME', default='postgres')

API_SCHEME = env('API_SCHEME')
API_DOMAIN = env('API_DOMAIN')
PATHS = {
    'TASK_PATH': env('TASK_PATH'),
}

HTTPS_CERTIFICATE_LOCATION = env("HTTPS_CERTIFICATE_LOCATION", default=None)

API_RETRY_COUNT = env('API_RETRY_COUNT', default=5)
API_BACKOFF_FACTOR = env('API_BACKOFF_FACTOR', default=0.5)
API_STATUS_FORCE_LIST = env('API_STATUS_FORCE_LIST', default='429,500,501,502,503,504')
