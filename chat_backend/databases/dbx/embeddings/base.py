from abc import ABC, abstractmethod


class BaseVectorizer(ABC):
    @abstractmethod
    def generator(self):
        pass

    @abstractmethod
    def storage(self):
        pass

    @abstractmethod
    def similarity(self):
        pass
