import os
from flask import Flask, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func
from sqlalchemy.orm import validates
import datetime
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
sql_url = os.getenv('DATABASE_URL', 'sqlite:///my-database.db')
engine = create_engine(sql_url)
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(25))

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '#%d: Username: %s' % (self.id, self.username)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(5000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='comments')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '#%d: Comment: %s   Owner: %s' % (self.id, self.comment, self.user)


@app.route('/init')
def init():
    """
    initialize tables here
    http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
    """
    db.drop_all()
    db.create_all()
    print "Finished Database Reset"
    return redirect("/")
    
@app.route("/comment", methods=["POST"])
def postComment():
    comment = request.form['comment']
    query = "INSERT INTO comments (comment) VALUES ('" + comment + "');"
    print query
    connection = engine.connect()
    result = connection.execute("INSERT INTO comments (comment) VALUES ('" + comment + "');")
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def hello():
    """
        Show list of comments with form to submit comments
    """
    comments = Comment.query.all()
    completeString = ""
    for c in comments:
        commentString = "<p>Comment: " + c.comment + "</p>"
        completeString += commentString
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Comments</h1>
        %s
        <form method="POST" action="/comment">
            <textarea name="comment" style="width: 300px; height: 150px;" placeholder="comment"></textarea>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """ %(completeString)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # insert user into database here
        result = connection.execute("select username from users")
        return request.form['username']
        
    return '''
    <!DOCTYPE html>
    <html>
        <body>
            Hello! Please register for my awesome, totally secure site
            <form method="POST">
                <input name="username" type="text" placeholder="username" pattern=".{3,}">
                <br>
                <input name="password" type="password" placeholder="password" pattern=".{3,}">
                <br>
                <input type="submit">
            </form>
        </body>
    </html>
'''

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=True, use_reloader=True)
