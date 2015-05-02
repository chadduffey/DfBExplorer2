import dropbox
import urllib2

#Powershell example:
#Invoke-RestMethod -Uri https://api.dropbox.com/1/team/get_info -Body "{}" -ContentType application/json -Headers @{
#   Authorization = $token } -Method Post | fl

request = urllib2.Request('https://api.dropbox.com/1/team/get_info')
request.add_header('Content-type', 'application/json')
request.add_header('Authorization','Bearer Roti84bECDUAAAAAAAACOhZz6DJtV9g4kWxk2_6gc7GOObK7nrmz1c4ITHm1wlOE')
body = str('{}')
request.add_data(body)

response = urllib2.urlopen(request)
data = response.read()
print data


#POST /1/team/get_info HTTP/1.1
#Content-Type: application/json
#Authorization: Bearer Roti84bECDUAAAAAAAACOhZz6DJtV9g4kWxk2_6gc7GOObK7nrmz1c4ITHm1wlOE
#Cookie: gvc=MzE2NDQwMzI4Nzg4MTE5MTE1MTMxNzQ5NzU5MzQ4MDk3MTEzODQ4
#Host: api.dropbox.com
#Connection: close
#User-Agent: Paw/2.2.1 (Macintosh; OS X/10.10.3) GCDHTTPRequest
#Content-Length: 2

#{}
