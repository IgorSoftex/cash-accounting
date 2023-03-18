from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import g
from app import db, CashExpenses, TypesOfMoves, Clients, CashDesks, Currency
from flask import flash
from .forms import CashExpensesForm # в поточній директорії
from datetime import datetime

cash_expenses = Blueprint('cash_expenses', __name__, template_folder='templates', static_folder='static')

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        {'name': 'Про програму', 'url': '/about'}
        ]

form_data = {}
operation_name = ''

# http://localhost:5000/cash_expenses/
@cash_expenses.route('/')
def index():
    q = request.args.get('q')
    if q:
        cash_expenses_list = db.session.query(CashExpenses).join(
            TypesOfMoves, CashExpenses.type_id == TypesOfMoves.id
        ).join(
            CashDesks, CashExpenses.cash_desk_id == CashDesks.id
        ).filter(CashExpenses.id.contains(q) | CashExpenses.description.contains(q) | TypesOfMoves.name.contains(q) | CashDesks.name.contains(q)
                 ).order_by(CashExpenses.date.desc(), CashExpenses.id.desc())
    else:
        cash_expenses_list = CashExpenses.query.order_by(CashExpenses.date.desc(), CashExpenses.id.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = cash_expenses_list.paginate(page=page, per_page=10)

    return render_template('cash_expenses/index.html', menu=menu, title='Список касових витрат', pages=pages)


# http://localhost:5000/cash_expenses/1
@cash_expenses.route('/<id>')
def cash_expense_detail(id):
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == id).first()
    return render_template('cash_expenses/cash_expense_detail.html', menu=menu, title="Прихід в касу", cash_expense_element=cash_expense_element)


# http://localhost:5000/cash_expenses/create
@cash_expenses.route('/create', methods=['POST', 'GET'])
def cash_expense_create():
    global form_data, operation_name
    operation_name = 'cash_expense_create'
    form = CashExpensesForm(date=datetime.now(), sum=0,
                            currency_code='UAH', currency_name='Гривня')
    if request.method == 'POST':
        form_data = {"id": request.form.get("id"),
                     "date": request.form.get("date"),
                     "sum": request.form.get("sum"),
                     "type_id": request.form.get("type_id"),
                     "type_name": request.form.get("type_name"),
                     "cash_desk_id": request.form.get("cash_desk_id"),
                     "cash_desk_name": request.form.get("cash_desk_name"),
                     "client_id": request.form.get("client_id"),
                     "client_name": request.form.get("client_name"),
                     "currency_code": request.form.get("currency_code"),
                     "currency_name": request.form.get("currency_name"),
                     "description": request.form.get("description")
                     }
        # print(form_data)
        if request.form.get('client_choice'):  # вибір клієнта
            return redirect(url_for('.client_choice'))

        elif request.form.get('cash_desk_choice'):  # вибір каси
            return redirect(url_for('.cash_desk_choice'))

        elif request.form.get('type_choice'):  # вибір операції
            return redirect(url_for('.type_choice'))

        elif request.form.get('currency_choice'):  # вибір валюти
            return redirect(url_for('.currency_choice'))

        else:
            if form.validate_on_submit():
                cash_expenses_element = CashExpenses(date=request.form.get('date'), sum=request.form.get('sum'),
                                                     type_id=request.form.get('type_id'), cash_desk_id=request.form.get('cash_desk_id'),
                                                     client_id=request.form.get('client_id'), currency_code=request.form.get('currency_code'),
                                                     description=request.form.get('description'))
                # print(cash_expenses_element)
                # try:
                db.session.add(cash_expenses_element)
                db.session.commit()
                flash('Розхід з каси створено', category='success')
                # except:
                #     flash('Помилка створення витрати з каси', category='error')

                return redirect(url_for('.cash_expense_detail', id=cash_expenses_element.id))

            else:
                flash('Форма не пройшла валідацію', category='error')
                return 'Форма не пройшла валідацію'

    else:
        return render_template('cash_expenses/cash_expense_create.html', menu=menu, title="Створення витрати з каси", form=form)


# http://localhost:5000/cash_expenses/1/edit
@cash_expenses.route('/<id>/edit', methods=['POST', 'GET'])
def cash_expense_edit(id):
    global form_data, operation_name
    operation_name = 'cash_expense_edit'
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == id).first()
    form = CashExpensesForm(id=cash_expense_element.id, date=cash_expense_element.date,
                            type_id=cash_expense_element.type.id, type_name=cash_expense_element.type.name,
                            cash_desk_id=cash_expense_element.cash_desk.id, cash_desk_name=cash_expense_element.cash_desk.name,
                            client_id=cash_expense_element.client.id, client_name=cash_expense_element.client.name,
                            currency_code=cash_expense_element.currency.code, currency_name=cash_expense_element.currency.name,
                            sum=cash_expense_element.sum,
                            description=cash_expense_element.description
                            )
    if request.method == 'POST':
        form_data = {"id": request.form.get("id"),
                     "date": request.form.get("date"),
                     "sum": request.form.get("sum"),
                     "type_id": request.form.get("type_id"),
                     "type_name": request.form.get("type_name"),
                     "cash_desk_id": request.form.get("cash_desk_id"),
                     "cash_desk_name": request.form.get("cash_desk_name"),
                     "client_id": request.form.get("client_id"),
                     "client_name": request.form.get("client_name"),
                     "currency_code": request.form.get("currency_code"),
                     "currency_name": request.form.get("currency_name"),
                     "description": request.form.get("description")
                     }
        if request.form.get('client_choice'):  # вибір клієнта
            return redirect(url_for('.client_choice'))

        elif request.form.get('cash_desk_choice'):  # вибір каси
            return redirect(url_for('.cash_desk_choice'))

        elif request.form.get('type_choice'):  # вибір операції
            return redirect(url_for('.type_choice'))

        elif request.form.get('currency_choice'):  # вибір валюти
            return redirect(url_for('.currency_choice'))

        else:
            if form.validate_on_submit():
                cash_expense_element = CashExpenses(id=id, date=request.form.get('date'),
                                                    type_id=request.form.get('type_id'),
                                                    cash_desk_id=request.form.get('cash_desk_id'),
                                                    client_id=request.form.get('client_id'),
                                                    currency_code=request.form.get('currency_code'),
                                                    sum=request.form.get('sum'),
                                                    description=request.form.get('description')
                                                    )
                try:
                    db.session.merge(cash_expense_element)
                    db.session.commit()
                    flash('Документ оновлено', category='success')
                except:
                    flash('Помилка оновлення документа', category='error')

                return redirect(url_for('.cash_expense_detail', id=cash_expense_element.id))
            else:
                flash('Форма не пройшла валідацію', category='error')

    return render_template('cash_expenses/cash_expense_edit.html', menu=menu, title="Редагування витрати з каси", cash_expense_element=cash_expense_element, form=form)


# http://localhost:5000/cash_expenses/1/delete
@cash_expenses.route('/<id>/delete', methods=['POST', 'GET'])
def cash_expense_delete(id):
    try:
        CashExpenses.query.filter(CashExpenses.id == id).delete()
        db.session.commit()
        flash('Документ видалено', category='success')
    except:
        flash('Помилка видалення документа', category='error')

    return redirect(url_for('.index'))


@cash_expenses.route('/client_choice/')
def client_choice():
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
    pages = clients_list.paginate(page=page, per_page=10)

    return render_template('cash_expenses/client_choice.html', menu=menu, title='Форма вибору',
                           pages=pages)


@cash_expenses.route('/client_after_choice/<client_id>')
def client_after_choice(client_id):
    global form_data, operation_name
    client = Clients.query.filter(Clients.id == client_id).first()
    # print('client_after_choice()', 'client:', client, 'operation_name:', operation_name)
    date = form_data["date"]
    date = datetime.strptime(date, '%Y-%m-%d')
    sum = form_data["sum"]
    sum = float(sum)
    cash_desk_id = form_data["cash_desk_id"]
    cash_desk_name = form_data["cash_desk_name"]
    type_id = form_data["type_id"]
    type_name = form_data["type_name"]
    currency_code = form_data["currency_code"]
    currency_name = form_data["currency_name"]
    description = form_data["description"]
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == form_data["id"]).first()
    form = CashExpensesForm(id=form_data["id"], client_id=client_id, client_name=client.name,
                            date=date, sum=sum,
                            cash_desk_id=cash_desk_id, cash_desk_name=cash_desk_name,
                            type_id=type_id, type_name=type_name,
                            currency_code=currency_code, currency_name=currency_name,
                            description=description)
    if operation_name == 'cash_expense_create':
        return render_template('cash_expenses/cash_expense_create.html', menu=menu,
                               title="Створення витрати з каси", form=form)
    elif operation_name == 'cash_expense_edit':
        return render_template('cash_expenses/cash_expense_edit.html', menu=menu,
                               title="Редагування витрати з каси", form=form,
                               cash_expense_element=cash_expense_element)
    else:
        return 'client_after_choice ???'


@cash_expenses.route('/cash_desk_choice/')
def cash_desk_choice():
    q = request.args.get('q')
    if q:
        cash_desks_list = CashDesks.query.filter(CashDesks.name.contains(q))
    else:
        cash_desks_list = CashDesks.query.order_by(CashDesks.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = cash_desks_list.paginate(page=page, per_page=10)

    return render_template('cash_expenses/cash_desk_choice.html', menu=menu, title='Форма вибору',
                           pages=pages)


@cash_expenses.route('/cash_desk_after_choice/<cash_desk_id>')
def cash_desk_after_choice(cash_desk_id):
    global form_data, operation_name
    cash_desk = CashDesks.query.filter(CashDesks.id == cash_desk_id).first()
    date = form_data["date"]
    date = datetime.strptime(date, '%Y-%m-%d')
    sum = form_data["sum"]
    sum = float(sum)
    client_id = form_data["client_id"]
    client_name = form_data["client_name"]
    type_id = form_data["type_id"]
    type_name = form_data["type_name"]
    currency_code = form_data["currency_code"]
    currency_name = form_data["currency_name"]
    description = form_data["description"]
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == form_data["id"]).first()
    form = CashExpensesForm(id=form_data["id"], cash_desk_id=cash_desk_id, cash_desk_name=cash_desk.name,
                            date=date, sum=sum,
                            client_id=client_id, client_name=client_name,
                            type_id=type_id, type_name=type_name,
                            currency_code=currency_code, currency_name=currency_name,
                            description=description)
    if operation_name == 'cash_expense_create':
        return render_template('cash_expenses/cash_expense_create.html', menu=menu, title="Створення витрати з каси", form=form)
    elif operation_name == 'cash_expense_edit':
        return render_template('cash_expenses/cash_expense_edit.html', menu=menu,
                               title="Редагування витрати з каси", form=form,
                               cash_expense_element=cash_expense_element)
    else:
        return 'cash_desk_after_choice ???'


@cash_expenses.route('/type_choice/')
def type_choice():
    q = request.args.get('q')

    if operation_name == 'cash_expense_create' or operation_name == 'cash_expense_edit':
        debit = 0
    else:
        debit = 1

    if q:
        type_list = TypesOfMoves.query.filter(TypesOfMoves.debit.contains(debit) & TypesOfMoves.name.contains(q)).order_by(TypesOfMoves.name)
    else:
        type_list = TypesOfMoves.query.filter(TypesOfMoves.debit==debit).order_by(TypesOfMoves.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = type_list.paginate(page=page, per_page=10)

    return render_template('cash_expenses/type_choice.html', menu=menu, title='Форма вибору',
                           pages=pages)


@cash_expenses.route('/type_after_choice/<type_id>')
def type_after_choice(type_id):
    global form_data, operation_name
    type_of_moves = TypesOfMoves.query.filter(TypesOfMoves.id == type_id).first()
    # print('type_after_choice()', 'type:', type, 'operation_name:', operation_name)
    date = form_data["date"]
    date = datetime.strptime(date, '%Y-%m-%d')
    sum = form_data["sum"]
    sum = float(sum)
    cash_desk_id = form_data["cash_desk_id"]
    cash_desk_name = form_data["cash_desk_name"]
    client_id = form_data["client_id"]
    client_name = form_data["client_name"]
    currency_code = form_data["currency_code"]
    currency_name = form_data["currency_name"]
    description = form_data["description"]
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == form_data["id"]).first()
    form = CashExpensesForm(id=form_data["id"], type_id=type_id, type_name=type_of_moves.name,
                            date=date, sum=sum,
                            client_id=client_id, client_name=client_name,
                            cash_desk_id=cash_desk_id, cash_desk_name=cash_desk_name,
                            currency_code=currency_code, currency_name=currency_name,
                            description=description)
    if operation_name == 'cash_expense_create':
        return render_template('cash_expenses/cash_expense_create.html', menu=menu,
                               title="Створення витрати з каси", form=form)
    elif operation_name == 'cash_expense_edit':
        return render_template('cash_expenses/cash_expense_edit.html', menu=menu,
                               title="Редагування витрати з каси", form=form,
                               cash_expense_element=cash_expense_element)
    else:
        return 'type_after_choice ???'


@cash_expenses.route('/currency_choice/')
def currency_choice():
    q = request.args.get('q')

    if q:
        currency_list = Currency.query.filter(Currency.code.contains(q) & Currency.name.contains(q)).order_by(Currency.name)
    else:
        currency_list = Currency.query.order_by(Currency.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = currency_list.paginate(page=page, per_page=10)

    return render_template('cash_expenses/currency_choice.html', menu=menu, title='Форма вибору',
                           pages=pages)


@cash_expenses.route('/currency_after_choice/<currency_code>')
def currency_after_choice(currency_code):
    global form_data, operation_name
    currency = Currency.query.filter(Currency.code == currency_code).first()
    date = form_data["date"]
    date = datetime.strptime(date, '%Y-%m-%d')
    sum = form_data["sum"]
    sum = float(sum)
    cash_desk_id = form_data["cash_desk_id"]
    cash_desk_name = form_data["cash_desk_name"]
    client_id = form_data["client_id"]
    client_name = form_data["client_name"]
    type_id = form_data["type_id"]
    type_name = form_data["type_name"]
    description = form_data["description"]
    cash_expense_element = CashExpenses.query.filter(CashExpenses.id == form_data["id"]).first()
    form = CashExpensesForm(id=form_data["id"], currency_code=currency_code, currency_name=currency.name,
                            date=date, sum=sum,
                            client_id=client_id, client_name=client_name,
                            cash_desk_id=cash_desk_id, cash_desk_name=cash_desk_name,
                            type_id=type_id, type_name=type_name,
                            description=description)
    if operation_name == 'cash_expense_create':
        # print('type_after_choice() - cash_expense_create')
        return render_template('cash_expenses/cash_expense_create.html', menu=menu, title="Створення витрати з каси", form=form)
    elif operation_name == 'cash_expense_edit':
        return render_template('cash_expenses/cash_expense_edit.html', menu=menu,
                               title="Редагування витрати з каси", form=form,
                               cash_expense_element=cash_expense_element)
    else:
        return 'type_after_choice ???'


