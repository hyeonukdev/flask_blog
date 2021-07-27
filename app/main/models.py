from app import db
from datetime import datetime


class Project(db.Model):
    __table_name__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(120), nullable=False)
    project_content = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    views_count = db.Column(db.Integer, nullable=False, default=0)
    upload_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    likes_count = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comments', backref='project', lazy='dynamic')
    likes = db.relationship('Likes', backref='project', lazy='dynamic')

    def __repr__(self):
        return f"Project('{self.project_title}', '{self.upload_time}')"


class Likes(db.Model):
    __table_name__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comments(db.Model):
    __table_name__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    comment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"Comments('{self.author_id}', '{self.body}', {self.project_id})"