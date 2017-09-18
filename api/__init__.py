from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

from instance.config import app_config
from api.models import ShoppingListApi
from api.models import User

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/dashboard/', methods=['POST', 'GET'])
    def dashboard():
        if request.method == "POST":
            items = str(request.data.get(item='', quantity='', price=''))
            if items:
                shopping_list = ShoppingListApi(item=request.data.item, quantity=request.data.quantity,
                                                price=request.data.price)
                shopping_list.save()
                response = jsonify({
                    'id': shopping_list.id,
                    'item': shopping_list.item,
                    'quantity': shopping_list.quantity,
                    'price': shopping_list.price,
                    'date_created': shopping_list.date_created,
                    'date_modified': shopping_list.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            shopping = ShoppingListApi.get_all()
            results = []

            for shopping_list in shopping:
                obj = {
                    'id': shopping_list.id,
                    'item': shopping_list.item,
                    'quantity': shopping_list.quantity,
                    'price': shopping_list.price,
                    'date_created': shopping_list.date_created,
                    'date_modified': shopping_list.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/dashboard/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def dashboard_manipulation(id):
        # retrieve a shopping list using it's ID
        shopping_list = ShoppingListApi.query.filter_by(id=id).first()
        if not shopping_list:
            # Raise an HTTPException with a 404 not found status code
            return abort(404)

        if request.method == 'DELETE':
            shopping_list.delete()
            return {
                       "message": "Shopping list {} deleted successfully".format(shopping_list.id)
                   }, 200

        elif request.method == 'PUT':
            item = str(request.data.get(item='', quantity='', price=''))
            shopping_list.item = item
            shopping_list.save()
            response = jsonify({
                'id': shopping_list.id,
                'item': shopping_list.item,
                'quantity': shopping_list.quantity,
                'price': shopping_list.price,
                'date_created': shopping_list.date_created,
                'date_modified': shopping_list.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': shopping_list.id,
                'item': shopping_list.item,
                'quantity': shopping_list.quantity,
                'price': shopping_list.price,
                'date_created': shopping_list.date_created,
                'date_modified': shopping_list.date_modified
            })
            response.status_code = 200
        return response

    """User Sign Up Api section"""
    @app.route('/signup/', methods=['POST', 'GET'])
    def signup():
        if request.method == "POST":
            users = str(request.data.get(email='', username='', password=''))
            if users:
                user = User(email=request.data.email, username=request.data.username,
                            password=request.data.password)
                user.save()
                response = jsonify({
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'password': user.password
                })
                response.status_code = 201
                return response
        else:
            # GET
            app_users = User.get_all()
            results = []

            for user in app_users:
                obj = {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'password': user.password
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/signup/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def signup_manipulation(id):
        # retrieve  the user accounts using it's ID
        user = User.query.filter_by(id=id).first()
        if not user:
            # Raise an Exception with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            user.delete()
            return {
                       "message": "Account {} deleted successfully".format(user.id)
                   }, 200

        elif request.method == 'PUT':
            user_details = str(request.data.get(email='', username='', password=''))
            user.email = user_details
            user.username = user_details
            user.save()
            response = jsonify({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'password': user.password
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'password': user.password
            })
            response.status_code = 200
            return response

    return app
