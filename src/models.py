
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

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

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }