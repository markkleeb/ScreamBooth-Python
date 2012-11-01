# -*- coding: utf-8 -*-

import os, datetime
import re
#import boto
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

#from boto.s3.connection import S3Connection
#conn = S3Connection('AKIAJUCJRHFFJ3VIWKPQ', 'wGxMAeKlMbjHjtVvTwcBnnQ+s2OlRvAG77QpeGMC')

# import all of mongoengine
from mongoengine import *

# import data models
import models

app = Flask(__name__)   # create our flask app

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
print "Connecting to MongoLabs"



# --------- Routes ----------

# this is our main page
@app.route("/")
def index():

	photos = models.Photo.objects().order_by('-img')

	templateData = {
		'photos' : photos
		
	}
	return render_template("main.html", **templateData)


@app.route("/itp-halloween-2012")
def itp():

	itp = models.Photo.objects(event='itp-halloween-2012').order_by('-img')

	templateData = {
		'photos' : itp
	}

	return render_template("itp-halloween-2012.html", **templateData)


@app.route("/photos/add", methods=["POST"])
def newphoto():

	app.logger.debug("JSON received...")
	app.logger.debug(request.form)

	
	if request.form:
		data = request.form

		photo = models.Photo()
		photo.img = data.get("photo")  
		photo.event = "itp-halloween-2012"
		photo.slug = data.get("photo")  #slugify(photo.img)
		photo.mic = data.get("mic")
		photo.save() 
		return "Received %s" %data.get("photo") 


	else:

		return "FAIL : %s" %request.form
	# get form data - create new idea


	

@app.route("/photos/<photo_slug>")
def photo_display(photo_slug):

	# get idea by idea_slug
	try:
		photo = models.Photo.objects.get(slug=photo_slug)
	except:
		abort(404)

	# prepare template data
	templateData = {
		'photo' : photo
	}

	# render and return the template
	return render_template('photo_entry.html', **templateData)
	
@app.route("/photos/<photo_id>/comment", methods=['POST'])
def photo_comment(photo_id):

	name = request.form.get('name')
	comment = request.form.get('comment')

	if name == '' or comment == '':
		# no name or comment, return to page
		return redirect(request.referrer)


	#get the idea by id
	try:
		photo = models.Photo.objects.get(id=photo_id)
	except:
		# error, return to where you came from
		return redirect(request.referrer)


	# create comment
	comment = models.Comment()
	comment.name = request.form.get('name')
	comment.comment = request.form.get('comment')
	
	# append comment to photo
	photo.comments.append(comment)
	photo.save()

	return redirect('/photos/%s' % photo.slug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	