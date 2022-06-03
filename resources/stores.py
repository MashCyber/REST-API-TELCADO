from flask import jsonify
from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'msg':'store not found'}, 404
    
    def post(self,name):
        
        if StoreModel.find_by_name(name):
            return {'msg':f'Store {name} already exist!'},500
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:    
            return {'msg':'Error creating store!'},500
        return store.json(),201
    
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            
        return {'msg':f'deletion successful'} 
            
    

class StoreList(Resource):
    def get(self):
        # stores = list(map(lambda store: store.json(),StoreModel.query.all()))
        stores = [store.json() for store in StoreModel.query.all()]
        return {'stores':stores}