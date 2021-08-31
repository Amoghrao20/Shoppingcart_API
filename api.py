from flask import Flask, Response, request
import json
from bson.objectid import  ObjectId
import pymongo

app = Flask(__name__)

#-------------------------------------
# Connecting  with MongoDB database
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    mongo.server_info() ## trigger  exception if cannot connect to database
    db = mongo.shopping  
except:
    print("ERROR - Cannot connect  to  database")




#--------------------------------------
# Create the cart
@app.route("/carts", methods=["POST"])
def create_cart():
    try:
        #
        item = {"name":request.form["name"],
                "price":request.form["price"],
                "quantity":request.form["quantity"]}
        dbResponse = db.carts.insert_one(item)
        print(dbResponse.inserted_id)
        #for attr in dir(dbResponse):
        #    print(attr)
        return Response(
            response=json.dumps(
                {"message":"item added to cart",
                 "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
        
    except Exception as ex:
        print("*****************")
        print(ex)
        print("*****************")
	return Response(
            response=json.dumps(
                {"message":"cannot add it to the cart"
                }),
            status=500,
            mimetype="application/json"

#--------------------------------------------
#get items from the cart
@app.route("/carts", methods=["GET"])
def show_items_in_cart():
    try:
        data = list(db.carts.find())
        print(data)
        for item in data:
            item["_id"] = str(item["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message":"Error fetching items in cart"}),
            status=500,
            mimetype="application/json"
        )



#-----------------------------------------------------
# update name of item in the cart 

    
@app.route("/carts/name/<id>", methods=["PUT"])
def update_item_name(id):
    try:
        dbResponse = db.carts.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        #for attr in dir(dbResponse):
        #    print(f"*******{attr}************")
        if (dbResponse.modified_count > 0):
            return Response(
                response=json.dumps({"message":"Item name updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message":"Nothing to Update"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("**********")
        print(ex)
        return Response(
            response=json.dumps({"message":"Error updating items in cart"}),
            status=500,
            mimetype="application/json"
        )



#--------------------------------------------------
# remove item from cart
@app.route("/carts/<id>", methods=["DELETE"])
def delete_item(id):
    try:
        dbResponse = db.carts.delete_one(
            {"_id":ObjectId(id)}
        )
        #for attr in dir(dbResponse):
        #    print(attr)
        if (dbResponse.deleted_count > 0):
            return Response(
                response=json.dumps(
                    {"message":"item Deleted",
                    "id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {"message":"item doesn't exist",
                    "id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        
        print(ex)
        
        return Response(
            response=json.dumps({"message":"Error deleting items in cart"}),
            status=500,
            mimetype="application/json"
        )




#----------------------------------------
if (__name__ == "__main__"):
    app.run(port=5000, debug=True)
