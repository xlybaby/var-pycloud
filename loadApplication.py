# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web

from app.init.populateWebComponent import WebApplication 
from app.init.fileBasedConfiguration import ApplicationProperties
from app.context.initializedInstancePool import ApplicationContext 

class Main(object):
    
    @staticmethod
    def init(p_command=None):
        
        properties = ApplicationProperties(p_command)
        application = WebApplication()
        application.populate(p_properties=properties)
        if application is None:
            raise Exception("Applcation can't be initialized!")
        ioLoop = tornado.ioloop.IOLoop.current()

        ApplicationContext.getContext().putInstance( p_name='var.application.webApplication', p_obj=application )
        ApplicationContext.getContext().putInstance( p_name='var.application.configuration', p_obj=properties )
        ApplicationContext.getContext().putInstance( p_name='var.ioloop.current', p_obj=ioLoop )

        ioLoop.start()
 
if __name__ == '__main__':
    props={}
    if len(sys.argv) > 1:
        for idx in range(1, len(sys.argv)):
            arg = sys.argv[idx]
            if arg.startswith("--") :
                prop = arg[2:]
                pair = prop.split("=")
                props[pair[0]]=pair[1]
                print ("command props", props)
     
Main.init(p_command=props)                                                                           