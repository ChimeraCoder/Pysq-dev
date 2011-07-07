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

    def authorize_uri(self):
        return 'https://foursquare.com/oauth2/authenticate?client_id=' + self.client_id + '&response_type=code&redirect_uri='+ self.redirect_uri    

    def set_token(self, code):
        #make http request to foursquare to get the access token from the code
        #Response will contain access token
        self.access_token = json.load(urllib2.urlopen("https://foursquare.com/oauth2/access_token?client_id=" + self.client_id + "&client_secret=" + self.client_secret +  "&grant_type=authorization_code&redirect_uri=" + self.redirect_uri + "&code=" + code))['access_token']


    def auth_param(self):
        return "?oauth_token=" + self.access_token

class UserFinder:
    def __init__(self, authenticator):
        '''Given an FSAuthenticator, search for a user'''
        self.authenticator = authenticator

    def findUser(self, id):
        #Issue a request to create and return a new user object
        #return a new FSUser object
        return FSUser(self.authenticator, urllib2.urlopen("https://api.foursquare.com/v2/users/" + str(id) + self.authenticator.auth_param()))


class FSUser:
    
    def __init__(self, authenticator, json_query):
        '''Given a JSON query that describes the user, store the JSON for use at a later date. Also store the authenticator object for future queries'''
        #response = urllib2.urlopen('https://foursquare.com/oauth2/access_token?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth&code=' + code)

        #TODO have this accept string instead of query
        self.data = json.loads(json_query.read())
        self.authenticator = authenticator 

    def first_name(self):
        '''Return the user's first name'''
        return self.data['response']['user']['firstName']

    def last_name(self):
        '''Return the user's last name'''
        return self.data['response']['user']['lastName']

    def gender(self):
        '''Return the user's gender'''
        return self.data['response']['user']['gender']

    def twitter(self):
        '''Load the user's Twitter contact information'''
        #TODO fix case where Twitter is not linked
        return self.data['response']['user']['contact']['twitter']
 
    def facebook(self):
        '''Load the user's Twitter contact information'''
        #TODO fix case where Facebook is not linked
        return self.data['response']['user']['contact']['facebook']

    def phone(self):
        '''Load the user's Twitter contact information'''
        #TODO fix case where phone is not given
        return self.data['response']['user']['contact']['phone']

    def badge_count(self):
        '''Return the number of badgers that the user has earned'''
        return self.data['response']['user']['badges']['count']

    #def all_checkins(self):
    #    '''Return the user's checkins'''

    def mayorships_count(self):
        '''Returns the number of mayorships that the user has earned'''
        return self.data['response']['user']['mayorships']['count']

    def mayorships(self):
        '''Returns the mayorships that the user has earned'''
        return self.data['response']['user']['mayorships']['items'] 

    def checkins_count(self):
        '''Returns the number of checkins'''
        return self.data['response']['user']['checkins']['count']

    def last_checkin(self):
        '''Return the most recent checkin of the user'''
        checkin_data = self.data['response']['user']['checkins']['items'][-1]
        return Checkin(self.authenticator, checkin_data)
    
    def following(self):
        return self.data['response']['user']['following']['count']  

    def tips_count(self):
        '''Return the number of tips that the user has left'''
        return self.data['response']['user']['tips']['count']

    def todos_count(self):
        return self.data['response']['user']['todos']['count']

    def recent_scores(self):
        return self.data['response']['user']['scores']['recent']

    def max_scores(self):
        return self.data['response']['user']['scores']['max']


class Checkin:
    
    def __init__(self, authenticator, json_string):
    
        #TODO #FIXME
        self.authenticator = authenticator
        self.data = json_string

    def id(self):
        '''Return the id of the checkin'''
        return self.data['id']

    def createdAt(self):
        '''Return the Unix timestamp of the checkin'''
        return self.data['createdAt']

    def timeZone(self):
        '''Return the timezone of the checkin'''
        return self.data['timeZone']

    def type(self):
        '''Return the type of the checkin'''
        return self.data['type']

    def hasShout(self):
        '''Return True if the checkin has a shout'''
        return ('shout' in self.data)

    def shout(self):
        '''Return any shout associated with the checkin'''
        return self.data['shout']

    def venue(self):
        '''Return the Venue object associated with the checkin'''
        return Venue(self.authenticator, self.data['venue'])

    def hasPhotos(self):
        '''Return True if any photos are associated with this checkin'''
        return ('photos' in self.data) 

    def photos(self):
        '''Get the photos associated with this checkin. Assumes photo exists'''
        #TODO fix thix
        #return Photo(self.authenticator, self.data['venue'])


class Venue:
    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string

    def id(self):
        return self.data['id']

    def name(self):
        return self.data['name']

    def contact(self):
        return self.data['contact']

    def location(self):
        #TODO add Location
        return Location(self.data['location'])

    def verified(self):
        return self.data['verified']

    def checkinsCount(self):
        return self.data['stats']['checkinsCount']

    def usersCount(self):
        return self.data['stats']['usersCount']
        
    def url(self):
        #FIXME url may not be defined
        return self.data['url']
        
       

class Photo:

    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string

    def id(self):
        return self.data['response']['photo']['id']

    def createdAd(self):
        return self.data['response']['photo']['createdAd']

    def url(self):
        return self.data['response']['photo']['url']



class Tip:

    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string


    def id(self):
        return self.data['response']['tip']['id']

    def createdAt(self):
        return self.data['response']['tip']['createdAt']

    def text(self):
        return self.data['response']['tip']['text']

    def status(self):
        return self.data['response']['tip']['status']


