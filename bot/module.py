import sys
import asyncio
import logging

import time
from pikabot_graphs import settings


class Module:
    _logger = None
    processing_period = 1
    last_processing_timestamp = 0

    # you should implement this method
    async def _process(self):
        pass

    def __init__(self, module_name):
        self._logger = logging.getLogger('pikabot_graphs/{}'.format(module_name))
        self._logger.setLevel(logging.DEBUG)

        error_file_handler = logging.FileHandler('logs/{}.error.log'.format(module_name))
        error_file_handler.setLevel(logging.ERROR)
        info_file_handler = logging.FileHandler('logs/{}.log'.format(module_name))
        info_file_handler.setLevel(logging.INFO)

        if settings.DEBUG:
            debug_file_handler = logging.FileHandler('logs/{}.debug.log'.format(module_name))
            debug_file_handler.setLevel(logging.DEBUG)
            self._logger.addHandler(debug_file_handler)

        self._logger.addHandler(error_file_handler)
        self._logger.addHandler(info_file_handler)

        self._logger.info('{} initialization...'.format(module_name))

    async def process(self):
        while True:
            if self.last_processing_timestamp + self.processing_period < int(time.time()):
                await self._call_coroutine_with_logging_exception(self._process())
                self.last_processing_timestamp = int(time.time())
            else:
                await asyncio.sleep(1)

    async def _call_coroutine_with_logging_exception(self, coroutine):
        try:
            await coroutine
        except KeyboardInterrupt as ex:
            raise ex
        except BaseException as ex:
            exc_type, value, traceback = sys.exc_info()
            exception_string = """Error during processing module: {}
            Traceback: {}
            Some other information: {}
            """.format(repr(ex), traceback, str(exc_type) + str(value))
            self._logger.error(exception_string)
            self._logger.exception(ex)
            await asyncio.sleep(1)
