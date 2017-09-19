from flask import Flask, request , jsonify
import mongoengine as me 

class User(me.Document):
	name = me.StringField()
	email = me.StringField()

class Task(me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	added = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()


#Instancia um objeto do Flask
app = Flask(__name__)
me.connect('todo_app')

#Cria uma rota raiz (/)
@app.route("/users",methods = ['GET'])
def  get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append({
			'id':user._id,
			'name':user.name,
			'email':user.email
			})
	return jsonify(array)

#Roda seu servidor Web
if __name__ == "__main__":
	app.run()

