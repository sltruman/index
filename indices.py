
#!/usr/bin/env python
import copy
import json
import os
import requests
import lxml

from flask import Flask, abort, redirect, request, url_for
from gevent import pywsgi

app = Flask(__name__,'')
app.config['JSON_AS_ASCII'] = False

def gather(id,date_begin,date_end):
    r = requests.post(f'https://cn.investing.com/instruments/HistoricalDataAjax',
        data={
            'curr_id': 40820,
            'smlID': 2057370,
            'header':'上证指数历史数据',
            'st_date':'2021/01/05',
            'end_date':'2021/01/05',
            'interval_sec':'Daily',
            'sort_col':'date',
            'sort_ord':'DESC',
            'action':'historical_data'
        },
        headers={
            'Host': 'cn.investing.com',
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '224',
            'Origin': 'https://cn.investing.com',
            'Connection': 'keep-alive',
            'Referer': 'https://cn.investing.com/indices/shanghai-composite-historical-data',
            'Cookie': 'SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2240820%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fshanghai-composite%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22995201%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A28%3A%22%2Findices%2Fshanghai-se-a-share%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22179%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A20%3A%22%2Findices%2Fhang-sen-40%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228839%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fus-spx-500-futures%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22169%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A14%3A%22%2Findices%2Fus-30%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22166%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Findices%2Fus-spx-500%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2214958%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A25%3A%22%2Findices%2Fnasdaq-composite%22%3B%7D%7D%7D%7D; adBlockerNewUserDomains=1609727643; udid=c178b80872b3333de875cf4f0744633e; adbBLk=6; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1609819174,1609822697,1609851549,1609858159; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jan+05+2021+23%3A04%3A44+GMT%2B0800+(China+Standard+Time)&version=6.7.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=HK%3BHCW; G_ENABLED_IDPS=google; OptanonAlertBoxClosed=2021-01-05T15:04:42.851Z; ses_id=YiwxcGVqMTk3c21rZjdiYjZnMWNiYDMyZ29lYzQ1ZHI3IzI8bzg%2BeD4xOXdjYGN%2FMjY1MWZkOjw8azRtYWNnN2JlMWRlNzE4N2NtZWY3YmI2ZjE4Ym0zZGdmZWQ0NGQ4NzgyYW9hPjI%2BajlgY2xjPjIgNSlmIjorPG40ZGEgZyBibTFwZTYxOzc3bWVmPWJgNmUxY2JgM2dnYmU0NDFkfDd8; r_p_s_n=1; _fbp=fb.1.1609739253134.1792794552; OB-USER-TOKEN=bc5080fb-f1f4-400f-8f2e-7b2923c84138; __atuvc=6%7C1; usprivacy=1YNN; adfreePlanOrderCookie=0; _hjid=b8b84274-4262-497e-a6af-b1b047da44db; _VT_content_1989876_2=1; PHPSESSID=j9lnbtl2i6cgkvfvnmm9fl6cfc; StickySession=id.38310535431.589cn.investing.com; logglytrackingsession=75a6c684-3cfa-402f-bd5c-1302d735270b; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1609859082; comment_notification_220953956=1; adsFreeSalePopUp4c924bb49bb7e8e7c410b17b3064248f=1; _VT_content_200460198_1=1; geoC=HK; smd=c178b80872b3333de875cf4f0744633e-1609858148; nyxDorf=MDRmNzRmYyE0Y2BpZTBmemc3MG8zNDEtYmVmZw%3D%3D; UserReactions=true; outbrain_cid_fetch=true'
        }
    )
    
    html = lxml.etree.HTML(r.text)
    html.xpath()
gather(1,2,3)

@app.route('/indices')
def status():
    date_begin = request.args['date_begin']
    date_end = request.args['date_end']

    return {
        'val': {
            date:['2011-5-19'],
            data:[1231.09],
        },
        'err': None 
    }

http_server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
http_server.serve_forever()
