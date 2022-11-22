from abc import ABC, abstractmethod

class StorageDrive(ABC):

    @abstractmethod
    def upload(self):
        pass

    def download(self):
        pass

    def search(self):
        pass


