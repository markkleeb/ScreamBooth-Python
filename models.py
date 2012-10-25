# -*- coding: utf-8 -*-
from mongoengine import *
from datetime import datetime

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())


class Band(Document):

	name = StringField(max_length=120, required=True)
	email = StringField(max_length=120, required=True)
	location = StringField(max_length=120, required = True)
	slug = StringField()

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())


	


class Member(Document):

	name = StringField(max_length=120, required=True)
	email = StringField(max_length=120, required=True)
	location = StringField(max_length=120, required = True)

	slug = StringField()

	
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())


	



	

class Venue(Document):

	name = StringField(max_length=120, required=True)
	email = StringField(max_length=120, required=True)
	location = StringField(max_length=120, required = True)
	slug = StringField()

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

	
	

class Show(Document):

	date = StringField(max_length=120, required=True)



	
	

	

