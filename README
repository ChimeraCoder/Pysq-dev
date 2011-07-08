Pysq
=========

Introduction
-------------

Pysq is an unofficial wrapper for version 2 of the Foursquare API. It was developed on Python 2.7 on a Linux machine, though it should work on Python 2.6 and on other platforms.



Use
-----------

Pysq provides a wrapper for authentication through OAuth. First, register your application on the Foursquare developer homepage to receive your client_id and client_secret values. Then, authenticate using the FSAuthenticator class. (Note that redirect_uri is the uri for your application, which you register with Foursquare).

>  >>>authenticator = FSAuthenticator(client_id, client_secret, redirect_uri)



Then, redirect your user to the uri that the FSAuthenticator object generates:

> >>>uri = authenticator.authorize_uri()

The user will sign in with his/her Foursquare credentials, and Foursquare will redirect back to your registered page (redirect_uri), with a code passed as a GET parameter. Retrieve this code and pass it in to the set_token method:

> >>>authenticator.set_token(code)

You are now ready to begin making queries that this user is authorized to make!


Querying Users
--------------

To obtain a User object, use the UserFinder object.

> >>>finder = UserFinder(authenticator)

> >>>my_user = finder.findUser(id)


