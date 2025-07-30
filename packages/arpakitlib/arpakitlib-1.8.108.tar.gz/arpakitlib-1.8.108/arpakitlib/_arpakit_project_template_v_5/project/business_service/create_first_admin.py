import logging

from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

_logger = logging.getLogger(__name__)


def create_first_admin():
    with get_cached_sqlalchemy_db().new_session() as session:
        user_dbm = (
            session
            .query(UserDBM)
            .filter(UserDBM.roles.any(UserDBM.Roles.admin))
            .first()
        )
        if user_dbm is not None:
            _logger.info("first admin already exists")
            return
        user_dbm = UserDBM(
            username="admin",
            roles=[UserDBM.Roles.client, UserDBM.Roles.admin],
            password="admin",
        )
        session.add(user_dbm)
        session.commit()
        _logger.info("first admin was created")


def command():
    setup_logging()
    create_first_admin()


if __name__ == '__main__':
    command()
