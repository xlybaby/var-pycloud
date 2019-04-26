# -*- coding: utf-8 -*-
import sys,os,json

#ucFectchTemplateByIdAccess
class FetchTemplateByIdFromIgnite(object):
    
    def __init__(self):
        self._service_name = 'ucFectchTemplateByIdAccess'
    
    def execute(self, args):
        return args
    
    def __fetchTemplate(self, p_tid):
        pass

#ucFectchTemplateByIdAccess    
class FetchTemplateByIdFromMySql(object):
    
    def __init__(self):
        self._service_name = 'ucFectchTemplateByIdAccess'
    
    def execute(self, args):
        return args
    
    def __fetchTemplate(self, p_tid):
        pass
    
def mapping():
    persistence_mapping_list = [{'instance_name':'ucFectchTemplateByIdAccess','instance':FetchTemplateByIdFromIgnite()}]
    return persistence_mapping_list;