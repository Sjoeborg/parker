## Flowbird:
1. Create:
  https://betalap.flowbirdapp.com/order/create?platform=europe&rt=1638616964396&version=2.8.0+1103
  Headers:
    ``
    POST /order/create?platform=europe&rt=1638616964396&version=2.8.0+1103 HTTP/1.1
    Host: betalap.flowbirdapp.com
    Connection: keep-alive
    Content-Length: 575
    Accept: application/json, text/plain, */*
    Accept-Language: en
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
    Content-Type: application/json
    Sec-GPC: 1
    Origin: https://betalap.flowbirdapp.com
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: cors
    Sec-Fetch-Dest: empty
    Referer: https://betalap.flowbirdapp.com/
    Accept-Encoding: gzip, deflate, br
    Cookie: server=.apachen1; PHPSESSID=i3f0ea9dt8f6a76cqcsd75pu5s; user=485d00e9bb450f412c5a64f91fa2a356aeae790708430f068b74a8d9923984a9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22user%22%3Bi%3A1%3Bs%3A32%3A%22df95590dc766c2c4b10d3c75a0206eff%22%3B%7D
    ``
  Payload:
    ``
    {"preferredLanguage":"en","author":"martin@sjoborg.org","channel":"web","pos":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PoS/v1/30945868/","posLabel":"Taxa 5","vehicle":{"id":884376,"plate":"GFD578","default":true,"category":"car","country-plate":"SE","isExternalTicketNotification":false},"platform":"europe","class":"hourly","startTime":"2021-12-04T11:22:31Z","duration":"P1DT11H49M29S","freeDuration":"PT0S","paidDuration":"PT12M","usertype":"1","usertypeLabel":"Visitor Parking","space":null,"type":"user","geo":{"latitude":59.3307,"longitude":18.0718}}
    ```
  
  Response:
    ``
    {"response":{"customer":"http://api-europe.whooshstore.com/tm/betala.p/customer/v1/5c811100548811ec8c8b506b8d9e5398/","platform":"europe","order_1":{"id":"10423674","status":"pending","channel":"web","parkingticketorder":{"class":"hourly","vehicle":{"plate":"GFD578","country":"SE","category":"car"},"startTime":"2021-12-04T11:22:31Z","duration":"P1DT11H49M29S","freeDuration":"PT0S","paidDuration":"PT12M","pos":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PoS/v1/30945868/","posLabel":"Taxa 5","geo":{"latitude":"59.3307","longitude":"18.0718"},"usertype":"1","usertypeLabel":"Visitor Parking","preferredLanguage":"en","zoneNumber":"5","posNumber":"30945868","pndNumber":"30945868","operator":"http://api.whooshstore.com/tm/betala.p/operator/v1/2/","city":"Stockholm","country":"SE","tariff":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/tariff/90005/","parkFacility":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/","posAlternateName":"5","brand":"betalap","version":"2.8.0+1103"},"parkingticketresponse":{"class":"hourly","startTime":"2021-12-04T11:22:31Z","endTime":"2021-12-05T23:12:00Z","paidDuration":"PT12M","freeDuration":"PT0S","paidAndFreeDuration":"PT12M","duration":"P1DT11H49M29S","isExtendable":true,"isStoppable":true,"parkingAmount":"0","parkingTaxAmount":"0","parkingTaxFreeAmount":"0","taxAmount":"0","taxFreeAmount":"0","taxRate":"25","tariffName":"Taxa 5","timezone":"Europe/Stockholm","timezoneOffset":"+0100","startTimeTimezoneOffset":"+0100","endTimeTimezoneOffset":"+0100","endTimeChanged":false,"currency":"SEK","timestamp":"2021-12-04T11:22:42Z","confirmationAmount":"0","remindersAmount":"0","reminderAmount":"0","totalAmount":"0","serviceFeeAmount":"0","withdrawalMessage":"parking.summary.hourly.withdraval_message.text","alertproposals":{"push":{"reminder":{"amount":0,"href":"http://api.whooshstore.com/tm/betala.p/messages/en/reminder/push/"}}},"suggestTokenization":true,"paymentMethods":[{"uid":"","name":"systemPayExStockholm","psp":"payex","type":"directSale","status":"missing_token","cardTypeAccepted":["visa","mastercard","amex","maestro"],"paymentSecurity":[],"gatewayMerchantId":"75443343-545f-4d21-b0e5-6b3db9acedb3","suggestTokenization":true},{"uid":"","name":"systemPayExSwishStockholm","psp":"payexSwish","type":"directSale","status":"missing_token","cardTypeAccepted":[],"paymentSecurity":[],"gatewayMerchantId":"75443343-545f-4d21-b0e5-6b3db9acedb3","suggestTokenization":true}],"pedestrianNavigationActive":true,"timezoneStartOffset":"+0100","timezoneEndOffset":"+0100"}}}}
    ``
  
2. Get:
  https://betalap.flowbirdapp.com/payment-account/get?rt=1638616965017&customerId=5c811100548811ec8c8b506b8d9e5398&version=2.8.0+1103
  Headers:
    ``
    POST /payment-account/get?rt=1638616965017&customerId=5c811100548811ec8c8b506b8d9e5398&version=2.8.0+1103 HTTP/1.1
    Host: betalap.flowbirdapp.com
    Connection: keep-alive
    Content-Length: 0
    Accept: application/json, text/plain, */*
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
    Sec-GPC: 1
    Origin: https://betalap.flowbirdapp.com
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: cors
    Sec-Fetch-Dest: empty
    Referer: https://betalap.flowbirdapp.com/
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-GB,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-US;q=0.6
    Cookie: server=.apachen1; PHPSESSID=i3f0ea9dt8f6a76cqcsd75pu5s; user=485d00e9bb450f412c5a64f91fa2a356aeae790708430f068b74a8d9923984a9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22user%22%3Bi%3A1%3Bs%3A32%3A%22df95590dc766c2c4b10d3c75a0206eff%22%3B%7D
    ``
3. Confirm:
    https://betalap.flowbirdapp.com/order/confirm?id=10423674&platform=europe&rt=1638616971086&version=2.8.0+1103
    Headers:
      ``
      POST /order/confirm?id=10423674&platform=europe&rt=1638616971086&version=2.8.0+1103 HTTP/1.1
      Host: betalap.flowbirdapp.com
      Connection: keep-alive
      Content-Length: 21
      Accept: application/json, text/plain, */*
      Accept-Language: en
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
      Content-Type: application/json
      Sec-GPC: 1
      Origin: https://betalap.flowbirdapp.com
      Sec-Fetch-Site: same-origin
      Sec-Fetch-Mode: cors
      Sec-Fetch-Dest: empty
      Referer: https://betalap.flowbirdapp.com/
      Accept-Encoding: gzip, deflate, br
      Cookie: server=.apachen1; PHPSESSID=i3f0ea9dt8f6a76cqcsd75pu5s; user=485d00e9bb450f412c5a64f91fa2a356aeae790708430f068b74a8d9923984a9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22user%22%3Bi%3A1%3Bs%3A32%3A%22df95590dc766c2c4b10d3c75a0206eff%22%3B%7D
      ``
    Response:
      ``
      {"response":{"customer":"http://api-europe.whooshstore.com/tm/betala.p/customer/v1/5c811100548811ec8c8b506b8d9e5398/","platform":"europe","order_1":{"id":"10423674","status":"confirmed","channel":"web","parkingticketorder":{"class":"hourly","vehicle":{"plate":"GFD578","country":"SE","category":"car"},"startTime":"2021-12-04T11:22:31Z","duration":"P1DT11H49M29S","freeDuration":"PT0S","paidDuration":"PT12M","pos":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PoS/v1/30945868/","posLabel":"Taxa 5","geo":{"latitude":"59.3307","longitude":"18.0718"},"usertype":"1","usertypeLabel":"Visitor Parking","preferredLanguage":"en","zoneNumber":"5","posNumber":"30945868","pndNumber":"30945868","operator":"http://api.whooshstore.com/tm/betala.p/operator/v1/2/","city":"Stockholm","country":"SE","tariff":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/tariff/90005/","parkFacility":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/","posAlternateName":"5","brand":"betalap","version":"2.8.0+1103"},"parkingticketresponse":{"class":"hourly","startTime":"2021-12-04T11:22:31Z","endTime":"2021-12-05T23:12:00Z","paidDuration":"PT12M","freeDuration":"PT0S","paidAndFreeDuration":"PT12M","duration":"P1DT11H49M29S","isExtendable":true,"isStoppable":true,"parkingAmount":"0","parkingTaxAmount":"0","parkingTaxFreeAmount":"0","taxAmount":"0","taxFreeAmount":"0","taxRate":"25","tariffName":"Taxa 5","timezone":"Europe/Stockholm","timezoneOffset":"+0100","startTimeTimezoneOffset":"+0100","endTimeTimezoneOffset":"+0100","endTimeChanged":false,"currency":"SEK","timestamp":"2021-12-04T11:22:42Z","confirmationAmount":"0","remindersAmount":"0","reminderAmount":"0","totalAmount":"0","serviceFeeAmount":"0","withdrawalMessage":"parking.summary.hourly.withdraval_message.text","alertproposals":{"push":{"reminder":{"amount":0,"href":"http://api.whooshstore.com/tm/betala.p/messages/en/reminder/push/"}}},"suggestTokenization":true,"paymentMethods":[{"uid":"","name":"systemPayExStockholm","psp":"payex","type":"directSale","status":"missing_token","cardTypeAccepted":["visa","mastercard","amex","maestro"],"paymentSecurity":[],"gatewayMerchantId":"75443343-545f-4d21-b0e5-6b3db9acedb3","suggestTokenization":true},{"uid":"","name":"systemPayExSwishStockholm","psp":"payexSwish","type":"directSale","status":"missing_token","cardTypeAccepted":[],"paymentSecurity":[],"gatewayMerchantId":"75443343-545f-4d21-b0e5-6b3db9acedb3","suggestTokenization":true}],"pedestrianNavigationActive":true,"timezoneStartOffset":"+0100","timezoneEndOffset":"+0100"},"freetransaction_14362204":{"paymentSystem":"systemPayExStockholm","timestamp":"2021-12-04T11:22:49Z"}},"parkingticket":{"class":"hourly","country":"SE","city":"Stockholm","posLabel":"Taxa 5","posAlternateName":"5","vehiclePlate":"GFD578","vehicleCountry":"SE","vehicleCategory":"car","pos":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PoS/v1/30945868/","zoneNumber":"5","usertype":"1","usertypeLabel":"Visitor Parking","tariff":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/tariff/90005/","endTimeWithGracePeriod":"2021-12-05T23:12:00Z","currency":"SEK","tariffName":"Taxa 5","operator":"http://api.whooshstore.com/tm/betala.p/operator/v1/2/","isVehicleEditable":false,"controlPlate":"GFD578","posNumber":"30945868","pnd":"http://api.whooshstore.com/tm/betala.p/parkFacility/v1/8155/PnD/v1/30945868/","pndNumber":"30945868","pndLabel":"Taxa 5","parkingAmount":"0","parkingTaxFreeAmount":"0","parkingTaxAmount":"0","totalAmount":"0","serviceFeeAmount":"0","confirmationAmount":"0","reminderAmount":"0","remindersAmount":"0","taxAmount":"0","taxFreeAmount":"0","taxRate":"25","startTime":"2021-12-04T11:22:31Z","endTime":"2021-12-05T23:12:00Z","timezone":"Europe/Stockholm","timezoneOffset":"+0100","startTimeTimezoneOffset":"+0100","endTimeTimezoneOffset":"+0100","duration":"P1DT11H49M29S","paidDuration":"PT12M","freeDuration":"PT0S","paidAndFreeDuration":"PT12M","isExtendable":true,"isStoppable":true,"PRDBId":"7452306f-7f29-4e08-ac0f-bdad2bc90e15","brand":"betalap"}}}
      ``
4. AddNote:
    https://betalap.flowbirdapp.com/order/add-note?id=10423674&platform=europe&class=purpose&rt=1638616971902&version=2.8.0+1103
    Headers:
      ``
      POST /order/add-note?id=10423674&platform=europe&class=purpose&rt=1638616971902&version=2.8.0+1103 HTTP/1.1
      Host: betalap.flowbirdapp.com
      Connection: keep-alive
      Content-Length: 18
      Accept: application/json, text/plain, */*
      Accept-Language: en
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
      Content-Type: application/json
      Sec-GPC: 1
      Origin: https://betalap.flowbirdapp.com
      Sec-Fetch-Site: same-origin
      Sec-Fetch-Mode: cors
      Sec-Fetch-Dest: empty
      Referer: https://betalap.flowbirdapp.com/
      Accept-Encoding: gzip, deflate, br
      Cookie: server=.apachen1; PHPSESSID=i3f0ea9dt8f6a76cqcsd75pu5s; user=485d00e9bb450f412c5a64f91fa2a356aeae790708430f068b74a8d9923984a9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22user%22%3Bi%3A1%3Bs%3A32%3A%22df95590dc766c2c4b10d3c75a0206eff%22%3B%7D
      ``
    Response:
      ``
      {"response":{"note":"private"}}
      ``
