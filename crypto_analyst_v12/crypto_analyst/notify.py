import requests
def telegram(token,chat_id,text):
    if not token or not chat_id: return
    r=requests.post(f"https://api.telegram.org/bot{token}/sendMessage",json={"chat_id":chat_id,"text":text},timeout=10)
    r.raise_for_status()
