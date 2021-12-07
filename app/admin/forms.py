from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, BooleanField, SelectField, DecimalField, IntegerField,\
    FileField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegionForm(FlaskForm):
    ru = StringField("Название по-русски")
    ua = StringField("Назва українською")
    submit = SubmitField("Сохранить")

services = (
    ('i', 'Абонплата за интернет'),
    ('c', 'Стоимость подключения'),
    ('e', 'Дополнительные услуги')
)
class PriceForm(FlaskForm):
    ru = StringField("Название по-русски")
    ua = StringField("Назва українською")
    service = SelectField("Тип услуги", choices=services)
    speed = IntegerField("Скорость", default=0)
    price = DecimalField("Цена", default=0)
    submit = SubmitField("Сохранить")

class NewArticleForm(FlaskForm):
    ru_name = StringField("Название по-русски")
    ua_name = StringField("Назва українською")
    submit = SubmitField("Сохранить")

class ArticleForm(NewArticleForm):
    ru_text = TextAreaField("Текст по-русски")
    ua_text = TextAreaField("Текст українською")


class ImageForm(FlaskForm):
    file = FileField("Выберите файл")
    submit = SubmitField("Загрузить")