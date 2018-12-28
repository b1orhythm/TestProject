import requests

result = requests.get('http://ip-api.com/json')
data = result.json()

def check_ip(ip):
    new_ip = ip.split('.')
    for i in new_ip:
        if int(i) < 0 or int(i) > 255: return False
    return True

def test_status():
    assert result.status_code == 200, 'Connection error!'

def test_check_country():
    country = data['country']
    assert country != 'None', 'Country not found'
    assert country != ''
    assert len(country) > 1

def test_check_city():
    city = data['city']
    assert city != 'None'
    assert city != ''
    assert len(city) > 1

def test_check_ip():
    ip = data['query']
    assert check_ip(ip)

def test_check_latLong():
    lat = data['lat']
    lon = data['lon']
    assert lat != 0
    assert lon != 0



