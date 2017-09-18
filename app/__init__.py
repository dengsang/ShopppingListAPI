from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

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

    return app
