from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():

    if request.method == "GET":
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list =[]
        for message in messages:
            message_dict = {
            "id":message.id,
            "body":message.body,
            "username": message.username,
            "created_at": message.created_at.isoformat()
            }
            messages_list.append(message_dict)
        return make_response(jsonify(messages_list), 200)

    elif request.method == "POST":
         data = request.get_json()
         new_message = Message(
             body = data.get("body"),
             username = data.get("username")
         )
         db.session.add(new_message)
         db.session.commit()

         message_dict = new_message.to_dict()
         return make_response(jsonify(message_dict), 201)

@app.route('/messages/<int:id>', methods = ["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id =id).first()

    if message == None:
        response_body = {
            "message": "This record does not exist in our database."
        }
        return make_response(jsonify(response_body), 404)
    
    else:
        if request.method == "PATCH":
            data = request.get_json()
            if "body" in data:
                message.body = data.get("body")
            db.session.commit()
            message_dict = message.to_dict()
            return make_response(jsonify(message_dict), 200)
        
        elif request.method == "DELETE":
           message = Message.query.filter_by(id=id).first()
           db.session.delete(message)
           db.session.commit()

           return "", 200 


if __name__ == '__main__':
    app.run(port=5555)
