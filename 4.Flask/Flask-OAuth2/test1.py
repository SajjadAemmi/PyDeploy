from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['GOOGLE_CLIENT_ID'] = '541528393247-jfhvthc9haagengcdo5p2corr8udh22p.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'
app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
def home():
    email = dict(session).get('email', None)
    return f'Hello, {email}' if email else 'You are not logged in <a href="/login">Log in</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    print("------------------------------------------------------------------------------------------1")
    token = google.authorize_access_token()
    # token = google.authorize_access_token()
    print("------------------------------------------------------------------------------------------2")
    print(token)
    user_info = google.parse_id_token(token)
    session['email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
