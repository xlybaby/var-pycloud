# -*- coding: utf-8 -*-
import sys,os,json
import tornado.web

from app.common.constants import RequestMapping
from app.common.decorator import controller_process_agent


class UcFectchTemplateById(tornado.web.RequestHandler):
    
    def prepare(self):
        if 'Content-Type' not in self.request.headers:
            raise Exception('Unsupported content-type!')
         
        if  self.request.headers['Content-Type'].strip().startswith('application/json'):
            self.args = json.loads(self.request.body)
        else:
            raise Exception('Unsupported content-type!',self.request.headers['Content-Type'])
        
    @controller_process_agent('ucFectchTemplateById')
    def post(self):
        print('request handle -> fetch template by id ->', self.args)

class UcFectchTemplatesByUserId(tornado.web.RequestHandler):
    def get(self):
        pass

class UcFectchSharedTemplates(tornado.web.RequestHandler):
    def get(self):
        pass

class UcFectchTemplatesByKeywords(tornado.web.RequestHandler):
    def get(self):
        pass
                                

def mapping():    
    list = []
    list.append((RequestMapping.fetch_template_by_id, UcFectchTemplateById))
    list.append((RequestMapping.fetch_template_by_uid, UcFectchTemplatesByUserId))
    list.append((RequestMapping.fetch_shared_templates, UcFectchSharedTemplates))
    list.append((RequestMapping.fetch_template_by_keywords, UcFectchTemplatesByKeywords))
    return list