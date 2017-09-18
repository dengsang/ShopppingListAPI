from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

from instance.config import app_config
from app.models import ShoppingListApi

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
            shoppings = ShoppingListApi.get_all()
            results = []

            for shopping_list in shoppings:
                obj = {
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
    def dashboard_manipulation(id, **kwargs):
        # retrieve a shopping list using it's ID
        shopping_list = ShoppingListApi.query.filter_by(id=id).first()
        if not shopping_list:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            shopping_list.delete()
            return {
                       "message": "Shopping list {} deleted successfully".format(shopping_list.id)
                   }, 200

        elif request.method == 'PUT':
            items = str(request.data.get(item='', quantity='', price=''))
            shopping_list.name = items
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

    return app
