from browsermobproxy import Server
from selenium import webdriver
import json,re
from tld import get_tld

class Traffic:
	# Constructor with/without url as argumnet
	def __init__(self,*args):
		if(len(args)>1):
			raise TypeError("Expected at most one argument")
		elif(len(args)==1):
			self.__url=args[0]
		else:
			self.__url=None
		self.__server=None
		self.__proxy=None
		self.__driver=None

	#Starts the proxy server and returns it
	def __init_proxy_server(self):
		server= Server("dependencies\\browsermob-proxy\\bin\\browsermob-proxy")#The argument is path to browsermob proxy
		server.start()
		return server

	#Creates a proxy
	def __init_proxy(self):
		proxy=self.__server.create_proxy(params={"trustAllServers":"true"})
		return proxy

	#Configures the web driver and returns it
	def __configure_driver(self):
		options=webdriver.ChromeOptions()
		options.add_argument("--proxy-server={}".format(self.__proxy.proxy))
		#configues the web driver by giving the chromedriver's path and the proxy and chromeoptions
		driver = webdriver.Chrome(executable_path = "dependencies\\chromedriver\\chromedriver", options=options)
		return driver

	#Filters the captured data
	def __filter_data(self,data):
		domain=get_tld(self.__url,as_object=True).fld # Parses the domain name from the given url
		pattern='image|font|css|html|javascript' # Declares a pattern
		entries=data['log']['entries'] # Gets all the entries from the captured data
		length=len(entries)
		filtered_data=[] #Stores the filtered data
		for i in range(length):
			request=entries[i]['request'] # Stores the request details of an entry
			response=entries[i]['response'] # Stores the response details of an entry
			contentType=response['content']['mimeType'] # Stores the response content type
			type=contentType.split(';')[0].split('/') # Splits the content type by ';' and then splits the first value by '/'
													  # eg. application/json;char-utf8 -> application/json,char-utf8 -> application,json
			url=request['url'] # Stores the request url

			if(len(type)==1 or bool(re.search(pattern, type[1])) or bool(re.search(pattern, type[0]))): # If any values of type matches with pattern then the request is filtered out
				continue
			headers=request['headers'] # Stores the headers of the request
			flag=True
			for header in headers:
				# The requests with 'navigate' as 'Sec-Fetch-Mode' are filtered out
				if(header['name']=='Sec-Fetch-Mode' and header['value']=='navigate'):
					flag=False
					break
				# The requests with 'font'/'style'/'script'/'image' as 'Sec-Fetch-Dest' are filtered out
				if(header['name']=='Sec-Fetch-Dest' and (header['value']=='font' or header['value']=='style' or header['value']=='script'\
					or header['value']=='image')):
					flag=False
					break
				# The requests that don't have the domain as substring of host name are filtered out
				if(header['name']=='Host' and not bool(re.search(domain,header['value']))):
					flag=False
					break
			if(not flag):
				continue
			filtered_data.append({'request':request,'response':response}) # The required request-response pair is stored
		return filtered_data

	# Opens the web page in chrome browser, url can be given as argument, only one argument allowed
	def open_page(self,*args):
		if(len(args)>1):
			raise TypeError("Expected at most one argument")
		elif(len(args)==1):
			self.__url=args[0]
		if(self.__url==None):
			raise ValueError("No url given")
		self.__server=self.__init_proxy_server()
		self.__proxy=self.__init_proxy()
		self.__driver=self.__configure_driver()
		try:
			self.__proxy.new_har("req",options={'captureHeaders': True,'captureContent':True, 'captureBinaryContent': True}) # Defines what data should be captured
			self.__driver.get(self.__url) # Opens the url
			return True,'Okay'
		except Exception as e:
			return False,("Exception: {}".format(e))

	#Captures the data and returns it
	def get_data(self):
		try:
			data=self.__proxy.har # Captures the data
			self.__driver.quit()
			self.__server.stop()
			return True,self.__filter_data(data) # Returns a flag which is true if everything goes well and the filtered data
		except Exception as e:
			return False,("Exception: {}".format(e)) # Returns a flag which is false and the exception message
	
	def close(self):
		try:
			self.__driver.quit()
			self.__server.stop()
		except:
			pass

if __name__ == '__main__':
	pass
