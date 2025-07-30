from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    # Swagger docs config
    DOCS_URL: str|None = '/docs'
    REDOC_URL: str|None = '/redoc'
    OPENAPI_URL: str|None = '/openapi.json'

    # Logging config
    LOGGER_NAME: str|None = 'uvicorn'

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = ""
    AWS_PARAMETER_PATH_PREFIX: str = ""
    AWS_LOGGROUP_NAME: str = ""

    # Celery config
    CELERY_APP: str|None = ""
    CELERY_BROKER_URL: str|None = ""
    CELERY_BACKEND_URL: str|None = ""