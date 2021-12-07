from flask_wtf import FlaskForm
from wtforms import Label, StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length

class FeedbackForm(FlaskForm):
    name = StringField("", validators=[Length(min=2, max=128)])
    phone = StringField("", validators=[Length(min=10, max=32)])
    message = TextAreaField("", validators=[Length(min=1, max=2048)])
    submit = SubmitField("")

    def __init__(self, lang=None, **kwargs):
        super().__init__(**kwargs)
        if lang=='ua':
            self['name'].label = Label(self['name'].id, 'Ваше ім\'я')
            self['phone'].label = Label(self['phone'].id, 'Ваш телефон')
            self['message'].label = Label(self['message'].id, 'Повідомлення')
            self['submit'].label = Label(self['submit'].id, 'Відправити')
        elif lang=='ru':
            self['name'].label = Label(self['name'].id, 'Ваше имя')
            self['phone'].label = Label(self['phone'].id, 'Ваш телефон')
            self['message'].label = Label(self['message'].id, 'Сообщение')
            self['submit'].label = Label(self['submit'].id, 'Отправить')