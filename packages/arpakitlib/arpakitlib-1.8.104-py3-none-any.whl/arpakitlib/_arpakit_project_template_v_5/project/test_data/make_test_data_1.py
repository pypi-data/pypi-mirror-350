import asyncio
import logging

from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM, UserDBM, UserTokenDBM

_logger = logging.getLogger(__name__)


def make_test_data_1():
    setup_logging()

    get_cached_settings().raise_if_prod_mode()

    get_cached_sqlalchemy_db().reinit()

    with get_cached_sqlalchemy_db().new_session() as session:

        for i in range(1000):
            api_key = ApiKeyDBM(value=str(i + 1))
            session.add(api_key)
            _logger.info(api_key)
        session.commit()

        arpakit_user = UserDBM(
            email="arpakit@gmail.com",
            username="arpakit",
            roles=[UserDBM.Roles.client, UserDBM.Roles.admin],
            is_active=True,
            is_verified=True,
            password="123",
            tg_id=269870432
        )
        session.add(arpakit_user)
        session.commit()
        _logger.info(arpakit_user)

        for i in range(1000):
            user_token_dbm = UserTokenDBM(user_id=arpakit_user.id, value=str(i))
            session.add(user_token_dbm)
            _logger.info(user_token_dbm)
        session.commit()


async def async_make_test_data_1():
    get_cached_settings().raise_if_prod_mode()


def __example():
    make_test_data_1()


async def __async_example():
    await async_make_test_data_1()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
