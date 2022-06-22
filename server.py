import json
from flask import Flask, Response, abort, request
from about_me import me
from mock_data import catalog  # important step
from config import db
from bson import ObjectId
from flask_cors import CORS


app = Flask('youdidnotknow')
CORS(app)


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


@app.get("/api/catalog")
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
    try:
        product = request.get_json()
        errors = ""

        # title exist, 5 characters long
        if not "title" in product or len(product["title"]) < 5:
            errors += "Title is required and should have at least 5 characters"

        # must have an image
        if not "image" in product:
            errors += ", Product must contain an image"

        # must have a price, the price should be => to 1
        if not "price" in product or product["price"] < 1:
            errors += ", Price is required and should be > = 1"

        if errors:
            return abort(400, errors)

        db.products.insert_one(product)
        product["_id"] = str(product["_id"])

        return json.dumps(product)
    except Exception as ex:
        return abort(500, F"Unexpected Error: {ex}")


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


# Request 127.0.0.1:5000/api/product/146A
@app.route("/api/products/<id>", methods=["GET"])
def get_product(id):
    # find the product whose _id is equal to id
    # catalog
    # travel the catalog with a for loop
    # get every product inside the list
    # if the _id of the product is equal to the id variable
    # found it, return product as json

    try:

        if not ObjectId.is_valid(id):
            return abort(400, "Invalid id")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
            return abort(400, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)

    except Exception as ex:
        return abort(500, "Unexpected Error")

    # for prod in catalog:

    #     if prod["_id"] == id:
    #         return json.dumps(prod)

    # return abort(404, "Id does not match any product")


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

    results = []
    cursor = db.products.find({"category": category})

    for prod in cursor:
        # if prod["category"] == category:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


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
@app.get("/api/products/lowest-price")
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
@app.get("/api/coupons")
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)


# save coupon code
@app.post("/api/coupons")
def save_coupon():
    try:

        coupon = request.get_json()

        # validations
        errors = ""
        # discount must be 1 < discount < 50
        # code should have at least 5 characters
        if not "code" in coupon or len(coupon["code"]) < 5:
            errors = "Coupon should have at least 5 characters"

        if not "discount" in coupon or coupon["discount"] < 1 or coupon["discount"] > 50:
            errors += "Discount is required and should be between 1 and 50"

        if errors:
            return Response(errors, status=400)

        # do not duplicate code
        # query db to see if there is an object with the same code
        # if there is, return an error
        # otherwise, save

        exists = db.coupons.find_one({"code": coupon["code"]})

        if exists:
            return Response("A coupon already esist for that code", status=400)

        db.coupons.insert_one(coupon)

        coupon["_id"] = str(coupon["_id"])

        return json.dumps(coupon)

    except Exception as ex:
        print(ex)
        return Response("Unexpected Error", status=500)


# get CC by code
@app.get("/api/coupons/<code>")
def get_coupon_code(code):

    # code, code > 4
    try:
        if not len["code"] > 4:
            return Response("Code must contain at least 5 characters", status=400)

        coupon = db.coupons.find_one({"code": code})
        if not coupon:
            return Response("Coupon not found", status=404)

        coupon["_id"] = str(coupon["_id"])

        return json.dumps(coupon)
    except:
        return Response("Unexpected Error", status=500)


app.run(debug=True)
