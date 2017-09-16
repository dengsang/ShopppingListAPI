from app import db


class ShoppingListApi(db.Model):
    """This class represents the Shopping list table."""

    __tablename__ = 'shopping_list'

    item = db.Column(db.String(255), primary_key=True)
    quantity = db.Column(db.Integer(20))
    price = db.Column(db.Integer(30))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, item, quantity, price):
        self.item = item
        self.quantity = quantity
        self.price = price

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ShoppingListApi.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Shopping-List: {}>".format({self.item, self.quantity, self.price})


class User(db.Model):

    __tablename__ = 'shopping_users'

    email = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Shopping App Users: {}>".format({self.email, self.username, self.password})
