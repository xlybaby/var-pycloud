# -*- coding: utf-8 -*-
import sys,os
import tornado.web

from app.common.constants import RequestMapping

class Controller(object):
    
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
        print('Controller initializing...')
        print(cls)
        
    def __call__(self):
        print('Controller() called...')
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]
    
class SignUp(tornado.web.RequestHandler):
    def get(self):
        self.write("UcFectchTemplateById")

class SignIn(tornado.web.RequestHandler):
    def get(self):
        self.write("UcFectchTemplatesByUserId")

class SignOut(tornado.web.RequestHandler):
    def get(self):
        self.write("UcFectchSharedTemplates")
    
def mapping():    
    list = []
    list.append((RequestMapping.user_sign_in, SignIn))
    list.append((RequestMapping.user_sign_out, SignOut))
    list.append((RequestMapping.user_sign_up, SignUp))
    return list