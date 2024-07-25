from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import timedelta
import os
from summarizer import create_summaries, get_earnings_call_transcript
from flask_session import Session
from redis import Redis
from dotenv import load_dotenv


load_dotenv()



app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

# Configure session to use Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'flask_session:'
app.config['SESSION_REDIS'] = Redis.from_url(os.getenv('REDIS_URL'))

# Initialize the session
Session(app)


# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()






########################################
""" Authentication and Authorization """

# Decorator for routes that require authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))
        
        # else:

        #     if session['user']['uid'] not in ['TfwhiA8iXaXdcJCakG95BrOmqKF2']:
        #         return "Unauthorized", 401
            
        #    else:

        return f(*args, **kwargs)
        
    return decorated_function


@app.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        print('here I am')
        decoded_token = auth.verify_id_token(token) # Validate token here
        print('the problem is here')
        session['user'] = decoded_token # Add user to session
        return redirect(url_for('dashboard'))
    
    except:
        
        return "Unauthorized", 401


#####################
""" Public Routes """

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')


@app.route('/reset-password')
def reset_password():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('forgot_password.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0) 
    return response


##############################################
""" Private Routes (Require authorization) """

@app.route('/api/summary', methods=['GET', 'POST'])
@auth_required
def summary():
    if request.method == 'POST':
        data = request.json
        symbol = data['symbol'].upper()

        transcript_data = get_earnings_call_transcript(symbol)

        # # Store transcript_data in session
        session['transcript_data'] = transcript_data

        # print(transcript_data)

        summaries = create_summaries(symbol)

        return jsonify(summaries)
    else:
        return jsonify({'message': 'GET request received'})


@app.route('/dashboard')
@auth_required
def dashboard():

    return render_template('dashboard.html')



@app.route('/view')
def view():
    return str(session['transcript_data'])





if __name__ == '__main__':
    app.run(debug=True)