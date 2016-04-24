# coding=utf-8
import urllib, urllib2
import re
import os
import datetime
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
def getAll(baseurl,basedir,starttime):
    html = getHtml(baseurl)
    reg = r'<a href="([^\"]+)"'
    href_re = re.compile(reg)
    href_list = re.findall(href_re,html)
    x = 0
    for href_url in href_list:
        if not href_url.startswith("?") and not href_url.endswith("2007/"):
            print href_url
            #url end with / which is a dir,here we create a dir in local path,and download all files recursively
            if href_url.endswith("/"):
                dir_path=basedir+os.sep+href_url
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                url = baseurl + href_url
                getAll(url,dir_path,starttime)
            else:
                data_path = basedir + os.sep+href_url
                url = baseurl+ href_url
                f = urllib2.urlopen(url)
                x += 1
                meta = f.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                file_size_dl = 0
                block_sz = 8192
                file_local = open(data_path, 'wb')
                now_percent_i=1
                while True:
                    buffer = f.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    file_local.write(buffer)
                    if file_size_dl/float(file_size) > now_percent_i/10.0:
                        endtime = datetime.datetime.now()
                        interval = (endtime - starttime).seconds
                        print "now %d,time collapese:%d s, downloading %s: %f percent" % (x,interval, url, (file_size_dl/float(file_size))*100)
                        now_percent_i=now_percent_i+1
                file_local.close()

if __name__ == '__main__':
    baseurl = "http://www.fon.hum.uva.nl/david/ma_ssp/2007/TIMIT/"
    local_data_dir = os.path.abspath('../data')
    starttime = datetime.datetime.now()
    getAll(baseurl,local_data_dir,starttime)
