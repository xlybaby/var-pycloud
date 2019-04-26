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
    
class imageCode(tornado.web.RequestHandler):
    def get(self):
        pass

class dynamicCode(tornado.web.RequestHandler):
    def get(self):
        pass

class humanIdentify(tornado.web.RequestHandler):
    def get(self):
        pass
    
def mapping():    
    list = []
    list.append((RequestMapping.get_image_code, imageCode))
    list.append((RequestMapping.get_dynamic_code, dynamicCode))
    list.append((RequestMapping.get_human_identify, humanIdentify))
    return list