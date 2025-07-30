# Seatools Flask Starter

This framework must be used in conjunction with the `seatools-starter-server-*` packages, using `seatools-starter-server-uvicorn` as an example here.

[中文文档](./README_zh.md)

## Usage Guide
1. Install with `poetry add flask seatools-starter-server-uvicorn seatools-starter-web-flask`
2. Configure `config/application.yml` as follows:
```yaml
seatools:
  server:
    # Here are the uvicorn parameter configurations
    uvicorn:
      host: 0.0.0.0
      port: 8000
      workers: 1
      reload: true
  # Here are the Flask configurations
  flask:
    # Consistent with Flask parameters
    import_name: seatools.ioc.server.app
    static_folder: static
    template_folder: templates
    ...
```
3. Usage, load by defining ioc container functions

```python
import abc
from seatools.ioc import Autowired, Bean
from flask import Flask

# Add route
from flask import Flask

@Bean
def api_controller(app: Flask):
    @app.get('/')
    def hello():
        return 'hello flask'

class Service(abc.ABC):
    
    def hello(self):
        raise NotImplementedError

# Flask integration with seatools ioc injection
@Bean
class ServiceA(Service):

    def hello(self):
        return "serviceA"

@Bean
def a2_router(app: Flask, service: Service):  # Specific injection method see seatools

    @app.get('/service')
    def service():
        return service.hello() # return hello flask
```
3. Run, see `seatools-starter-server-*`, example: [`seatools-starter-server-uvicorn`](https://gitee.com/seatools-py/seatools-starter-server-uvicorn)
