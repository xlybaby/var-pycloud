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
    
class UcSubmitTemplateByUserId(tornado.web.RequestHandler):
    def get(self):
        self.write("UcSubmitTemplateByUserId")

class UcSaveTemplateByUserId(tornado.web.RequestHandler):
    def get(self):
        self.write("UcSaveTemplateByUserId")

def mapping():    
    list = []
    list.append((RequestMapping.submit_template_with_uid, UcSubmitTemplateByUserId))
    list.append((RequestMapping.save_template_with_uid, UcSaveTemplateByUserId))
    return list