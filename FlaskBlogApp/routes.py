from flask import(render_template,
                  redirect,
                  url_for,
                  request,
                  flash, session)

from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm 

from FlaskBlogApp import app, db, bcrypt

from FlaskBlogApp.models import User, Article 

@app.route("/index/")
@app.route("/")#arxikh selida!
def root():
    user = None

    if "user" in session:
        user = session["user"]
    
    articles = Article.query.all()
    return render_template("index.html", articles=articles, myuser=user)


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

    session.permanent= True
    
    form=LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user"] = { "username":user.username,
                                 "email":user.email,
                                 "profile_image":user.profile_image,
                                 "id":user.id
                                }

        # print(email, password)
            flash(f"Login succeed with eimail : {email}", "success")
            return redirect(url_for("root"))
        else:
            flash("Connection failed!", "warning")
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("root"))

    # mydict.pop("mykey"[, default])

@app.route("/new_article/",methods=['GET', 'POST'])
def new_article():

    if "user" in session:
        form = NewArticleForm()

        if request.method == "POST" and form.validate_on_submit():
            article_title = form.article_title.data
            article_body = form.article_body.data
            print(article_title, article_body)

        return render_template("new_article.html", form=form)
    else:
        flash("You have to login first!", "warning")
    return redirect(url_for("root"))    

