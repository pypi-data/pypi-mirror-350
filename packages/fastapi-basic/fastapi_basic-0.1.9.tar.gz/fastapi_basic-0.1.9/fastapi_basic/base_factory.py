from abc import ABCMeta, abstractmethod
from functools import lru_cache
import os, dotenv

import watchtower
from celery import Celery
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool
import logging

from .const import LOG_DEFAULT_LOGGER_NAME, LOG_FMT, CELERY_CONFIG
from .ext.aws import init_app as init_aws_app
from .exception.base_exception import InternalBaseException
from .utils import update_dict_with_cast

class BaseFactory(metaclass=ABCMeta):
    @abstractmethod
    @lru_cache()
    def get_app_config(self):
        """
        Each factory should define what config it wants.
        """

    def __load_local_config(self):
        dotenv.load_dotenv(dotenv_path='.env', override=True)
        update_dict_with_cast(self.get_app_config(), os.environ)

    def __setup_main_logger(self, app, logger_name=LOG_DEFAULT_LOGGER_NAME, level=logging.DEBUG):
        logger = self.__setup_logger(app, logger_name, level)
        app.logger = logger

    def __setup_logger(self, app, logger_name, level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(LOG_FMT))
        logger.addHandler(stream_handler)
        return logger

    def __setup_aws_cloud_log(self, app):
        if app.state.aws_session and app.state.config.get("AWS_LOGGROUP_NAME"):
            logs_client = app.state.aws_session.client("logs")
            watchtower_handler = watchtower.CloudWatchLogHandler(
                log_group_name=app.state.config.get("AWS_LOGGROUP_NAME"),
                boto3_client=logs_client, create_log_group=True)
            watchtower_handler.setFormatter(logging.Formatter(LOG_FMT))
            app.logger.addHandler(watchtower_handler)

    def __setup_celery_app(self, app):
        if not all([app.state.config.get(key) for key in CELERY_CONFIG]):
            app.logger.info("Lack Celery config keys, ignore get Celery_app")
            return None

        app.state.celery_app = Celery(
            app.state.config.get("CELERY_APP"),
            broker=app.state.config.get("CELERY_BROKER_URL"),
            backend=app.state.config.get("CELERY_BACKEND_URL")
        )

    def create_app(self):
        """
        Create an application instance.
        """
        self.__load_local_config()
        app_config = self.get_app_config()
        app = FastAPI(docs_url=app_config.get('DOCS_URL'), redoc_url=app_config.get('REDOC_URL'), openapi_url=app_config.get('OPENAPI_URL'))
        app.state.config = app_config

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.__setup_main_logger(app, logger_name=app.state.config.get('LOGGER_NAME', LOG_DEFAULT_LOGGER_NAME), level=logging.DEBUG)
        app.state.aws_session = init_aws_app(app)
        self.__setup_aws_cloud_log(app)

        self.__setup_celery_app(app)

        @app.exception_handler(InternalBaseException)
        async def http_exception_handler(request: Request, exc: InternalBaseException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "code": exc.detail["code"],
                    "message": exc.detail["message"],
                    "data": exc.detail["data"]
                }
            )

        @app.middleware("http")
        async def handle_request_headers(request: Request, call_next):
            body = await request.body()
            form = await request.form()
            app.logger.info(f"request.url: {request.url}, method: {request.method}, headers: {request.headers}, body: {body}, form: {form}")
            response = await call_next(request)
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            if response_body:
                app.logger.info(f"response_body: {response_body[0].decode()}")
            return response

        return app
