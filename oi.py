from flask import Flask, request , jsonify
import mongoengine as me 

class User(me.Document):
	name = me.StringField()
	email = me.StringField()

	def to_dict(self):
		return{
			'id':str(self.id),
			'name':self.name,
			'email':user.email

		}

class Task(me.Document):
	description = me.StringField()
	deadline = me.DateTimeField()
	title = me.StringField()
	finished = me.BooleanField()
	tags = me.ListField(me.StringField())
	added = me.DateTimeField()
	user = me.ReferenceField(User)
	color = me.StringField()

	def to_dict(self):
		return{
		'id':str(self.user.id),
		'title':self.title,
		'description':self.description,
		'deadline':int(self.deadline.timestamp()),
		'added':int(self.added.timestamp()),
		'color':self.color,
		'finished':self.finished,
		'user':str(self.user)
		}

#Instancia um objeto do Flask
app = Flask(__name__)
me.connect('todo_app')

#Cria uma rota raiz (/)
@app.route("/users",methods = ['GET'])
def  get_users():
	users = User.objects.all()
	array = []
	for user in users:
		array.append(user.to_dict())
	return jsonify(array)

@app.route('/users',methods=['POST'])
def create_user():
	if not request.is_json:
		return jsonify({'error':'not_json'}),400
	data=request.get_json()
	name=data.get('name')
	email=data.get('email')
	user = User(name=name,email=email)
	user.save()
	return jsonify(user.to_dict())

@app.route('/tasks',methods=['POST'])
def create_task():
	if not request.is_json:
		return jsonify({'error':'not_json'}),400
	data=request.get_json()
	task = Task(finished=False,added=datetime.now())
	task.title=data.get('title')
	task.description = data.get('description')
	task.deadline=datetime.fromtimestamp(data.get('deadline',0))
	task.color=data.get('color')
	task.tags=data.get('tags',[])
	if 'user' in data.keys():
		task.user=User.objects.filter(id=data.get('user')).first()
	task.save()
	return jsonify(user.to_dict())

@app.route('/tasks/<string:id>',methods=['PATCH'])
def update_tasks(task_id):
	if not request.is_json:
		return jsonify({'error':'not_json'}),400
	task = Task.objects.filter(id=task_id)
	if not task:
		return jsonify({'error':'not_json'}),400
	data=request.get_json()
	task.finished=data.get('finished',task.finished)
	task.save()
	return jsonify(user.to_dict())

#Roda seu servidor Web
if __name__ == "__main__":
	app.run(port=5001, debug=True)

