from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.ids=set();self.h1=0;self.title=False;self.description=False;self.noindex=False;self.labels=set();self.inputs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.description=True
  if tag=='meta' and a.get('name')=='robots' and 'noindex'in a.get('content',''):self.noindex=True
  if tag=='label':self.labels.add(a.get('for'))
  if tag in ['input','textarea'] and a.get('type')!='hidden':self.inputs.append(a.get('id'))
  if tag=='a' and 'href'in a:self.links.append(a['href'])
  if tag in ['img','script'] and 'src'in a:self.links.append(a['src'])
  if tag=='link' and a.get('rel') in ['stylesheet','icon']:self.links.append(a.get('href',''))
pages={p:Page() for p in root.rglob('*.html')}
for p,doc in pages.items():doc.feed(p.read_text())
errors=[];linkcount=0
for p,doc in pages.items():
 for key,val in [('one H1',doc.h1==1),('title',doc.title),('description',doc.description),('draft noindex',doc.noindex)]:
  if not val:errors.append(f'{p.relative_to(root)}: missing {key}')
 for inputid in doc.inputs:
  if inputid not in doc.labels:errors.append(f'{p}: unlabeled input {inputid}')
 for link in doc.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  linkcount+=1
  target=root/unquote(u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
  if not u.path:target=p
  elif target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(root)}: missing target {link}')
  elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{p.relative_to(root)}: missing anchor {link}')
print(json.dumps({'pages_checked':len(pages),'internal_link_and_asset_references_checked':linkcount,'errors':errors},indent=2))
raise SystemExit(bool(errors))
