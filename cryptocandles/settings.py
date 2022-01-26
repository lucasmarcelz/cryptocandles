import logging

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_host: str = Field(..., env='SMARTTBOT_TEST_DATABASE_HOST')
    database_user: str = Field(..., env='SMARTTBOT_TEST_DATABASE_USER')
    database_password: str = Field(..., env='SMARTTBOT_TEST_DATABASE_PASSWORD')
    database_name: str = Field(..., env='SMARTTBOT_TEST_DATABASE_NAME')
    database_port: int = Field(..., env='SMARTTBOT_TEST_DATABASE_PORT')
    url_api_poloniex: str = Field("https://poloniex.com/public?command=returnTicker",
                                  env='SMARTTBOT_TEST_URL_API_POLONIEX')


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
settings = Settings()
