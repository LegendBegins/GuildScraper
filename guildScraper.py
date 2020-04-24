PAGECOUNT = 217
URL = "https://www.roleplayerguild.com/topics/75056-mahzs-dev-journal/ooc?page=217#post-5113336"


import urllib.request
import re
import ast
from multiprocessing.dummy import Pool as ThreadPool		#Multithreading


outputFileName = 'RPGThreadData'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
rawURL='http://roleplayerguild.com/posts/%s/raw'
headers={'User-Agent':user_agent,} 

if URL.find('?') > 0:			#If they included the page parameters
	URL = URL[:URL.find('?')]	#Remove parameters


output = []				#The data we'll be returning
pages = [i for i in range(1, PAGECOUNT + 1)]


def loadRaw(index):
	while True:							#Repeat until request succeeds
		try:
			request = urllib.request.Request(rawURL % str(index), None, headers)
			response = urllib.request.urlopen(request, timeout = 60)
			post = response.read()
			return str(post)
		except Exception as ex:
			print('Error on post ' + str(index) + '\n' + str(ex))
			continue
	
	
def processPage(i):			#Page i
	while True:				#Reload until page is loaded properly
		try:
			list=[]
			#if(i % 50 == 0):
			print(i)
			request = urllib.request.Request(URL + '?page=' + str(i), None, headers) #The assembled request
			response = urllib.request.urlopen(request, timeout = 60)
			data = response.read()
			id = re.findall(r"<a name=\"post-\b(\d+)", str(data))		#Retrieves the IDs to check if formatting has switched yet
			#The above line can be broken if that particular regex is (albeit unlikely) fulfilled in a text post. Not sure if < is seen as &lt; by urllib or not, so it may be a nonissue
			results = []
			
			postNumbers = []
			for index in id:
				postNumbers.append(index)
			rawPool = ThreadPool(20) 
			results = (rawPool.map(loadRaw, postNumbers))
			rawPool.close()
			rawPool.join()

			posters = re.findall(r"<div class=\"user-uname\">\\n\s*<a href=\"/users/\b([\w|-]+)", str(data)) #Successfully retrieves list of users in order
			if len(posters) != 20:
				print("Only " + str(len(posters)) + ' posts on page ' + str(i))
				#Mods may have hidden a post or something else caused the post count to be off. Don't worry about it.
				
			for postnum in range(len(results)):
				list.append((results[postnum], posters[postnum], id[postnum]))
				
			#Saves data as a byte array before it saves that as a string, causing it to be preceeded by b'. Remind me to fix that ¯\_(ツ)_/¯
				
			return list
			
		except Exception as ex:
			print('Error on page ' + str(i) + '\n' + str(ex))
			continue
	
#Feel free to increase the number of threads if you want to. 10 worked fine for me.
pool = ThreadPool(10) 
output.extend(pool.map(processPage, pages))
pool.close()	#Required pool stuff
pool.join()

with open(outputFileName, 'w+') as file:
    file.write(str(output))
	
	
#print(str(len(results)) + str(len(posters)))
#To get data back: ast.literal_eval(string)
#ouput format: data[page][postOnPage][(text, poster, global post number)]
#e.g. data[1][4][0] gets the fifth post on page 2 (0-index) 
