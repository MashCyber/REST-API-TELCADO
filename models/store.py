from db import db

class StoreModel(db.Model):
    #tablename
    __tablename__ = 'stores'
    #Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel',lazy='dynamic') #allows store to see which items in the items db that have a store id = to its own
    #above is a list of ItemModel,many items with same store id ==> many to one
    
    def __init__(self,name) -> None:
        self.name = name
    
    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}
    
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        