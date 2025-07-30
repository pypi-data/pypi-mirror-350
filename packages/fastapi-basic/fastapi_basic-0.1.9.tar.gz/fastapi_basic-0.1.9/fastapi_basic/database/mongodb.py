from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, username: str, password: str, host: str, port: int, db_name: str, ssl: str=None, ssl_ca_certs: str=None):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.ssl = ssl
        self.ssl_ca_certs = ssl_ca_certs

    async def connect(self, document_models: list):
        db_settings = dict(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            retryWrites=False
        )
        if self.ssl:
            db_settings["ssl"] = self.ssl

        if self.ssl_ca_certs and self.ssl_ca_certs != "":
            db_settings["tlsCAFile"] = self.ssl_ca_certs

        self.client = AsyncIOMotorClient(**db_settings)
        await init_beanie(database=self.client[self.db_name], document_models=document_models)