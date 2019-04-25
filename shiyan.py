import requests
import time
import random
import threading
import logging

xuehao = ['02111610'+ str(x) for x in range(1,10)] + ['0211161'+ str(x) for x in range(10,40)]+['062316102','021216116','021214111','021316322','053114316','021114121','021116214','021116202']
logging.basicConfig(
        filename='shiyan.log',
        level=logging.INFO
    )

def shiyan(xh):
    print(str(xh)+' start...')
    logging.error(str(xh)+' start...')
    loginUrl = 'http://202.121.126.68/exam_login.php'
    loginData = {'xuehao':xh,'password':'123456','postflag':'1','cmd':'login','role':'0'}
    login = requests.post(loginUrl, data = loginData)
    cookies = dict(wsess=login.cookies['wsess'])
    headers = {'Content-Type':'application/x-www-form-urlencoded', 'charset':'UTF-8', 'Content-Length':'16', 'Connection':'keep-alive'}
    heartBeatUrl = 'http://202.121.126.68/exam_xuexi_online.php'
    heartBeatData = {'cmd':'xuexi_online'}
    hearBeat = requests.post(heartBeatUrl, heartBeatData, headers=headers, cookies=cookies)
    if dict(hearBeat.json())['status'] == 1:
        while(dict(hearBeat.json())['shichang'][:2]!='1时'):
            hearBeat = requests.post(heartBeatUrl, heartBeatData, headers=headers, cookies=cookies)
            logging.error('xuehao=%s, json=%s\n', xh, hearBeat.json())
            time.sleep(random.uniform(50,70))
        print(str(xh)+' end successfully...')
    else:
        print(str(xh)+' end with status 0...')

threadpool = []
for xh in xuehao:
    th = threading.Thread(target=shiyan, args=(xh,))
    threadpool.append(th)

for th in threadpool:
        th.start()

for th in threadpool:
    threading.Thread.join(th)