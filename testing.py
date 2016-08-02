# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 09:04:51 2016

@author: gizzle
"""
import cv2
import decoder

import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re
import time
import sys 

reload(sys)  

def postData(posturl,headers,postData):
	postData = urllib.urlencode(postData)  #Post数据编码   
	request = urllib2.Request(posturl, postData, headers)#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
	try:	
		response = urllib2.urlopen(request, timeout = 20)
		text = response.read().decode('utf-8')
	except:
		text = ""
	return text
				
def getData(geturl,header,getData):
    getData = urllib.urlencode(getData)
    request = urllib2.Request(geturl, getData, header)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8') 
    return text

if __name__ == "__main__":
	# 这个测试方法仅在选课不开放时段有效
	# 若需要在选课开放时测试，请加入判断是否登陆成功的语句
	userID = raw_input("enter the userid: ")
	password = raw_input("enter the password: ")
	testRange = 100  #how many test cases you want
	cj = cookielib.LWPCookieJar()
	cookie_support = urllib2.HTTPCookieProcessor(cj)
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
	 
	posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
	header = {   
		'Host' : 'xk.urp.seu.edu.cn',   
		'Proxy-Connection' : 'keep-alive',
		'Origin' : 'http://xk.urp.seu.edu.cn',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
		'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
		}

	success = 0
	failure = 0
	mismatch = 0

	status = True
	try:
		h = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/system/showLogin.action', timeout = 10)
	except:
		print "urlopen failed"
		status = False			
	for i in range(testRange):
		if status == True:			
			print i
			try:
				image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode', timeout = 10)
			except:
				print 'image open timeout'
				raw_input('input any value to continue')
			try:
				f = open('code.jpg', 'wb')
				f.write(image.read())
				f.close()
			except:
				print 'file operation error'
#				raw_input('input any value to continue')
				continue
			img = cv2.imread('code.jpg', 0)
			
			try:
				(code, img) = decoder.imageToString(img)
				print code
			except:
				code = ""
			if len(code) == 4:
#				cv2.imwrite('codes\\%d_%s.bmp' % (i,code), img)
				data = {
					'userId' : userID,
					'userPassword' : password, #你的密码，  
					'checkCode' : code,           #验证码 
					'x' : '33',
					'y' : '5'
				}
				try:
					text = postData(posturl, header, data)
					text = text.encode('utf-8')
					if(text.find('验证码错误') != -1):
						mismatch += 1
#							cv2.imwrite('codes\\dismatch_%d_%s.bmp' % (i,code), img)
						print 'mismatch'
					elif(text.find('尚未开放') != -1):
						success += 1
						print 'success'
					elif(text.find('密码错误') != -1):
						status = False
						print 'incorrect userid or password'
#						raw_input('wrong username/password')
					else: 
						print 'unknown error'
						failure += 1
#						raw_input()
				except:
					print 'error'
					failure += 1
			else:
#					cv2.imwrite('codes\\fail_%d.bmp' % i, img)
				print 'cant recognize'
				failure += 1
	
	print 'success: %d' % success
	print 'failure: %d' % failure
	print 'mismatch: %d' % mismatch