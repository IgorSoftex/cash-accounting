from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import g
from app import db, Currency
from flask import flash
from .forms import CurrencyForm # в поточній директорії

currency = Blueprint('currency', __name__, template_folder='templates', static_folder='static')

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Види операцій', 'url': '/types_of_moves'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        # {'name': 'Про програму', 'url': '/about'}
        ]


# http://localhost:5000/currency/
@currency.route('/')
def index():
    q = request.args.get('q')
    if q:
        currency_list = Currency.query.filter(Currency.code.contains(q) | Currency.name.contains(q)).order_by(Currency.name)
    else:
        currency_list = Currency.query.order_by(Currency.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = currency_list.paginate(page=page, per_page=10)

    return render_template('currency/index.html', menu=menu, title='Список валют', pages=pages)


# http://localhost:5000/currency/1
@currency.route('/<code>')
def currency_detail(code):
    currency_element = Currency.query.filter(Currency.code == code).first()
    return render_template('currency/currency_detail.html', menu=menu, title="Валюта", currency_element=currency_element)


# http://localhost:5000/currency/create
@currency.route('/create', methods=['POST', 'GET'])
def currency_create():
    currency_element = Currency.query.filter(False).first()
    form = CurrencyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            currency_element = Currency(code=request.form.get('code'), name=request.form.get('name'))
            try:
                db.session.add(currency_element)
                db.session.commit()
                flash('Валюту створено', category='success')
            except:
                flash('Помилка створення валюти', category='error')

            # print('currency_create()', 'currency_element.code: ', currency_element.code)
            return redirect(url_for('.currency_detail', code=currency_element.code))

        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('currency/currency_create.html', menu=menu, title="Створення валюти",
                           currency_element=currency_element, form=form)


# http://localhost:5000/currency/1/edit
@currency.route('/<code>/edit', methods=['POST', 'GET'])
def currency_edit(code):
    currency_element = Currency.query.filter(Currency.code == code).first()
    form = CurrencyForm(code=currency_element.code, name=currency_element.name)
    if request.method == 'POST':
        if form.validate_on_submit():
            currency_element = Currency(code=code, name=request.form.get('name'))
            try:
                db.session.merge(currency_element)
                db.session.commit()
                flash('Валюту оновлено', category='success')
            except:
                flash('Помилка оновлення валюти', category='error')

            return redirect(url_for('.currency_detail', code=currency_element.code))
        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('currency/currency_edit.html', menu=menu, title="Редагування валюти", currency_element=currency_element, form=form)


# http://localhost:5000/currency/1/delete
@currency.route('/<code>/delete', methods=['POST', 'GET'])
def currency_delete(code):
    try:
        Currency.query.filter(Currency.code == code).delete()
        db.session.commit()
        flash('Валюту видалено', category='success')
    except:
        flash('Помилка видалення валюти', category='error')

    return redirect(url_for('.index'))
