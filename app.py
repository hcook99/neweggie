from flask import Flask, render_template, request, redirect, url_for, session
from queryHandler import *
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
import hashlib
from PIL import Image

uplaod_location = 'static/img'
app = Flask(__name__)
app.secret_key = '12345678910111213141516'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = uplaod_location
categories = getallCategories()

'''
Home page to display a random list of 9 products
'''
@app.route('/')
def homePage():
    dropAllAdminInfo()
    queryToDi = queryRunner('SELECT * FROM PRODUCT ORDER BY RANDOM()*(SELECT COUNT(*) FROM PRODUCT) LIMIT 9')
    if 'email' in session:
        user = session['name']
    else:
        user = 'Sign In'
    return render_template('index.html', categories=categories, products=queryToDi, user=user)

'''
Sign in page
'''
@app.route('/signin')
def login():
    dropAllAdminInfo()
    return render_template('signin.html', errorM='')


'''
Post for signing to see if the users email and password is in the database
'''
@app.route('/signin', methods=['POST', 'GET'])
def login_data():
    eMail = request.form['email']
    password = request.form['password']
    password = hashlib.md5(password.encode())
    password = password.hexdigest()
    queryRan = getUser(eMail, password)
    if len(queryRan) == 0:
        return render_template('signin.html',
                               errorM='Your Neweggie email and/or password could not be found or are invalid.')
    else:
        session['email'] = eMail
        session['name'] = queryRan[0]['firstname']
        return redirect(url_for('homePage'))


'''
Sign up to the website page
'''
@app.route('/signup')
def signup():
    return render_template('signup.html', errorM='')


'''
Writes to the database the new user
'''
@app.route('/signup', methods=['POST', 'GET'])
def signup_data():
    eMail = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = hashlib.md5(password.encode())
    password = password.hexdigest()
    queryRan = createUser(eMail, firstname, lastname, password)
    if queryRan == False:
        return render_template('signup.html', errorM='Email already in use.')
    else:
        return redirect(url_for('login'))


'''
Page to display the product
'''
@app.route('/product/<given_product>')
def product(given_product):
    productDict = getProduct(given_product)
    if len(productDict) > 0:
        productDict = productDict[0]
        avg = getAverage(productDict['product_id'])
        count = getCount(productDict['product_id'])
        reviews = getListOfReviews(productDict['product_id'])
        if 'name' not in session:
            return render_template('productpage.html', categories=categories, user='Sign In', userEmail='', products=productDict,
                               average_stars=avg, number_reviews=count, reviews=reviews)
        else:
            return render_template('productpage.html', categories=categories, user=session['name'], userEmail=session['email'], products=productDict,
                               average_stars=avg, number_reviews=count, reviews=reviews)
    else:
        return render_template('404.html')


'''
Adds to the cart the product and redirects to users cart
'''
@app.route('/product/<given_product>', methods=['POST'])
def product_post(given_product):
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        if 'addtocart' in request.form:
            addtocart(session['email'], given_product)
            return redirect(url_for('cart'))


'''
Allows a user to write a review
'''
@app.route('/writeReview',  methods=['post'])
def writeReview():
    product=request.form['productName']
    rating=request.form['rate']
    comments=request.form['comments']
    createReview(product,session['email'], rating, comments)
    return redirect(url_for('product', given_product=product))


'''
Users cart displaying all the products in it
'''
@app.route('/cart')
def cart():
    if 'email' in session:
        productsInCart = getProductsInCart(session['email'])
        totalCost = getCart(session['email'])
        totalCost = totalCost[0]['total_cost']
        userAdd = getAddress(session['email'])
        cards = getCards(session['email'])
        addresses = getAddress(session['email'])
        return render_template('cart.html', categories=categories, user=session['name'], products=productsInCart,
                               totalCost=totalCost, address=userAdd, cards=cards, addresses=addresses)
    else:
        return redirect(url_for('login'))

'''
Allows the user to add more to their cart or remove a product from the cart
'''
@app.route('/cart/<product_id>', methods=['POST'])
def cart_post(product_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    if 'remove' in request.form:
        removeFromCart(session['email'], product_id)
        return redirect(url_for('cart'))
    elif 'itemCount' in request.form:
        numToAdd = request.form['itemCount']
        removeFromCart(session['email'], product_id)
        addToCartMulti(session['email'], product_id, numToAdd)
        return redirect(url_for('cart'))


'''
Lets user add a new address
'''
@app.route('/cart/changeaddress', methods=['post'])
def changeAddressOrder():
    if 'email' not in session:
        return redirect(url_for('login'))
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    addAddress(session['email'], address, city, state)
    return redirect(url_for('cart'))

'''
Lets user add a new card
'''
@app.route('/cart/addcard', methods=['post'])
def changeCard():
    if 'email' not in session:
        return redirect(url_for('login'))
    cardNum = request.form['cardnumber']
    ccv = request.form['ccv']
    nameOnCard = request.form['name']
    zipCode = request.form['zip']
    month = request.form['month']
    year = request.form['year']
    addCards(session['email'], cardNum, month, year, ccv, nameOnCard, zipCode)
    return redirect(url_for('cart'))


'''
Order page to create a user
'''
@app.route('/order', methods=['post'])
def order():
    if 'email' not in session:
        return redirect(url_for('login'))
    card = request.form['card']
    addressBeforeSplit = request.form['address']
    addressBeforeSplit = addressBeforeSplit.split('@')
    address = addressBeforeSplit[0]
    city = addressBeforeSplit[1]
    state = addressBeforeSplit[2]
    makeOrder(session['email'], card, address, city, state)
    return render_template('order.html')


'''
User control page
'''
@app.route('/user')
def user():
    if 'email' not in session:
        return redirect(url_for('login'))
    addresses = getAddress(session['email'])
    cards = getCards(session['email'])
    orders = getOrder(session['email'])

    for num, order in enumerate(orders):
        order['address'] = getOrderAddress(order['addressid'])
    productsOrdered = getOrderDetails(session['email'])
    orders=orders[::-1]
    return render_template('userControl.html', categories=categories,user=session['name'], addresses=addresses,
                           cards=cards, orders=orders, purchaseHistory=productsOrdered)

'''
Delete use function
'''
@app.route('/deleteUserControl', methods=['post'])
def deleteUserApp():
    if 'email' not in session:
        return redirect(url_for('login'))
    deleteUser(session['email'])
    session.pop('email')
    session.pop('name')
    return redirect(url_for('homePage'))


'''
User page to add address
'''
@app.route('/user/addaddress', methods=['post'])
def addAddressUser():
    if 'email' not in session:
        return redirect(url_for('login'))
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    addAddress(session['email'], address, city, state)
    return redirect(url_for('user'))

'''
User page to add card
'''
@app.route('/user/addcard', methods=['post'])
def addCardUser():
    if 'email' not in session:
        return redirect(url_for('login'))
    cardNum = request.form['cardnumber']
    ccv = request.form['ccv']
    nameOnCard = request.form['name']
    zipCode = request.form['zip']
    month = request.form['month']
    year = request.form['year']
    addCards(session['email'], cardNum, month, year, ccv, nameOnCard, zipCode)
    return redirect(url_for('user'))

'''
User page to remove address
'''
@app.route('/userremoveaddress/<useraddressremove>')
def removeAddress(useraddressremove):
    addressBeforeSplit = useraddressremove.split('@')
    address = addressBeforeSplit[0]
    city = addressBeforeSplit[1]
    state = addressBeforeSplit[2]
    removeaddressfromuser(session['email'], address, city, state)
    return redirect(url_for('user'))

'''
User page to remove card
'''
@app.route('/userremovecard/<userremovecard>')
def removeCard(userremovecard):
    deleteCard(userremovecard)
    return redirect(url_for('user'))


'''
User page to cancel an order
'''
@app.route('/userremoveorder/<orderID>', methods=['post'])
def deleteUserOrder(orderID):
    deleteOrder(orderID)
    return redirect(url_for('user'))


'''
Display products related to categories
'''
@app.route('/category/<category_picked>')
def category(category_picked):
    products = getCategory(category_picked)
    if 'email' in session:
        user = session['name']
    else:
        user = 'Sign In'
    return render_template('index.html', categories=categories, products=products, user=user)


'''
Page to display all products related to a search
'''
@app.route('/', methods=['post'])
def searchPro():
    products = searchForPro(request.form['search_text'])
    if 'email' in session:
        user = session['name']
    else:
        user = 'Sign In'
    return render_template('index.html', categories=categories, products=products, user=user)


'''
Admin login page
'''
@app.route('/admin')
def adminLogin():
    if 'email' in session:
        return redirect(url_for('homePage'))
    else:
        return render_template('adminLogin.html')


'''
Check if user exist in admin database
'''
@app.route('/admin', methods=['post'])
def adminLogin_into():
    user = request.form['user']
    password = request.form['password']
    password = hashlib.md5(password.encode())
    password = password.hexdigest()
    adminQ = getAdmin(user, password)
    if len(adminQ) == 0:
        return redirect(url_for('adminLogin'))
    else:
        session['user'] = user
        return redirect(url_for('adminPage'))


'''
Page to show all the options for an admin
'''
@app.route('/adminpage')
def adminPage():
    if 'user' not in session:
        return redirect(url_for('adminLogin'))
    if 'doesuserexist' not in session:
        session['doesuserexist'] = ''

    return render_template('adminPage.html', doesUserExist=session['doesuserexist'])


'''
Redirects to appropriate page from option selected
'''
@app.route('/adminpage', methods=['post'])
def adminPagePost():
    if 'user' not in session:
        return redirect(url_for('adminLogin'))
    if 'email' in request.form:
        email = request.form['email']
        if len(email) == 0:
            return redirect(url_for('adminPagePost'))
        else:
            session['emailSearch'] = email
            return redirect(url_for('userSearch'))
    elif 'product' in request.form:
        if 'doesuserexist' in session:
            session.pop('doesuserexist')
        product = request.form['product']
        session['product'] = product
        return redirect(url_for('productAdmin'))
    elif 'createPro' in request.form:
        if 'doesuserexist' in session:
            session.pop('doesuserexist')
        return redirect(url_for('adminCreatePro'))
    else:
        return render_template('adminPage.html')


'''
Page shows user orders and option to delete a user
'''
@app.route('/adminpage/userSearch')
def userSearch():
    if 'user' not in session:
        return redirect(url_for('adminLogin'))
    emailSearch = session['emailSearch']
    if (len(checkIfUserExist(emailSearch)) == 0):
        session['doesuserexist'] = 'Invalid Entry'
        return redirect(url_for('adminPage'))
    else:
        if 'doesuserexist' in session:
            session.pop('doesuserexist')
        usersOrders = getOrder(emailSearch)
        return render_template('adminUserControlPage.html', people=usersOrders)

'''
Actually deletes the user
'''
@app.route('/adminpage/userSearch/deleteUser', methods=['post'])
def userSearchPost():
    deleteUser(session['emailSearch'])
    return redirect(url_for('adminPage'))


'''
Deletes the selected order
'''
@app.route('/adminpage/userSearch/<orderID>', methods=['post'])
def removeOrder(orderID):
    deleteOrder(orderID)
    return redirect(url_for('userSearch'))


'''
Shows all the products related to a search
'''
@app.route('/productAdmin')
def productAdmin():
    if 'user' not in session:
        return redirect(url_for('adminLogin'))
    getProductsForSearch = searchForPro(session['product'])
    return render_template('adminproduct.html', product=getProductsForSearch, search=session['product'])


'''
Changes the amount of products in database
'''
@app.route('/adminproduct/changePro/<productID>', methods=['post'])
def productQuantityChange(productID):
    changeQuantity(productID, request.form['itemCount'])
    return redirect(url_for('productAdmin'))

'''
Change cost of product
'''
@app.route('/adminproduct/changeCost/<productID>', methods=['post'])
def productCostChange(productID):
    changeCost(productID, request.form['itemCost'])
    return redirect(url_for('productAdmin'))

'''
Goes to the list of reviews of a product
'''
@app.route('/adminProductReviews/<productName>')
def adminProductReviews(productName):
    if 'user' not in session:
        return redirect(url_for('adminLogin'))
    product=getProduct(productName)[0]
    reviews=getListOfReviews(product['product_id'])
    average_stars=getAverage(product['product_id'])
    return render_template('adminproductinfo.html', reviews=reviews, average_stars=average_stars)


'''
Lets admin delete a review
'''
@app.route('/removeProductReview', methods=['post'])
def removeProductReview():
    review_id = request.form['reviewID']
    product_id = request.form['productID']
    productName=getProName(product_id)
    print(productName)
    deleteReview(review_id)
    return redirect(url_for('adminProductReviews', productName=productName))


'''
Lets admin create a new product
'''
@app.route('/adminpage/createProduct')
def adminCreatePro():
    if 'user' in session:
        return render_template('adminCreateProduct.html')
    else:
        return redirect(url_for('adminLogin'))


'''
Creates a new product
'''
@app.route('/adminpage/createProduct', methods=['post'])
def adminCreateProPost():
    productName = request.form['productname']
    category = request.form['category']
    quantity = request.form['quantity']
    companyname = request.form['companyname']
    description = request.form['description']
    cost = request.form['cost']
    file = request.files['photo']
    filename = secure_filename(file.filename)
    filenameOS = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filenameOS)
    fileNameToPass = '/' + (productName.lower().replace(' ', ''))
    newFileName = app.config['UPLOAD_FOLDER'] + fileNameToPass + '.jpg'
    imToTansfer = Image.open(filenameOS)
    conversionForImage = imToTansfer.convert('RGB')
    conversionForImage.save(newFileName)
    os.remove(filenameOS)
    createProduct(productName, category, quantity, fileNameToPass, companyname, description, cost)
    return redirect(url_for('adminPage'))


'''
Logs out user
'''
@app.route('/logoutuser')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('homePage'))


'''
Used to drop all admin related session variables
'''
def dropAllAdminInfo():
    if 'doesuserexist' in session:
        session.pop('doesuserexist', None)
    if 'user' in session:
        session.pop('user', None)
    if 'emailSearch' in session:
        session.pop('emailSearch', None)
    if 'product' in session:
        session.pop('product', None)

if __name__ == '__main__':
    app.run()