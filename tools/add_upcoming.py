# 「AIの動向」(index.html)の「代表的な動き」の上に、折りたたみの「これから変わること」を入れる。
# data/upcoming.json から作る。日付を過ぎた項目は出さない。項目が0件なら欄ごと置かない。
# 毎週 index.html を書き直したあとに `python3 tools/add_upcoming.py` を実行する(何度実行しても同じ結果)。
import re,json,datetime,html
def block(items):
    wd='月火水木金土日'
    def one(x):
        d=datetime.date.fromisoformat(x['date'])
        links=''.join('<a href="%s" target="_blank" rel="noopener" style="display:inline-block;margin-top:4px;padding:4px 12px;border:0.5px solid #cfd6da;border-radius:14px;background:#fff;font-size:12.5px;font-weight:600;color:#1f2a30;text-decoration:none">%s</a>'%(html.escape(l['url']),html.escape(l['label'])) for l in x['links'])
        return ('<div style="padding:10px 0;border-top:0.5px solid #dfe5e9"><div style="font-size:12.5px;color:#64717a"><b style="color:#1f2a30">%d月%d日(%s)</b> ・ %s</div>'
                '<div style="font-size:14px;font-weight:700;line-height:1.6;margin:2px 0">%s</div><div style="font-size:13.5px;line-height:1.7">%s</div>%s</div>')%(d.month,d.day,wd[d.weekday()],html.escape(x['service']),html.escape(x['title']),html.escape(x['text']),links)
    body=''.join(one(x) for x in items)
    return ('<!--up--><details id="upcoming" style="margin:18px 0 0;border:0.5px solid #dfe5e9;border-left:4px solid #8a949b;border-radius:0 12px 12px 0;background:color-mix(in srgb,#8a949b 6%%,#fff);padding:0 14px">'
            '<summary style="cursor:pointer;padding:10px 0;font-size:14px;font-weight:700">これから変わること(%d件)<span style="font-size:12px;font-weight:400;color:#64717a"> ・ 発表済みで、まだ実施されていない変更</span></summary>%s</details><!--/up-->')%(len(items),body)
def apply(s,today=None):
    today=today or datetime.date.today()
    items=[x for x in json.load(open('data/upcoming.json'))['items'] if datetime.date.fromisoformat(x['date'])>=today]
    items.sort(key=lambda x:x['date'])
    s=re.sub(r'<!--up-->.*?<!--/up-->','',s,flags=re.S)
    if not items: return s
    k='<h2>代表的な動き</h2>'; assert k in s
    return s.replace(k,block(items)+k,1)
if __name__=='__main__':
    p='docs/index.html'; s=open(p).read(); open(p,'w').write(apply(s))
