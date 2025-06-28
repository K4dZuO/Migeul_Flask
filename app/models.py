from datetime import datetime, timezone
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class User(db.Model):
    __tablename__ = "users"
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64),
                                                index = True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64),
                                             index = True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='author')

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
        return f"""Author: {self.author.username}
Comment: {self.body}"""
