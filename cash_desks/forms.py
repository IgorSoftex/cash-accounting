from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class CashDeskForm(FlaskForm):
    id = IntegerField('Ідентифікатор: ', render_kw={'readonly': True}, default=0)
    name = StringField('Назва: ', validators=[DataRequired(), Length(min=1, max=140, message='Назва')])
    submit = SubmitField('Записати')
