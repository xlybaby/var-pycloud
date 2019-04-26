# -*- coding: utf-8 -*-
import sys,os,json
from app.context.initializedInstancePool import ApplicationContext 
from app.common.decorator import injectComponent

#ucFectchTemplateByIdProcedure
class FetchTemplateById(object):
    
    def __init__(self):
        self._service_name = 'ucFectchTemplateByIdProcedure'
    
    def execute(self, args):
        access = self.getTemplateAccess()
        return access.execute(args)
        
    @injectComponent('ucFectchTemplateByIdAccess')
    def getTemplateAccess(self):
        pass
    
def mapping():
    service_mapping_list = [{'instance_name':'ucFectchTemplateById','instance':FetchTemplateById()}]
    return service_mapping_list;