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
    # 5分類とメニュー(タブ)を、薄い色の帯でまとめる(「ここがメイン」の目印)。何度実行しても同じ結果になる。
    s=re.sub(r'<div id="band"[^>]*>','',s); s=s.replace('</div><!--/band-->','')
    a=s.find('<div id="cats"'); n=s.find('<nav',a); e=s.find('</nav>',n)+6
    assert a>=0 and n>a and e>n
    nav=s[n:e]
    if inmain: nav=nav.replace('margin:0 -20px 16px','margin:0 -20px',1)
    st='background:%s;margin:0 -20px 16px;padding:10px 20px 0'%BAND if inmain else 'background:%s;padding:10px 0 0'%BAND
    # 下段メニュー(目的から選ぶ/最初の7日間 など)がある頁は、それも帯に入れる
    m=re.match(r'\s*<div style="max-width:640px;margin:0 auto;padding:0 20px"><div style="display:flex;gap:',s[e:])
    if m:
        k=s.find('</div></div>',e)+12; e2=k
    else: e2=e
    return s[:a]+'<div id="band" style="%s">'%st+s[a:n]+vline(nav)+vline(s[e:e2])+'</div><!--/band-->'+s[e2:]
VL=';padding-left:10px;background:linear-gradient(#cfd6da,#cfd6da) left 22%/1px 56% no-repeat'
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
