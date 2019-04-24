# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web

from var.init.populateWebController import WebApplication 
from var.context.initializedInstancePool import ApplicationContext 
from var.init.fileBasedConfiguration import ApplicationProperties

class Main(object):
    
    @staticmethod
    def init(p_command=None):
        #properties
        #application = WebApplication.populate(p_properties=properties)
        configuration = ApplicationProperties(p_command)
        ioLoop = tornado.ioloop.IOLoop.current()
        
        ApplicationContext.getContext().putInstance( p_name='var.application.configuration', p_obj=configuration )
        ApplicationContext.getContext().putInstance( p_name='var.ioloop.current', p_obj=ioLoop )
        configuration.list()
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
