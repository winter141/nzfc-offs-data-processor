from abc import ABC, abstractmethod


class Processor(ABC):

    @abstractmethod
    def send_post_requests(self):
        pass
