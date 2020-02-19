import bs4, urllib.request

def sydney():
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	url = "http://www.bom.gov.au"
	req = urllib.request.Request(url, headers=headers)
	raw = urllib.request.urlopen(req).read() 
	soup= bs4.BeautifulSoup(raw, 'html.parser')


	caps = soup('div', 'capital')
	syd  = [x for x in caps if x('h3')[0].text == 'Sydney'][0]
	temp = float(syd('p', 'now')[0]('span', 'val')[0].text[:-1])
	
	return temp

if __name__ == '__main__':
	print(sydney())