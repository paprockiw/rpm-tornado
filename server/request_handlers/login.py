"""
This is the request handler incharge of login in users
"""

import json

import tornado.web
import tornado.gen

import document

import pdb

class RequestHandler(document.RequestHandler):

    @tornado.web.asynchronous # sets up route to be asynchronous
    @tornado.gen.coroutine # allows us to use generators and coroutins for async io
    def post(self, param):
        """
        user post login reqest. 
        passes in paramiters username, and password.
        if everything checks out then it finishes connections.
        if anything wrong happens an exception is thrown
        """

        # pdb.set_trace()

        # get database 
        database = param.split('/')[0]

        # get document _id 
        _id = param.split('/')[1]

        # get path to property of document 
        path = param.split('/')[2:]

        # get post data
        data = json.loads(self.request.body)

        # extract username from data
        username = data['username']

        # extract password from data
        password = data['password']

        # get users 
        users, cache = yield self.get_data(\
            url="http://localhost:5984/"+database+"/"+_id,\
            path=path\
            )

        # pdb.set_trace()

        # check is username is administrator
        if username == users['administrator']:

            # check if password is correct
            if users['password'] == password:

                # assign secure cookie
                self.set_secure_cookie("login", 'true',  expires_days=None)
                self.finish()

            # incorect password
            else:

                self.custom_error_response('incorect password')

        # incorrect username
        else:

            self.custom_error_response('incorect username')


        



