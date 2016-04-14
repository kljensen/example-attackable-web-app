import os
from flask import Flask

app = Flask(__name__)
sql_url = os.getenv('DATABASE_URL', 'sqlite:///my-database.db')
engine = create_engine(sql_url)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/register")
def register():
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
