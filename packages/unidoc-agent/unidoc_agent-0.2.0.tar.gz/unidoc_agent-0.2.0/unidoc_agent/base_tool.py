from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def can_handle(self, file_path, mime_type):
        pass

    @abstractmethod
    def extract_content(self, file_path):
        pass