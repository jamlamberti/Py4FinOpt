from common import config
CACHE_CONFIG = config.Section('cache')
DB_CONFIG = None


def __setup_connections(cache_config):
    db_mgr = None
    if cache_config.get('cache-impl') == 'mysql':
        # pylint: disable=ungrouped-imports, wrong-import-position
        from common import mysql_manager as db_mgr
        db_config = config.Section('mysql')

    else:
        # pylint: disable=ungrouped-imports, wrong-import-position
        from common import sqlite_manager as db_mgr
        db_config = config.Section('sqlite')
    return db_config, db_mgr


# Need to expose db_mgr properly
DB_CONFIG, db_mgr = __setup_connections(CACHE_CONFIG)
