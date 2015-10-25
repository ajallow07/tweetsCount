from celery import Celery, group, subtask
from flask import Flask, jsonify, make_response
from collections import Counter
from tweets import tweets
from config import app
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import StringIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@app.route("/chart/plot.png", methods=['GET'])
def stats():
	queue=[tweets.s("tweets_{}.txt".format(i)) for i in xrange(0,20)]
        g = group(queue)
        res = g()
        while res.ready()=="False":
                time.slee(3)
        dicts = res.get()
        counter = Counter()
        for dic in dicts:
                counter.update(dic)
	dic = dict(counter)
 
 	fig = Figure()
	ax = fig.add_subplot(1,1,1)
	x=[]
	for i in range(len(dic)):
		x.append(i)

	ax.bar(x, dic.values(),width=0.8)
	#plt.xticks(range(len(dic)),dic.keys())
	#plt.title ="Data Visualization"
	#plt.xlabel ="words"
	#plt.ylabel = "Counts"

	canvas = FigureCanvas(fig)
	output =StringIO.StringIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
	
		
@app.route("/tweet_count", methods=['GET']) 
def get_tweet():

	queue=[tweets.s("tweets_{}.txt".format(i)) for i in xrange(0,20)]
	g = group(queue)
		
	res = g()
	while res.ready()=="False":
		time.slee(3)
	dicts = res.get()
	counter = Counter()
	for dic in dicts:
		counter.update(dic)
#	open('values.txt','a').write(json.dumps(dict(counter)))

	return jsonify(dict(counter))

if __name__=='__main__':
	app.run(host='0.0.0.0',debug=True)

