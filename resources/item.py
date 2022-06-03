import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cant be blank!')
    parser.add_argument('store_id', type=int, required=True, help='item must have a store ID!')
    
    # @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #since find by name returns an ItemModel obj we make it json using the static method json()
        return {'message':f"Item '{name}' not found!"},404
        
    def post(self,name): 
        if ItemModel.find_by_name(name):
            return {'message':'Item already exists!'},400
        
        request_data = Item.parser.parse_args()
        # item = ItemModel(name,request_data['price'],request_data['store_id']) #ensure its an ItemModel obj,takes in 2 params
        item = ItemModel(name,**request_data) 
        #item is an ItemModel Obj with ability to use up methods
        try:
            item.save_to_db()
        except:
            return {'message':"An error occured inserting item"}, 500 #internal server err
        return item.json(), 201
    
    @jwt_required()
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted!'}
        return {'message':'Item not found'},404
    
    def put(self,name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            # item = ItemModel(name,request_data['price'],request_data['store_id'])
            item = ItemModel(name,**request_data)
        else:
            item.price = request_data['price']
            
        item.save_to_db()
        return item.json()
    
class ItemList(Resource):
    @jwt_required()
    def get(self):
        items=  list(map(lambda x: x.json(),ItemModel.query.all())) #iterate through entire all() and apply lambda fxn 
        # i.e for every iterate do x.json() and store in the list
        # items = [item.json() for item in ItemModel.query.all()] #returns all of the objects in the database 
        
        return {'items':items}