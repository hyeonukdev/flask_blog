import os
import secrets
from app import db
from flask import render_template, current_app, url_for, flash, redirect, request, abort
from app.main import main
from app.main.models import Project, Comments, Likes
from app.main.forms import ProjectUploadForm, UpdateProjectForm, CommentForm
from flask_login import login_user, current_user, logout_user, login_required


@main.route("/")
@main.route("/home")
def home():
    """Home Page view"""
    projects = Project.query.all()
    return render_template('home.html', title='Home', projects=projects)


def save_video(form_video):
    '''Function to save video into static/videos directory'''

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(current_app.root_path, 'static/videos', video_fn)

    form_video.save(video_path)

    return video_fn

def save_image(form_image):
    '''Function to save image into static/images directory'''

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/covers', image_fn)

    form_image.save(image_path)

    return image_fn


@main.route('/project/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Project Upload Page view"""

    form = ProjectUploadForm()

    if form.validate_on_submit():
        video_file = save_video(form.project_video.data)
        image_file = save_image(form.project_image.data)
        project = Project(project_title=form.project_title.data,
                          project_team_name=form.project_team_name.data,
                          description=form.description.data,
                          category=form.category.data,
                          project_purpose=form.project_purpose.data,
                          project_detail=form.project_detail.data,
                          project_background=form.project_background.data,
                          project_date=form.project_date.data,
                          project_url=form.project_url.data,
                          project_keyword=form.project_keyword.data,
                          project_etc=form.project_etc.data,
                          project_video=video_file,
                          project_image=image_file,
                          author=current_user)

        db.session.add(project)
        db.session.commit()
        flash('Your Video has been posted!', 'success')
        return redirect(url_for('main.home'))

    return render_template('upload.html', title='Upload Project', form=form, legend='Upload Your Project')


@main.route("/project/<int:id>", methods=['GET', 'POST'])
def project(id):
    project = Project.query.get_or_404(id)

    if request.method == 'GET':
        project.views_count += 1
        db.session.commit()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(body=form.body.data, project=project,
                           author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.project', id=project.id))

    comments = project.comments.order_by(Comments.comment_time.desc())
    return render_template('project.html', title=project.project_title, form=form, project=project, comments=comments)


@main.route('/project/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_project(id):
    """Function to update project contents"""

    project = Project.query.get_or_404(id)
    if project.author != current_user:
        abort(403)

    form = UpdateProjectForm()
    if form.validate_on_submit():
        project.project_title = form.project_title.data
        project.description = form.description.data
        project.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.project', id=project.id))
    elif request.method == 'GET':
        form.project_title.data = project.project_title
        form.description.data = project.description
        form.category.data = project.category
    return render_template('update_project.html', title='Update Project', form=form, legend='Update Project')


@main.route('/project/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """Function to delete project contents"""

    project = Project.query.get_or_404(id)
    print(f"project: {project}")
    if project.author != current_user:
        abort(403)
        flash('You can not delete this project')
        return redirect(url_for('main.home'))

    Likes.query.filter_by(project_id=id).delete()

    db.session.delete(project)
    db.session.commit()

    projects = Project.query.all()

    flash('Your project has been deleted!', 'success')
    return render_template('home.html', title='Home', projects=projects)


@main.route('/project/like/<int:project_id>/<action>')
@login_required
def like_action(project_id, action):
    project = Project.query.filter_by(id=project_id).first_or_404()
    if action == 'like':
        current_user.like_project(project)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_project(project)
        db.session.commit()
    return redirect(request.referrer)