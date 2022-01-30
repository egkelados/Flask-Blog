from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from FlaskBlogApp.models import User
from flask_login import current_user


def maxImageSize(max_size=2):
   max_bytes = max_size * 1024 * 1024
   def _check_file_size(form, field):
      if len(field.data.read()) > max_bytes:
         raise ValidationError(f'The size of the image has to be smaller than {max_size} MB')

   return _check_file_size


def validate_email(form, email):

   user = User.query.filter_by(email=email.data).first()
   if email:
      raise ValidationError("This email already exists!!")


class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="This field can not be empty!"),
                                       Length(min=3, max=15, message="This field has to be from 3 to 15 characters!")])

    email = StringField(label="email",
                           validators=[DataRequired(message="This field can not be empty!"), 
                                       Email(message="Please enter valid email!"),validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="This field can not be empty!"),
                                       Length(min=3, max=15, message="This field has to be from 3 to 15 characters!")])
    
    password2 = StringField(label="Επιβεβαίωση password",
                           validators=[DataRequired(message="This field can not be empty!"),
                                       Length(min=3, max=15, message="This field has to be from 3 to 15 characters!"),
                                       EqualTo('password', message='Passwords has to be the identical!')])
    
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
                           validators=[DataRequired(message="This field can not be empty!"), 
                                       Email(message="Please enter valid email!")])

    password = StringField(label="password",
                           validators=[DataRequired(message="This field can not be empty!")])

    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Login')


class NewArticleForm(FlaskForm):
    article_title = StringField(label="Article title",
                                 validators=[DataRequired(message="This field can not be empty!"),
                                 Length(min=3, max=50, message="This field has to be from 3 to 15 characters!")])

    article_body = TextAreaField(label="Article content",
                        validators=[DataRequired(message="This field can not be empty!"), 
                                       Length(min=3, message="The body of the article has to have atleast 5 characters")])
    article_image = FileField('Article Image', validators=[Optional(strip_whitespace=True),
                                                           FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            'The files that allowed are jpg, jpeg and png!'),
                                                           maxImageSize(max_size=2)])

    submit = SubmitField('Upload')



class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="This field can not be empty!"),
                                       Length(min=3, max=15, message="This field has to be from 3 to 15 characters!")])

    email = StringField(label="email",
                           validators=[DataRequired(message="This field can not be empty!"), 
                                       Email(message="Please input valid email")])

    profile_image = FileField('Profile Image', validators=[Optional(strip_whitespace=True),
                                                           FileAllowed([ 'jpg', 'jpeg', 'png' ],
                                                            'The files that allowed are jpg, jpeg and png!'),
                                                           maxImageSize(max_size=2)])
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
