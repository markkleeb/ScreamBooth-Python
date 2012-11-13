# -*- coding: utf-8 -*-

import os, datetime
import re
import requests
#import boto
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify

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


@app.route('/data/photos')
def data_photos():

	# query for the ideas - return oldest first, limit 10
	photos = models.Photo.objects().order_by('-timestamp').limit(30)

	if photos:

		# list to hold ideas
		public_photos = []

		#prep data for json
		for p in photos:

			tmpPhoto = {
				'id' : p.img,
				'event' : p.event,
				'timestamp' : str( p.timestamp )
			}

			# comments / our embedded documents
			tmpPhoto['comments'] = [] # list - will hold all comment dictionaries

			# loop through idea comments
			for c in p.comments:
				comment_dict = {
					'name' : c.name,
					'comment' : c.comment,
					'timestamp' : str( c.timestamp )
				}

				# append comment_dict to ['comments']
				tmpPhoto['comments'].append(comment_dict)

			# insert idea dictionary into public_ideas list
			public_photos.append( tmpPhoto )

		# prepare dictionary for JSON return
		data = {
			'status' : 'OK',
			'photos' : public_photos
		}

		# jsonify (imported from Flask above)
		# will convert 'data' dictionary and set mime type to 'application/json'
		return jsonify(data)

	else:
		error = {
			'status' : 'error',
			'msg' : 'unable to retrieve ideas'
		}
		return jsonify(error)


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





#----------Get ITP Demographics ----------------------

@app.route('/getdemographics')
def get_remote_demographics():

	# ideas available via json
	dem_url = "http://itp-demographics.herokuapp.com/data/demographics"

	# make a GET request to the url
	dem_request = requests.get(dem_url)

	# log out what we got
	app.logger.info(dem_request.json)

	# requests will automatically convert json for us.
	# .json will convert incoming json to Python dictionary for us
	dem_data = dem_request.json

	# alternative way
	# ideas_data = json.loads( idea_request.text )

	# the returned json looks like
	# {
	# 	'status' : 'OK',
	# 	'ideas' : [
	# 		{
	# 		timestamp: "2012-10-02 09:16:54.086000",
	# 		title: "Immortality",
	# 		idea: "Immortality is the ability to live forever, or put another way, it is an immunity from death. It is unknown whether human physical (material) immortality is an achievable condition.",
	# 		comments: [ ],
	# 		creator: "John"
	# 		},
	# 		...
	# 	]
	# }

	users = dem_data.get('users')


	america =0
	korea=0
	china=0
	brazil=0
	paraguay=0
	canada = 0
	mexico = 0
	germany = 0
	argentina = 0
	chile = 0
	venezuela = 0
	denmark = 0
	turkey = 0
	pakistan = 0
	russia = 0
	peru = 0
	india = 0
	france = 0


	for u in users:

		if (u['birthplace'] == 'USA') | (u['birthplace'] == 'usa') | (u['birthplace'] == 'US') | (u['birthplace'] == 'America') | (u['birthplace'] == 'United States') | (u['birthplace'] == 'united states'):
			america = america +1
		end

		if (u['birthplace'] == 'Brazil') | (u['birthplace'] == 'brasil'):
			brazil = brazil + 1
		end

		if (u['birthplace'] == 'china') | (u['birthplace'] == 'China'):
			china = china +1
		end

		if u['birthplace'] == 'South Korea': 
			korea = korea +1
		end

		if u['birthplace'] == 'Paraguay': 
			paraguay = paraguay +1
		end

		if (u['birthplace'] == 'CANADA') | (u['birthplace'] == 'Canada'):
			canada = canada + 1
		end

		if u['birthplace'] == 'Mexico': 
			mexico = mexico +1
		end

		if u['birthplace'] == 'Germany':
			germany = germany +1
		end

		if u['birthplace'] == 'Argentina': 
			argentina = argentina +1
		end

		if u['birthplace'] == 'Chile':
			chile = chile +1
		end

		if (u['birthplace'] == 'USSR (Russia)') | (u['birthplace'] == 'USSR/Russia'):
			russia = russia +1
		end

		if u['birthplace'] == 'Peru':
			peru = peru +1
		end

		if u['birthplace'] == 'France': 
			france = france +1
		end

		if u['birthplace'] == 'Pakistan': 
			pakistan = pakistan +1
		end

		if u['birthplace'] == 'India': 
			india = india+1
		end

		if u['birthplace'] == 'denmark': 
			denmark = denmark +1
		end

		if u['birthplace'] == 'Turkey': 
			turkey = turkey +1
		end

		if u['birthplace'] == 'Venezuela': 
			venezuela = venezuela +1
		end

	end



	if dem_data.get('status') == "OK":
		templateData = {
			'users' : dem_data.get('users'),
			'america' : america,
			'brazil' : brazil,
			'france' : france,
			'argentina' : argentina,
			'chile' : chile,
			'paraguay' : paraguay,
			'venezuela' : venezuela,
			'peru' : peru,
			'mexico' : mexico,
			'canada' : canada,
			'russia' : russia,
			'india' : india,
			'pakistan' : pakistan,
			'turkey' : turkey,
			'denmark' : denmark,
			'germany' : germany,
			'korea' : korea,
			'china' : china


		}

		return render_template('itp-demographics.html', **templateData)


	else:
		return "uhoh something went wrong - status = %s" % ideas_data.get('status')




	