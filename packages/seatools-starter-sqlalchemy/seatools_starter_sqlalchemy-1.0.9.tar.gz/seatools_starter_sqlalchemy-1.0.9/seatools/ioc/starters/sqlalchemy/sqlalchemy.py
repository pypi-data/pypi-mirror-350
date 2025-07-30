from typing import Optional
from seatools.ioc.config import cfg
from seatools.ioc.base import get_bean_factory
from seatools.ioc.injects import Bean
from seatools.sqlalchemy.utils import new_client
from seatools.utils.dict_utils import deep_update
from loguru import logger
from seatools.sqlalchemy.dbconfig import CommonDBConfig


class SqlalchemyDBConfig(CommonDBConfig):
    config: Optional[dict] = None


@Bean
def init_db_beans():
    db_config, sqlalchemy_config = None, None
    config = cfg()
    if 'seatools' in config and 'datasource' in config['seatools']:
        db_config = config['seatools']['datasource']
    # Backward compatibility with old configuration
    elif 'db' in config:
        db_config = config['db']

    # Backward compatibility with old sqlalchemy configuration
    sqlalchemy_config = (config.get('seatools') or {}).get('sqlalchemy') or config.get('sqlalchemy')

    if not db_config:
        logger.warning(
            'Configuration [seatools.datasource] does not exist, unable to automatically initialize database bean instances.')
        return
    if not isinstance(db_config, dict):
        logger.error(
            'Configuration [seatools.datasource] property is not of dict type, unable to automatically initialize database bean instances.')
        exit(1)
    bean_factory = get_bean_factory()
    for name, v in db_config.items():
        config = SqlalchemyDBConfig(**v)
        if config.config:
            if not sqlalchemy_config:
                sqlalchemy_config = config.config
            else:
                sqlalchemy_config = deep_update(sqlalchemy_config, config.config)
        elif config.sqlalchemy:
            if not sqlalchemy_config:
                sqlalchemy_config = config.sqlalchemy
            else:
                sqlalchemy_config = deep_update(sqlalchemy_config, config.sqlalchemy)
        client = new_client(config, config=sqlalchemy_config)
        # Register bean, not a lazy registration
        bean_factory.register_bean(name=config.name or name, cls=client, primary=config.primary, lazy=False)
