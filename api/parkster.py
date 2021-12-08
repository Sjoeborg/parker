import requests, base64, time

def buy(email,password):
    url = "http://api.parkster.se/api/mobile/v2/parkings/short-term"

    querystring = {"parkingZoneId":"5909","feeZoneId":"4754","carId":"4131856","paymentAccountId":"PRIVATE%3A3075336","timeout":"30"}

    payload = {'version':'321',
    'platform':'android',
    'platformVersion':'24',
    'locale':'en_US',
    'clientTime':time.time.now(),
    'debugPhoneModel':'unknown_Android SDK built for x86_64_f62tlYkBQqOLKeWO55-vut'}

    string = email + ":" + password
    token = base64.b64encode(string.encode('ascii')).decode()
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