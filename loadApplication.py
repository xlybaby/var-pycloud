# -*- coding: utf-8 -*-
import sys,os,time,shutil,json,traceback,requests,re
from datetime import datetime
import urllib3
import urllib3.contrib.pyopenssl
import certifi

from scrapy.selector import Selector

from app.init.fileBasedConfiguration import ApplicationProperties,Logger

from flask import Flask, request, make_response
app = Flask(__name__)

ApplicationProperties.populate()
logger = Logger(module='LoadApplication', filename=ApplicationProperties.configure("application.logger.output.filename"))

def response(msg='', status=200):      
    response = make_response(msg, status)
    response.headers['Content-Type'] = 'text/json; charset=utf-8'
    return response      
                                   
@app.route('/pycloud/fetchPage', methods=['POST'])
def calc():
    try:
        if request.method == "POST":
             src=None
             body = request.json
             logger.info("fetch page: %s"%(body['url']))
             url=body['url']
             r = requests.get(url)
             selector = Selector(text=r.text)
             metaChr = selector.xpath('//meta/@charset')
             charset = 'utf-8'
             if  metaChr  :
                charset = metaChr.get()                
             else:
                metaChr = selector.xpath("//meta[contains('http-equiv','Content-Type')]/@content")
                if metaChr:
                    charsetM=re.search(r'(?<=charset=)\w+',metaChr.get().lower())
                    if charsetM:
                        charset=charsetM.group(0)
             logger.info('Page encoding charset is %s'%(charset))
             
             pattern = re.compile(r"<script.*>.*</script>|<script.*/>|<link.*[/]?>",re.I)
             prehtm = pattern.sub('',r.text)
             
             seapre = re.finditer(r'<script.*>',prehtm)
             seasuf = re.finditer(r'</script>',prehtm)
             if seapre and seasuf:
                filterIndexPair=[]  
                for match in seapre:
                    pair=[]
                    s = match.start()
                    e = match.end()
                    pair.append(s)
                    filterIndexPair.append(pair)
                for idx, match in enumerate(seasuf):
                    s = match.start()
                    e = match.end()
                    pair = filterIndexPair[idx]
                    pair.append(e)
                secondDomain = re.search(r"[A-Za-z0-9\-]+\.com|[A-Za-z0-9\-]+\.edu.cn|[A-Za-z0-9\-]+\.cn|[A-Za-z0-9\-]+\.com.cn|[A-Za-z0-9\-]+\.org|[A-Za-z0-9\-]+\.net|[A-Za-z0-9\-]+\.tv|[A-Za-z0-9\-]+\.vip|[A-Za-z0-9\-]+\.cc|[A-Za-z0-9\-]+\.gov.cn|[A-Za-z0-9\-]+\.gov|[A-Za-z0-9\-]+\.edu|[A-Za-z0-9\-]+\.biz|[A-Za-z0-9\-]+\.net.cn|[A-Za-z0-9\-]+\.org.cn",url.lower()).group()
                path = ApplicationProperties.configure("application.storage.filesystem.download.staticdir")+'/'+secondDomain
                if not os.path.exists(path):
                    os.mkdir(path)
                filename=datetime.now().strftime('%Y%m%d%H%M%S')+'.html'
                fp = open(path+"/"+filename, 'w+', encoding=charset)
                s=0
                for item in filterIndexPair:
                    e=item[0]-1
                    fp.write(prehtm[s:e])
                    s=item[1]+1
                fp.write(prehtm[s:])
                fp.close()
                src = secondDomain+"/"+filename
             logger.info(body['url'])
             result = {"retMsg":"OK","retData":{"src":src}}
             return response(json.dumps(result))
    except Exception as e:
        logger.error(e)
        msg = traceback.format_exc()
        logger.error(msg)
        return response({'retMsg':'error: %s'%(e)}, 500)
          
if __name__ == '__main__':
    logger.info("Application listening %s"%(ApplicationProperties.configure("server.port")))
    app.run('0.0.0.0',ApplicationProperties.configure("server.port"))