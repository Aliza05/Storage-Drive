from abc import ABC, abstractmethod


class StorageDrive(ABC):

    @abstractmethod
    def upload(self, file_path):
        pass

    @abstractmethod
    def download(self, file_id):
        pass

    @abstractmethod
    def search(self):
        pass
