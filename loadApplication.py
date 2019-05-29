# -*- coding: utf-8 -*-
import sys,os,time,shutil,json
import datetime
import urllib3
import urllib3.contrib.pyopenssl
import certifi
from scrapy.selector import Selector 

import tornado.ioloop
import tornado.web
from tornado import gen, httpclient, ioloop, queues

from app.init.populateWebComponent import WebApplication 
from app.init.fileBasedConfiguration import ApplicationProperties
from app.context.initializedInstancePool import ApplicationContext 

inq = queues.Queue()

async def async_fetch_https(url):
    header = {
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) VAR/1.0.0.1"
    }
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url,method='GET',headers=header)
        return response.body
    except Exception as e:
        print("Error: %s" % e)
        return ''

def fetch_https(url):
    #if scenarioId == 'sid-003' or scenarioId == 'sid-007' or scenarioId == 'sid-0013' or scenarioId == 'sid-0016':
     #   await gen.sleep(15)
    
    print('[%s] fetch_https |  url[%s]'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), url))    
    header = {
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) VAR/1.0.0.1"
    }
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url, None, header)
    return response.data
        
def corpus(pageno, pages, content, parent=None):
    page = pages[pageno]
    selector = page['selector']
    extract = page['extract'] if "extract" in page else 'False'
    wholeTxt =  page['wholeTxt'] if "wholeTxt" in page else 'False'
    
    sel = Selector(text=content,type='html')
    items = sel.xpath(selector['xpath'])
    for item in items:
        itemObj={}
        itemObj['children']=[]
        if extract == 'True':
            href = item.xpath('@href').get()
            itemObj['href'] = href
            #body = async_fetch_https(href)
            body = fetch_https(href)
            corpus(pageno+1, pages, content=body, parent=itemObj)
        if wholeTxt == 'True':
            itemObj['text'] = item.xpath('//*/text()').getall()
        else:
            itemObj['text'] = item.xpath('text()').get()
        parent['children'].append(itemObj)
    return
    
def parse(content):
    print(content)
    selector = Selector(text=content,type='html')
    #print('content: ', content)
    items = selector.xpath("//ul[contains(@class, 'hot-list')]/li/a")
    #print(items)
    values=''
    for item in items:
        val={}
        values+=item.xpath('@href').get() + ' - '
        values+=item.xpath('text()').get() + '\n'
        print('<a href="%s">%s</a>'%(item.xpath('@href').get(), item.xpath('text()').get()))
    return values    
    
async def worker(idx, parent):
    props = ApplicationContext.getContext().getInstance( p_name='var.application.configuration' )
    datadir = props.getProperty(p_key='application.persistence.rootdir')
    async for task in inq:
                    
        try:
            preLen=task[0:6]
            print('Got task, preLen: %s'%(preLen))
            print('Task: %s'%(task[6:int(preLen)+6]))
            taskObj = json.loads(task[6:int(preLen)+6])
            print(taskObj)
            selector = Selector(text=task[6+int(preLen):],type='html')
            items = selector.xpath("//ul[contains(@class, 'hot-list')]/li/a")
            for item in items:
                print('<a href="%s">%s</a>'%(item.xpath('@href').get(), item.xpath('text()').get()))
        except Exception as e:
            print("Exception: %s" % (e))
        finally:
            inq.task_done()

    #print('worker[%s] starts'%(idx))
#     while True:
#         print('worker[%s] check dir - %s'%(idx, parent+'/'+idx))
#         for file in os.listdir( parent+'/'+idx ):
#             try:
#                 print('work[%s] find file - %s'%(idx, file))
#                 f = open(parent+'/'+idx+'/'+file, 'r')
#                 props = {}
#                 for line in f.readlines():
#                     if len(line.strip()) > 0 and not line.startswith('#') :
#                         pair = line.split("=")
#                         if len(pair) == 2:
#                             props[pair[0]] = pair[1].strip('\n\r\t ')
#                 
#                 html = open(props['htmlPath'], 'r')
#                 task = json.loads(props['task'])
#                 #values = parse(content=html.read())
#                 values={}
#                 values['children']=[]
#                 values['scenarioId']=task['scenarioId']
#                 values['userId']=task['userId']
#                 if task['sceType'] == 'corpus':
#                     corpus(pageno=0, pages=task['pages'], content=html.read(), parent=values)
#                 
#                 print(values)
#                 res = open('F:\\var\\data\\result', 'ab+')
#                 res.write(bytes(json.dumps(values),encoding='utf-8'))
#                 res.close()
#                 #f.close()
#                 #os.remove(parent+'/'+idx+'/'+file)
#             except Exception as e:
#                 print("worker[%s] encounter exception: %s, parent dir: %s" % (idx, e, parent))
#                 #remove exception file to log dir
#                 #shutil.move(parent+'/'+idx+'/'+file, parent+'/exception/'+file)
#             finally:
#                 if f:
#                     f.close()
#                     os.remove(parent+'/'+idx+'/'+file)
#                     
#         await gen.sleep(5)

class MainHandler(tornado.web.RequestHandler):
    
    async def post(self):
        print('reqeust incoming...%s'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        #print(self.request.body)
        #print(self.request.headers)
        #print(str(self.request.body, encoding="gb2312"))
        await inq.put(str(self.request.body, encoding="gb2312"));
        #await inq.put(self.request.body);
        #print('[%s] -- put message into queue'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.write('Gotta')
        
def Main(p_command=None):        
    print('PyCloud loaded!')
    properties = ApplicationProperties(p_command)
    #dlist = dashboard.populate() + [ (RequestMapping.submit_fetch_url_task, MainHandler)]
    application = tornado.web.Application([ (r'/sfut', MainHandler),])
    application.listen(properties.getProperty(p_key='server.port'))
    
    vols=[]
    partitiondir = properties.getProperty(p_key='application.persistence.fetchdir') + '/'  + properties.getProperty(p_key='application.persistence.defaultPartition') 
    if( os.path.exists( partitiondir ) ):
        for vol in os.listdir( partitiondir ):
            if vol.lower().startswith('volumn'):
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
    urllib3.contrib.pyopenssl.inject_into_urllib3()
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