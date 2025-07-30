from seatools.ioc import Autowired
from fastapi import FastAPI


def asgi_app():
    """server app factory."""
    # Get FastAPI instance from value
    return Autowired(cls=FastAPI).value

