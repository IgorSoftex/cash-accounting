from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import g
from app import db, Clients
from flask import flash
from .forms import ClientsForm # в поточній директорії

clients = Blueprint('clients', __name__, template_folder='templates', static_folder='static')

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Види операцій', 'url': '/types_of_moves'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        # {'name': 'Про програму', 'url': '/about'}
        ]


# http://localhost:5000/clients/
@clients.route('/')
def index():
    q = request.args.get('q')
    if q:
        clients_list = Clients.query.filter(Clients.name.contains(q))
    else:
        clients_list = Clients.query.order_by(Clients.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = clients_list.paginate(page=page, per_page=8)

    return render_template('clients/index.html', menu=menu, title='Список контрагентів', pages=pages)


# http://localhost:5000/clients/1
@clients.route('/<id>/')
def client_detail(id):
    client_element = Clients.query.filter(Clients.id == id).first()
    return render_template('clients/client_detail.html', menu=menu, title="Карточка контрагента", client_element=client_element)


# http://localhost:5000/clients/create
@clients.route('/create', methods=['POST', 'GET'])
def client_create():
    client_element = Clients.query.filter(False).first()
    form = ClientsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            client_element = Clients(name=request.form.get('name'))
            try:
                db.session.add(client_element)
                db.session.commit()
                flash('Контрагента створено', category='success')
            except:
                flash('Помилка створення контрагента', category='error')

            return redirect(url_for('.client_detail', id=client_element.id))

        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('clients/client_create.html', menu=menu, title="Створення контрагента",
                           client_element=client_element, form=form)


# http://localhost:5000/clients/1/edit
@clients.route('/<id>/edit', methods=['POST', 'GET'])
def client_edit(id):
    client_element = Clients.query.filter(Clients.id == id).first()
    form = ClientsForm(id=client_element.id, name=client_element.name)
    if request.method == 'POST':
        if form.validate_on_submit():
            client_element = Clients(id=id, name=request.form.get('name'))
            try:
                db.session.merge(client_element)
                db.session.commit()
                flash('Контрагента оновлено', category='success')
            except:
                flash('Помилка оновлення контрагента', category='error')

            return redirect(url_for('.client_detail', id=client_element.id))
        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('clients/client_edit.html', menu=menu, title="Редагування контрагента", client_element=client_element, form=form)


# http://localhost:5000/clients/1/edit
@clients.route('/<id>/delete', methods=['POST', 'GET'])
def client_delete(id):
    try:
        Clients.query.filter(Clients.id == id).delete()
        db.session.commit()
        flash('Контрагента видалено', category='success')
    except:
        flash('Помилка видалення контрагента', category='error')

    return redirect(url_for('.index'))
