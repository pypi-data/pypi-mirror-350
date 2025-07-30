import copy
from flask import Flask
from seatools.ioc import Bean
from seatools.ioc.config import cfg


@Bean(lazy=False)
def flask() -> Flask:
    """fastapi bean."""
    config = cfg()
    if 'seatools' in config and 'flask' in config['seatools']:
        config = config['seatools']['flask']
        if not isinstance(config, dict):
            config = {}
    else:
        config = {}
    config = copy.deepcopy(config)
    # none support
    for k, v in config.items():
        if v and isinstance(v, str) and v.lower() == 'none':
            config[k] = None

    # set default import_name
    if 'import_name' not in config:
        config['import_name'] = 'seatools.ioc.server.app'

    return Flask(**config)
