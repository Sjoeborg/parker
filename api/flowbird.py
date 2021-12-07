import requests
import time,re
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
        print('Error in get_cookie',response.status_code, response.text)

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
        print('Error in get_user_session',response.status_code, response.text)

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
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    assert response.status_code == 200, print('Error in create_order',response.status_code, response.text)

    confirm_url = response.json()['response']['customer']   
    try:
        customer_id= re.match('.*customer\/v[0-9]\/(.*)\/', confirm_url).group(1)
    except TypeError:
        print('Error in create_order. Could not find customer_id from the response url', confirm_url)
        return None, None
    order_id = response.json()['response']['order_1']['id']
    #TODO: validation here
    return customer_id, order_id
        

def get_payment(customer_id,headers):
    url = 'https://betalap.flowbirdapp.com/payment-account/get?'
    querystring = {"customerId":customer_id,"rt":time.time(),"version":"2.8.0 1103"}

    response = requests.request("POST", url, headers=headers, params=querystring)

    assert response.status_code == 200, print('Error in get_payment', response.status_code, response.text)

    return


def confirm_order(order_id,headers):
    url = 'https://betalap.flowbirdapp.com/order/confirm'
    querystring = {"id":order_id,"rt":time.time(),"version":"2.8.0 1103", 'platform': 'europe'}
    response = requests.request("POST",url, params=querystring, headers=headers)
    try:
        status = response.json()['response']['order_1']['status']
        return status
    except:
        print('Error in confirm_order',response.status_code, response.text)
        return None

def login(username,password):
    headers = get_cookie()
    headers = get_user_session(username, password, headers)
    return headers

def buy(username,start_time, duration, lat, long,headers):
    order_dict = {'username':username,'lat': lat, 'long': long, 'start_time': start_time, 'duration': duration, 'vehicle': {
                "id": 884376,
                "plate": "GFD578",
                "default": True,
                "category": "car",
                "country-plate": "SE",
                "isExternalTicketNotification": False
            }}
    customer_id, order_id = create_order(order_dict,headers)
    get_payment(customer_id, headers)
    response = confirm_order(order_id, headers)
    return response

def login_and_buy(username,password,start_time, duration, lat, long):
    headers = login(username,password)
    status = buy(username,start_time, duration, lat, long,headers)
    
    return status

if __name__ == '__main__':
    pass