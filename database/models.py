
class Order:
    pass 

class History: 
    def __init__(self,):
        pass



class User:
    def __init__(self, id,fullname,phone):
        self.id = id 
        self.fullname= fullname 
        self.phone = phone 
        self.recomend = None
    def orders()->list[Order]:
        pass
    def history()->list[History]:
        pass

class Dish:
    def __init__(self, name=None, price=None, tags=None, desc=None,photo=None):
        self.id=None
        self.name = name 
        self.price = price 
        self.tags = tags 
        self.desc = desc
        self.photo = photo 
        self.ans_neurlink = None
        self.properties = None
    def to_tuple(self):
        return (self.name,self.price,self.photo,self.tags,self.desc,self.properties,self.ans_neurlink)
    def from_tuple(self,data):
        self.id = data[0]
        self.name = data[1]
        self.price = data[2]
        self.photo = data[3]
        self.tags = data[4]
        self.desc = data[5]
        self.properties = data[6]
        self.ans_neurlink = data[7]





