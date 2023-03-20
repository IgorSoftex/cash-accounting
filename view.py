from app import app
from flask import render_template

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Види операцій', 'url': '/types_of_moves'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        # {'name': 'Про програму', 'url': '/about'}
        ]


@app.route('/')
def index():
    return render_template('index.html', menu=menu, title='Касовий облік Холдингу')


@app.route('/about')
def about():
    return render_template('about.html', menu=menu, title='Касовий облік Холдингу v 1.0.0.1')
