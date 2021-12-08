import requests, base64, time

def get_token(email, password):
    string = email + ":" + password
    token = base64.b64encode(string.encode('ascii')).decode()
    return token

def buy(token,user_id):
    url = "http://api.parkster.se/api/mobile/v2/parkings/short-term"

    querystring = {"parkingZoneId":"5909","feeZoneId":"4754","carId":"4131856","paymentAccountId":f"PRIVATE%3A{user_id}","timeout":"30"}

    payload = {'version':'321',
    'platform':'android',
    'platformVersion':'24',
    'locale':'en_US',
    'clientTime':time.time.now(),
    'debugPhoneModel':'unknown_Android SDK built for x86_64_f62tlYkBQqOLKeWO55-vut'}

    headers = {
        "authorization": f"Basic {token}",
        "accept": "application/json",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    assert response.status_code == 200, print('Error in buy', response.status_code, response.text)
    print(response.text)
    status = 'confirmed'
    return status

def verify(token):

    url = "https://api.parkster.se/api/mobile/v2/latestparkings"

    querystring = {"version":"321",
                   "platform":"android",
                   "platformVersion":"24",
                   "locale":"en_US",
                   "clientTime":time.time.now(),
                   "debugPhoneModel":"unknown_Android SDK built for x86_64_f62tlYkBQqOLKeWO55-vut"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

def search(query, token, user_id):
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/search"

    querystring = {"query":query,
                   "countryCode":"SE",
                   "userId":user_id,
                   "version":"321",
                   "platform":"android",
                   "platformVersion":"24",
                   "locale":"en_US",
                   "clientTime":time.time.now(),
                   "debugPhoneModel":"unknown_Android SDK built for x86_64_f62tlYkBQqOLKeWO55-vut"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

def get_user_id(token):
    url = "https://api.parkster.se/api/mobile/v2/people/login"

    querystring = {"version":"321","platform":"android","platformVersion":"29","locale":"en_US","clientTime":time.time.now(),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

def find_parking(lat,long,token,user_id):
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/location-search"

    querystring = {"searchLat":lat,"searchLong":long,"userLat":lat,"userLong":long,"radius":"250","countryCode":"SE","userId":user_id,"version":"321","platform":"android","platformVersion":"29","locale":"en_US","clientTime":time.time.now(),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)