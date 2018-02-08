import abc

from aioserver.base_controller import BaseController

import inspect


class ParamsValidationError(ValueError):
    pass


class ParamsController(BaseController):
    @abc.abstractmethod
    def get(self, request):
        pass

    @abc.abstractmethod
    def post(self, request):
        pass

    def _prepare_params(self, params: dict) -> dict:
        signature = inspect.signature(self.get)
        signature_params = signature.parameters

        for key, val in params.items():
            if key not in signature_params:
                raise ParamsValidationError('key "{}" is not allowed here'.format(key))

        for param_name, parameter_info in signature_params.items():
            if param_name not in params and parameter_info.default is inspect.Parameter.empty:
                raise ParamsValidationError('param "{}" is required'.format(param_name))

        try:
            bind = signature.bind(**params)
        except TypeError:
            raise ParamsValidationError('Not enough params')

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
                        raise ParamsValidationError('key "{}" should be "{}" or type convertable to "{}"'.format(
                            key, parameter_info.annotation, parameter_info.annotation))

        return result
