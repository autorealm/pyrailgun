#    coding: UTF-8
#    User: princehaku
#    Date: 13-2-12
#    Time: 1:01
#
__author__ = 'haku'
from pyrailgun import RailGun
import os, sys, re, json, time
import urllib
import urllib2
import requests
import logging

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()

console = logging.FileHandler("bangumi.log")
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
console.setFormatter(formatter)
railgun.logger.addHandler(console)
railgun.setTask(file("bangumi.json"))
railgun.fire();
nodes = railgun.getShells()
file = file("bangumi.demo.txt", "w+")


def request_connnect(post, n=0):
	try:
		response = requests.Session().post(
			'http://localhost/dev/api/bgm.php',
			data=post,
			headers={'Connection':'close',\
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'},
			timeout=30
		)
		response.encoding = "UTF-8"
		print (response.text).encode('utf-8')
	except Exception, e:
		print e
		n = n + 1
		if n < 6:
			print '-- try request again... ' + str(n)
			time.sleep(10 + n)
			request_connnect(post, n)
		else:
			print '(!) request failed.'
		pass

m = 0
for id in nodes:
	node = nodes[id]
	m = m + 1
	if node.get('title') == None:
		continue
	n = 0
	for title in node.get('title', [""]):
		data = {}
		title = node.get('title')[n]
		
		tags = []
		if None != node.get('tags')[n]:
			tags = list(set(node.get('tags')[n]))
			if '' in tags:
				tags.remove('')
			if None in tags:
				tags.remove(None)
			
		title1 = node.get('title1') != None and node.get('title1')[n] or None
		image1 = node.get('image1') != None and node.get('image1')[n] or None
		info1 = node.get('info1') != None and node.get('info1')[n] or None
		info = node.get('info') != None and node.get('info')[n] or None
		desc = node.get('desc') != None and node.get('desc')[n] or ''
		src = node.get('src') != None and ('http://bangumi.tv' + str(node.get('src')[n])) or None
		image = node.get('image') != None and ('http:' + str(node.get('image')[n])) or None
		tracks = node.get('tracks') != None and node.get('tracks')[n] or None
		
		users = []
		_user = node.get('user_name') != None and node.get('user_name')[n] or None
		if None != _user:
			user_name = node.get('user_name') != None and node.get('user_name')[n] or None
			user_avatar = node.get('user_avatar') != None and node.get('user_avatar')[n] or None
			user_link = node.get('user_link') != None and node.get('user_link')[n] or None
			for i in range(0, len(_user)):
				user = {}
				user['link'] = user_link[i]
				user['name'] = user_name[i]
				user['avatar'] = 'http:' + str(user_avatar[i])
				users.append(user)

			
		n = n + 1
		
		data['title'] = title
		data['title_s'] = title1
		data['src'] = src
		data['image'] = image
		data['tags'] = tags
		data['info_s'] = info1
		data['info'] = info
		data['desc'] = desc
		data['tracks'] = tracks
		data['users'] = users
		
		file.write(title.encode('utf-8', 'ignore') + "\r\n")
		file.write(json.dumps(data, ensure_ascii=False) + "\r\n=================== " + str(m) + "-" + str(n) + " =================\r\n")
	
	if False:
		post = {}
		post['title'] = title
		post['title_s'] = title1
		post['data'] = json.dumps(data, ensure_ascii=False)
		post['desc'] = desc
		post['src'] = src
		post['image'] = image
		post['tags'] = (',').join(tags)
		post['info_s'] = info1
		post['info'] = json.dumps(info, ensure_ascii=False)
		post['tracks'] = json.dumps(tracks, ensure_ascii=False)
		post['users'] = json.dumps(users, ensure_ascii=False)
		
		try:
			req = urllib2.Request(
				url = 'http://localhost/dev/api/bgm.php',
				data = urllib.urlencode(post),
				headers = {'Connection':'keep-alive',\
					'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'},
				)
			f = urllib2.urlopen(req)
			c = f.read()
			#c = unicode(f.read(), 'utf-8')
			print (c).encode('utf-8')
			#f.close()
		except Exception, e:
			print e
			print '-- try request again...'
			time.sleep(5);
			request_connnect(post)
			pass
		finally:
			print str(m) + ' - ' + str(n) + ' : completed'
		
		time.sleep(1);
	

def image_download(url, image_name):
	cureent_dir = os.path.dirname(os.path.abspath(__file__))
	urllib.urlretrieve(url, cureent_dir + "/data/" + image_name)
