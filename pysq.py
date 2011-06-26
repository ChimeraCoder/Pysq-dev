from __future__ import division, print_function
import urllib2
import json
import httplib


class FSAuthenticator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri #same as callback_uri
        self.access_token = None 

    def authorize_uri():
        return 'https://foursquare.com/oauth2/authenticate?client_id=' + CLIENT_ID + '&response_type=code&redirect_uri='+ REDIRECT_URI

    def get_token(code):
        pass
        pass
        #make http request to foursquare to get the access token from the code
        #make urllib2 request to this url
        "https://foursquare.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI&code=CODE"
        #Response will contain access token
        self.access_token = access_token
        return access_token

def checkin(checkin_id):
        '''Given a checkin id, return the information for that checkin'''


class UserFinder:
    def __init__(self, authenticator):
    '''Given an FSAuthenticator, search for a user'''
        self.authenticator = authenticator

    def findUser(self, id):
        #Issue a get request to create and return a new user object
        pass
        return #return a new FSUser object



class FSUser:
    
    def __init__(self, authenticator, json_query):
        '''Given a JSON query that describes the user, store the JSON for use at a later date. Also store the authenticator object for future queries'''
        response = urllib2.urlopen('https://foursquare.com/oauth2/access_token?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth&code=' + code)

        data = json.loads(response.read())
        self.authenticator = authenticator 

    def fetch(self):
        self.data = json.loads(########)

        #TODO cache this
    def first_name(self):
        '''Return the user's first name'''
        return data['response']['user']['firstName']

    def last_name(self):
        return data['response']['user']['lastName']

    def gender(self):
        return data['response']['user']['gender']

    def twitter(self):
        '''Load the user's Twitter contact information'''
        return data['response']['user']['contact']['twitter']
 
    def facebook(self):
        '''Load the user's Twitter contact information'''
        return data['response']['user']['contact']['facebook']

    def phone(self):
        '''Load the user's Twitter contact information'''
        return data['response']['user']['contact']['phone']

    def badge_count(self):
        '''Return the number of badgers that the user has earned'''
        return data['response']['user']['badges']['count']

    #def all_checkins(self):
        '''Return the user's checkins'''

    def mayorships_count(self):
        '''Returns the number of mayorships that the user has earned'''
        return data['response']['user']['mayorships']['count']

    #def last_checkin(self):

    
