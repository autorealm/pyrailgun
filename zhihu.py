#    coding: UTF-8
#    User: princehaku
#    Date: 13-2-12
#    Time: 1:01
#
__author__ = 'haku'
from pyrailgun import RailGun
import sys, re, json

reload(sys)
sys.setdefaultencoding("utf-8")

railgun = RailGun()

railgun.setTask(file("zhihu.json"))
railgun.fire();
nodes = railgun.getShells()
file = file("zhihu.txt", "w+")


for id in nodes:
	node = nodes[id]
	n = 0
	for title in node.get('title', [""]):
		file.write(title+ "\r\n")
		file.write(node.get('desc', [""])[n] + "\r\n" + "\r\n====================================\r\n")
		n = n + 1
	if node.get('title') == None:
		continue
	



from sgmllib import SGMLParser

class parserXml(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.links = {}
		self.srcs= []
		#������Ƶ����
		self.hrefs=[]
	#��ȡ������hrefֵ
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == "href"]
		self.href = href
		self.is_a=1
	def end_a(self):
		self.is_a=0
	def handle_data(self, text):
		if self.is_a:
			self.links[text] = self.href
	#��ȡͼƬ������hrefֵ
	def start_img(self, attrs):
		src = [v for k, v in attrs if k == "src"]
		self.srcs.extend(src)
	#��ȡ��Ƶ������hrefֵ
	def start_embed(self,attrs):
		href=[v for k, v in attrs if k=="href"]
		self.hrefs.extend(href)
