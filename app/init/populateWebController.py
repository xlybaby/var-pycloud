# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web

def createInstance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj
  
class WebApplication(object):
    
    def __init__(self):
        pass
    
    def populate(self, p_properties=None):
        if p_properties is None:
            return None
        
    def __scan(self):
        
        rootdir = open(sys.path[0]+'/module', 'r')
        for dir in os.listdir(sys.path[0]+'/module'):
            modulepath = sys.path[0]+'/module/'+dir
            if os.path.isdir(modulepath):
                for mod in os.listdir(modulepath):
                    if os.path.isdir(modulepath+'/'+mod) and mod == 'handler':
                        for controller in os.listdir(modulepath+'/'+mod):
                            if controller.find('Controller') >=0 :
                                o = createInstance('module.'+dir+'.'+mod+'.'+controller, 'Controller')
                                print(o)