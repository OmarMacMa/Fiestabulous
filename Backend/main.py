import datetime
import string
import random
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse, abort
from app import create_app

# app = Flask(__name__)
# api = Api(app)
# app.config["MYSQL_HOST"] = MYSQL_HOST
# app.config["MYSQL_USER"] = MYSQL_USER
# app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
# app.config["MYSQL_DB"] = MYSQL_DB

# mysql = MySQL(app)

app, api, mysql = create_app()

PET = {
    'pet1': {'name': 'Cacho', 'age': 11, 'animal': 'dog'},
    'pet2': {'name': 'Percy', 'age': 2, 'animal': 'cat'},
    'pet3': {'name': 'Perla', 'age': 5, 'animal': 'cat'},
    'pet4': {'name': 'Cloe', 'age': 1, 'animal': 'cat'}
}

def abort_if_pet_doesnt_exist(pet_id):
    if pet_id not in PET:
        abort(404, message="Pet {} doesn't exist".format(pet_id))


parser = reqparse.RequestParser()
parser.add_argument('name')


def make_code():
    digits = string.digits
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    special = string.punctuation
    password = random.choice(digits) + random.choice(uppercase) + random.choice(lowercase) + random.choice(special)
    for i in range(6):
        password += random.choice(digits + uppercase + lowercase + special)

    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

class Pet(Resource):
    def get(self, pet_id):
        abort_if_pet_doesnt_exist(pet_id)
        return PET[pet_id]

    def delete(self, pet_id):
        abort_if_pet_doesnt_exist(pet_id)
        del PET[pet_id]
        return '', 204
    
    def put(self, pet_id):
        args = parser.parse_args()
        name = {'name': args['name']}
        PET[pet_id] = {**PET[pet_id], **name}
        return name, 201

class PetList(Resource):
    def get(self):
        return PET

    def post(self):
        args = parser.parse_args()
        pet_id = int(max(PET.keys()).lstrip('pet')) + 1
        pet_id = 'pet%i' % pet_id
        PET[pet_id] = {'name': args['name'], 'age': args['age'], 'animal': args['animal']}
        return PET[pet_id], 201


class UserList(Resource):
    def get(self):
        """
        Get all users
        URL: /user
        JSON input: None
        JSON output: {
            "1": {
                "name": ,
                "email": ,
                "password":
            }
        }
        """
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM user''')
        rv = cur.fetchall()
        cur.close()
        json_data = {}
        for result in rv:
            d = {
                'name': result[1],
                'email': result[2],
                'password': result[3]
            }
            json_data[result[0]] = d
        return json_data
    
    def post(self):
        """
        Create a new user
        URL: /user
        JSON input: {
            "name": ,
            "email": ,
            "password":
        }
        JSON output: {
            "name": ,
            "email": ,
            "password":
        }
        """
        if not request.json or not 'name' in request.json or not 'email' in request.json or not 'password' in request.json:
            return "Error not all fields are present", 400
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM user WHERE email = "{request.json['email']}"''')
        rv = cur.fetchall()
        if len(rv) > 0:
            return "User already exists", 400
        try:
            cur.execute(f'''INSERT INTO user (name, email, password) VALUES ("{request.json['name'].capitalize()}", "{request.json['email'].lower()}", "{request.json['password']}")''')
            mysql.connection.commit()
            cur.close()
        except:
            return "Internal server error", 500
        return request.json, 201


class User(Resource):
    def get(self, user_id):
        """
        Get a specific user
        URL: /user/<user_id>
        JSON input: None
        JSON output: {
            "1": {
                "name": ,
                "email": ,
                "password":
            }
        }
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM user WHERE id = {user_id}''')
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 0:
            return "User doesn't exist", 400
        json_data = {}
        for result in rv:
            d = {
                'name': result[1],
                'email': result[2],
                'password': result[3]
            }
            json_data[result[0]] = d
        return json_data
    
    def put(self, user_id):
        """
        Update a specific user
        URL: /user/<user_id>
        JSON input (optional but at least one field must be present): {
            "name": ,
            "password":
        }
        JSON output: (same as input){
            "name": ,
            "password": 
        }
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM user WHERE id = {user_id}''')
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 0:
            return "User doesn't exist", 400
        if not request.json or (not 'name' in request.json and not 'password' in request.json):
            return "Error not all fields are present", 400
        cur = mysql.connection.cursor()
        if 'name' in request.json and 'password' in request.json:
            cur.execute(f'''UPDATE user SET name = "{request.json['name']}", password = "{request.json['password']}" WHERE id = {user_id}''')
            mysql.connection.commit()
        if 'name' in request.json:
            cur.execute(f'''UPDATE user SET name = "{request.json['name']}" WHERE id = {user_id}''')
            mysql.connection.commit()
        if 'password' in request.json:
            cur.execute(f'''UPDATE user SET password = "{request.json['password']}" WHERE id = {user_id}''')
            mysql.connection.commit()
        cur.close()
        return request.json, 200
    
    def delete(self, user_id):
        """
        Delete a specific user
        URL: /user/<user_id>
        JSON input: None
        JSON output: None
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM user WHERE id = {user_id}''')
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 0:
            return "User doesn't exist", 400
        cur = mysql.connection.cursor()
        cur.execute(f'''DELETE FROM user WHERE id = {user_id}''')
        mysql.connection.commit()
        cur.close()
        return "User deleted", 204


class EventList(Resource):
    def get(self):
        """
        Get all events
        URL: /event
        JSON input: None
        JSON output: {
            "1": {
                "name": ,
                "date": ,
                "location": ,
                "limit of guests": ,
                "budget": ,
                "limit of budget": ,
                "organizer": ,
                "description": ,
                "code": ,
                "status":
            }
        }
        """
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM event INNER JOIN user WHERE event.organizer = user.id''')
        rv = cur.fetchall()
        cur.close()
        json_data = {}
        for result in rv:
            d = {
                'name': result[1],
                'date': datetime.datetime.strftime(result[2], '%Y-%m-%d %H:%M'),
                'location': result[3],
                'limit of guests': result[4],
                'budget': float(result[5]),
                'limit of budget': float(result[6]),
                'organizer': result[12],
                'description': result[8],
                'code': result[9],
                'status': result[10]
            }
            json_data[result[0]] = d
        return json_data
    
    def post(self):
        """
        Create a new event
        URL: /event
        JSON input: {
            "name": ,
            "date": ,
            "location": ,
            "limitGuests": ,
            "limitBudget": ,
            "organizer": ,
            "description":
        }
        JSON output: (same as input){
            "name": ,
            "date": ,
            "location": ,
            "limitGuests": ,
            "limitBudget": ,
            "organizer": ,
            "description":
        }
        """
        if not request.json or not 'name' in request.json or not 'date' in request.json or not 'location' in request.json or not 'limitGuests' in request.json or not 'limitBudget' in request.json or not 'organizer' in request.json or not 'description' in request.json:
            return "Error not all fields are present", 400
        code = make_code()
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM event WHERE code = "{code}"''')
        rv = cur.fetchall()
        while len(rv) > 0:
            code = make_code()
            cur.execute(f'''SELECT * FROM event WHERE code = "{code}"''')
            rv = cur.fetchall()
        try:
            sql = f'''INSERT INTO event (name, date, location, limitGuests, budget, limitBudget, organizer, description, code) VALUES ("{request.json['name']}", STR_TO_DATE("{request.json['date']}", "%Y-%m-%d %H:%i"), "{request.json['location']}", {request.json['limitGuests']}, 0, {request.json['limitBudget']}, {request.json['organizer']}, "{request.json['description']}", "{code}")'''
            cur.execute(sql)
            mysql.connection.commit()
            cur.close()
        except:
            return "Internal server error", 500
        return request.json, 201


class Event(Resource):
    def get(self, event_id):
        """
        Get a specific event
        URL: /event/<event_id>
        JSON input: None
        JSON output: {
            "name": ,
            "date": ,
            "location": ,
            "limit of guests": ,
            "budget": ,
            "limit of budget": ,
            "organizer": ,
            "description": ,
            "code": ,
            "status":
        }
        """
        if event_id == 'active':
            cur = mysql.connection.cursor()
            cur.execute('''SELECT * FROM event INNER JOIN user WHERE event.organizer = user.id AND event.status <> 1''')
            rv = cur.fetchall()
            cur.close()
            json_data = {}
            for result in rv:
                d = {
                    'name': result[1],
                    'date': datetime.datetime.strftime(result[2], '%Y-%m-%d %H:%M'),
                    'location': result[3],
                    'limit of guests': result[4],
                    'budget': float(result[5]),
                    'limit of budget': float(result[6]),
                    'organizer': result[12],
                    'description': result[8],
                    'code': result[9],
                    'status': result[10]
                }
                json_data[result[0]] = d
            return json_data
        else:
            cur = mysql.connection.cursor()
            cur.execute(f'''SELECT * FROM event INNER JOIN user WHERE event.organizer = user.id AND event.id = {event_id}''')
            rv = cur.fetchall()
            cur.close()
            if len(rv) == 0:
                return "Event doesn't exist", 400
            json_data = {}
            for result in rv:
                d = {
                    'name': result[1],
                    'date': datetime.datetime.strftime(result[2], '%Y-%m-%d %H:%M'),
                    'location': result[3],
                    'limit of guests': result[4],
                    'budget': float(result[5]),
                    'limit of budget': float(result[6]),
                    'organizer': result[12],
                    'description': result[8],
                    'code': result[9],
                    'status': result[10]
                }
                json_data[result[0]] = d
            return json_data
    
    def put(self, event_id):
        """
        Update a specific event
        URL: /event/<event_id>
        JSON input (optional, at least one field must be present): {
            "name": ,
            "date": ,
            "location": ,
            "limitGuests": ,
            "limitBudget": ,
            "description": ,
            "status":
            }
        JSON output: (same as input){
            "name": ,
            "date": ,
            "location": ,
            "limitGuests": ,
            "limitBudget": ,
            "description": ,
            "status":
        }
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM event WHERE id = {event_id}''')
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 0:
            return "Event doesn't exist", 400
        if not request.json or (not 'name' in request.json and not 'date' in request.json and not 'location' in request.json and not 'limitGuests' in request.json and not 'limitBudget' in request.json and not 'description' in request.json and not 'status' in request.json):
            return "Error not all fields are present", 400
        try:
            cur = mysql.connection.cursor()
            if 'name' in request.json:
                cur.execute(f'''UPDATE event SET name = "{request.json['name']}" WHERE id = {event_id}''')
            if 'date' in request.json:
                cur.execute(f'''UPDATE event SET date = "STR_TO_DATE({request.json['date']}", "%Y-%m-%d %H:%i") WHERE id = {event_id}''')
            if 'location' in request.json:
                cur.execute(f'''UPDATE event SET location = "{request.json['location']}" WHERE id = {event_id}''')
            if 'limitGuests' in request.json:
                cur.execute(f'''UPDATE event SET limitGuests = {request.json['limitGuests']} WHERE id = {event_id}''')
            if 'limitBudget' in request.json:
                cur.execute(f'''UPDATE event SET limitBudget = {request.json['limitBudget']} WHERE id = {event_id}''')
            if 'description' in request.json:
                cur.execute(f'''UPDATE event SET description = "{request.json['description']}" WHERE id = {event_id}''')
            if 'status' in request.json:
                cur.execute(f'''UPDATE event SET status = {request.json['status']} WHERE id = {event_id}''')
            mysql.connection.commit()
            cur.close()
        except:
            return "Internal server error", 500
        return request.json, 200
    
    def delete(self, event_id):
        """
        Delete a specific event
        URL: /event/<event_id>
        JSON input: None
        JSON output: {
            "message": "Event deleted"
        }
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM event WHERE id = {event_id}''')
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 0:
            return "Event doesn't exist", 400
        try:
            cur = mysql.connection.cursor()
            cur.execute(f'''DELETE FROM event WHERE id = {event_id}''')
            mysql.connection.commit()
            cur.close()
        except:
            return "Internal server error", 500
        return "Event deleted", 200
    

class GuestList(Resource):
    def get(self, event_id):
        """
        Get all guests of a specific event
        URL: /guest/<event_id>/guest
        JSON input: None
        JSON output: {
            "1": {
                "name": ,
                "status": ,
                "event": 
            }
        }
        """
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT g.id, u.name, g.event, g.status, e.name FROM guest g INNER JOIN user u ON g.user = u.id INNER JOIN event e ON g.event = e.id WHERE g.event = {event_id}''')
        rv = cur.fetchall()
        cur.close()
        json_data = {}
        for result in rv:
            d = {
                'name': result[1],
                'status': "Going" if result[3] == 1 else ("Pending" if result[3] == 0 else "Not going"),
                'event': result[4]
            }
            json_data[result[0]] = d
        return json_data
    
    def post(self, event_id):
        """
        Add a guest to a specific event
        URL: /guest/<event_id>/guest
        JSON input: {
            "user": 
        }
        JSON output: {
            "user": 
        }
        """
        if not request.json or not 'user' in request.json:
            return "Error not all fields are present", 400
        try:
            cur = mysql.connection.cursor()
            cur.execute(f'''INSERT INTO guest (user, event) VALUES ({request.json['user']}, {event_id})''')
            mysql.connection.commit()
            cur.close()
        except:
            return "Internal server error", 500
        return request.json, 201
    



@app.route("/")
def index():
    return render_template("index.html")






api.add_resource(Pet, '/pet/<pet_id>')
api.add_resource(PetList, '/pet')
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(EventList, '/event/')
api.add_resource(Event, '/event/<event_id>')
api.add_resource(GuestList, '/event/<event_id>/guest')
