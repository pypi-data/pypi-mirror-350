import copy
from fastapi import FastAPI
from seatools.ioc import Bean
from seatools.ioc.config import cfg


@Bean(lazy=False)
def fastapi() -> FastAPI:
    """fastapi bean."""
    config = cfg()
    if 'seatools' in config and 'fastapi' in config['seatools']:
        config = config['seatools']['fastapi']
        if not isinstance(config, dict):
            config = {}
    else:
        config = {}
    config = copy.deepcopy(config)
    # none support
    for k, v in config.items():
        if v and isinstance(v, str) and v.lower() == 'none':
            config[k] = None

    return FastAPI(**config)
