from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired


class TimerForm(FlaskForm):
    time = FloatField('time', validators=[DataRequired()])
