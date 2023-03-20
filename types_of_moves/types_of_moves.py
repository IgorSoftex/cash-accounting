from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask import g
from app import db, TypesOfMoves
from flask import flash
from .forms import TypesOfMovesForm # в поточній директорії

types_of_moves = Blueprint('types_of_moves', __name__, template_folder='templates', static_folder='static')

menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Каси', 'url': '/cash_desks'},
        {'name': 'Контрагенти', 'url': '/clients'},
        {'name': 'Валюти', 'url': '/currency'},
        {'name': 'Види операцій', 'url': '/types_of_moves'},
        {'name': 'Надходження в касу', 'url': '/cash_receipts'},
        {'name': 'Розхід з каси', 'url': '/cash_expenses'},
        # {'name': 'Про програму', 'url': '/about'}
        ]


# http://localhost:5000/types_of_moves/
@types_of_moves.route('/')
def index():
    q = request.args.get('q')
    if q:
        types_of_moves_list = TypesOfMoves.query.filter(TypesOfMoves.name.contains(q) | TypesOfMoves.debit.contains(q))
    else:
        types_of_moves_list = TypesOfMoves.query.order_by(TypesOfMoves.name)

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = types_of_moves_list.paginate(page=page, per_page=8)

    return render_template('types_of_moves/index.html', menu=menu, title='Список видів операцій', pages=pages)


# http://localhost:5000/types_of_moves/1
@types_of_moves.route('/<id>/')
def type_of_move_detail(id):
    type_of_move_element = TypesOfMoves.query.filter(TypesOfMoves.id == id).first()
    return render_template('types_of_moves/type_of_move_detail.html', menu=menu, title="Карточка виду операції", type_of_move_element=type_of_move_element)


# http://localhost:5000/types_of_moves/create
@types_of_moves.route('/create', methods=['POST', 'GET'])
def type_of_move_create():
    type_of_move_element = TypesOfMoves.query.filter(False).first()
    form = TypesOfMovesForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            type_of_move_element = TypesOfMoves(name=request.form.get('name'), debit=request.form.get('debit'))
            try:
                db.session.add(type_of_move_element)
                db.session.commit()
                flash('Вид операції створено', category='success')
            except:
                flash('Помилка створення виду операції', category='error')

            return redirect(url_for('.type_of_move_detail', id=type_of_move_element.id))

        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('types_of_moves/type_of_move_create.html', menu=menu, title="Створення виду операції",
                           type_of_move_element=type_of_move_element, form=form)


# http://localhost:5000/types_of_moves/1/edit
@types_of_moves.route('/<id>/edit', methods=['POST', 'GET'])
def type_of_move_edit(id):
    type_of_move_element = TypesOfMoves.query.filter(TypesOfMoves.id == id).first()
    form = TypesOfMovesForm(id=type_of_move_element.id,
                            name=type_of_move_element.name,
                            debit=type_of_move_element.debit)
    if request.method == 'POST':
        if form.validate_on_submit():
            type_of_move_element = TypesOfMoves(id=id, name=request.form.get('name'), debit=request.form.get('debit'))
            try:
                db.session.merge(type_of_move_element)
                db.session.commit()
                flash('Вид операції оновлено', category='success')
            except:
                flash('Помилка оновлення виду операції', category='error')

            return redirect(url_for('.type_of_move_detail', id=type_of_move_element.id))
        else:
            flash('Форма не пройшла валідацію', category='error')

    return render_template('types_of_moves/type_of_move_edit.html', menu=menu, title="Редагування виду операції", type_of_move_element=type_of_move_element, form=form)


# http://localhost:5000/types_of_moves/1/edit
@types_of_moves.route('/<id>/delete', methods=['POST', 'GET'])
def type_of_move_delete(id):
    try:
        TypesOfMoves.query.filter(TypesOfMoves.id == id).delete()
        db.session.commit()
        flash('Вид операції видалено', category='success')
    except:
        flash('Помилка видалення виду операції', category='error')

    return redirect(url_for('.index'))
