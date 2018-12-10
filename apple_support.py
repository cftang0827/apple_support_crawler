import requests
import time 
import smtplib 
from email.mime.text import MIMEText
import getpass
import json
import datetime
import traceback


def init_gmail_server(gmail_user, gmail_password):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:  
        print("Something wrong, please check your account or password")
    return server

def send_notification(server, gmail_user, body):
    sent_from = gmail_user
    sent_to = [gmail_user]
    subject = 'Apple support notification'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sent_from
    server.sendmail(sent_from, sent_to, msg.as_string())


# gmail_user = input("Gmail account: ")
gmail_user = "cftang0827@gmail.com"
gmail_password = getpass.getpass("Password: ")
with open('cookie', 'r') as f:
    cookies_from_apple_web = f.read().split('\n')[0]

server = init_gmail_server(gmail_user, gmail_password)


url = "https://getsupport.apple.com/web/v2/takein/timeslots"

headers= {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Apple-CSRF-Token": "gXYPaEXtlbOn+Cg5IT5R1Shx73Y=",
    "Cookie": cookies_from_apple_web
}


body = {"store":"R713","athenaRetailRequest":{"dims":"Vta44j1e3NlY5BSo9z4ofjb75PaK4Vpjt3Q9cUVlOrXTAxw63UYOKES5jfzmkflFflNzl998tp7ppfAaZ6m1CdC5MQjGejuTDRNziCvTDfWogCjC8ZxQBgEhO3f9p_nH1u_eH3BhxUC550ialT0ial5me1zU0l5yjaY1WMsiZRPrwXC_JEkNgvlE4yy2XElgebiYMpztNKscKsgUs_43wuZPup_nH2t05oaYAhrcpMxE6DBUr5xj6KkuL5raZmThaL6qgXK_Pmtd0SUrs8WOUMnGWoz75PP9BLsBwe98vDdYejftckuyPBDjaY2ftckZZLQ084akJkFWHJBeNFBSQeLaD.SAxN4t1VKWZWuxbuJjkWick51W21BSkMk0ugN.xL43DdlK64Wyg1wWF9kmFxFjkWUdISFQeB0VcHmrk9B0WHGY5BNv_.BNlYCa1nkBMfs.2DK","clientTimeZone":480}}

status_ok_body = 'Time: {} \n There is an update from apple support webpage in Taipei 101, please visit https://getsupport.apple.com/ to get the support'.format(str(datetime.datetime.now()))

status_fail_body = "There some error in the program, please take a look"
fail_time = 0

while True:
    print("Check webpage from apple...")
    res = requests.post(url=url, headers=headers, data=json.dumps(body))
    if res.status_code == 200:
        try:
            fail_time = 0
            res_raw = json.loads(res.text)
            res_data = res_raw["data"]["timeslots"]["days"]
            for day in res_data:
                if day['available'] != 0:
                    print("Warning, there's an update!!!!!!!!!!!!!!!!!!!!!")
                    send_notification(server, gmail_user, status_ok_body)
        except Exception as e:
            err = traceback.format_exc()
            print(err)
            print("Maybe cookie is not available")
            fail_time += 1
            if fail_time > 5:
                send_notification(server, gmail_user, status_fail_body + "  error code: {}".format(err))
                break

    else:
        print("Error, maybe network is not available")
        send_notification(server, gmail_user, status_fail_body)
        break
    
    time.sleep(5)
server.close()


