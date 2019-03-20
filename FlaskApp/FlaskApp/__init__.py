from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return "HELL o"

if(__name__ == 'main'):
	app.run()
