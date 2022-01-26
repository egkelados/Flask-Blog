from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt


app = Flask(__name__)


app.config["SECRET_KEY"] = '18be292779b0e5adc0261befef613e4e'
app.config['WTF_CSRF_SECRET_KEY'] = '4d4e1bbd669554115557e787b76baaee'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_course_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from FlaskBlogApp import routes, models

