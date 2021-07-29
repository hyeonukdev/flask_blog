import os
import secrets
import json
from app import db
from flask import render_template, current_app, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app.main import main
from app.main.models import Project, Comments, Likes
from app.main.forms import ProjectUploadForm, UpdateProjectForm, CommentForm
from app.users.models import User
from app.api import api


@api.route("/api/projects", methods=['GET'])
def api_home():
    """Home Page Routes"""

    data = {}
    projects = Project.query.all()

    for project in projects:
        project_dict = {}

        # project_dict["id"] = project.id
        project_dict["name"] = project.project_title
        user = User.query.filter(User.id == project.user_id).first()
        project_dict["author"] = user.user_name
        project_dict["image"] = project.project_image
        project_dict["category"] = project.category
        project_dict["upload_time"] = str(project.upload_time)
        project_dict["views_count"] = project.views_count
        project_dict["likes_count"] = project.likes_count

        data[project.id] = project_dict

    result = json.dumps(data)

    return result

#
# def save_video(form_video):
#     '''Function to save video into static/videos directory'''
#
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_video.filename)
#     video_fn = random_hex + f_ext
#     video_path = os.path.join(current_app.root_path, 'static/videos', video_fn)
#
#     form_video.save(video_path)
#
#     return video_fn
#
#
# @main.route('/project/upload', methods=['GET', 'POST'])
# @login_required
# def upload():
#     """Video Upload Page view"""
#
#     form = ProjectUploadForm()
#
#     if form.validate_on_submit():
#         video_file = save_video(form.project_content.data)
#         project = Project(project_title=form.project_title.data, project_content=video_file,
#                       description=form.description.data, category=form.category.data, author=current_user)
#         db.session.add(project)
#         db.session.commit()
#         flash('Your Video has been posted!', 'success')
#         return redirect(url_for('main.home'))
#
#     return render_template('upload.html', title='Upload Video', form=form, legend='Upload Your Video')
#
#
# @main.route("/project/<int:id>", methods=['GET', 'POST'])
# def project(id):
#     project = Project.query.get_or_404(id)
#
#     if request.method == 'GET':
#         project.views_count += 1
#         db.session.commit()
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comments(body=form.body.data, project=project,
#                            author=current_user._get_current_object())
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('main.project', id=project.id))
#
#     comments = project.comments.order_by(Comments.comment_time.desc())
#     return render_template('project.html', title=project.project_title, form=form, project=project, comments=comments)
#
#
# @main.route('/project/<int:id>/update', methods=['GET', 'POST'])
# @login_required
# def update_project(id):
#     """Function to update video contents"""
#
#     project = Project.query.get_or_404(id)
#     if project.author != current_user:
#         abort(403)
#
#     form = UpdateProjectForm()
#     if form.validate_on_submit():
#         project.project_title = form.project_title.data
#         project.description = form.description.data
#         project.category = form.category.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('main.project', id=project.id))
#     elif request.method == 'GET':
#         form.project_title.data = project.project_title
#         form.description.data = project.description
#         form.category.data = project.category
#     return render_template('update_project.html', title='Update Project', form=form, legend='Update Project')
#
#
# @main.route('/project/like/<int:project_id>/<action>')
# @login_required
# def like_action(project_id, action):
#     project = Project.query.filter_by(id=project_id).first_or_404()
#     if action == 'like':
#         current_user.like_project(project)
#         db.session.commit()
#     if action == 'unlike':
#         current_user.unlike_project(project)
#         db.session.commit()
#     return redirect(request.referrer)