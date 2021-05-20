import os

from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Api, Resource
from flasgger import Swagger
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
api = Api(app)
mysql = MySQL()
swagger = Swagger(app)

password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
db = os.getenv('db')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = password
app.config['MYSQL_DATABASE_DB'] = db
app.config['MYSQL_DATABASE_HOST'] = host

mysql.init_app(app)


def check_posted_data(posted_data, function_name):
    """
    Takes posted data and function name, check data to confirm that it will work for the called function and returns
    status based on check.
    :param posted_data: JSON object sent by user
    :param function_name: name of function being called
    :return: returns status code to user
    """
    if function_name in ['states', 'cities', 'facility_name', 'facility_ids']:
        if function_name not in posted_data:
            return 301, 'Incorrect Key Value Used in JSON'
        # elif not all(str(value[0]) == str for value in posted_data.values()):
        #     return 302, 'Incorrect data type, string is expected'
        # elif function_name == 'states' and not len(all(posted_data[function_name])) == 2:
        #     return 303, 'Please enter 2 character state code'
        else:
            return 200, 'Successful Request'

    elif function_name == 'zipcodes':
        if function_name not in posted_data:
            return 301, 'Incorrect Key Value Used in JSON'
        # elif type(posted_data[function_name][0]) is not int:
        #     return 302, 'Incorrect data type, integer is expected'
        else:
            return 200, 'Successful Request'


facility_id_sql = '''
select hd.* 
                from dbo.hospital_data hd
                where hd.Facility_ID in {}
'''

facility_name_sql = '''
select hd.* 
                from dbo.hospital_data hd
                where hd.Facility_Name like "{!s}"
'''

state_sql = '''select hd.* 
                from dbo.hospital_data hd
                where hd.State in {}
'''

city_sql = '''
select hd.* 
                from dbo.hospital_data hd
                where hd.City in {}
'''

zipcode_sql = '''
select hd.* 
                from dbo.hospital_data hd
                where hd.ZIP_Code in {}
'''


class States(Resource):
    def get(self):
        """
        Request hospitals for a given list of states
        Request hospitals in a given list of states, returns JSON object with all hospitals in states specified
        ---
        tags:
          - Hospital Data
        parameters:
          - in: body
            name: body
            schema:
              id: States
              required:
                - states
              properties:
                states:
                  type: list of strings
                  description: list of 2 character state codes
                  default: ["ID", "AK"]
        responses:
          200:
            description: 'Successful Request'
            example:

            schema:
                type: json
        """
        posted_data = request.get_json()
        function_key = 'states'
        status_code, status_message = check_posted_data(posted_data, function_key)

        if status_code != 200:
            ret_json = {
                'Message': status_message,
                'Status Code': status_code
            }
            return jsonify(ret_json)

        search_str = str(posted_data[function_key]).replace('[', '(').replace(']', ')')

        cur = mysql.connect().cursor()
        cur.execute(state_sql.format(search_str))

        print(posted_data[function_key])

        print(state_sql.format(posted_data[function_key]))

        r = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]

        ret_map = {
            'Hospitals': r,
            'Status Code': status_code
        }

        return jsonify(ret_map)


class Cities(Resource):
    def get(self):
        """
        Request hospitals for a given list of cities
        Request hospitals in a given list of cities, returns JSON object with all hospitals in cities specified
        ---
        tags:
          - Hospital Data
        parameters:
          - in: body
            name: body
            schema:
              id: Cities
              required:
                - cities
              properties:
                cities:
                  type: list of strings
                  description: list of cities in state(s) of interest
                  default: ["Boise", "Meridian"]
        responses:
          200:
            description: 'Successful Request'
            example:

            schema:
                type: json
        """
        posted_data = request.get_json()
        function_key = 'cities'
        status_code, status_message = check_posted_data(posted_data, function_key)

        if status_code != 200:
            ret_json = {
                'Message': status_message,
                'Status Code': status_code
            }
            return jsonify(ret_json)

        search_str = str(posted_data[function_key]).replace('[', '(').replace(']', ')')

        cur = mysql.connect().cursor()
        cur.execute(city_sql.format(search_str))

        r = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]

        ret_map = {
            'Hospitals': r,
            'Status Code': status_code
        }

        return jsonify(ret_map)


class ZipCodes(Resource):
    def get(self):
        """
        Request hospitals for a given list of zipcodes
        Request hospitals for a given list of zipcodes, returns JSON object with all hospitals for zipcodes specified
        ---
        tags:
          - Hospital Data
        parameters:
          - in: body
            name: body
            schema:
              id: ZipCodes
              required:
                - zipcodes
              properties:
                zipcodes:
                  type: list of ints
                  description: list of zipcodes
                  default: 83702
        responses:
          200:
            description: 'Successful Request'
            example:

            schema:
                type: json
        """
        posted_data = request.get_json()
        function_key = 'zipcodes'

        status_code, status_message = check_posted_data(posted_data, function_key)

        if status_code != 200:
            ret_json = {
                'Message': status_message,
                'Status Code': status_code
            }
            return jsonify(ret_json)

        search_str = str(posted_data[function_key]).replace('[', '(').replace(']', ')')

        cur = mysql.connect().cursor()
        cur.execute(zipcode_sql.format(search_str))

        r = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]

        ret_map = {
            'Hospitals': r,
            'Status Code': status_code
        }

        return jsonify(ret_map)


class FacilityName(Resource):
    def get(self):
        """
        Request hospitals for a given facility name
        Request hospitals in a given facility name, returns JSON object with all hospitals for facility name specified
        ---
        tags:
          - Hospital Data
        parameters:
          - in: body
            name: body
            schema:
              id: FacilityName
              required:
                - facility_name
              properties:
                facility_name:
                  type: string
                  description: name of hospital
                  default: Ascension
        responses:
          200:
            description: 'Successful Request'
            schema:
                type: json
        """
        posted_data = request.get_json()
        function_key = 'facility_name'
        status_code, status_message = check_posted_data(posted_data, function_key)

        if status_code != 200:
            ret_json = {
                'Message': status_message,
                'Status Code': status_code
            }
            return jsonify(ret_json)

        cur = mysql.connect().cursor()
        cur.execute(facility_name_sql.format(posted_data[function_key]))

        r = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]

        ret_map = {
            'myCollection': r,
            'Status Code': status_code
        }

        return jsonify(ret_map)


class FacilityIDs(Resource):
    def get(self):
        """
        Request hospitals for a given list of facility ids
        Request hospitals in a given list of facility ids, returns JSON object with hospitals for facility ids specified
        ---
        tags:
          - Hospital Data
        parameters:
          - in: body
            name: body
            schema:
              id: FacilityIDs
              required:
                - facility_ids
              properties:
                facility_ids:
                  type: list of strings
                  description: list of hospital facility ids
                  default: ["100161", "100254"]
        responses:
          200:
            description: 'Successful Request'
            schema:
                type: json
        """
        posted_data = request.get_json()
        function_key = 'facility_ids'
        status_code, status_message = check_posted_data(posted_data, function_key)

        if status_code != 200:
            ret_json = {
                'Message': status_message,
                'Status Code': status_code
            }
            return jsonify(ret_json)

        search_str = str(posted_data[function_key]).replace('[', '(').replace(']', ')')

        print(search_str)

        cur = mysql.connect().cursor()
        cur.execute(facility_id_sql.format(search_str))

        r = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]

        ret_map = {
            'myCollection': r,
            'Status Code': status_code
        }

        return jsonify(ret_map)


api.add_resource(States, "/hospitals/{states}")
api.add_resource(Cities, "/hospitals/{cities}")
api.add_resource(ZipCodes, "/hospitals/{zipcodes}")
api.add_resource(FacilityName, "/hospitals/{facility_name}")
api.add_resource(FacilityIDs, "/hospitals/{facility_ids}")

if __name__ == '__main__':
    app.run()
