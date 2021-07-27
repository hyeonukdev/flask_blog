import os
import secrets
from app import db
from flask import render_template, current_app, url_for, flash, redirect, request, abort
from app.main import main
from app.main.models import Project
from app.main.forms import ProjectUploadForm, UpdateProjectForm
from flask_login import login_user, current_user, logout_user, login_required


@main.route("/")
@main.route("/home")
def home():
    """Home Page view"""
    projects = Project.query.all()
    print(f"projects: {projects}")
    return render_template('home.html', title='Home', projects=projects)


def save_video(form_video):
    '''Function to save video into static/videos directory'''

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(current_app.root_path, 'static/videos', video_fn)

    form_video.save(video_path)

    return video_fn


@main.route('/project/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Video Upload Page view"""

    form = ProjectUploadForm()

    if form.validate_on_submit():
        video_file = save_video(form.project_content.data)
        project = Project(project_title=form.project_title.data, project_content=video_file,
                      description=form.description.data, category=form.category.data, author=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Your Video has been posted!', 'success')
        return redirect(url_for('main.home'))

    return render_template('upload.html', title='Upload Video', form=form, legend='Upload Your Video')