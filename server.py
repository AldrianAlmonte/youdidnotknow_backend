import json
from flask import Flask
from about_me import me
from mock_data import catalog #important step




app = Flask('youdidnotknow')


#Request 127.0.0.1:5000/api/product/

@app.route("/", methods=['GET']) # root
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
    return json.dumps(catalog)



# Reques 127.0.0.1:5000/api/product/146A
@app.get("/api/product/<id>")
def get_product(id):
    return json.dumps(id)




# make an endpoint to send back the number of products the catalog has
@app.get("/api/catalog/count")
def get_count():
    #here... count how many products are in the list
    counts = len(catalog)
    return json.dumps(counts)






#Create and endpoint that returns the SUM of all the products' prices
#GET /api/catalog/total
#@app.route('/api/catalog/total', methods=['GET']
@app.get('/api/catalog/total')
def get_total():

    total = 0
    for prod in catalog:
        #total = total + prod["price"]
        total += prod["price"]
    
    return json.dumps(total)








# get a product by category
#get /api/products/<category>
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
    res = []
    for prod in catalog:
        cat = prod["category"]
        # if cat does not exist in results, then
        if not cat in res:
            res.append(cat)

    return json.dumps(res)







app.run(debug=True)
