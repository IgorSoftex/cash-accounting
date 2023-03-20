from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class TypesOfMovesForm(FlaskForm):
    id = IntegerField('Ідентифікатор: ', render_kw={'readonly': True}, default=0)
    name = StringField('Назва: ', validators=[DataRequired(), Length(min=1, max=140, message='Назва')])
    debit = IntegerField('Прихід(1)/Розхід(0): ', render_kw={'readonly': False}, default=0)
    submit = SubmitField('Записати')
