# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web
from app.context.initializedInstancePool import ApplicationContext 

def createInstance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello!")
          
class WebApplication(object):
    
    def __init__(self):
        self.__requestMapping = []
        self.__procedureMapping = []
        self.__persistenceMapping = []
        self.__application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    
    def populate(self, p_properties=None):
        if p_properties is None:
            return None
        self.__scan()
        for mapping in self.__requestMapping:
            print(mapping)
             
        self.__application.add_handlers( r'(.*)', self.__requestMapping )        
        self.__application.listen(p_properties.getProperty(p_key='server.port'))
        for mapping in self.__persistenceMapping:
            print(mapping)
            ApplicationContext.getContext().putInstance( p_name=mapping['instance_name'], p_obj=mapping['instance'] )

        for mapping in self.__procedureMapping:
            print(mapping)
            ApplicationContext.getContext().putInstance( p_name=mapping['instance_name'], p_obj=mapping['instance'] )
            
    def getTornadoWebApplication(self):
        return self.__application
    
    def __scan(self):
#         mapping = createInstance('module.uc.handler.fetchTemplateController', 'mapping')
#         #print(mapping())
#         print(mapping)
        for dir in os.listdir(sys.path[0]+'/module'):
            modulepath = sys.path[0]+'/module/'+dir
            if os.path.isdir(modulepath):
                for mod in os.listdir(modulepath):
                    
                    if os.path.isdir(modulepath+'/'+mod) and mod == 'handler':
                        print("find controller dir: %s"%(modulepath+'/'+mod))
                        for controller in os.listdir(modulepath+'/'+mod):
                            if controller.lower().find('controller') >=0 :
                                mapping = createInstance('module.'+dir+'.'+mod+'.'+controller[:-3], 'mapping')
                                self.__requestMapping = self.__requestMapping + mapping
                                
                    if os.path.isdir(modulepath+'/'+mod) and mod == 'procedure':
                        print("find procedure dir: %s"%(modulepath+'/'+mod))
                        for procedure in os.listdir(modulepath+'/'+mod):
                            if procedure.lower().find('procedure') >=0 :
                                pmapping = createInstance('module.'+dir+'.'+mod+'.'+procedure[:-3], 'mapping')
                                self.__procedureMapping = self.__procedureMapping + pmapping
                                
                    if os.path.isdir(modulepath+'/'+mod) and mod == 'persistence':
                        print("find persistence dir: %s"%(modulepath+'/'+mod))
                        for persistence in os.listdir(modulepath+'/'+mod):
                            if persistence.lower().find('persistence') >=0 :
                                print('module.'+dir+'.'+mod+'.'+persistence[:-3])
                                permapping = createInstance('module.'+dir+'.'+mod+'.'+persistence[:-3], 'mapping')
                                self.__persistenceMapping = self.__persistenceMapping + permapping
                              