from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import g
from app import db, CashDesks
from flask import flash
from .forms import CashDeskForm # в поточній директорії

cash_desks = Blueprint('cash_desks', __name__, template_folder='templates', static_folder='static')

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Види операцій', 'url': '/types_of_moves'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        # {'name': 'Про програму', 'url': '/about'}
        ]


# http://localhost:5000/cash_desks/
@cash_desks.route('/')
def index():
    q = request.args.get('q')
    if q:
        cash_desks_list = CashDesks.query.filter(CashDesks.name.contains(q)).order_by(CashDesks.name)
    else:
        cash_desks_list = CashDesks.query.order_by(CashDesks.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = cash_desks_list.paginate(page=page, per_page=6)

    return render_template('cash_desks/index.html', menu=menu, title='Список кас', pages=pages)


# http://localhost:5000/cash_desks/1
@cash_desks.route('/<id>')
def cash_desk_detail(id):
    cash_desk_element = CashDesks.query.filter(CashDesks.id == id).first()
    return render_template('cash_desks/cash_desk_detail.html', menu=menu, title="Карточка каси", cash_desk_element=cash_desk_element)


# http://localhost:5000/cash_desks/create
@cash_desks.route('/create', methods=['POST', 'GET'])
def cash_desk_create():
    cash_desk_element = CashDesks.query.filter(False).first()
    form = CashDeskForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            cash_desk_element = CashDesks(name=request.form.get('name'))
            try:
                db.session.add(cash_desk_element)
                db.session.commit()
                flash('Касу створено', category='success')
            except:
                flash('Помилка створення каси', category='error')

            # print('cash_desk_create()', 'cash_desk_element.id: ', cash_desk_element.id)
            return redirect(url_for('.cash_desk_detail', id=cash_desk_element.id))

        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('cash_desks/cash_desk_create.html', menu=menu, title="Створення каси",
                           cash_desk_element=cash_desk_element, form=form)


# http://localhost:5000/cash_desks/1/edit
@cash_desks.route('/<id>/edit', methods=['POST', 'GET'])
def cash_desk_edit(id):
    cash_desk_element = CashDesks.query.filter(CashDesks.id == id).first()
    form = CashDeskForm(id=cash_desk_element.id, name=cash_desk_element.name)
    if request.method == 'POST':
        if form.validate_on_submit():
            cash_desk_element = CashDesks(id=id, name=request.form.get('name'))
            try:
                db.session.merge(cash_desk_element)
                db.session.commit()
                flash('Касу оновлено', category='success')
            except:
                flash('Помилка оновлення каси', category='error')

            return redirect(url_for('.cash_desk_detail', id=cash_desk_element.id))
        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('cash_desks/cash_desk_edit.html', menu=menu, title="Редагування каси", cash_desk_element=cash_desk_element, form=form)


# http://localhost:5000/cash_desks/1/edit
@cash_desks.route('/<id>/delete', methods=['POST', 'GET'])
def cash_desk_delete(id):
    try:
        CashDesks.query.filter(CashDesks.id == id).delete()
        db.session.commit()
        flash('Касу видалено', category='success')
    except:
        flash('Помилка видалення каси', category='error')

    return redirect(url_for('.index'))
