from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index_page():
	return 'Welcome!'
