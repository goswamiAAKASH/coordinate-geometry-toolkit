# base.py
class Shape:

    # if a inherit class  not add the method in thr class it will raise an error
    def area(self):
        raise NotImplementedError("Subclasses must implement area method (add the area method)")

    def perimeter(self):
        raise NotImplementedError("Subclasses must implement perimeter method (add the perimeter method)")
