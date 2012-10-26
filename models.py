# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())


class Photo(Document):

	name = StringField(max_length=120)
	img = StringField(max_length=120, required=True)
	mic = StringField(max_length=120)
	slug = StringField()

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())


	



	
	

	

