from gettext import find
import json
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog  # important step
from config import db
from bson import ObjectId


app = Flask('youdidnotknow')


# Request 127.0.0.1:5000/api/product/

@app.route("/", methods=['GET'])  # root
def home():
    return "Welcome to your server!"

# Create an about endpoint and show your name


@app.route("/about", methods=['GET'])
def about():

    return me["first"] + " " + me["last"]


@app.route("/address")
def address():
    return f'{me["address"]["street"]} #{me["address"]["number"]}'


######################################################################
############################ API ENDPOINTS ###########################
######################################################################
# Postman -> allows you to test your endpoints


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    # get all data from the collection ({}) -> this is a filter
    cursor = db.products.find({})

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


# POST Method  to create new products
@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    product["_id"] = str(product["_id"])

    return json.dumps(product)


# make an endpoint to send back how many product do we have in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items)  # return the value


# make an endpoint to send back the number of products the catalog has
# @app.get("/api/catalog/count")
# def get_count():
#     # here... count how many products are in the list
#     counts = len(catalog)
#     return json.dumps(counts)  # return the value


# Reques 127.0.0.1:5000/api/product/146A
@app.get("/api/product/<id>")
def get_product(id):
    # find the product whose _id is equal to id
    # catalog
    # travel the catalog with a for loop
    # get every product inside the list
    # if the _id of the product is equal to the id variable
    # found it, return product as json

    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")


# Create and endpoint that returns the SUM of all the products' prices
#GET /api/catalog/total
# @app.route('/api/catalog/total', methods=['GET']
@app.get('/api/catalog/total')
def get_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        #total = total + prod["price"]
        total += prod["price"]

    return json.dumps(total)


# get a product by category
# get /api/products/<category>
@app.get("/api/products/<category>")
def get_products_category(category):
    res = []

    for prod in catalog:
        if prod["category"] == category:
            return json.dumps(prod)

    return json.dump(res)


# get the list of categories
# get /api/categories
@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        cat = prod["category"]
        # if cat does not exist in results, then
        if not cat in results:
            cursor.append(cat)

    return json.dumps(results)


# get the lowest price
@app.get("/api/product/lowest-price")
def get_lowest_price():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)


app.run(debug=True)


######################################################################
###########################  COUPON CODES  ###########################
######################################################################

# get all
@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons, find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)


# save coupon code
@app.route("/api/coupons", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    # validation

    db.coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

# get CC by code


app.run(debug=True)
