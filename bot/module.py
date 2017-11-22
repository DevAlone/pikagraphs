import sys
import asyncio
import logging

from .pikabot_graphs import settings


class Module:
    _logger = None
    processPeriod = 1
    lastProcessTimestamp = 0

    # you should implement this method
    async def _process(self):
        pass

    def __init__(self, module_name):
        self._logger = logging.getLogger('pikabot_graphs/{}'.format(module_name))
        self._logger.setLevel(logging.DEBUG)
        if settings.DEBUG:
            debug_file_handler = logging.FileHandler('logs/{}.debug.log'.format(module_name))
            debug_file_handler.setLevel(logging.DEBUG)
        error_file_handler = logging.FileHandler('logs/{}.error.log'.format(module_name))
        error_file_handler.setLevel(logging.ERROR)
        info_file_handler = logging.FileHandler('logs/{}.log'.format(module_name))
        info_file_handler.setLevel(logging.INFO)

        if settings.DEBUG:
            self._logger.addHandler(debug_file_handler)
        self._logger.addHandler(error_file_handler)
        self._logger.addHandler(info_file_handler)

        self._logger.info('{} initialization...'.format(module_name))

    async def process(self):
        await self._callCoroutineWithLoggingException(self._process())

    async def _callCoroutineWithLoggingException(self, coroutine):
        try:
            await coroutine
        except KeyboardInterrupt as ex:
            raise ex
        except Exception as ex:
            type, value, traceback = sys.exc_info()
            exception_string = """Error during processing module: {}
            Traceback: {}
            Some other information: {}
            """.format(repr(ex), traceback, str(type) + str(value))
            self._logger.error(exception_string)
            await asyncio.sleep(1)
        except:
            type, value, traceback = sys.exc_info()
            exception_string = """Error during processing module
            Traceback: {}
            Some other information: {}
            """.format(traceback, str(type) + str(value))
            self._logger.error(exception_string)
            await asyncio.sleep(1)

