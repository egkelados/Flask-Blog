from flask import(render_template,
                  redirect,
                  url_for,
                  request,
                  flash,
                  abort)

from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm, AccountUpdateForm 

from FlaskBlogApp import app, db, bcrypt

from FlaskBlogApp.models import User, Article 

from flask_login import login_user, current_user, logout_user, login_required

@app.route("/index/")
@app.route("/")#arxikh selida!
def root():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"The account for the user <b> {username} </b> created with success!", "success")

        return redirect(url_for('login'))

        #print(username, email, password, password2)
    return render_template("signup.html", form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("root"))
    
    form=LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"The login of the user with email: {email} was succesfull!","success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for("root"))
        else:
            flash("The login of the user was unsuccesfull", "warning")

        # print(email, password)
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()

    flash("Logout was succesfull", "success")
    return redirect(url_for("root"))

@app.route("/new_article/",methods=['GET', 'POST'])
@login_required
def new_article():
    form = NewArticleForm()

    if request.method == "POST" and form.validate_on_submit():
        article_title = form.article_title.data
        article_body = form.article_body.data

        article = Article(article_title=article_title, article_body=article_body, author=current_user)
        db.session.add(article)
        db.session.commit()
        flash(f"The article with title {article.article_title} created with success!", "success")

        return redirect(url_for("root"))
        # print(article_title, article_body)

    return render_template("new_article.html", form=form)

@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)
    # form.username.data = current_user.username
    # form.email.data = current_user.email
    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash(f"The account of user <b>{current_user.username}</b> was succesfully change!!", "success")
        return redirect(url_for('root'))

    return render_template("account_update.html", form=form)

@app.route("/edit_article/<int:article_id>", methods=['GET','POST'])
@login_required
def edit_article(article_id):
    
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()
    #same job
    # article = Article.query.get(article_id)
    # if article:
    #     if article.author != current_user:
    #         abort(403)
    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)
    #same job
    # form.article_title.data = article.artixle_title
    # form.article_body.data = article.artixle_body

    if request.method == "POST" and form.validate_on_submit():
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data

        db.session.commit()

        flash(f"The article with title <b>{article.article_title}</b> was updated with success!", "success")
        return redirect(url_for('root'))

    return render_template("new_article.html", form=form)