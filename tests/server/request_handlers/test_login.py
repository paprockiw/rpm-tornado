import os
import sys
import json

import unittest

from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none

import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

# add to sys.path
path = os.path.realpath(os.path.realpath(__file__) + '/../../../../fabfile/')
sys.path.append(path)

from server.request_handlers import login

 
class Login(AsyncHTTPTestCase):

    def get_app(self):
        """
        setup tornado application for this test
        """

        app = Application([(r'/login/(.+)', login.RequestHandler)])

        app.settings = {
            'cookie_secret': 'swipetechnologies'
        }

        return app


    def test_case1(self):
        """
        if correct username and password is submited,
        it should return OK
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/login/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'username':'admin', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'OK')
        assert_is_none(response.error)



    def test_case2(self):
        """
        if incorrect username was submited,
        it should return an error 
        """

        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/login/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'username':'failme', 'password':'swipe' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error) 
        assert_equals(response.body,'incorect username')
       
        

    def test_case3(self):
        """
        if incorrect password was submited,
        it should return error
        """
        
        request = tornado.httpclient.HTTPRequest(\
            url=self.get_url('/login/admin/administrator/users'),\
            method="POST",\
            body=json.dumps({ 'username':'admin', 'password':'failme' })\
            )

        self.http_client.fetch(request, self.stop)
        response = self.wait()

        assert_equals(response.reason,'Bad Request')
        assert_is_not_none(response.error) 
        assert_equals(response.body,'incorect password')






