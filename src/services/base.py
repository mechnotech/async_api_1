import abc


class BaseCacheEngine(abc.ABC):
    @abc.abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def set(self, *args, **kwargs):
        pass


class BaseSearchEngine(abc.ABC):
    @abc.abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def search(self, *args, **kwargs):
        pass
