# 「AI機能5分類」(色と機能の一覧)を、サブタイトルの下・メニューの上に入れる。全ページ共通。
import re,sys
SUB='まわりではAI・Webサービスがどう活用されているのかを、会社や組織に所属していなくても、はじめの一歩がわかるように説明していきます。'
CATS=[('調べる','#5b8fc9','探す・まとめる'),('作る','#d27a58','動画・資料・画像・文章'),('整理する','#3f9d86','表・フォルダ・メモ'),('代わりに動く','#8579cf','手順を踏んで進める'),('判断','#c19a3b','AIに頼まない・自分の役割')]
def block(inmain=False):
    items=''.join('<div style="flex:1 1 auto;text-align:center;padding:4px 6px 5px;border-bottom:3px solid %s;font-size:13px;font-weight:700;color:#1f2a30;white-space:nowrap">%s</div>'%(c,n) for n,c,f in CATS)
    box="max-width:640px;margin:0 auto 14px;padding:0 20px;box-sizing:border-box;font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN','Yu Gothic',Meiryo,sans-serif;line-height:1.8" if not inmain else "margin:0 0 14px"
    return '<div id="cats" style="%s"><div style="font-size:13px;font-weight:700;color:#64717a;margin-bottom:6px">AI機能5分類</div><div style="display:flex;flex-wrap:wrap;gap:4px">%s</div></div>'%(box,items)
def apply(s):
    s=re.sub(r'<div id="cats".*?</div></div></div>\n?','',s,flags=re.S) if 'id="cats"' in s else s
    i=s.find(SUB); assert i>=0
    o=s.rfind('<',0,i); name=re.match(r'<(\w+)',s[o:]).group(1)
    j=s.find('</%s>'%name,i)+len(name)+3
    s=s[:j]+block('<main>' in s)+s[j:]
    return band(s,'<main>' in s)
BAND='#f3f6f8'
def band(s,inmain):
    # 5分類とメニュー(タブ)を、薄い色の帯でまとめる(「ここがメイン」の目印)。5分類の帯とメニューの帯の間は、白い余白で切り離す。何度実行しても同じ結果になる。
    s=re.sub(r'<style id="bandstyle">.*?</style>','',s,flags=re.S)
    s=re.sub(r'<div id="(?:band|catsband|tabsband)"[^>]*>','',s)
    for k in ('band','catsband','tabsband'): s=s.replace('</div><!--/%s-->'%k,'')
    a=s.find('<div id="cats"'); n=s.find('<nav',a); e=s.find('</nav>',n)+6
    assert a>=0 and n>a and e>n
    nav=s[n:e]
    # メニューの幅: 最大640pxの中を、端から端まで使う(余白なし)。文字は各タブの真ん中にそろえる
    nst=('display:flex;gap:0;margin:0 -20px;padding:0;' if inmain
         else 'display:flex;gap:0;max-width:640px;margin:0 auto;padding:0;box-sizing:border-box;')
    nav=re.sub(r'^<nav style="[^"]*"','<nav style="%s"'%nst,nav,count=1)
    nav=nav.replace(';text-align:center','')
    nav=re.sub(r'(<a href="[^"]*" style="[^"]*?);?"',lambda m:m.group(1)+';text-align:center"',nav)
    if inmain and s[e:].startswith('<div id="subtabs"'):  # トップの下段メニュー(総評 / 代表的な動き / 発表済み変更点)
        e2=s.find('<!--/subtabs-->',e)+len('<!--/subtabs-->'); sub=s[e:e2]
    else:
        m=re.match(r'\s*<div style="max-width:640px;margin:0 auto;padding:0(?: 20px)?(?:;box-sizing:border-box)?"><div style="display:flex;(?:flex-wrap:wrap;)?gap:',s[e:])
        e2=s.find('</div></div>',e)+12 if m else e
        sub=fullw(snfit(vline(s[e:e2])))
        sub=sub.replace('max-width:640px;margin:0 auto;padding:0 20px','max-width:640px;margin:0 auto;padding:0;box-sizing:border-box',1)
    sub=sub.replace(';border-bottom:0.5px solid #dfe5e9','').replace('border-bottom:0.5px solid #dfe5e9;','').replace('border-bottom:0.5px solid #dfe5e9','')
    cs='background:%s;margin:0 -20px;padding:10px 20px 0'%BAND if inmain else 'background:%s;max-width:640px;margin:0 auto;padding:10px 0 0;box-sizing:border-box'%BAND
    ts='background:%s;margin:12px -20px 0;padding:0 20px'%BAND if inmain else 'background:%s;max-width:640px;margin:12px auto 0;box-sizing:border-box'%BAND
    css=('<style id="bandstyle">@media(min-width:681px){#tabsband>nav,#tabsband>#subtabs{margin-left:0!important;margin-right:0!important}#catsband,#tabsband{margin-left:0!important;margin-right:0!important;padding-left:0!important;padding-right:0!important}#catsband #cats{padding-left:20px!important;padding-right:20px!important}}</style>')
    if not inmain: css=''
    out=(s[:a]+css+'<div id="band" style="font-family:\'Noto Sans JP\',\'Hiragino Kaku Gothic ProN\',\'Yu Gothic\',Meiryo,sans-serif">'
         +'<div id="catsband" style="%s">'%cs+s[a:n]+'</div><!--/catsband-->'
         +'<div id="tabsband" style="%s">'%ts+vline(nav)+sub+'</div><!--/tabsband-->'
         +'</div><!--/band-->'+s[e2:])
    if inmain:
        out=re.sub(r'(<!--/band-->\s*(?:<div id="pane-sohyo">)?<h2 style=")margin-top:\d+px',r'\1margin-top:28px',out,count=1)
    return out
def fullw(t):
    # 図鑑の下段メニュー(目的から選ぶ / 連携チェック)は、画面の横幅いっぱいに2等分する
    if 'justify-content:center' not in t: return t
    t=t.replace('max-width:640px;margin:0 auto;padding:0 20px','max-width:640px;margin:0 auto;padding:0',1).replace('display:flex;gap:32px;justify-content:center','display:flex;gap:0',1)
    return re.sub(r'(<a href="[^"]*" style="[^"]*)"',lambda m: m.group(1)+('' if 'flex:1 1 0' in m.group(1) else ';flex:1 1 0;text-align:center;padding-left:0')+'"',t)
def snfit(t):
    # 学ぶ側の5つの選択肢は、横にスクロールさせず、字の大きさを画面幅に合わせて1段に収める
    if 'class="sn"' not in t: return t
    t=re.sub(r'display:flex;(?:flex-wrap:wrap;)?gap:\d+px','display:flex;gap:0',t,count=1)
    t=t.replace(';overflow-x:auto','')
    k=[0]
    def f(m):
        k[0]+=1
        st=m.group(2)
        col=re.search(r'color:(#[0-9a-f]+)',st).group(1)
        act='font-weight:700;border-bottom:2px solid #1f2a30;' if 'font-weight:700' in st else ''
        v=';background:linear-gradient(#cfd6da,#cfd6da) left 22%/1px 56% no-repeat' if k[0]>1 else ''
        return m.group(1)+'padding:10px 3px 8px;font-size:min(12px,calc((100vw - 70px)/31.5));line-height:1.4;text-decoration:none;color:'+col+';'+act+'white-space:nowrap;flex:1 1 auto;text-align:center'+v+'"'
    return re.sub(r'(<a href="[^"]*" style=")([^"]*)"',f,t)
VL=';background:linear-gradient(#cfd6da,#cfd6da) left 22%/1px 56% no-repeat'
def vline(t):
    # 並んだ選択肢の間に、細い縦線を入れる(2つ目以降の左側)。何度実行しても同じ結果になる。
    t=t.replace(VL,'')
    k=[0]
    def f(m):
        k[0]+=1
        return m.group(0) if k[0]==1 else m.group(1)+VL+'"'
    return re.sub(r'(<a href="[^"]*" style="[^"]*)"',f,t)
if __name__=='__main__':
    for f in ['index','start7','setup','templates','checklist','tips','zukan-link','zukan-video','zukan-slides','zukan-ai','zukan-agent','zukan-image','zukan-organize']:
        p='docs/%s.html'%f; s=open(p).read(); s=apply(s); open(p,'w').write(s)
