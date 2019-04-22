# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Server starts...")
            
class Main(object):
    
    @staticmethod
    def init():
        print (u'Application loading...')
        application = tornado.web.Application([(r"/", MainHandler),])
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
        
Main.init()                                                                           
