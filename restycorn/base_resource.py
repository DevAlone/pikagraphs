import abc


class BaseResource:
    @abc.abstractmethod
    async def list(self) -> list:
        """
        It is called when client send GET request with url like this http://example.com/comments/
        Returns all items

        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def replace_all(self, items: list):
        """
        Replaces whole collection with another one

        :param items: list of new items
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, item) -> object:
        """
        Creates new item and returns it or raises exception if error happened

        :param item: item to create
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all(self):
        """
        Deletes entire collection, be careful using it
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, item_id) -> object:
        """
        Returns specific item with id = item_id, should return exception if item cannot be retrieved

        :param item_id: id of item to retrieve
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_or_replace(self, item_id, item: dict) -> object:
        """
        Replaces item or creates new one

        :param item_id: id of item
        :param item: item's fields
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, item_id, item: dict) -> object:
        """
        Updates item

        :param item_id: id of item to update
        :param item: new item's fields
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, item_id):
        raise NotImplementedError()
