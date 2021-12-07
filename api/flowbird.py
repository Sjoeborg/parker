import requests
import time
def get_cookie():
    url = "https://betalap.flowbirdapp.com/customer/get"

    querystring = {"id":"1","withAccountCompletion":"yes","version":" 2.8.0 1103"}

    payload = "server=.apachen1"
    headers = {
        "cookie": "server=.apachen1",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    try:
        headers['cookie'] += f'; PHPSESSID={response.cookies.get_dict()["PHPSESSID"]}'
        #headers['PHPSESSID'] = response.cookies.get_dict()["PHPSESSID"]
        return headers
    except:
        print(response.status_code, response.text)

def get_user_session(user,password,headers):

    url = "https://betalap.flowbirdapp.com/customer/login/"

    payload = {'username': user,
    'countryCode':'undefined',
    'password': password,
    'rememberMe':'false',
    'rt':time.time()}

    response = requests.request("POST", url, data=payload, headers=headers)

    try:
        user_token = response.cookies.get_dict()["user"]
        headers['user'] = user_token
        headers['cookie'] += f'; user={user_token}'
        return headers
    except:
        print(response.status_code, response.text)

def create_order(order_dict,headers):
    url = "https://betalap.flowbirdapp.com/order/create"

    querystring = {"platform":"europe","rt":time.time(),"version":"2.8.0 1103"}

    payload = {
        "preferredLanguage": "en",
        "author": order_dict['username'],
        "channel": "web",
        "pos": "http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PoS/v1/30945868/",
        "posLabel": "Taxa 5",
        "vehicle": order_dict['vehicle'],
        "platform": "europe",
        "class": "hourly",
        "startTime": order_dict['start_time'],
        "duration": order_dict['duration'],
        "freeDuration": "PT0S",
        "paidDuration": "PT12M",
        "usertype": "1",
        "usertypeLabel": "Visitor Parking",
        "space": None,
        "type": "user",
        "geo": {
            "latitude": order_dict['lat'],
            "longitude": order_dict['long']
        }
    }
    response = requests.request("GET", url, json=payload, headers=headers, params=querystring)
    try:
        confirm_url = response.json()['response']['customer'] #URL to see order
        return confirm_url
    except:
        print(response.status_code, response.text)
    
def login(username,password):
    headers = get_cookie()
    headers = get_user_session(username, password, headers)
    return headers

def buy(username,start_time,headers):
    
    lat = 59.3307
    long = 18.0718
    order_dict = {'username':username,'lat': lat, 'long': long, 'start_time': start_time, 'duration': 'P1DT11H49M29S', 'vehicle': {
                "id": 884376,
                "plate": "GFD578",
                "default": True,
                "category": "car",
                "country-plate": "SE",
                "isExternalTicketNotification": False
            }}
    order_url = create_order(order_dict,headers)
    return order_url

def login_and_buy(username,password,start_time):
    headers = login(username,password)
    order_url = buy(username,start_time,headers)
    return order_url

if __name__ == '__main__':
    pass