# 「AI機能5分類」(色と機能の一覧)を、サブタイトルの下・メニューの上に入れる。全ページ共通。
import re,sys
SUB='まわりではAI・Webサービスがどう活用されているのかを、会社や組織に所属していなくても、わかりやすく説明していきます。'
CATS=[('調べる','#5b8fc9','探す・まとめる'),('作る','#d27a58','動画・資料・画像・文章'),('整理する','#3f9d86','表・フォルダ・メモ'),('代わりに動く','#8579cf','手順を踏んで進める'),('判断','#c19a3b','AIに頼まない・自分の役割')]
def block():
    items=''.join('<div style="--c:%s;display:flex;align-items:baseline;gap:10px;min-width:0;padding:3px 10px;border:0.5px solid %s;border-left:3px solid %s;border-radius:10px;background:color-mix(in srgb,%s 7%%,#fff);"><span style="flex:none;width:84px;font-size:13px;font-weight:700;color:%s">%s</span><span style="font-size:12.5px;color:#1f2a30">%s</span></div>'%(c,c,c,c,c,n,f) for n,c,f in CATS)
    return '<div id="cats" style="margin:0 0 14px"><div style="font-size:12px;font-weight:700;color:#64717a;margin-bottom:6px">AI機能5分類</div><div style="display:flex;flex-direction:column;gap:4px">%s</div></div>'%items
def apply(s):
    s=re.sub(r'<div id="cats".*?</div></div></div>\n?','',s,flags=re.S) if 'id="cats"' in s else s
    i=s.find(SUB); assert i>=0
    o=s.rfind('<',0,i); name=re.match(r'<(\w+)',s[o:]).group(1)
    j=s.find('</%s>'%name,i)+len(name)+3
    return s[:j]+block()+s[j:]
if __name__=='__main__':
    for f in ['index','start7','setup','templates','checklist','tips','zukan-link','zukan-video','zukan-slides','zukan-ai','zukan-agent','zukan-image','zukan-organize']:
        p='docs/%s.html'%f; s=open(p).read(); s=apply(s); open(p,'w').write(s)
