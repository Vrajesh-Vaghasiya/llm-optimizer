# import environ
# import os
#
# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
# environ.Env.read_env()
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# if env.bool('DJANGO_READ_DOT_ENV_FILE', default=True):
#     env_file = str(os.path.join(BASE_DIR, '.env'))
#     if os.path.exists(env_file):
#         env.read_env(env_file)
#
# WAFERMAP_DB_CONNECTION_NAME = env('WAFERMAP_DB_CONNECTION_NAME', default='postgres')
#
# API_SCHEME = env('API_SCHEME')
# API_DOMAIN = env('API_DOMAIN')
PATHS = {
    'TASK_PATH': '/api/task',
}

HTTPS_CERTIFICATE_LOCATION = "HTTPS_CERTIFICATE_LOCATION"

API_RETRY_COUNT = 5
API_BACKOFF_FACTOR = 0.5
API_STATUS_FORCE_LIST = '429,500,501,502,503,504'
