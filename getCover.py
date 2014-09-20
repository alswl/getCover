#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @base author: mingcheng http://www.gracecode.com/# @site
# @create: 2010-01-22
# @update author: alswl http://log4d.com
# @update: 2011-08-26

import eyeD3, re, os, sys, time, urllib2
import hashlib

urlread = lambda url: urllib2.urlopen(url).read()

def urlreadpic(url):
    """通过url读取豆瓣图片，如果404则换一台图片服务器"""
    n = 5
    cover = False
    while n > 0:
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            cover = opener.open(url).read()
            return cover
        except Exception, e:
            print '%s [被block]' %url
            #print e
            img_static  = re.findall('img(\d)', url)[0]
            img_static_2 = (int(img_static) + 1) % n + 1
            url = url.replace('img' + img_static,
                    'img' + str(img_static_2))
            n -= 1
            time.sleep(3) # 间隔 3s ，防止被豆瓣 Block
            continue
    return cover

class getAlbumCover:
    '''从豆瓣获取专辑封面数据，并写入对应的 mp3 文件'''

    _eyeD3 = None

    # 豆瓣搜索以及专辑封面相关的 API 和格式
    _doubanSearchApi    = 'http://music.douban.com/subject_search?search_text={0}&cat=1003'
    _doubanCoverPattern = '<img src="http://img(\d).douban.com/spic/s(\d+).jpg"'
    _doubanConverAddr   = 'http://img{0}.douban.com/lpic/s{1}.jpg'
    
    artist = '' # 演唱者
    album  = '' # 专辑名称
    title  = '' # 歌曲标题

    def __init__(self, mp3):
        self._eyeD3 = eyeD3.Tag()
        # file exists or readable?
        try:
            self._eyeD3.link(mp3)
            self.getFileInfo()
        except:
            print '读取文件错误'

    def updateCover(self, cover_file):
        '''更新专辑封面至文件'''
        try:
            self._eyeD3.removeImages()
            # cover exists or readable?
            #self._eyeD3.removeLyrics()
            #self._eyeD3.removeComments()
            self._eyeD3.addImage(3, cover_file, u'')
            self._eyeD3.update()
            return True
        except:
            print '修改文件错误'
            return False

    def getFileInfo(self):
        ''' 获取专辑信息 '''
        self.artist = self._eyeD3.getArtist().encode('utf-8')
        self.album  = self._eyeD3.getAlbum().encode('utf-8')
        self.title  = self._eyeD3.getTitle().encode('utf-8')

    def getCoverAddrFromDouban(self, keywords = ''):
        ''' 从豆瓣获取专辑封面的 URL '''
        if not len(keywords):
            keywords = self.artist + ' ' + (self.album or self.title)

        request = self._doubanSearchApi.format(urllib2.quote(keywords))
        result  = urlread(request)
        if not len(result):
            return False

        match = re.compile(self._doubanCoverPattern, re.IGNORECASE).search(result)
        if match:
            g_img = 's' + match.groups()[1]
            return self._doubanConverAddr.format(match.groups()[0],
                    match.groups()[1])
        else:
            return False

if __name__ == "__main__":
    if not os.path.exists('cover'):
        os.mkdir('cover')
    for i in sys.argv:
        if re.search('.mp3$', i):
            print '正在处理:', i,
            handler = getAlbumCover(i)
            if handler.artist and (handler.album or handler.title):
                #print '[内容]', handler.artist, handler.title,
                cover_addr = handler.getCoverAddrFromDouban()
                if cover_addr:
                    cover_file = './cover/cover_%s.jpg' \
                            %hashlib.md5(cover_addr).hexdigest()
                    if os.path.isfile(cover_file):
                        print '[已有cover]'
                        continue

                    cover = urlreadpic(cover_addr)
                    if not cover:
                        print '[重试后失败]'
                        continue
                    f = file(cover_file, 'w')
                    f.write(cover)
                    f.close()
                    if handler.updateCover(cover_file):
                        print '[完成]'
                    else:
                        print '[失败]'
                    #os.remove(cover_file)
                else:
                    print '[失败]'
            else:
                print '[没有idv3]'
            handler = None
            #time.sleep(3) # 间隔 3s ，防止被豆瓣 Block

# vim: set et sw=4 ts=4 sts=4 fdm=marker ff=unix fenc=utf8 nobomb ft=python:
