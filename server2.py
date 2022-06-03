def get_product(id):

    for prod in catalog:
        if prod["id"] == id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")





    
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
        if not cat in results:
            res.append(cat)

    return json.dumps(res)


# get the cheapest product
@app.get("/api/products/lowest-price")
def lowest_price():
     solution = catalog[0]

    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod


    return json.dumps(res)