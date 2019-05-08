# -*- coding: utf-8 -*-
import sys,os,time,shutil

from scrapy.selector import Selector 

import tornado.ioloop
import tornado.web
from tornado import gen, httpclient, ioloop, queues

from app.init.populateWebComponent import WebApplication 
from app.init.fileBasedConfiguration import ApplicationProperties
from app.context.initializedInstancePool import ApplicationContext 

def parse(content):
    selector = Selector(text=content)
    #print('content: ', content)
    print('Title: %s'%(selector.xpath('//html/head/title/text()').get().strip('\r\n\t ')) )
    
async def worker(idx, parent):
    print('worker[%s] starts'%(idx))
    while True:
        print('worker[%s] check dir - %s'%(idx, parent+'/'+idx))
        for file in os.listdir( parent+'/'+idx ):
            try:
                print('work[%s] find file - %s'%(idx, file))
                f = open(parent+'/'+idx+'/'+file, 'rb')
                parse(content=f.read())
                #f.close()
                #os.remove(parent+'/'+idx+'/'+file)
            except Exception as e:
                print("worker[%s] encounter exception: %s, parent dir: %s" % (idx, e, parent))
                #remove exception file to log dir
                #shutil.move(parent+'/'+idx+'/'+file, parent+'/exception/'+file)
            finally:
                if f:
                    f.close()
                    os.remove(parent+'/'+idx+'/'+file)
                    
        await gen.sleep(5)

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write('Working...')
        
def Main(p_command=None):        
    properties = ApplicationProperties(p_command)
    #dlist = dashboard.populate() + [ (RequestMapping.submit_fetch_url_task, MainHandler)]
    application = tornado.web.Application([ (r'/', MainHandler),])
    application.listen(properties.getProperty(p_key='server.port'))
    
    vols=[]
    partitiondir = properties.getProperty(p_key='application.persistence.fetchdir') + '/'  + properties.getProperty(p_key='application.persistence.defaultPartition') 
    if( os.path.exists( partitiondir ) ):
        for vol in os.listdir( partitiondir ):
            if vol != 'exception':
                vols.append(vol)
    print('%d volumns in partion'%(len(vols)))
        
    workers = gen.multi([worker( v, partitiondir ) for v in vols])
    ioLoop = tornado.ioloop.IOLoop.current()
    
    #request = HttpRequest()
    #await request.do()
    #ApplicationContext.getContext().putInstance( p_name='var.application.inq', p_obj=inq )
    ApplicationContext.getContext().putInstance( p_name='var.application.workers', p_obj=workers )
    ApplicationContext.getContext().putInstance( p_name='var.application.configuration', p_obj=properties )
    ApplicationContext.getContext().putInstance( p_name='var.application.webApplication', p_obj=application )
    #ApplicationContext.getContext().putInstance( p_name='var.application.urlRequest', p_obj=request )
    ApplicationContext.getContext().putInstance( p_name='var.ioloop.current', p_obj=ioLoop )
    ioLoop.start()
    #ioLoop.run_sync()
  
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
                
    Main( p_command=props )                                                                          