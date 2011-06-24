from __future__ import division, print_function
import urllib2
import json
import httplib

CLIENT_ID = None#FILL IN THE CLIENT ID
REDIRECT_URI = None#FILL IN THE REDIRECT URI
CLIENT_SECRET = None #FILL IN THE CLIENT SECRET KEY



def authenticate():
    return HttpResponseRedirect('https://foursquare.com/oauth2/authenticate?client_id=' + CLIENT_ID + '&response_type=code&redirect_uri='+ REDIRECT_URI)

def checkin(checkin_id):
        '''Given a checkin id, return the information for that checkin'''

class FSUser:
    
    def __init__(self, code):
        '''Given a code, query the user's id, username, and access token and store these'''
        response = urllib2.urlopen('https://foursquare.com/oauth2/access_token?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth&code=' + code)

        data = json.loads(response.read())
        access_token = data['access_token']
        self.id = data['response']['user']['id']
        self.username = data['response']['user']['contact']['twitter']
        self.access_token = data['access_token']
        
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

    

