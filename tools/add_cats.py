# 「AI機能5分類」(色と機能の一覧)を、サブタイトルの下・メニューの上に入れる。全ページ共通。
import re,sys
SUB='まわりではAI・Webサービスがどう活用されているのかを、会社や組織に所属していなくても、わかりやすく説明していきます。'
CATS=[('調べる','#5b8fc9','探す・まとめる'),('作る','#d27a58','動画・資料・画像・文章'),('整理する','#3f9d86','表・フォルダ・メモ'),('代わりに動く','#8579cf','手順を踏んで進める'),('判断','#c19a3b','AIに頼まない・自分の役割')]
def block(inmain=False):
    items=''.join('<div style="--c:%s;flex:1 1 auto;text-align:center;padding:5px 7px;border:0.5px solid #dfe5e9;border-left:3px solid %s;border-radius:10px;background:#fff;font-size:12.5px;font-weight:600;color:#44525b;white-space:nowrap">%s</div>'%(c,c,n) for n,c,f in CATS)
    box="max-width:640px;margin:0 auto 14px;padding:0 20px;box-sizing:border-box;font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN','Yu Gothic',Meiryo,sans-serif;line-height:1.8" if not inmain else "margin:0 0 14px"
    return '<div id="cats" style="%s"><div style="font-size:12px;font-weight:700;color:#64717a;margin-bottom:6px">AI機能5分類</div><div style="display:flex;flex-wrap:wrap;gap:4px">%s</div></div>'%(box,items)
def apply(s):
    s=re.sub(r'<div id="cats".*?</div></div></div>\n?','',s,flags=re.S) if 'id="cats"' in s else s
    i=s.find(SUB); assert i>=0
    o=s.rfind('<',0,i); name=re.match(r'<(\w+)',s[o:]).group(1)
    j=s.find('</%s>'%name,i)+len(name)+3
    return s[:j]+block('<main>' in s)+s[j:]
if __name__=='__main__':
    for f in ['index','start7','setup','templates','checklist','tips','zukan-link','zukan-video','zukan-slides','zukan-ai','zukan-agent','zukan-image','zukan-organize']:
        p='docs/%s.html'%f; s=open(p).read(); s=apply(s); open(p,'w').write(s)
