from flask import render_template, flash, url_for, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os
from app import db
from app.admin import bp
from app.admin.models import Admin
from app.site.models import Region, Price, Feedback, Articles
from app.admin.forms import LoginForm, RegionForm, PriceForm, NewArticleForm, ArticleForm, ImageForm

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin()
        if not user.check_password(form.username.data, form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin_login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@bp.route("/")
@login_required
def index():
    return render_template("admin_index.html")

@bp.route("/regions", methods=['GET', 'POST'])
@login_required
def regions():
    form = RegionForm()
    if form.validate_on_submit():
        region = Region(ru=form.ru.data, ua=form.ua.data)
        db.session.add(region)
        db.session.commit()
        return redirect(url_for("admin.regions"))
    regions = db.session.query(Region).all()
    return render_template("regions.html", regions=regions, form=form)

@bp.route("/region/del/<int:id>")
@login_required
def region_del(id):
    region = db.session.query(Region).filter(Region.id==id).one()
    db.session.delete(region)
    db.session.commit()
    return redirect(url_for("admin.regions"))

@bp.route("/region/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def region_edit(id):
    form = RegionForm()
    region = db.session.query(Region).filter(Region.id == id).one()
    if form.validate_on_submit():
        region.ru = form.ru.data
        region.ua = form.ua.data
        db.session.commit()
        return redirect(url_for("admin.regions"))
    form.ru.data = region.ru
    form.ua.data = region.ua
    return render_template("region_edit.html", form=form)

@bp.route("/price/<int:region>", methods=['GET', 'POST'])
@login_required
def price(region):
    form = PriceForm()
    if form.validate_on_submit():
        price = Price(region=region, ru=form.ru.data, ua=form.ua.data, service=form.service.data,
                      speed=form.speed.data, price=form.price.data)
        db.session.add(price)
        db.session.commit()
        return redirect(url_for("admin.price", region=region))
    city = db.session.query(Region).filter(Region.id==region).one()
    internet = db.session.query(Price).filter(Price.region==region, Price.service=='i').all()
    connection = db.session.query(Price).filter(Price.region==region, Price.service=='c').all()
    extra = db.session.query(Price).filter(Price.region==region, Price.service=='e').all()
    return render_template("admin_price.html", form=form, city=city, internet=internet, connection=connection, extra=extra)

@bp.route("/price/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def price_edit(id):
    form = PriceForm()
    price = db.session.query(Price).filter(Price.id == id).one()
    if form.validate_on_submit():
        price.ru = form.ru.data
        price.ua = form.ua.data
        price.speed = form.speed.data
        price.price = form.price.data
        price.service = form.service.data
        db.session.commit()
        return redirect(url_for("admin.price", region=price.region))
    form.ru.data = price.ru
    form.ua.data = price.ua
    form.speed.data = price.speed
    form.price.data = price.price
    form.service.data = price.service
    return render_template("admin_price_edit.html", form=form)

@bp.route("/price/del/<int:id>")
@login_required
def price_del(id):
    price = db.session.query(Price).filter(Price.id == id).one()
    db.session.delete(Price)
    db.session.commit()
    return redirect(url_for("admin.price", region=price.region))

@bp.route("/feedback")
@login_required
def feedback():
    messages = db.session.query(Feedback).all()
    return render_template("admin_feedback.html", messages=messages)

@bp.route("/feedback/del/<int:id>")
@login_required
def feedback_del(id):
    message = db.session.query(Feedback).filter(Feedback.id == id).one()
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for("admin.feedback"))

@bp.route("/articles", methods=['GET', 'POST'])
@login_required
def articles():
    form = NewArticleForm()
    if form.validate_on_submit():
        article = Articles(ru_name=form.ru_name.data, ua_name=form.ua_name.data, visible=False)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('admin.articles'))
    articles = db.session.query(Articles.id, Articles.visible, Articles.ru_name, Articles.ua_name).all()
    return render_template("admin_articles.html", articles=articles, form=form)


@bp.route("/articles/del/<int:id>")
@login_required
def articles_del(id):
    article = db.session.query(Articles).filter(Articles.id==id).one()
    db.session.delete(article)
    db.session.commit()
    if os.path.exists('./app/static/pic/' + str(id)):
        for f in os.listdir('./app/static/pic/' + str(id)):
            os.remove('./app/static/pic/' + str(id) + '/' + f)
        os.rmdir('./app/static/pic/' + str(id))
    return redirect(url_for('admin.articles'))

@bp.route("/articles/show/<int:id>")
@login_required
def articles_show(id):
    article = db.session.query(Articles).filter(Articles.id == id).one()
    article.visible = True
    db.session.commit()
    return redirect(url_for('admin.articles'))

@bp.route("/articles/hide/<int:id>")
@login_required
def articles_hide(id):
    article = db.session.query(Articles).filter(Articles.id == id).one()
    article.visible = False
    db.session.commit()
    return redirect(url_for('admin.articles'))

@bp.route("/articles/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def articles_edit(id):
    form = ArticleForm()
    article = db.session.query(Articles).filter(Articles.id == id).one()
    if form.validate_on_submit():
        article.ru_name = form.ru_name.data
        article.ua_name = form.ua_name.data
        article.ru_text = form.ru_text.data
        article.ua_text = form.ua_text.data
        db.session.commit()
        return redirect(url_for('admin.articles'))
    form.ru_name.data = article.ru_name
    form.ua_name.data = article.ua_name
    form.ru_text.data = article.ru_text
    form.ua_text.data = article.ua_text
    return render_template("admin_articles_edit.html", form=form, id=id)

@bp.route("/pictures/<int:id>", methods=['GET', 'POST'])
@login_required
def pictures(id):
    picdir = './app/static/pic/' + str(id)
    form = ImageForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif']:
            if not os.path.exists(picdir):
                os.mkdir(picdir)
            filename = secure_filename(file.filename)
            file.save(os.path.join(picdir, filename))
        return redirect(url_for("admin.pictures", id=id))
    if os.path.exists(picdir):
        pics=dict()
        for f in os.listdir(picdir):
            pics[f] = url_for('static', filename= 'pic/' + str(id) + '/' + f)
    else:
        pics = None
    return render_template("admin_article_pictures.html", form=form, id=id, pics=pics)

@bp.route("/pictures/del/<int:id>/<file>")
@login_required
def pictures_del(id, file):
    pic = './app/static/pic/' + str(id) + '/' + file
    if os.path.exists(pic):
        os.remove(pic)
    return redirect(url_for('admin.pictures', id=id))

