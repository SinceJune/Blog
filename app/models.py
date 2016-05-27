from app import db
from hashlib import md5

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # openid auth
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def avatar(self, size):
        # 将self.email 修改成self.account
        return 'http://www.gravatar.com/avatar/' + md5(self.account.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(
            size)

    def __repr__(self):
        return '<User %r>' % self.account


class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(30))
    body = db.Column('body', db.String(3000))
    timestamp = db.Column('timestamp', db.DateTime)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    update = db.Column('update', db.Integer)

    def __repr__(self):
        return '<Post %r>' % self.body


class Favorite(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column('timestamp', db.DateTime)
    collection_id = db.Column('collector_id', db.Integer, db.ForeignKey('collection.id'))

    def __repr__(self):
        return '<Favorite %r>' % self.post_id


class Collection(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('id', db.Integer, db.ForeignKey('user.id'))
    title = db.Column('title', db.String(30))
    timestamp = db.Column('timestamp', db.DateTime)
    total = db.Column('total', db.Integer)

    def __repr__(self):
        return '<Collection %r>' % self.total


class Comment(db.Models):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user_id'))
    post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
    reply_id = db.Column('reply_id', db.Integer)
    content = db.Column('content', db.String(300))
    timestamp = db.Column('timestamp', db.DateTime)

    def __repr__(self):
        return '<Comment %r>' % self.content


class Tag(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user_id'))
    content = db.Column('content', db.String(300))
    # TODO
