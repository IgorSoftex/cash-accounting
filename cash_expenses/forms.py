from wtforms import StringField, SubmitField, IntegerField, DateField, DecimalField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class CashExpensesForm(FlaskForm):
    id = IntegerField('Номер: ', render_kw={'readonly': True}, default=0)
    date = DateField('Дата: ', validators=[DataRequired()])
    type_id = HiddenField('ID:', render_kw={'readonly': True})
    type_name = StringField('Операція:', render_kw={'readonly': True})
    cash_desk_id = HiddenField('ID:', render_kw={'readonly': True})
    cash_desk_name = StringField('Каса:', render_kw={'readonly': True})
    client_id = HiddenField('ID:', render_kw={'readonly': True})
    client_name = StringField('Кому:', render_kw={'readonly': True})
    currency_code = HiddenField('Валюта:', render_kw={'readonly': True})
    currency_name = StringField('Валюта', render_kw={'readonly': True})
    sum = DecimalField('Сума:')
    description = StringField('Коментарій:')
    submit = SubmitField('Записати')
