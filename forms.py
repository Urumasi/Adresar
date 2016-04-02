from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(Form):
    firstname = StringField('Jméno', validators=[DataRequired()])
    lastname = StringField('Příjmení', validators=[DataRequired()])
    submit = SubmitField('Submit')