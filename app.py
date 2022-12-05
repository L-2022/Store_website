from config import host, user, password, db_name
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, url_for, flash, g, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import redirect, make_response
import os
import datetime
from FDataBase import FDataBase
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, AddProduct

# from admin.admin import admin
app = Flask(__name__)
app.config[
    'SECRET_KEY'] = 'iugferbfdfd56ivrfh4fwiuryf43gdsfwergr34548i_9thfh4cggdfgstre4hregfdgdfgfdgfg7ythgrfg56ygyuj8sivthgfdgfdfgr8'

# app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Log in to access restricted pages"
login_manager.login_message_category = "success"

user_id = None


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name)
    conn.autocommit = True
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
wiev = False
contentCategories = None


@app.before_request
def before_request():
    global dbase
    db = connect_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template("index.html", posts=dbase.getPostsAnonce(),
                           categories=dbase.getCategoriesAnonce(),)


@app.route("/product/<alias>")
def showPost(alias):
    characteristic, cost, title = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template("product.html", title=title, cost=cost, characteristic=characteristic,
                           categories=dbase.getCategoriesAnonce())


@app.route("/categories/<categories>")
def showCategories(categories):
    categories = dbase.getCategories(categories)
    print(categories[0])
    contentCategories = dbase.getCategoriesSelect(categories[0])
    if not categories:
        abort(404)
    return render_template("categories.html",
                           contentCategories=contentCategories, categories=dbase.getCategoriesAnonce())


@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        res = dbase.AddProduct(form.product_name.data, form.characteristic.data,
                               form.cost.data, form.categories.data, )
        if not res:
            flash('Error adding product', category='error')
        else:
            flash('Added!', category='success')
            return redirect(url_for('index'))

    return render_template("add_product.html", form=form)


@app.route('/delete_product/', methods=('GET', 'POST'))
@login_required
def dell_product():
    if request.method == 'POST':
        title = request.form['title']
        poost_dell = dbase.dellProduct(title)
        if poost_dell:
            return redirect(url_for('index'))
    return render_template('delete_product.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # hash = generate_password_hash(getPost)
            user = dbase.getUserByEmail(form.email.data)
            if not user:
                return redirect(url_for('login'))
            hesh = check_password_hash(user['psw'], form.psw.data)
            if user and hesh:
                userlogin = UserLogin().create(user)
                rm = form.remember.data
                login_user(userlogin, remember=rm)
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Invalid username/password", "error")
            return redirect(url_for('login'))
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))
    return render_template("login.html", title="Authorization", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out", "success")
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    old = str(form.old.data)
    phone = str(form.phone.data)
    password = form.psw.data
    if form.validate_on_submit():
        hash = generate_password_hash(password)
        account = dbase.addUser(form.email.data, hash, form.first_name.data,
                                form.last_name.data, old, phone)
        if account:
            flash('You have successfully registered!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Avatar update error", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("File read error", "error")
        else:
            flash("Avatar update error", "error")

    return redirect(url_for('profile'))


@app.route("/buy")
@login_required
def buy():
    return render_template("buy.html")


if __name__ == "__main__":
    app.run(debug=True)
