import requests
import time,re


def get_session_id():
    '''
    Starts a session and returns the session_id
    '''

    url = "https://betalap.flowbirdapp.com/customer/get"

    querystring = {"id":"1","withAccountCompletion":"yes","version":" 2.8.0 1103"}

    payload = "server=.apachen1"
    headers = {
        "cookie": "server=.apachen1",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    try:
        return response.cookies.get_dict()["PHPSESSID"]
    except:
        print('Error in get_cookie',response.status_code, response.text)

def get_zone_info(park_id, headers):
    url = "https://betalap.flowbirdapp.com/search/index/"

    querystring = {"parkCode":park_id,"class":"tariffArea","kind":"pos","count":"1","language":"en","rt":int(time.time()*1e3),"version":"2.8.0 1103"}


    response = requests.request("GET", url, headers=headers, params=querystring)
    label = response.json()['response']['response']['docs'][0]['label'] #To be used as posLabel
    id = response.json()['response']['response']['docs'][0]['id'] #To be used as pos

    return label,id

def search_by_lat_long(lat,lon, session_id):
    '''
    Returns a list of `(zone_name, zone_id)` tuples
    '''
    url = "https://betalap.flowbirdapp.com/search/index/"

    querystring = {"latitude":lat,
                   "longitude":lon,
                   "distance":"0.5267302077787829",
                   "count":"100",
                   "language":"sv",
                   "kind":"pos",
                   "rt":int(time.time()*1e3),
                   "version":"2.8.0 1103"}

    headers = {
        "host": "betalap.flowbirdapp.com",
        "connection": "keep-alive",
        "accept": "application/json",
        "accept-language": "sv",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "content-type": "application/json",
        "sec-gpc": "1",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://betalap.flowbirdapp.com/",
        "accept-encoding": "gzip, deflate, br",
        "cookie": f"server=.apachen2; PHPSESSID={session_id}"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    assert response.status_code == 200, print('Error in search_by_lat_long',response.status_code, response.text)
    result_list = response.json()['response']
    results = [(result['label'], result['parkCode']) for result in result_list]
    return results


def get_user_id(user,password,session_id):
    '''
    Returns the headers containing user id and session id.
    '''

    url = "https://betalap.flowbirdapp.com/customer/login/"

    querystring = {"rt":int(time.time()*1e3),"version":"2.8.0 1103"}

    payload= {'username': user, 'countryCode': 'undefined', 'password': password, 'rememberMe': 'false', 'rt': int(time.time()*1e3)}
    headers = {
        "host": "betalap.flowbirdapp.com",
        "connection": "keep-alive",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "sec-gpc": "1",
        "origin": "https://betalap.flowbirdapp.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://betalap.flowbirdapp.com/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cookie": f"server=.apachen2; PHPSESSID={session_id}"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    try:
        headers['cookie'] += '; user=' + response.cookies.get_dict()["user"]
        return headers
    except:
        print('Error in get_user_session',response.status_code, response.text)

def create_order(order_dict,headers):
    url = "https://betalap.flowbirdapp.com/order/create"

    querystring = {"platform":"europe","rt":int(time.time()*1e3),"version":"2.8.0 1103"}

    payload = {
        "preferredLanguage": "en",
        "author": order_dict['username'],
        "channel": "web",
        "pos": order_dict['zone_id'],
        "posLabel": order_dict['zone_name'],
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
    customer_id= re.match('.*customer\/v[0-9]\/(.*)\/', confirm_url).group(1)
    order_id = response.json()['response']['order_1']['id']
    status = response.json()['response']['order_1']['status']
    return customer_id, order_id, status

def get_payment_info(customer_id, headers):

    url = "https://betalap.flowbirdapp.com/payment-account/get"

    querystring = {"rt":int(time.time()*1e3),"customerId":customer_id,"version":"2.8.0 1103"}


    response = requests.request("POST", url, headers=headers, params=querystring)
    assert response.status_code == 200, print('Error in get_payment_info',response.status_code, response.text)
    uid = response.json()['response'][0]['uid']
    currentPaymentProvider = response.json()['response'][0]['data']['psp'] #Weird naming, but correct
    psp = response.json()['response'][0]['data']['pspId']

    return uid, currentPaymentProvider, psp

def confirm_order(id, uid, psp, currentPaymentProvider, headers):
    url = "https://betalap.flowbirdapp.com/order/confirm"
    querystring = {"id":id,"platform":"europe","uid":uid,"psp":psp,"currentPaymentProvider":currentPaymentProvider,"rt":int(time.time()*1e3),"version":"2.8.0 1103"}
    payload = {"alertProposals": []}
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    assert response.status_code == 200, print('Error in confirm_order',response.status_code, response.text)
    status = response.json()['response']['order_1']['status']
    return status


def login(username,password):
    session_id = get_session_id()
    headers = get_user_id(username, password, session_id)
    return headers

def buy(username,zone_name,zone_id,start_time, duration, lat, long,headers):
    order_dict = {'username':username,"zone_name": zone_name,"zone_id": zone_id,'lat': lat, 'long': long, 'start_time': start_time, 'duration': duration, 'vehicle': {
                "id": 884376,
                "plate": "GFD578", #TODO: Get vehicle plate and id 
                "default": True,
                "category": "car",
                "country-plate": "SE",
                "isExternalTicketNotification": False}}
    customer_id, order_id, status = create_order(order_dict,headers)
    if status == 'pending':
        uid, currentPaymentProvider, psp = get_payment_info(customer_id,headers)
        status = confirm_order(order_id, uid, psp, currentPaymentProvider, headers)
    else:
        print(status)
    return status

def login_and_buy(username,password,lat, long, start_time=None, duration=None):
    if start_time is None:
        time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime(time.time() + 5))
    if duration is None:
        duration = 'P0DT0H10M0S'
    headers = login(username,password)
    search_result =search_by_lat_long(lat,long,headers)
    park_name, park_id = search_result[0] #TODO: choose this better
    zone_name, zone_id=get_zone_info(park_id,headers)
    print('Found', park_name, zone_name)
    status = buy(username,zone_name,zone_id,start_time, duration, lat, long,headers)
    
    return status
if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    login_and_buy(os.getenv('FLOWBIRD_USERNAME'),os.getenv('FLOWBIRD_PASSWORD'), 59.3307, 18.0718)