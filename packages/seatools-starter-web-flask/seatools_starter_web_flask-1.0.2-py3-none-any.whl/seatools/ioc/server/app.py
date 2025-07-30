from seatools.ioc import Autowired
from flask import Flask


def wsgi_app():
    """server wsgi app factory."""
    # Get Flask instance from value
    return Autowired(cls=Flask).value


def asgi_app():
    """server asgi app factory."""
    # base on uvicorn
    from uvicorn.middleware.wsgi import WSGIMiddleware
    app = wsgi_app()
    return WSGIMiddleware(app)
