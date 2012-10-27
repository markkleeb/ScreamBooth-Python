# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())



class Photo(Document):

	img = StringField(max_length=120, required=True)
	slug = StringField()
	#event = StringField(max_length=120, required=True)

	
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())



	

