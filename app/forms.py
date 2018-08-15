from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class SubmitProductIdForm(FlaskForm):
    productId = StringField('',validators=[DataRequired()], render_kw={"placeholder": "Please enter Amazon product ASIN number"})
    submit = SubmitField('GO', render_kw={"data-toggle":"", "data-target":"#exampleModalCenter", "onclick":"checkEmpty()"})

class RidgePredictionForm(FlaskForm):
    degree = IntegerField('Polynomial Degree (Recommend: 5)', validators=[DataRequired(), NumberRange(min=1, max=10)], render_kw={"placeholder": "Please choose from 1 to 10"})
    alpha = DecimalField('Regularization Term (Recommend: 1.0)', places=1, validators=[DataRequired()], render_kw={"placeholder": "Please enter the value for alpha"})
    submit = SubmitField('Predict', render_kw={"id":"ridge-submit"})

class AdaPredictionForm(FlaskForm):
    depth = IntegerField('Maximum Depth (Recommend: 3)', validators=[DataRequired(), NumberRange(min=3, max=15)], render_kw={"placeholder": "Please choose from 3 to 15"})
    submit = SubmitField('Predict', render_kw={"id":"ada-submit"})
