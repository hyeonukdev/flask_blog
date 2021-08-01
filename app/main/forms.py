from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class ProjectUploadForm(FlaskForm):
    project_title = TextField('Title', validators=[
                            DataRequired(), Length(max=60)])
    project_team_name = TextField('Team Name', validators=[
        DataRequired(), Length(max=60)])
    description = TextField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[
                           DataRequired(), Length(max=20)])
    project_purpose = StringField('Purpose', validators=[DataRequired()])
    project_detail = StringField('Detail', validators=[DataRequired()])
    project_background = StringField('Background', validators=[DataRequired()])
    project_date = StringField('Date', validators=[DataRequired(), Length(max=30)])
    project_url = StringField('URL', validators=[DataRequired()])
    project_keyword = StringField('Keyword', validators=[DataRequired()])
    project_etc = StringField('Etc', validators=[DataRequired()])

    project_video = FileField('Video', validators=[FileAllowed(
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
    project_purpose = StringField('Purpose', validators=[DataRequired()])
    project_detail = StringField('Detail', validators=[DataRequired()])
    project_background = StringField('Background', validators=[DataRequired()])
    project_date = StringField('Date', validators=[DataRequired()])
    project_url = StringField('URL', validators=[DataRequired()])
    project_keyword = StringField('Keyword', validators=[DataRequired()])
    project_etc = StringField('Etc', validators=[DataRequired()])

    project_video = FileField('Video', validators=[FileAllowed(
        ['mp4', 'mkv', '3gp', 'mov'])])

    project_image = FileField('Image', validators=[FileAllowed(
        ['jpeg', 'png', 'gif'])])
    submit = SubmitField('Update')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired(), Length(max=400)])
    submit = SubmitField('Comment Here')
