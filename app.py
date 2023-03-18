from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db, command='db')   # https://flask-migrate.readthedocs.io/en/latest/

app.app_context().push()    # Ihor


""" models """
class CashDesks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)

    cash_receipts = db.relationship('CashReceipts', backref='cash_desk', lazy=True)
    cash_expenses = db.relationship('CashExpenses', backref='cash_desk', lazy=True)

    def __init__(self, *args, **kwargs):
        super(CashDesks, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}'.format(self.name)


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    cash_receipts = db.relationship('CashReceipts', backref='client', lazy=True)
    cash_expenses = db.relationship('CashExpenses', backref='client', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Clients, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}'.format(self.name)


class TypesOfMoves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    debit = db.Column(db.Integer, nullable=False)

    cash_receipts = db.relationship('CashReceipts', backref='type', lazy=True)
    cash_expenses = db.relationship('CashExpenses', backref='type', lazy=True)

    def __init__(self, *args, **kwargs):
        super(TypesOfMoves, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}'.format(self.name)


class Currency(db.Model):
    """Валюти"""
    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    cash_receipts = db.relationship('CashReceipts', backref='currency', lazy=True)
    cash_expenses = db.relationship('CashExpenses', backref='currency', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Currency, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{}'.format(self.name)


class CashReceipts(db.Model):
    """операції поступлення грошей в касу"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.now())
    type_id = db.Column(db.Integer, db.ForeignKey('types_of_moves.id'), nullable=False)
    cash_desk_id = db.Column(db.Integer, db.ForeignKey('cash_desks.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    currency_code = db.Column(db.String(3), db.ForeignKey('currency.code'), nullable=False)
    sum = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        super(CashReceipts, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{} від {}, операція: {}, № каса: {}, № клієнт: {}'.format(self.id, self.date,
                                                                          self.type.name, self.cash_desk.name,
                                                                          self.client.name)


class CashExpenses(db.Model):
    """операції витрати грошей з каси"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.now())
    type_id = db.Column(db.Integer, db.ForeignKey('types_of_moves.id'), nullable=False)
    cash_desk_id = db.Column(db.Integer, db.ForeignKey('cash_desks.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    currency_code = db.Column(db.String(3), db.ForeignKey('currency.code'), nullable=False)
    sum = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        super(CashExpenses, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{} від {}, операція: {}, № каса: {}, № клієнт: {}'.format(self.id, self.date,
                                                                          self.type.name,
                                                                          self.cash_desk.name,
                                                                          self.client.name)
        # return '{} від {}, операція: {}, № каса: {}, № клієнт: {}'.format(self.id, self.date,
        #                                                                   self.type,
        #                                                                   self.cash_desk,
        #                                                                   self.client)

