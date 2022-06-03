from db import db

class ItemModel(db.Model): #extends the Model class for db
    #define the table name
    __tablename__ = 'items'
    #define the table columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2)) #2 decimal places
    
    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') #finds the store in the db that matches store id
    
    def __init__(self,name,price,store_id) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id
        
    def json(self):
        return {'name':self.name,'price':self.price}
    
    @classmethod
    def find_by_name(cls,name):
      return ItemModel.query.filter_by(name=name).first()  #SELECT * FROM __tablename__ WHERE name=name LIMIT 1
        #returns an item model obj that has self.name,self.price
        
    def save_to_db(self):
        #save the item model obj(self) to the database and save
        #can be used also for update
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()