from flask import Flask, render_template, session, redirect, flash, request

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

if(__name__ == 'main'):
	app.run()
