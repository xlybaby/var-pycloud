# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web

from app.init.populateWebController import WebApplication 
from app.context.initializedInstancePool import ApplicationContext 
from app.init.fileBasedConfiguration import ApplicationProperties

class Main(object):
    
    @staticmethod
    def init(p_command=None):
        
        properties = ApplicationProperties(p_command)
        application = WebApplication()
        application.populate(p_properties=properties)
        if application is None:
            raise Exception("Applcation can't be initialized!")
        ioLoop = tornado.ioloop.IOLoop.current()

        ApplicationContext.getContext().putInstance( p_name='var.application.context', p_obj=application )
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
