from __future__ import division, print_function
import urllib2
import json
import time

MAX_CHECKIN_REQUEST = 250


class FSAuthenticator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri #same as callback_uri
        self.access_token = None 

    def authorize_uri(self):
        '''Return the URI that directs the user to authenticate with foursquare'''
        return 'https://foursquare.com/oauth2/authenticate?client_id=' + self.client_id + '&response_type=code&redirect_uri='+ self.redirect_uri    

    def set_token(self, code):
        '''Given the temporary code, make a request to obtain the access token'''
        #make http request to foursquare to get the access token from the code
        #Response will contain access token
        url = "https://foursquare.com/oauth2/access_token?client_id=" + self.client_id + "&client_secret=" + self.client_secret +  "&grant_type=authorization_code&redirect_uri=" + self.redirect_uri + "&code=" + code
        self.access_token = json.load(urllib2.urlopen(url))['access_token']

    def auth_param(self):
        '''Return the authorization parameter string'''
        #The oauth_token should always be the first parameter passed
        return "?oauth_token=" + self.access_token

    def query(self, path, parameters=None):
        '''Given a query path and parameters, return the json response to the query'''
        if parameters == None:
            parameters = {}
        #parameters should be given as a dictionary
        url = "https://api.foursquare.com/v2/" + path + self.auth_param() + self.expand_params(parameters)
        print(url)
        return json.load(urllib2.urlopen(url))['response']

    def expand_params(self, parameters):
        '''Given a dictionary of parameters, return the substring that corresponds to those parameters in a GET request'''
        result = ""
        for key in parameters:
            result += "&" + str(key) + "=" + str(parameters[key])
        return result

class UserFinder:
    def __init__(self, authenticator):
        '''Given an FSAuthenticator, search for a user'''
        self.authenticator = authenticator

    def findUser(self, id):
        '''Retrieve the User associated with the given id. Raise an error if the authenticator is not authorized to access the User'''
        #Issue a request to create and return a new user object
        #return a new User object
        
        json_result =  urllib2.urlopen("https://api.foursquare.com/v2/users/" + str(id) + self.authenticator.auth_param()).read()
        return User(self.authenticator, json_result['response']['user'])


class User:
    
    def __init__(self, authenticator, json_string):
        '''Given a JSON string that describes the user, store the JSON for use at a later date. Also store the authenticator object for future queries'''
        #response = urllib2.urlopen('https://foursquare.com/oauth2/access_token?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth&code=' + code)

        self.data = json.loads(json_string)
        self.authenticator = authenticator 
        self.time = time.time()

    def id(self):
        '''Return the user's id'''
        return self.data['id']

    def first_name(self):
        '''Return the user's first name'''
        return self.data['firstName']

    def last_name(self):
        '''Return the user's last name'''
        return self.data['lastName']

    def gender(self):
        '''Return the user's gender'''
        return self.data['gender']

    def email(self):
        '''Return the user's email address'''
        return self.data['contact']['email']

    def twitter(self):
        '''Return the user's Twitter contact information'''
        return self.data['contact']['twitter']
 
    def facebook(self):
        '''Return the user's Twitter contact information'''
        return self.data['contact']['facebook']

    def phone(self):
        '''Return the user's Twitter contact information'''
        return self.data['contact']['phone']

    def badges_count(self):
        '''Return the number of badgers that the user has earned'''
        return self.data['badges']['count']

    def checkins_count(self):
        '''Return the number of checkins'''
        return self.data['checkins']['count']

    def get_checkins(self, params = {}):
        '''Return the user's recent checkins. Parameters can be passed as a dictionary'''
        json_objects = self.authenticator.query("users/" + self.id() + "/checkins", params)['checkins']['items']
        checkins = [Checkin(self.authenticator, object) for object in json_objects]
        return checkins

    def all_checkins(self):
        '''Return the user's checkins'''
        count = MAX_CHECKIN_REQUEST
        offset = 0
        checkins = []
        #When count is not 250, there are no more checkins that need to be queried
        while count == 250:
            checkins.extend(self.get_checkins({"limit" : count, "offset" : offset}))
            count = len(checkins)
            offset += count
        
        return checkins

    def last_checkin(self):
        '''Return the most recent checkin of the user'''
        checkin_data = self.data['checkins']['items'][-1]
        return Checkin(self.authenticator, checkin_data)

    def checkins_here(self):
        '''Return the checkins at the last venue visited. (This will only work for friends of the authenticating user)'''
        last_checkin_id = self.last_checkin().venue().id()
        #Get the checkin JSON for the most recently visited venue
        checkin_items = self.authenticator.query("venues/" + last_checkin_id + "/herenow")
        checkin_objects = []
        for checkin in checkin_items:
            try:
                result = self.authenticator.query("checkins/" + checkin["id"])['checkin']
                checkin_objects.add(Checkin(self.authenticator, result))
            #Skip over checkins which we are not authorized to access
            except:
                print(checkin["id"] + " could not be queried")
                continue
    
    def mayorships_count(self):
        '''Returns the number of mayorships that the user has earned'''
        return self.data['mayorships']['count']

    def mayorships(self):
        '''Returns the mayorships that the user has earned'''
        return self.data['mayorships']['items'] 

    def following_count(self):
        '''Return the number of users that the user is following'''
        return self.data['following']['count']  

    def tips_count(self):
        '''Return the number of tips that the user has left'''
        return self.data['tips']['count']

    def todos_count(self):
        return self.data['todos']['count']

    def recent_scores(self):
        return self.data['scores']['recent']

    def max_scores(self):
        return self.data['scores']['max']

    def friends(self):
        '''Return a list of the user's friends'''
        response = self.authenticator.query("users/" + self.id() + "/friends")["friends"]["items"]
        return [User(self.authenticator, element) for element in response]

    def tips(self):
        '''Return a list of the user's tips'''
        response = self.authenticator.query("users/" + self.id() + "/tips")['tips']['items']
        return [Tip(self.authenticator, element) for element in response]

    def photo(self):
        '''Return the uri of the photo (icon) associated with the user'''
        return self.data['photo']


class Checkin:
    
    def __init__(self, authenticator, json_string):
    
        self.authenticator = authenticator
        self.data = json_string
        self.time = time.time()


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

    def photos_count(self):
        '''Return the number of photos associated with this checkin'''
        return self.data['photos']['count']

    def photos(self):
        '''Get the photos associated with this checkin. Assumes photo exists'''
        photos_list = [Photo(self.authenticator, photo_json) for photo_json in self.data['photos']['items']]
        return photos_list

class Venue:
    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string
        self.time = time.time()


    def id(self):
        '''Return the venue id'''
        return self.data['id']

    def name(self):
        '''Return the name of the venue'''
        return self.data['name']

    def contact(self):
        '''Return the contact information for the venue'''
        return self.data['contact']

    def location(self):
        '''Return the location of the venue'''
        return Location(self.data['location'])

    def verified(self):
        '''Return True if the venue has been verified'''
        return self.data['verified'] == 'true'

    def checkinsCount(self):
        return self.data['stats']['checkinsCount']

    def usersCount(self):
        return self.data['stats']['usersCount']
        
    def url(self):
        '''Return the url of the venue'''
        return self.data['url']
   
    def here_now_count(self):
        '''Return the number of users at the venue'''
        return self.data['hereNow']['count']
       
    def mayor(self):
        '''Return the mayor of the venue'''
        return User(self.data['mayor']['user'])

    def tips_count(self):
        '''Return the number of tips'''
        return self.data['tips']['count']

class Photo:

    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string
        self.time = time.time()

    def id(self):
        '''Return the id of the photo'''
        return self.data['id']

    def createdAt(self):
        '''Return the UNIX time at which the photo was created'''
        return self.data['createdAt']

    def url(self):
        '''Return the url for the photo'''
        return self.data['url']



class Tip:

    def __init__(self, authenticator, json_string):
        self.authenticator = authenticator
        self.data = json_string
        self.time = time.time()

    def id(self):
        '''Return the id of the tip'''
        return self.data['id']

    def createdAt(self):
        '''Return the UNIX time at which the tip was created'''
        return self.data['createdAt']

    def text(self):
        '''Return the text of the tip'''
        return self.data['text']

if __name__ == '__main__':
    print("redefining")
    authenticator = FSAuthenticator("D0PJDUVDEWECQ3ZM3JMAR13G20RLPPUO4OJLMXNGGNYUCAE1", "2YIJX5T1IQC1QCU15J30WYG2X3SKGFNFH35IDQBIMJZVXTX2", "http://localhost.com:8080")

    authenticator.access_token = "XNC12SB5HY4UFBGEDWXHVSOKEFUNLEP3WR2AZSXX4GC5KQNB"

    finder = UserFinder(authenticator)

    my_id = "10867705" 
    
    my_user = finder.findUser(my_id)

