from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class ProjectUploadForm(FlaskForm):
    project_title = TextField('Title', validators=[
                            DataRequired(), Length(max=60)])
    description = TextField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[
                           DataRequired(), Length(max=20)])
    project_content = FileField('Video', validators=[FileAllowed(
        ['mp4', 'mkv', '3gp', 'mov']), FileRequired()])
    project_image = FileField('Image', validators=[FileAllowed(
        ['jpeg', 'png', 'gif']), FileRequired()])
    submit = SubmitField('Upload')


class UpdateProjectForm(FlaskForm):
    project_title = TextField('Title', validators=[
                            DataRequired(), Length(max=60)])
    description = TextField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[
                           DataRequired(), Length(max=20)])

    # TODO : update video and images
    # project_content = FileField('Video', validators=[FileAllowed(
    #     ['mp4', 'mkv', '3gp', 'mov']), FileRequired()])
    #
    # project_image = FileField('Image', validators=[FileAllowed(
    #     ['jpeg', 'png', 'gif']), FileRequired()])
    submit = SubmitField('Update')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired(), Length(max=400)])
    submit = SubmitField('Comment Here')
