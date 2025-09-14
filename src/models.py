
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # RELACIONES ENTRE TABLAS
    followers = db.relationship(
        'Follower',
        foreign_keys='Follower.user_to_id',
        backref='followed',
        lazy='True'
    )
    following = db.relationship(
        'Follower',
        foreign_keys='Follower.user_from_id',
        backref='follower',
        lazy='True'
    )
    comments = db.relationship(
        'Comment',
        backref='user',
        lazy='True'
    )
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='True'
    )
    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }
    

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    
    # RELACIONES
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='True'
    )

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }