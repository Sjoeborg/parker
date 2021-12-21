from os import error
import requests,time

def get_price(end_date,license_plate,user_id,parking_id,token):
    '''
    Returns the tuple `(price, currency)` for the given parameters.
    '''
    url = "https://app-bff.easyparksystem.net/android/api/parking/price"

    querystring = {"includePriceInUserCurrency":"false"}
    payload = {'carCountryCode':'SE',
               'carLicenseNumber':license_plate,
               'endDate':end_date,
               'parkingAreaCountryCode':'SE',
               'parkingAreaNo':parking_id,
               'parkingType':'NORMAL_TIME',
               'parkingUserId':user_id}
    headers = {
        "x-authorization": f"Bearer {token}",
        "easypark-application-channel-name": "Android",
        "easypark-application-device-os": "Android Mobile",
        "easypark-application-version-number": "15.30.0",
        "easypark-application-build-number": "14809",
        "easypark-application-device-os-version": "29",
        "easypark-application-market-country": "SE",
        "easypark-application-preferred-language": "en-US",
        "easypark-application-install-id": "21fc3be1-a67e-4d1a-aa5a-38ebc24f5370",
        "content-type": "application/json; charset=UTF-8",
        "host": "app-bff.easyparksystem.net",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.0"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    print(response.json())
    try:
        return response.json()['priceInclVat'], response.json()['currency']
    except KeyError:
        return None, None

def login(username, password):
    '''
    Returns `(token, user_id, car)` for the given username and password.
    '''
    url = "https://app-bff.easyparksystem.net/android/api/login"

    payload = {
        "password": password,
        "username": username
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)
    try:
        token = response.json()['sso']['idToken']
        user_id = response.json()['status']['accounts'][0]['parkingUser']['id']
        car = response.json()['status']['cars'][0]['licenseNumber'] # TODO: smarter car picker. (no need to pick car here though)
    except KeyError:
        print(response.json())
        return None, None, None
    return token, user_id, car

def search_lat_long(lat,lon,token):
    '''
    Returns a list of parking areas near the given coordinates. The list contain tuples `(name, id)`
    '''
    url = "https://app-bff.easyparksystem.net/android/api/location/inrectangle/V2"
    querystring = {"lat1":float(lat) - 5e-4,"lon1":float(lon) -5e-4,"lat2":float(lat) + 5e-4,"lon2":float(lon) + 5e-4}

    headers = {
        "x-authorization": f"Bearer {token}",
        "easypark-application-channel-name": "Android",
        "easypark-application-device-os": "Android Mobile",
        "easypark-application-version-number": "15.30.0",
        "easypark-application-build-number": "14809",
        "easypark-application-device-os-version": "29",
        "easypark-application-market-country": "SE",
        "easypark-application-preferred-language": "en-US",
        "easypark-application-install-id": "21fc4be1-a67e-4d1a-aa5a-32ebc24f5370",
        "host": "app-bff.easyparksystem.net",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.0",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    area_response = response.json()['areas']
    area_list = [(area['areaName'],area['areaNo']) for area in area_response if area['parkingOperatorStickerType'] == 'DIGITAL']
        
    return area_list

def buy(lat,long,end_date,license_plate,user_id,parking_id,token):
    url = "https://app-bff.easyparksystem.net/android/api/parking/start"

    payload = {
        "carCountryCode": "SE",
        "carLicenseNumber": license_plate,
        "endDate": end_date,
        "insufficientBalanceAllowed": 'false',
        "parkingAreaCountryCode": "SE",
        "parkingAreaNo": parking_id,
        "parkingType": "NORMAL_TIME",
        "parkingUserId": user_id,
        "pointerLatitude": lat,
        "pointerLongitude": long
    }
    headers = {
        "x-authorization": f"Bearer {token}",
        "easypark-application-channel-name": "Android",
        "easypark-application-device-os": "Android Mobile",
        "easypark-application-version-number": "15.30.0",
        "easypark-application-build-number": "14809",
        "easypark-application-device-os-version": "29",
        "easypark-application-market-country": "SE",
        "easypark-application-preferred-language": "en-US",
        "easypark-application-install-id": "21fc4be1-a67e-4d1a-aa5a-38ebc24f5370",
        "content-type": "application/json; charset=UTF-8",
        "host": "app-bff.easyparksystem.net",
        "connection": "Keep-Alive",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.0"
    }
    querystring = {"isAutomotive":"false"}

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    assert response.status_code == 200 or response.status_code == 201, print('Error in buy()', response.status_code, response.text)

    if response.json()['active'] is True:
        status = 'confirmed'
        #print(f'Bought parking spot for {license_plate}')
    else:
        status = 'failed'
    return status

def login_and_buy(username,password, lat,lon, duration=None):
    token,user_id,car = login(username,password)
    search_result = search_lat_long(lat,lon,token)
    zoneName, zoneNo = search_result[0] #TODO: better picker
    if duration is None:
        duration = int((time.time()+600)*1e3)
    else:
        duration += int((time.time())*1e3)
    status = buy(lat,lon, duration, car,user_id, zoneNo, token) #TODO: handle time
    return status

def get_price(username, password, lat, lon, end_date):
        try:
            token,user_id,car = login(username,password)
        except IndexError as e:
            return 'Error:' + e , 401
        try:
            search_result = search_lat_long(float(lat),float(lon),token)
            zoneName, zoneNo = search_result[0]
            amount, currency = get_price(int(float(end_date)*1e3),car,user_id,zoneNo,token)
        except error as e:
            return 'Error when searching:'+ e , 400
        return {'price': amount, 'currency': currency}, 200
if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    login_and_buy(os.getenv('EASYPARK_USERNAME'), os.getenv('EASYPARK_PASSWORD'), 59.3307, 18.0718)
    #get_price(int((time.time()+200)*1e3), car,user_id,zoneNo,token)