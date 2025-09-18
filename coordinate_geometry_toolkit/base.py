# base.py
from abc import ABC, abstractmethod

class Shape(ABC):

  # if a ***"inherit class"***  not add the  method in thr class it will raise an error
    @abstractmethod
    def area(self):
        raise NotImplementedError("Subclasses must implement area method")

    @abstractmethod
    def perimeter(self):
        raise NotImplementedError("Subclasses must implement perimeter method")
