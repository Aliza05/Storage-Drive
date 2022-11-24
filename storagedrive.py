from abc import ABC, abstractmethod

class StorageDrive(ABC):

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def search(self):
        pass


