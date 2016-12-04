#!/usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import re
import thread
import time


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except utllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect to qsbk fail, the reason of error: ", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u"get the page fail..."
            return None
        pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search("img", item[1])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                text = text.replace("<span>", "")
                text = text.replace("</span>", "")
                pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1])

    def start(self):
        print "geting stories from qsbs,press enter to view the new story, Q quit"
        self.enable = True
        self.loadPage()
        newPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                newPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, newPage)

splider = QSBK()
splider.start()

