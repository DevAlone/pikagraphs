from aiohttp import web

from .base_resource import BaseResource

from .resource_request_handler import ResourceRequestHandler


class Server:
    def __init__(self, host: str="localhost", port: int=4444):
        if port < 0 or port > 65535:
            raise ValueError("Port should be in range 0 - 65535")

        self.host = host
        self.port = port
        self.base_address = '/'
        self.app = web.Application()

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)

    def register_resource(self, resource_name, resource: BaseResource):
        handler = ResourceRequestHandler(resource)
        resource_url = self.base_address + '/' + resource_name

        self.app.router.add_route('*', resource_url, handler.request_resource)
        self.app.router.add_route('*', resource_url + '/{id}', handler.request_resource_item)

    def set_base_address(self, base_address: str):
        self.base_address = base_address
