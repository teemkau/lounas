from __future__ import annotations
import json,re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; TZ=ZoneInfo('Europe/Helsinki'); TODAY=datetime.now(TZ).date()
HEADERS={'User-Agent':'Mozilla/5.0 (compatible; AvantiLunchBot/1.0; +https://github.com/teemkau/lounas)'}
SHORT={0:'ma',1:'ti',2:'ke',3:'to',4:'pe',5:'la',6:'su'}
LONG={0:'MAANANTAI',1:'TIISTAI',2:'KESKIVIIKKO',3:'TORSTAI',4:'PERJANTAI',5:'LAUANTAI',6:'SUNNUNTAI'}
def text(url):
 r=requests.get(url,headers=HEADERS,timeout=30); r.raise_for_status(); s=BeautifulSoup(r.text,'html.parser')
 for t in s(['script','style','noscript']): t.decompose()
 return '\n'.join(x.strip() for x in s.stripped_strings if x.strip())
def lines(s):
 out=[]
 for x in s.splitlines():
  x=re.sub(r'\s+',' ',x).strip(' \t\ufeff')
  if x and x not in out: out.append(x)
 return out
def pegasus(s):
 a=lines(s); target=f"{LONG[TODAY.weekday()]} {TODAY.day}.{TODAY.month}.{TODAY.year}"; i=next((i for i,x in enumerate(a) if target in x.upper()),None)
 if i is None: raise ValueError('päivää ei löytynyt')
 out=[]; day=re.compile(r'^(MAANANTAI|TIISTAI|KESKIVIIKKO|TORSTAI|PERJANTAI|LAUANTAI|SUNNUNTAI)\b',re.I)
 for x in a[i+1:]:
  if day.match(x) or x.upper().startswith('LOUNAASEEN KUULUU'): break
  out.append(x)
 return out[:12]
def kajuutta(s):
 a=lines(s); target=SHORT[TODAY.weekday()]; marks={'ma','ti','ke','to','pe','la','su'}; i=next((i for i,x in enumerate(a) if x.lower().strip('.:')==target),None)
 if i is None: raise ValueError('viikonpäivää ei löytynyt')
 out=[]
 for x in a[i+1:]:
  if x.lower().strip('.:') in marks or x.lower().startswith(('g =','l =','lounaaseen sisältyy','hinnasto')): break
  out.append(x)
 return out[:10]
def paviljonki(s):
 a=lines(s); name=LONG[TODAY.weekday()].capitalize(); i=next((i for i,x in enumerate(a) if re.match(rf'^{name}\s*:?$',x,re.I)),None)
 if i is None:
  iso=TODAY.isoformat(); i=next((i for i,x in enumerate(a) if x.startswith(iso)),None)
 if i is None: raise ValueError('päivää ei löytynyt')
 days=tuple(v.capitalize() for v in LONG.values()); out=[]
 for x in a[i+1:]:
  if any(re.match(rf'^{d}\s*:?$',x,re.I) for d in days) or re.match(r'^\d{4}-\d{2}-\d{2}$',x): break
  if x.lower().startswith(('lounaaseen','aukioloajat','hinta')): break
  out.append(x.lstrip('•*- '))
 return out[:12]
def fetch(name,urls,parser,hours,price):
 errs=[]
 for url in urls:
  try:
   s=text(url)
   if 'request is being verified' in s.lower() or 'please wait' in s.lower(): raise RuntimeError('automaattinen haku estetty')
   d=parser(s)
   if d:return {'name':name,'source':url,'hours':hours,'price':price,'ok':True,'message':'','dishes':d}
  except Exception as e: errs.append(str(e))
 return {'name':name,'source':urls[0],'hours':hours,'price':price,'ok':False,'message':'Lista ei saatavilla automaattisesti','dishes':[]}
def main():
 rs=[fetch('Avantin Paviljonki',['https://avantinpaviljonki.fi/','https://lounasvahti.fi/lieto/avantin-paviljonki'],paviljonki,'10.30–14.30','12,90 €'),fetch('Kajuutta',['https://www.kajuutta.fi/lounaslista'],kajuutta,'arkisin','11,90 €'),fetch('Pegasus Avanti',['https://www.pegasus-ravintolat.fi/pegasusavanti'],pegasus,'10.30–14.30','13,00 €')]
 data={'date':TODAY.isoformat(),'updated_at':datetime.now(TZ).isoformat(),'restaurants':rs}; (ROOT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
