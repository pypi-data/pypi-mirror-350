import requests
import datetime 
def sendMES(message,key='0f313-17b2-4e3d-84b8-3f9c290fa596',NN = None):
    webHookUrl = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={NN}{key}'
    if NN=="MT":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8b7df0c1-bde0-4091-9e11-f77519439823"
    elif NN=="MT1":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=461a6eab-90e1-48d9-bb7e-ee91f6e16131"
    elif NN=="WT":
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=de0c3cc5-d32b-4631-b807-9db3ae44c6df"
    elif NN=="H9":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=652ed7d5-7f31-437c-90e2-25efce6a8a8a"
    elif NN=="GOES18":
       webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=32c59698-92ff-4049-a1bb-12908fb7b0da"
    elif NN=="GOES19":
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aac8d435-2d21-4c5e-a465-7b51396f4b25"  
    elif NN=="FY4B":
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0f4e28f6-af3b-44b0-9889-827df8f3dcc1" 
    elif NN=="GFS":
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=13f39c2f-e191-4100-b1ee-7316ac9c2451" 
    else:
        webHookUrl ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=13f39c2f-e191-4100-b1ee-7316ac9c2451"
        
    try:
        url=webHookUrl
        headers = {"Content-Type":"application/json"}
        data = {'msgtype':'text','text':{"content":message}}
        res = requests.post(url,json=data,headers=headers)
    except Exception as e:
        print(e)
 