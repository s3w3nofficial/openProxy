import socketIO_client
import sys, socket, urllib2

def doCheck(ip):	
	try:
		proxy_handler = urllib2.ProxyHandler({'http': ip})
		opener = urllib2.build_opener(proxy_handler)
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib2.install_opener(opener)
		req=urllib2.Request('http://www.google.com')  # change the URL to test here
		sock=urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print 'Error code: ', e.code
		return e.code
	except Exception, detail:
		print "ERROR:", detail
		return False
	return True

class WikiNamespace(socketIO_client.BaseNamespace):
	def on_change(self, change):
		ip = True
		for s in change['user'].split('.'):
			try:
				int(s)
			except:
				ip = False
				break
		if ip:
				print change['user']
				for i in range(20): 
					if doCheck(change['user'] + ':80'):
						print change['user'] + "after testing"
						break

	def on_connect(self):
		self.emit('subscribe', 'cs.wikipedia.org')

socketIO = socketIO_client.SocketIO('https://stream.wikimedia.org')
socketIO.define(WikiNamespace, '/rc')

socketIO.wait()
