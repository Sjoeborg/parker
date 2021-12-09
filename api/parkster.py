import requests, base64, time

def get_token(email, password):
    '''
    Returns the base64 token for the given `email` and `password`.
    '''
    string = email + ":" + password
    token = base64.b64encode(string.encode('ascii')).decode()
    return token

def buy(parkingzone_id,feezone_id,car_id,token,user_id):
    '''
    Buys a ticket. 
    Needs `parkingzone_id` from `search_by_query()` or `search_by_location()`,
    `feezone_id` from `get_fee_id()`,
    `user_id` and `car_id` from `get_user_id_and_cars()`,
    and `token` from `get_token()`.
    '''

    url = "https://api.parkster.se/api/mobile/v2/parkings/short-term"

    payload = f"parkingZoneId={parkingzone_id}&feeZoneId={feezone_id}&carId={car_id}&timeout=30&paymentAccountId=PRIVATE%3A{user_id}"
    
    querystring = {'version':'321',
    'platform':'android',
    'platformVersion':'29',
    'locale':'sv_SV',
    'clientTime':int((time.time())*1e3),
    'debugPhoneModel':'Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ'}

    headers = {
        "authorization": f"Basic {token}",
        "accept": "application/json",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    assert response.status_code == 200, print('Error in buy', response.status_code, response.text)
    status = 'confirmed'
    return status

def get_latest_ticket(token):
    '''
    Returns `(amount, currency)` of the latest ticket the user has bought.
    '''

    url = "https://api.parkster.se/api/mobile/v2/latestparkings"

    querystring = {"version":"321",
                   "platform":"android",
                   "platformVersion":"29",
                   "locale":"sv_SV",
                   "clientTime":int(time.time()*1e3),
                   "debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {token}",
        "host": "api.parkster.se",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    latest_ticket = response.json()['parkings'][0]
    return latest_ticket['paymentAmount'] , latest_ticket['paymentCurrency']['symbol']


def get_fee_id(parkingzone_id, token):
    '''
    Returns the fee zone id for the given `parkingzone_id`.
    '''

    url = f"https://api.parkster.se/api/mobile/v2/parking-zones/{parkingzone_id}"

    querystring = {"version":"321","platform":"android","platformVersion":"29","locale":"sv_SV","clientTime":int(time.time()*1e3),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

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
    '''
    Returns a list of parking zones matching the `query`. Each element is a tuple with `(zone_name, zone_adress, zone_id)`
    '''
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/search"

    querystring = {"query":query,
                   "countryCode":"SE",
                   "userId":user_id,
                   "version":"321",
                   "platform":"android",
                   "platformVersion":"29",
                   "locale":"sv_SV",
                   "clientTime":int(time.time()*1e3),
                   "debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

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
    '''
    Returns the user_id and a dict of cars the user has. The car list contains the `id` and `licenseNbr` of the cars.
    '''
    url = "https://api.parkster.se/api/mobile/v2/people/login"

    querystring = {"version":"321","platform":"android","platformVersion":"29","locale":"sv_SV","clientTime":int(time.time()*1e3),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

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
    '''
    Returns a list of the parking zones near the given `lat` and `long`. Each element is a tuple with `(zone_name, zone_adress, zone_id)`
    '''
    url = "https://api.parkster.se/api/mobile/v2/parking-zones/location-search"

    querystring = {"searchLat":lat,"searchLong":long,"userLat":lat,"userLong":long,"radius":"250","countryCode":"SE","userId":user_id,
    "version":"321","platform":"android","platformVersion":"29","locale":"sv_SV","clientTime":int(time.time()*1e3),"debugPhoneModel":"Genymobile_Google Pixel 3_cT-CAsh8Qg63-aRpE5NFDZ"}

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
    '''
    Buys a ticket for the location closes to the given `lat` and `long`. Picks the first car of the user if `license_plate` is not provided.
    '''
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
    status = buy(zone_id, feezone_id,car_id, token, user_id)
    return status

def buy_from_search(email, password, query, license_plate=None):
    '''
    Buys a ticket for the first seach result from `query`. Picks the first car of the user if `license_plate` is not provided.
    '''
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
    print('Buying ticket at', zone_name, zone_adress)
    status = buy(zone_id,feezone_id, car_id, token, user_id)
    return status


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    buy_from_search(os.getenv('PARKSTER_USERNAME'), os.getenv('PARKSTER_PASSWORD'), query='Hägerstensåsens BP', license_plate=None)
    get_latest_ticket(get_token(os.getenv('PARKSTER_USERNAME'), os.getenv('PARKSTER_PASSWORD')))