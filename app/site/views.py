from flask import g, render_template, redirect, request, url_for
from app import app, db
from app.site import bp
from app.site.menu import menu
from app.site.models import Region, Price, Feedback, Articles
from app.site.forms import FeedbackForm
from app.site.telegram import send_message as tg
from app.site.converter import text2html
import datetime

#@bp.before_request
#def ensure_lang_support():
#    lang = g.get('lang', None)
#    session['lang'] = lang
#    if lang and lang not in app.config['SUPPORTED_LANGUAGES'].keys():
#        session['lang'] = app.config['DEFAULT_LANGUAGE']
#        g.lang = app.config['DEFAULT_LANGUAGE']
#        return redirect("/")

@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    l = values.pop('lang')
    if l in app.config['SUPPORTED_LANGUAGES'].keys():
        g.lang = l
    else:
        g.lang = app.config['DEFAULT_LANGUAGE']
    g.menu = menu[g.lang]
    g.langs = app.config['SUPPORTED_LANGUAGES']
    g.act_page = request.path.split('/')[2]
    g.page = '/'.join(request.path.split('/')[2:])

@bp.after_request
def set_lang_cookie(response):
    response.set_cookie('lang', g.lang)
    return response

@bp.route('/')
@bp.route('/about')
def about():
    return render_template(g.lang + "/about.html")

@bp.route('/price')
def price():
    regions = db.session.query(Region).all()
    return render_template(g.lang + "/price.html", regions=regions)


@bp.route('/price/<int:id>')
def price_city(id):
    tariffs = db.session.query(Price).filter(Price.region==id, Price.service=='i').all()
    cons = db.session.query(Price).filter(Price.region==id, Price.service=='c').all()
    extras = db.session.query(Price).filter(Price.region==id, Price.service=='e').all()
    return render_template(g.lang + "/price_city.html", tariffs=tariffs, cons=cons, extras=extras)

@bp.route('/contacts')
def contacts():
    return render_template(g.lang + "/contacts.html")

@bp.route('/abon')
def abon():
    if g.lang == 'ua':
        articles = db.session.query(Articles.id, Articles.ua_name).filter(Articles.visible is True).all()
    elif g.lang == 'ru':
        articles = db.session.query(Articles.id, Articles.ru_name).filter(Articles.visible is True).all()
    return render_template("abon.html", articles=articles)

@bp.route('/abon/<int:id>')
def article(id):
    if g.lang == 'ua':
        (head, text) = db.session.query(Articles.ua_name, Articles.ua_text).filter(Articles.id==id).one()
    elif g.lang == 'ru':
        (head, text) = db.session.query(Articles.ru_name, Articles.ru_text).filter(Articles.id == id).one()
    path = 'pic/{}/'.format(id)
    return render_template("article.html", head=head, text=text2html(text=text, path=path))

@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm(g.lang)
    if form.validate_on_submit():
        msg = Feedback(ip=request.environ.get('HTTP_X_FORWARDED_FOR'), time=datetime.datetime.now,
                       name=form.name.data, phone=form.phone.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        message = ['Сообщение с сайта']
        message.append(datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"))
        message.append('Имя: {}'.format(form.name.data))
        message.append('Телефон: {}'.format(form.phone.data))
        message.append(form.message.data)
        tg('\n'.join(message))
        return redirect(url_for("site.feedback_sent", lang=g.lang))
    return render_template("feedback.html", form=form)

@bp.route('/feedback/sent')
def feedback_sent():
    return render_template(g.lang + "/feedback_sent.html")

@app.route('/')
def redir():
    lang = request.cookies.get('lang', None)
    if lang in app.config['SUPPORTED_LANGUAGES'].keys():
        return redirect('/'+ lang + '/')
    else:
        return redirect('/' + app.config['DEFAULT_LANGUAGE'] + '/')