class Contacts:
    def __init__(self, brand=None, subbrand=None, tech = None, typ=None, duration=None, power=None, cylinder=None, axis=None, add=None, diameter=None, bc=None):
        self.brand = brand
        self.subbrand = subbrand
        self.tech = tech 
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
            "Subbrand": self.line,
            "Tech": self.tech,
            "Type": self.typ,
            "Duration": self.duration,
            "Power": self.power,
            "Cylinder": self.cylinder,
            "Axis": self.axis,
            "Add": self.add,
            "Diameter": self.diameter,
            "BC": self.bc
        }
    
    
    
    
        

