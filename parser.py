from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

def give_url():
	for i in range(1, 46):
		yield "https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998%2C996&special_categories=&filter=topsellers&page={}".format(i)

def parse(page):
	page_soup = soup(page, "html.parser")
	containers = page_soup.findAll("a" , {"class" : "search_result_row"})
	
	for container in containers:
		name = container.find("span", {"class" : "title"}).text
		slug = container["href"]
		if container.find("div", {"class" , "search_price"}).find("strike"):
			steam_price = container.find("div", {"class" , "search_price"}).span.strike.text.strip()
		else:
			steam_price = container.find("div", {"class" , "search_price"}).text.strip()

		yield (name, slug, steam_price)

for url in give_url():
	client = urlopen(url)
	page_html = client.read()
	client.close()
	
	# here must be write to db code instead of print calls
	for name, slug, steam_price in parse(page_html):
		print("name : " + name)
		print("href : " + slug)
		print("price : " + steam_price)
		print()


