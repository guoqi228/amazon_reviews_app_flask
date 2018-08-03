from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class SubmitProductIdForm(FlaskForm):
    productId = StringField('',validators=[DataRequired()], default=u"Enter Amazon ASIN Number")
    submit = SubmitField('GO')
