class Contacts:
    def __init__(self, brand=None, line=None, typ=None, duration=None, power=None, cylinder=None, axis=None, add=None, diameter=None, bc=None):
        self.brand = brand
        self.line = line
        self.typ = typ
        self.duration = duration
        self.power = power
        self.cylinder = cylinder
        self.axis = axis
        self.add = add
        self.diameter = diameter
        self.bc = bc

    def to_dict(self):
        return {
            "Brand": self.brand,
            "Line": self.line,
            "Type": self.typ,
            "Duration": self.duration,
            "Power": self.power,
            "Cylinder": self.cylinder,
            "Axis": self.axis,
            "Add": self.add,
            "Diameter": self.diameter,
            "BC": self.bc
        }
    
    
    
    
        

