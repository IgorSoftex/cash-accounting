from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class ClientsForm(FlaskForm):
    id = IntegerField('Ідентифікатор: ', render_kw={'readonly': True}, default=0)
    name = StringField('Назва: ', validators=[DataRequired(), Length(min=1, max=140, message='Назва')])
    # full_name = StringField('Повна назва: ', validators=[DataRequired(), Length(min=1, max=200, message='Повна назва')])
    # address = StringField('Адреса: ')
    # edrpou_code = StringField('Код по ЄДРПОУ: ')
    submit = SubmitField('Записати')
