from google.cloud import ndb
from datetime import datetime
import os


class stats(ndb.Model):
    light = ndb.TextProperty()
    curr_time = ndb.DateTimeProperty()
     
def create_record(light_value):
    one = stats(
        light = light_value,
        curr_time = datetime.now())
    one.put()
    

def cors_enabled_function(request):
    
    ndbclient = ndb.Client()

    request_json = request.get_json(silent=True)
    request_args = request.args

    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    else:

        if request_json and 'light' in request_json:
            light = request_json['light']
         
        elif request_args and 'light' in request_args:
            light = request_args('light')

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*'
        }

        if request.method == "POST":
            with ndbclient.context():
                create_record(light)
            
            return ("Uploaded", 200, headers)

        else:

            with ndbclient.context():

                query = stats.query()
                results = list(query.fetch())

            packet = {
                "data": {str(e.curr_time):e.light for e in results}
            }

            return (packet, 200, headers)