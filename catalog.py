from flask import Flask, render_template, request, \
    redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sports_database import Base, Categories, LatestItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Reading from json files for 3rd party Authentication
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///sports_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# It is called inside login.html to connect through Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' \
          'fb_exchange_token&' \
          'client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
              app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&' \
          'fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order
    # to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?' \
          'access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
              'border-radius: 150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# called in another function disconnect to Log out the User.
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?' \
          'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# called inside login.html to enable 3rd party
# Authentication through Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps
                                 ('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/''tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.
                                            get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match "
                       "given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match "
                       "app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == \
            stored_gplus_id:
        response = make_response(json.dumps('Current user '
                                            'is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return 'Redirecting'


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their
#  login_session and called inside disconnect function


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given'
                       ' user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# returns Database information of the
# arbitrary(desired) Category entered by the user in json format
@app.route('/catalog/<string:category_name>/JSON')
def showCategoryJson(category_name):
    # Checks whether the user is logged in or not.
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Categories) \
        .filter_by(name=category_name).all()
    sport = session.query(Categories) \
        .filter_by(name=category_name).first()
    sport_id = sport.id
    items = session.query(LatestItem) \
        .filter_by(category_id=sport_id).all()
    return jsonify(category=[r.serialize for r in category],
                   items=[r.serialize for r in items])


@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def showItemJson(category_name, item_name):
    # Checks whether the user is logged in or not.
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(LatestItem) \
        .filter_by(title=item_name).all()
    return jsonify(item=[r.serialize for r in item])


# connects to catalog.html/public.html for catalog Menu
@app.route('/')
@app.route('/catalog')
def show_catalog():
    # This function is called inside catalog.html/public.html
    #  to print the List of Categories
    def show(title_cat):
        list = session.query(LatestItem.category_id) \
            .filter_by(title=title_cat).one()
        req_id = list.category_id
        data = session.query(Categories.name) \
            .filter_by(id=req_id).one()
        return data.name

    # This Query gives the list of Latest updated
    # items up to 14
    sports = session.query(Categories)
    items = session.query(LatestItem) \
        .order_by(LatestItem.time_updated.desc()).limit(14)
    # Checks whether the user is logged in or not
    # and renders html pages accordingly!
    if 'username' not in login_session:
        return render_template('public_catalog.html',
                               sports=sports, items=items, show=show)
    else:
        return render_template('catalog.html',
                               sports=sports, items=items, show=show)


# This functions gives the items of a
# particular Category
@app.route('/catalog/<string:sport_name>')
def sportMenu(sport_name):
    # For extracting the listed items of the
    # asked sports category
    sport_unique = session.query(Categories)
    sport = session.query(Categories) \
        .filter_by(name=sport_name).first()
    sport_id = sport.id
    items = session.query(LatestItem) \
        .filter_by(category_id=sport_id).all()
    # For counting items
    count = session.query(LatestItem) \
        .filter_by(category_id=sport_id).count()
    # html page is provided with the resulted
    #  queries to display them
    return render_template('item_menu.html',
                           items=items, sport=sport,
                           count=count, sport_unique=sport_unique)


# This function gives the full description of the selected item
@app.route('/catalog/<string:sport_name>/<string:item_name>')
def itemInfo(sport_name, item_name):
    item_des = session.query(LatestItem) \
        .filter_by(title=item_name).one()
    return render_template('item_description.html',
                           item_des=item_des, sport_name=sport_name)


# This function edits the selected item by the user
@app.route('/catalog/<string:sport_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def itemEdit(sport_name, item_name):
    # Checks whether the user is logged in or not.
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(LatestItem).filter_by(title=item_name).one()
    if login_session['user_id'] != item.user_id:
        # if the logged in user is not the creator of the
        # selected item the this alert is displayed and
        #  user is redirected to the main menu
        return "<html><script>setTimeout(function() {" \
               "{alert('You are not authorized to " \
               "edit items to this Category. " \
               "Please create your own Category in " \
               "order to edit items.');}" \
               'window.location.href = "/";}, 0)' \
               '</script></html>'

    # If the method is POST then database is updated with
    # the values provided by the user and redirected to the menu.
    # If the method is GET then user is provided with a
    # html form to insert the desired values.
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['item_description']:
            item.description = request.form['item_description']
        if request.form['item_category']:
            item.item_category = request.form['item_category']
            i = session.query(LatestItem).filter_by(item_category=item.
                                                    item_category).first()
            j = session.query(Categories).filter_by(name=item.
                                                    item_category).first()
            i.category_id = j.id
            item.category_id = i.category_id
        session.add(item)
        session.commit()
        flash('Item Successfully Edited!')
        return redirect(url_for('show_catalog'))
    else:
        return render_template('edit_item.html', sport_name=sport_name,
                               item_name=item_name, item=item)


# If the method is POST then the selected item
# is deleted from the database.
# If the method is GET then the user redirected to
# the menu without any deletion.
@app.route('/catalog/<string:sport_name>/'
           '<string:item_name>/delete', methods=['GET', 'POST'])
def itemDelete(item_name, sport_name):
    # Checks whether the user is logged in or not.
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(LatestItem) \
        .filter_by(title=item_name).one()
    # if the logged in user is not the creator
    # of the selected item the
    # this alert is displayed and user is
    # redirected to the main menu
    if login_session['user_id'] != itemToDelete.user_id:
        return "<html><script>setTimeout(function() {" \
               "{alert('You are not authorized to " \
               "delete items to this Category. " \
               "Please create your own Category in " \
               "order to delete items.');}" \
               'window.location.href = "/";}, 0)' \
               '</script></html>'
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('show_catalog'))
    else:
        return render_template('delete_Item.html',
                               item=itemToDelete)


# If the method is POST then the user is provided
# to a html form to enter data to be added.
# If the method is Get then the user is redirected
# to the menu and addition is cancelled.
@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    # Checks whether the user is logged in or not.
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # This Query checks whether the new item
        # entered by the user is unique or not
        # i.e(To Prevent duplicacy in the database)
        item = session.query(LatestItem) \
            .filter_by(title=request.form['title']).count()
        if item == 0:
            # This query links the added item to its
            # selected Category by the means of id which
            # is the FOREIGN KEY.
            cat = session.query(Categories) \
                .filter_by(name=request.form['category']).one()
            cat_id = cat.id
            newItem = LatestItem(user_id=login_session['user_id'],
                                 title=request.form['title'],
                                 description=request.form['description'],
                                 item_category=request.form['category'],
                                 category_id=cat_id)
            session.add(newItem)
            session.commit()
            flash('New Item (%s) has been added to Category'
                  '(%s)' % (newItem.title, newItem.item_category))
        # If count is not ZERO(0) then the item with same
        # title is already present in the database
        # and ERROR message is displayed
        if item > 0:
            flash('ERROR: Item is already present in the Database!')
        return redirect(url_for('show_catalog'))
    else:
        return render_template('new_item.html')


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del_me = login_session.get('credentials')
            del del_me
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        # Succesfully logs out the user with the message.
        flash("You have successfully been logged out.")
        return redirect(url_for('show_catalog'))
    # Displays the message if user is not logged
    # in or if session has expired.
    else:
        flash("You were not logged in")
        return redirect(url_for('show_catalog'))


# Runs the server on this 'http://localhost:8000' Link.
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
