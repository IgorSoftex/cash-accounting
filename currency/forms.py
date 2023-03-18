from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class CurrencyForm(FlaskForm):
    code = StringField('Код: ', validators=[DataRequired(), Length(min=3, max=3, message='Код')])
    name = StringField('Назва: ', validators=[DataRequired(), Length(min=3, max=100, message='Назва')])
    submit = SubmitField('Записати')
