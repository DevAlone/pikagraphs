from pikabot_graphs import settings

import sys
import asyncio
import logging
import time
import os


class Module:
    logger = None
    processing_period = 1
    last_processing_timestamp = 0

    # you should implement this method
    async def _process(self):
        pass

    def __init__(self, module_name):
        self.logger = logging.getLogger('pikabot_graphs/{}'.format(module_name))
        self.logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

        logger_file_handler = logging.FileHandler('logs/{}.log'.format(module_name))
        logger_file_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
        logger_file_handler.setFormatter(logging.Formatter(settings.LOGS_FORMAT))
        self.logger.addHandler(logger_file_handler)

        self.logger.info('{} initialization...'.format(module_name))

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
            # TODO: fix logging this shit
            exc_type, value, traceback = sys.exc_info()
            exception_string = """Error during processing module: {}
            Traceback: {}
            Some other information: {}
            """.format(repr(ex), traceback, str(exc_type) + str(value))
            self.logger.error(exception_string)
            self.logger.exception(ex)
            if settings.DEBUG:
                os._exit(1)

            await asyncio.sleep(10)
