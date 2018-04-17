from flask import Flask, Response
import time

app = Flask(__name__)
x=0
@app.route('/')
def index():
	return Response("x is ", gen(x))
def gen(x):
	x=x+1
	yield (x)
	#time.sleep(1)

if (__name__=='__main__'):
	app.run(debug=True, host='0.0.0.0')
