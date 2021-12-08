import requests, base64, time

def get_token(email, password):
    string = email + ":" + password
    token = base64.b64encode(string.encode('ascii')).decode()
    return token

def buy(parkingzone_id,feezone_id,car_id,token,user_id):
    url = "http://api.parkster.se/api/mobile/v2/parkings/short-term"

    querystring = {"parkingZoneId":parkingzone_id,"feeZoneId":feezone_id,"carId":car_id,"paymentAccountId":f"PRIVATE%3A{user_id}","timeout":"30"}

    payload = {'version':'321',
    'platform':'android',
    'platformVersion':'24',
    'locale':'en_US',
    'clientTime':int(time.time()),
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
                   "clientTime":int(time.time()),
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
    print(response.text)


def get_fee_id(parkingzone_id, token):
    import requests

    url = f"https://api.parkster.se/api/mobile/v2/parking-zones/{parkingzone_id}"

    querystring = {"version":"321","platform":"android","platformVersion":"29","locale":"en_US","clientTime":int(time.time()),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    feezone_id = response.json()['feeZone']['id'] #TODO: here we can get a lot of payment info for the different fee zones
    return feezone_id

def search_by_query(query, token, user_id):
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/search"

    querystring = {"query":query,
                   "countryCode":"SE",
                   "userId":user_id,
                   "version":"321",
                   "platform":"android",
                   "platformVersion":"24",
                   "locale":"en_US",
                   "clientTime":int(time.time()),
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
    parkingZones = response.json()['parkingZones']
    result = []
    for zone in parkingZones:
        if zone['active'] is True:
            try:
                zone_adress = zone['address']
            except KeyError:
                zone_adress = 'Unknown'
            result.append((zone['name'],zone_adress, zone['id']))
    return result

def get_user_id_and_cars(token):
    url = "https://api.parkster.se/api/mobile/v2/people/login"

    querystring = {"version":"321","platform":"android","platformVersion":"29","locale":"en_US","clientTime":int(time.time()),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    user_id = response.json()['id']
    cars = response.json()['cars']
    return user_id, cars

def search_by_location(lat,long,token,user_id):
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/location-search"

    querystring = {"searchLat":lat,"searchLong":long,"userLat":lat,"userLong":long,"radius":"250","countryCode":"SE","userId":user_id,
    "version":"321","platform":"android","platformVersion":"29","locale":"en_US","clientTime":int(time.time()),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    parkingZones = response.json()['parkingZonesAtPosition']
    results = []

    for zone in parkingZones:
        try:
            zone_adress = zone['address']
        except KeyError:
            zone_adress = 'Unknown'
        results.append((zone['name'],zone_adress, zone['id']))
    return results

def buy_from_location(email, password, lat,long, license_plate=None):
    token = get_token(email, password)
    user_id, cars = get_user_id_and_cars(token)
    if license_plate is None:
        car_id = cars[0]['id']
        car_numberplate = cars[0]['licenseNbr']
        print(f'Picked car {car_numberplate}')
    else:
        for car in cars:
            if car['licenseNbr'] == license_plate:
                car_id = car['id']
                car_numberplate = car['licenseNbr']
                print(f'Picked car {car_numberplate}')
                break
    search_results = search_by_location(lat,long,token,user_id)
    zone_name, zone_adress, zone_id = search_results[0] #TODO: logic to pick the best zone
    print(f'Found zone {zone_name} at {zone_adress}')
    feezone_id = get_fee_id(zone_id, token)
    buy(zone_id, feezone_id,car_id, token, user_id)

def buy_from_search(email, password, query, license_plate=None):
    token = get_token(email, password)
    user_id, cars = get_user_id_and_cars(token)
    if license_plate is None:
        car_id = cars[0]['id']
        car_numberplate = cars[0]['licenseNbr']
        print(f'Picked car {car_numberplate}')
    else:
        for car in cars:
            if car['licenseNbr'] == license_plate:
                car_id = car['id']
                car_numberplate = car['licenseNbr']
                print(f'Picked car {car_numberplate}')
                break
    search_results = search_by_query(query,token,user_id)
    zone_name, zone_adress, zone_id = search_results[0]
    feezone_id = get_fee_id(zone_id, token)
    buy(zone_id,feezone_id, car_id, token, user_id)

buy_from_search('martin@sjoborg.org', password, query='Fisksätra', license_plate=None)