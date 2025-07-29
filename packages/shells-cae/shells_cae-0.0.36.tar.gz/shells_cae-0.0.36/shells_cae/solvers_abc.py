from abc import ABC, abstractmethod

class ABCSolver(ABC):

    preprocessed_data = dict()
    name = 'abc_solver'

    @abstractmethod
    def preprocessor(self, data: dict, global_state: dict):
        pass

    @abstractmethod
    def run(self, data: dict, global_state: dict):
        pass