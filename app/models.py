from datetime import datetime, timezone
from typing import Optional, List
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import md5

from app import db, login


followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('users.id'),
              primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                index = True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64),
                                             index = True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    added_at: so.Mapped[datetime] = so.mapped_column(index=True,
                                                      default=lambda: datetime.now(timezone.utc))
    
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='author')
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers'
    )
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following'
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        if not self.is_following(user):     
            self.following.add(user)
            
    def unfollow(self, user):
        if self.is_following(user):     
            self.following.remove(user)
        
    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return (db.session.scalar(query) is not None)
    
    def count_following(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def count_followers(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (sa.select(Post)
                .join(Post.author.of_type(Author))
                .join(Author.followers.of_type(Follower), isouter=True)
                .where(sa.or_(
                    Follower.id == self.id,
                    Author.id == self.id,
                ))
                .group_by(Post)
                .order_by(Post.added_at.desc()))
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    __tablename__ = "posts"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[int] = so.mapped_column(sa.String(256))
    added_at: so.Mapped[datetime] = so.mapped_column(index=True,
                                                      default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    
    author: so.Mapped['User'] = so.relationship(back_populates='posts')
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='post')
    
    def __repr__(self):
        return f"""Author: {self.author.username}
Post: {self.body}"""


class Comment(db.Model):
    __tablename__ = "comments"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(512))
    added_at: so.Mapped[datetime] = so.mapped_column(index=True,
                                                    default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Post.id), index=True)
    reply_comment_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('comments.id'), index=True)
    
    author: so.Mapped['User'] = so.relationship(back_populates="comments")
    post: so.Mapped['Post'] = so.relationship(back_populates="comments")
    reply_comment: so.Mapped[Optional['Comment']] = so.relationship(remote_side=[id], back_populates='replies')
    replies: so.Mapped[List['Comment']] = so.relationship(back_populates='reply_comment')
    
    def __repr__(self):
        return f"""Author: {self.author.username}\nComment: {self.body}"""
