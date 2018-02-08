import abc


class BaseSerializer:
    @abc.abstractmethod
    def serialize(self, item) -> dict:
        pass
