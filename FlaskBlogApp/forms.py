from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from FlaskBlogApp.models import User
from flask_login import current_user



def validate_email(form, email):

   user = User.query.filter_by(email=email.data).first()
   if email:
      raise ValidationError("This email already exists!!")


class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email"),validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label="Επιβεβαίωση password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                       EqualTo('password', message='Τα δύο πεδία password πρέπει να είναι τα ίδια')])
    
    submit = SubmitField('Εγγραφή')


    def validate_username(self, username):

      user = User.query.filter_by(username=username.data).first()
      if user:
         raise ValidationError("This username already exists!")

    # def validate_email(self, email):

    #   user = User.query.filter_by(email=email.data).first()
    #   if email:
    #      raise ValidationError("This email already exists!!")


class LoginForm(FlaskForm):
    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])

    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Login')


class NewArticleForm(FlaskForm):
    article_title = StringField(label="Article title",
                                 validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                 Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    article_body = TextAreaField(label="Article content",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Length(min=3, message="The body of the article has to have atleast 5 characters")])

    submit = SubmitField('Upload')



class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    submit = SubmitField('Update')

    def validate_username(self, username):
      if username.data != current_user.username:
         user = User.query.filter_by(username=username.data).first()
         if user:
            raise ValidationError("This username already exists!")

    def validate_email(self, email):
      if email.data != current_user.email:
         user = User.query.filter_by(email=email.data).first()
         if email:
            raise ValidationError("This email already exists!!")
