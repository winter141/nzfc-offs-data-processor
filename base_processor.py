from abc import ABC, abstractmethod


class Processor(ABC):

    @abstractmethod
    def send_food_post_requests(self):
        pass

    @abstractmethod
    def send_csm_post_requests(self):
        pass
