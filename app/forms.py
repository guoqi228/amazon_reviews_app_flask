from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class SubmitProductIdForm(FlaskForm):
    productId = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Please enter Amazon product ASIN number"})
    submit = SubmitField('GO', render_kw={"data-toggle":"modal", "data-target":"#exampleModalCenter"})
