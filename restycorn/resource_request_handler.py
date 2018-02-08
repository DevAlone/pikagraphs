import inspect
import traceback

import aiohttp
from aiohttp.web import json_response
from .base_resource import BaseResource
from .exceptions import ResourceItemDoesNotExistException, ParamsValidationException


class ResourceRequestHandler:
    def __init__(self, resource: BaseResource):
        self.resource = resource

    async def request_resource(self, request: aiohttp.ClientRequest):
        kwargs = {}

        if request.method == 'GET':
            func = self.resource.list
        elif request.method == 'PUT':
            func = self.resource.replace_all
            kwargs = {'items': await request.json()}
        elif request.method == 'PATCH':
            func = self.resource.create,
            kwargs = {'items': await request.json()}
        elif request.method == 'DELETE':
            func = self.resource.delete_all
        else:
            return json_response({
                'status': 'error',
                'error_message': 'Method "{}" is not allowed here'.format(request.method)
            })

        return await self.make_request(request, func, **kwargs)

    async def request_resource_item(self, request: aiohttp.ClientRequest):
        if 'id' not in request.match_info:
            return json_response({
                'status': 'error',
                'error_message': 'id is required',
            })

        item_id = request.match_info['id']

        kwargs = {}

        if request.method == 'GET':
            func = self.resource.get
            kwargs = {'item_id': item_id}
        elif request.method == 'PUT':
            func = self.resource.create_or_replace
            kwargs = {'item_id': item_id, 'item': await request.json()}
        elif request.method == 'PATCH':
            func = self.resource.update
            kwargs = {'item_id': item_id, 'item': await request.json()}
        elif request.method == 'DELETE':
            func = self.resource.delete
            kwargs = {'item_id': item_id}
        else:
            return json_response({
                'status': 'error',
                'error_message': 'Method "{}" is not allowed here'.format(request.method)
            })

        return await self.make_request(request, func, **kwargs)

    @staticmethod
    async def make_request(request, func, **kwargs):
        try:
            kwargs.update(dict(request.query))
            kwargs = ResourceRequestHandler._prepare_params(func, kwargs)

            result = await func(**kwargs)
            return json_response({
                'status': 'ok',
                'data': result,
            })
        except ResourceItemDoesNotExistException:
            return json_response({
                'status': 'error',
                'error_message': 'item does not exist',
            })
        except ParamsValidationException as ex:
            return json_response({
                'status': 'error',
                'error_message': str(ex),
            })
        except BaseException as ex:
            print(type(ex))
            print(ex)
            traceback.print_exc()

            return json_response({
                'status': 'error',
                'error_message': 'Error during processing resource "{}" with request method "{}"'.format(
                    request.url, request.method
                )
            })

    @staticmethod
    def _prepare_params(func, params: dict) -> dict:
        signature = inspect.signature(func)
        signature_params = signature.parameters

        for key, val in params.items():
            if key not in signature_params:
                raise ParamsValidationException('key "{}" is not allowed here'.format(key))

        for param_name, parameter_info in signature_params.items():
            if param_name not in params and parameter_info.default is inspect.Parameter.empty:
                raise ParamsValidationException('param "{}" is required'.format(param_name))

        try:
            bind = signature.bind(**params)
        except TypeError:
            raise ParamsValidationException('Not enough params')

        bind.apply_defaults()

        result = bind.arguments

        for key, parameter_info in signature_params.items():
            if key in result:
                if parameter_info.annotation is inspect.Parameter.empty \
                        or (parameter_info.default is None and result[key] is None):
                    continue

                if type(result[key]) is not parameter_info.annotation:
                    try:
                        result[key] = parameter_info.annotation(result[key])
                    except ValueError:
                        raise ParamsValidationException('key "{}" should be "{}" or type convertible to "{}"'.format(
                            key, parameter_info.annotation, parameter_info.annotation))

        return result
