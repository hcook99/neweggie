import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

engine = db.create_engine('postgresql://hcook:admin@localhost/finalproject')
connection = engine.connect()

'''
Query to see if a user exist
'''
def getUser(email, password):
    queryToRun = text('SELECT * FROM "User" WHERE email=:eMail AND "password"=:password')
    rs = connection.execute(queryToRun, eMail=email, password=password)
    queryToDi = queryToDict(rs)
    return queryToDi

'''
Creates a new user
'''
def createUser(eMail, firstName, lastName, passWord):
    try:
        print(firstName)
        queryToRun = text('INSERT INTO "User"("email", "firstname", "lastname", "password") VALUES(:eMail, :firstName, :lastName, :password)')
        rs = connection.execute(queryToRun, eMail=eMail, firstName=firstName, lastName=lastName, password=passWord)
    except IntegrityError:
        return False
    return True


'''
Function to run a query
'''
def queryRunner(queryToRun):
    rs = connection.execute(queryToRun)
    queryToDi = queryToDict(rs)
    return queryToDi

'''
Converts a query object to an array of objects
'''
def queryToDict(query):
    arrayOfDict = []
    for row in query:
        arrayOfDict.append(dict(row))
    return arrayOfDict

'''
Gets the product that equals a product name
'''
def getProduct(productName):
    queryToRun = text('SELECT * FROM product WHERE product_name=:product')
    rs = connection.execute(queryToRun, product=productName)
    queryRan = queryToDict(rs)
    return queryRan

'''
Gets the average rating for a product
'''
def getAverage(product_id):
    queryToRun = text('SELECT AVG(rating) FROM reviews WHERE product_id=:product_id GROUP BY product_id')
    rs = connection.execute(queryToRun, product_id=product_id)
    queryRan = queryToDict(rs)
    if len(queryRan) > 0:
        return round(queryRan[0]['avg'], 2)
    else:
        return 0

'''
Gets the number of ratings for a product
'''
def getCount(product_id):
    queryToRun = text('SELECT COUNT(rating) FROM reviews WHERE product_id=:product_id GROUP BY product_id')
    rs = connection.execute(queryToRun, product_id=product_id)
    queryRan = queryToDict(rs)
    if len(queryRan) > 0:
        return queryRan[0]['count']
    else:
        return 0


'''
Gets all the reviews related to a product
'''
def getListOfReviews(product_id):
    queryToRun = text('SELECT * FROM reviews WHERE product_id=:product_id')
    rs = connection.execute(queryToRun, product_id=product_id)
    queryRan = queryToDict(rs)
    return queryRan


'''
Gets all the categories
'''
def getallCategories():
    rs = connection.execute('SELECT * FROM PRODUCT;')
    queryToDi = queryToDict(rs)
    arrayOfCategories = []
    for queryResult in queryToDi:
        if queryResult['category'] not in arrayOfCategories:
            arrayOfCategories.append(queryResult['category'])
    return arrayOfCategories


'''
Adds a product to a users cart
'''
def addtocart(email, product_name):
    queryToRun = text(
        'INSERT INTO productandcarts VALUES((SELECT cart_id FROM cart WHERE email=:email), (SELECT product_id FROM product WHERE product_name=:product_name))')
    connection.execute(queryToRun, email=email, product_name=product_name)


'''
Gets all the products in a users cart
'''
def getProductsInCart(email):
    queryToRun = text(
        'SELECT product.product_id, product_name, "category", image_link, company_name, description, "cost", COUNT(*) FROM product INNER JOIN productandcarts ON product.product_id=productandcarts.product_id WHERE productandcarts.cart_id=(SELECT cart_id FROM cart WHERE email=:email) GROUP BY product.product_id;')
    rs = connection.execute(queryToRun, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Gets a user cart
'''
def getCart(email):
    queryToRun = text('SELECT total_cost FROM cart WHERE email=:email')
    rs = connection.execute(queryToRun, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi

'''
Removes a product from a cart
'''
def removeFromCart(email, productID):
    queryToRun = text(
        'DELETE FROM productandcarts WHERE cart_id=(SELECT cart_id FROM cart WHERE email=:email) AND product_id=:product_id; COMMIT;')
    connection.execute(queryToRun, email=email, product_id=productID)

'''
Adds more of a product to a cart
'''
def addToCartMulti(email, product_id, numToAdd):
    queryToRun = text('SELECT addToCartXTimes(:email, :product_id, :numToAdd); COMMIT;')
    connection.execute(queryToRun, email=email, product_id=product_id, numToAdd=numToAdd)

'''
Get all the products for a category
'''
def getCategory(category):
    queryToRun = text('SELECT * FROM product WHERE category=:category')
    rs = connection.execute(queryToRun, category=category)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Calls function to search for products
'''
def searchForPro(searchText):
    queryToRun = text('SELECT * FROM searchForProduct('':searchText'');')
    rs = connection.execute(queryToRun, searchText=searchText)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Checks if an admin exist
'''
def getAdmin(user, password):
    query = text('SELECT * FROM admin WHERE adminUser=:userG AND password=:password')
    rs = connection.execute(query, userG=user, password=password)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Creates a new product
'''
def createProduct(product_name, category, quantity, image_link, company_name, description, cost):
    query = text(
        'INSERT INTO product(product_name, category, quantity, image_link, company_name, description, cost) VALUES(:product_name, :category, :quantity, :image_link, :company_name, :description, :cost)')
    connection.execute(query, product_name=product_name, category=category, quantity=quantity, image_link=image_link,
                       company_name=company_name, description=description, cost=cost)



'''
Checks if a user exist
'''
def checkIfUserExist(email):
    query = text('SELECT * FROM "User" WHERE email=:email')
    rs = connection.execute(query, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi

'''
Gets all the user orders
'''
def getOrder(email):
    query = text('SELECT "Order".order_id, "Order".email, "Order".card_number, "Order".order_date, "Order".isorderdone, "Order".addressID, SUM(cost) FROM purchasehistory INNER JOIN "Order" ON purchasehistory.order_id="Order".order_id WHERE purchasehistory.email=:email GROUP BY "Order".order_id;')
    rs = connection.execute(query, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Deletes an order
'''
def deleteOrder(orderID):
    query = text('SELECT deleteOrder(:orderID); COMMIT;')
    connection.execute(query, orderID=orderID)


'''
Option to delete a user
'''
def deleteUser(email):
    query = text('SELECT deleteUser(:email); COMMIT;')
    connection.execute(query, email=email)


'''
Change the quantity of products
'''
def changeQuantity(productID, quantity):
    query = text('UPDATE product SET quantity=:quantity WHERE product_id=:productID; COMMIT;')
    connection.execute(query, quantity=quantity, productID=productID)

'''
Change the cost of a product
'''
def changeCost(productID, cost):
    query = text('UPDATE product SET cost=:cost WHERE product_id=:productID; COMMIT;')
    connection.execute(query, cost=cost, productID=productID)


'''
Gets all the users cards
'''
def getCards(email):
    query = text('SELECT card_number FROM Card WHERE email=:email')
    rs = connection.execute(query, email=email)
    queryRan = queryToDict(rs)
    return queryRan


'''
Creates a new card
'''
def addCards(email, card_number, year, month, ccv, nameG, zip_code):
    experation_date = str(year) + '-01-' + str(month)
    try:
        query = text('INSERT INTO card VALUES(:card_number, :email, :ccv, DATE :experation_date, :nameG, :zip_code)')
        connection.execute(query, card_number=card_number, email=email, ccv=ccv, experation_date=experation_date,
                           nameG=nameG, zip_code=zip_code)
    except IntegrityError:
        pass


'''
Makes a new order
'''
def makeOrder(email, card_number, address, city, state):
    query = text(
        'INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID) VALUES(:email, :card_number, (SELECT CURRENT_DATE), false, (SELECT addressID FROM address WHERE address=:address AND city=:city AND state=:state))')
    connection.execute(query, email=email, card_number=card_number, address=address, city=city, state=state)


'''
Create a new address and link it to a user
'''
def addAddress(email, address, city, state):
    try:
        query = text('INSERT INTO address(address, city, state) VALUES (:address, :city, :state)')
        connection.execute(query, address=address, city=city, state=state)
    except IntegrityError:
        pass
    try:
        query = text(
            'INSERT INTO addressanduser VALUES (:email, (SELECT addressID FROM address WHERE address=:address AND city=:city AND state=:state))')
        connection.execute(query, email=email, address=address, city=city, state=state)
    except IntegrityError:
        pass


'''
Gets all the addresses of a user
'''
def getAddress(email):
    query = text(
        'SELECT address, city, state FROM address INNER JOIN addressanduser ON address.addressID=addressanduser.addressID WHERE email=:email')
    rs = connection.execute(query, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Removes an address from user
'''
def removeaddressfromuser(email, address, city, state):
    query = text(
        'DELETE FROM addressanduser WHERE email=:email AND addressID=(SELECT addressID FROM address WHERE address=:address AND city=:city AND state=:state); COMMIT;')
    connection.execute(query, email=email, address=address, city=city, state=state)


'''
Deletes a user card
'''
def deleteCard(card_number):
    query = text('DELETE FROM card WHERE card_number=:card_number; COMMIT;')
    connection.execute(query, card_number=card_number)


'''
Get address an order is being sent to
'''
def getOrderAddress(addressID):
    query = text('SELECT address, city, state FROM address WHERE addressID=:addressID')
    rs = connection.execute(query, addressID=addressID)
    queryToDi = queryToDict(rs)
    addressUse = ''
    for addresses in queryToDi:
        addressUse = addresses['address'] + ' ' + addresses['city'] + ', ' + addresses['state']
    return addressUse


'''
Gets all the details of an order
'''
def getOrderDetails(email):
    query = text('SELECT product.product_id, product_name, "category", image_link, company_name, description, purchasehistory.cost, purchasehistory.order_id, COUNT(*) FROM product INNER JOIN purchasehistory ON product.product_id=purchasehistory.product_id WHERE email=:email GROUP BY product.product_id, purchasehistory.cost, purchasehistory.order_id;')
    rs = connection.execute(query, email=email)
    queryToDi = queryToDict(rs)
    return queryToDi


'''
Creates a review in the database
'''
def createReview(productName,email,rating,comments):
    product_id=getProduct(productName)[0]['product_id']
    query = text('INSERT INTO reviews(product_id, rating, email, comment) VALUES(:product_id, :rating, :email, :comments)')
    connection.execute(query, product_id=product_id, rating=rating, email=email, comments=comments)


'''Deletes a review'''
def deleteReview(review_id):
    query = text('DELETE FROM reviews WHERE review_id=:review_id; COMMIT;')
    connection.execute(query, review_id=review_id)

'''
Gets the name of a product given the product id
'''
def getProName(product_id):
    query = text('SELECT product_name FROM product WHERE product_id=:product_id')
    rs=connection.execute(query, product_id=product_id)
    querytoD=queryToDict(rs)
    return querytoD[0]['product_name']