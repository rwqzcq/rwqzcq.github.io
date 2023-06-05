import requests
import random

def get_proxy():
	url = 'https://dps.kdlapi.com/api/getdps/?orderid=982754533918498&num=10&pt=1&format=json&sep=1'
	url = 'https://dps.kdlapi.com/api/getdps/?orderid=932761201975752&num=3&pt=1&format=json&sep=1'
	data = requests.get(url).json()
	proxy_list = data['data']['proxy_list']
	proxy = random.choice(proxy_list)
	proxy = {'http': proxy, 'https': proxy}
	return proxy
