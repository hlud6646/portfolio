import bs4, urllib.request

def sydney():
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	url = "https://m.weatherzone.com.au/nsw/sydney/sydney"
	req = urllib.request.Request(url, headers=headers)
	raw = urllib.request.urlopen(req).read() 
	soup= bs4.BeautifulSoup(raw, 'html.parser')

	temp = float(soup('div', id='today_now')[0].text[3:-2])

	return temp

if __name__ == '__main__':
	print(sydney())