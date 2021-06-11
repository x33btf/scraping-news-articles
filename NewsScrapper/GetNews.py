from bs4 import BeautifulSoup
from lxml import etree
import requests
import yaml
import pymongo
import time

""" 
	---------------------------------- Config File ----------------------------
	site:title:desc:date:author:img:content:minUrlLent
	----------------------------------   database  ----------------------------

	"site" : website url

	"title" :  news titl
			 
	"desc" : news description
			
	"date" : news creation date 

	"author" : news author
			
	"img"  : news principal image

	"content" : news content

	"category" : new category to add when classification is done

"""

class Article():
	
	def __init__(self, site, title, author, desc, content, date, img):
		
		self.site = site
		
		self.title = title
		
		self.author = author
		
		self.desc = desc
		
		self.content = content
		
		self.date = date
		
		self.img = img
		"""--------------------------------------------------------------"""
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		
		self.mydb = self.myclient["NewsDB"]
		
		self.mycol = self.mydb["News"]
		"""--------------------------------------------------------------"""
		self.debug = True


	def printArticle(self):
		
		print("------------------------------------------------------------------")
		
		print("site : ",self.site)
		
		print("title : ",self.title)
		
		print("author : ",self.author)
		
		print("date : ",self.date)
		
		print("desc : ",self.desc)
		
		print("img : ",self.img)
		
		print("content : ",self.content)
		
		print("------------------------------------------------------------------")


	def saveArticle(self):

		Art = {

			"site" : self.site, 

			"title" : self.title, 
			
			"desc" : self.desc,
			
			"date" : self.date,

			"author" : self.author,
			
			"img" : self.img,

			"content" : self.content,

			"category" : ""

			}
		
		myquery = { "title": self.title }
		
		result = self.mycol.find(myquery)

		for x in result:
			
			if self.debug:
				
				print("News already in database")
		
			return -1

		if self.debug:

			print("News added to database")
		
		self.mycol.insert_one(Art)


	def showAllNews(self):
		
		for x in self.mycol.find({},{ "_id": 1, "title": 1}):
			
			print(x) 


class GetNews():
	

	def __init__(self):
		
		self.config = dict()
		
		self.cookies = {
		    'ak-inject-mpulse': 'false',
		    'didomi_token': 'eyJ1c2VyX2lkIjoiMTc5YjMwZTUtZTlkNS02MjJiLWI1NjAtNjQyMDk4N2NmZWZkIiwiY3JlYXRlZCI6IjIwMjEtMDUtMjhUMTI6NTg6NTcuNDI1WiIsInVwZGF0ZWQiOiIyMDIxLTA1LTI4VDEyOjU4OjU3LjQyNVoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbInR3aXR0ZXIiLCJnb29nbGUiLCJmYWNlYm9vayIsImM6dmRvcGlhIiwiYzp3b29iaSIsImM6ZGlkb21pIiwiYzphZHZlcnRpc2luZ2NvbSIsImM6a3J1eC1kaWdpdGFsIiwiYzp5b3V0dWJlIiwiYzppbnN0YWdyYW0iLCJjOnlhbmRleG1ldHJpY3MiLCJjOmNoYXJ0YmVhdCIsImM6bmV3LXJlbGljIiwiYzpxdWFudHVtLWFkdmVydGlzaW5nIiwiYzpwaW5nZG9tIiwiYzphdWRpZW5jZS1zcXVhcmUiLCJjOmxrcWQiLCJjOnNvYXN0YS1tcHVsc2UiLCJjOmxpdmVpbnRlcm5ldCIsImM6bWFpbHJ1LWdyb3VwIiwiYzpiYXRjaCJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==',
		    'euconsent-v2': 'CPG6RquPG6RquAHABBENBbCgAAAAAAAAAAqIAAAAAAEkoHgACAAFgAUAAyABwAEUAMAAxAB4AEQAJgAVQAuABfADEAGYANoAhABDQCIAIkARwAowBSgC3AGEAMoAaoA2QB3gD8AIwARwAp4BV4C0ALSAXUAxQBuADqAHyAQ6AioBF4CRAE2ALFAWwAu0BeYDDwGRAMnAZYAzkBngDPgGkANYAcAA6wB2oaBQAFYALgAhgBkADLAGoANkAdgA_ACAAEFAIwAUsAp4BV4C0ALSAawA3gB1QD5AIbAQ6AioBF4CRAE2AJ2AUiAuQBgQDCQGHgMYAZOAzkBngDPgHJAOUAdYKgPgAUACGAEwALgAjgBlgDUAHYAPwAjABHAClgFXgLQAtIBvAEggJiATYApsBbAC5AF5gMCAYeAyIBnIDPAGfANyAckA5QpBTAAXABQAFQAMgAcgA-AEAAIoAYABlADQANQAeQBDAEUAJgATwApABVACwAFwAL4AYgAzABzAEIAIaARABEgCjAFKALEAW4AwgBlADRAGqANkAd8A-wD9AIsARgAjgBKQCggFDAKuAVsAuYBeQDFAG0ANwAegBDoCLwEiAJOATYAnYBQ4CtgFigLQAWwAuABcgC7QF5gMNAYeAxgBkQDJAGTgMuAZyAzwBn0DSANJgawBrIDYwG6wOTA5QBy4DrAHagPHAfKOg6gALgAoACoAGQAOQAfACAAEQALoAYABlADQANQAeAA-gCGAIoATAAnwBVAFYALEAXABdAC-AGIAMwAbwA5gB6AEIAIaARABEgCOgEsATAAmgBRgClAFiALeAYQBhgDIAGUANEAagA2QBvgDvAHtAPsA_QB_gEDgIsAjABHICUgJUAUEAp4BVwCxQFoAWkAuYBdQC8gF-AMUAbQA3ABxIDpgOoAegBDYCHQERAIqAReAkEBIgCVAEyAJsATsAocBTQCrAFigLQgWwBbIC4AFyALtAXeAvMBgwDCQGGgMPAYkAxgBjwDJAGTgMqAZYAy4BnIDPgGiQNIA0kBpYDTgGqgNYAbGA3UBxcDkgOVAcuA6MB1gDxwHpAPVAfKA-shBDAAWABQADIAIgAXAAxACGAEwAKoAXAAvgBiADMAG8APQAjgBYgDCAGUANQAb4A74B9gH4AP8AjABHACUgFBAKGAU8Aq8BaAFpALmAX4AxQBtADqAHoASCAkQBJwCVAE2AKaAWKAtGBbAFtALgAXIAu0Bh4DEgGRAMnAZyAzwBnwDRAGkgNLAaqA4AByQDowHWAO1AeOEgvgAIAAXABQAFQAMgAcgA8AEAAIgAYAAygBoAGoAPIAhgCKAEwAJ8AVQBWACwAFwAN4AcwA9ACEAENAIgAiQBHQCWAJcATQApQBbgDDAGQAMuAagBqgDZAHeAPYAfEA-wD9AIAAQOAi4CMAEaAI4ASkAoIBSwCngFXALmAX4AxQBrADaAG4AN4AcQA9AB8gENgIdAReAkQBMQCZQE2AJ2AUOApEBTQCxQFoALYAXIAu8BeYDAgGDAMJAYaAw8BkQDJAGTgMuAZyAz4BpADToGsAayA3WByIHKgOXAdGA6wB44D5RECIAKwAXABDADIAGWANQAbIA7AB-AEAAIwAUsAp4BVwDWAHVAPkAhsBDoCLwEiAJsATsApEBcgDAgGEgMPAZOAzkBnwDkgHKAOsGQHgAKABDACYAFwARwAywBqADsgH2AfgBGACOAFLAKuAVsA3gCTgExAJsAWiAtgBeYDAgGHgMiAZyAzwBnwDkgHKAPiAA.YAAAAAAAAAAA',
		    'atuserid': '%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22da8cbe86-1316-49e1-bbfd-298d71252be9%22%2C%22options%22%3A%7B%22end%22%3A%222022-06-29T12%3A59%3A01.042Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
		    'atauthority': '%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222022-06-29T12%3A59%3A01.043Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
			}

		self.headers = {
		    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
		    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		    'Accept-Language': 'en-US,en;q=0.5',
		    'Connection': 'keep-alive',
		    'Upgrade-Insecure-Requests': '1',
			}

		self.configFileName = "config.yaml"

		self.webSiteLinks = []

		self.articles = []

		self.debug = False

		self.run()


	def LoadConfig(self):

		if self.debug:
			
			print("Loading Config ...")

		dt = ""
		
		with open(self.configFileName) as f:
		
			dt = yaml.load(f, Loader=yaml.FullLoader)

		for line in dt:
			
			data = dict()
			
			data["titleXpath"] = dt[line][1-1]
			
			data["descXpath"] = dt[line][2-1]
			
			data["dateXpath"] = dt[line][3-1]

			data["authorXpath"] = dt[line][4-1]
			
			data["imgXpath"] = dt[line][5-1]

			data["contentXpath"] = dt[line][6-1]

			data["minLenLink"] = dt[line][7-1]
			
			
			self.config[line] = data

		if self.debug:
			
			for config in self.config:
			
				print(config+" : ",self.config[config])


	def getAllLinkFromHomePage(self):

		for site in self.config:

			webpage = requests.get("https://"+site, headers=self.headers, cookies=self.cookies)
			
			soup = BeautifulSoup(webpage.content, "html.parser")
			
			links = soup.find_all('a',href=True)
			
			for link in links:
			
				href = link['href']
			
				if href != "#" and len(href) > int(self.config[site]["minLenLink"]):

					if "https" not in href:
			
						href = "https://"+site+href
			
					else:
			
						if site not in href:
			
							continue
					
					self.webSiteLinks.append(href)

		if self.debug:

			print("found :",len(self.webSiteLinks),"News")


	def getAllNewNewsFromLink(self):

		for link in self.webSiteLinks:

			try:

				webpage = requests.get(link, headers=self.headers, cookies=self.cookies)
					
				soup = BeautifulSoup(webpage.content, "html.parser")
					
				dom = etree.HTML(str(soup))

				title=""

				author=""

				desc=""

				content=""

				date=""

				img=""

				try:

					title = dom.xpath(self.config[link.split("/")[2]]["titleXpath"])[0].text.strip()

				except Exception as e:

					if self.debug:

						print(e)

				try:

					desc = dom.xpath(self.config[link.split("/")[2]]["descXpath"])[0].text.strip()

				except Exception as e:

					if self.debug:

						print(e)

				try:			

					date = dom.xpath(self.config[link.split("/")[2]]["dateXpath"])[0].text.strip()	

				except Exception as e:

					if self.debug:

						print(e)

				try:

					author = dom.xpath(self.config[link.split("/")[2]]["authorXpath"])[0].text.strip()	

				except Exception as e:

					if self.debug:

						print(e)

				try:

					img = dom.xpath(self.config[link.split("/")[2]]["imgXpath"])[0]

				except Exception as e:

					if self.debug:

						print(e)

				try:

					html = etree.tostring(dom.xpath(self.config[link.split("/")[2]]["contentXpath"])[0])

					soup = BeautifulSoup(html, "html.parser")

					content = soup.text

					content = " ".join(content.split())
						
					content = content.replace("app google-play-badge_EN","")

					content = content.replace("Advertising Read more","")

				except Exception as e:

					if self.debug:

						print(e)

				ar = Article(link.split("/")[2],title,author,desc,content,date,img)
					
				ar.saveArticle()

				#self.articles.append(ar)

				#print(ar.printArticle())

			except Exception as e:

				if self.debug:

					print(e)


	def main(self):
		
		self.LoadConfig()
		
		self.getAllLinkFromHomePage()
		
		self.getAllNewNewsFromLink()

	#run this scipt every timeToRun second
	def run(self,timeToRun=3600):

		self.main()

		while True:

			startTime = time.time()

			while time.time() - startTime < timeToRun:

				time.sleep(1)

			self.main()


GetNews()