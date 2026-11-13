#!/usr/bin/env python3
"""連携チェック(docs/zukan-link.html)の各カードから、組ごとのページ docs/link-<ai>-<svc>.html と
docs/sitemap.xml を作り直す。一覧側のカードの末尾に「この組だけのページ」リンクも入れる。
使い方: python3 tools/build_pairs.py  (zukan-link.html を直したあとに毎回実行して、一緒にcommitする)"""
import re, glob, os, html
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')
BASE='https://sazare-ishi.github.io/ai-map/'
src=open(os.path.join(ROOT,'zukan-link.html'),encoding='utf-8').read()
tag=re.compile(r'<div\b|</div>')
M1,M2='<!--pairlink-->','<!--/pairlink-->'
# ヘッダー(サイト名〜メニュー)と、中身を包む div の開きタグ
hs=src.index('<div style="max-width: 640px; margin: 0 auto; box-sizing')
head=src[:hs]; wrap=src[hs:src.index('>',hs)+1]
# カード切り出し
cards=[];pos=0
while True:
    i=src.find('<div class="lk"',pos)
    if i<0: break
    d=0
    for m in tag.finditer(src,i):
        d+=1 if m.group().startswith('<div') else -1
        if d==0: end=m.end();break
    cards.append((i,end,src[i:end]));pos=end
def attr(c,k): return re.search(k+'="([^"]*)"',c).group(1)
def clean(c): return re.sub(re.escape(M1)+'.*?'+re.escape(M2),'',c,flags=re.S)
info=[]
for i,e,c in cards:
    c=clean(c)
    ai,svc=attr(c[:200],'data-ai'),attr(c[:200],'data-svc').split()[0]
    name=html.unescape(re.sub('<.*?>','',re.search(r'color: #1f2a30">(.*?)</div>',c).group(1)))
    info.append(dict(ai=ai,svc=svc,name=name,card=c,file='link-%s-%s.html'%(ai,svc)))
LINK='<a href="%s" style="font-size:13px;color:#2d5f94;border-bottom:0.5px solid #9db9d9;text-decoration:none">この組だけのページ</a>'
# 一覧側にリンクを足す(作り直し可能)
out=[];p=0
for (i,e,c),it in zip(cards,info):
    new=clean(c); k=new.rindex('</div>')
    new=new[:k]+M1+'<div style="margin-top: 12px">'+LINK%it['file']+'</div>'+M2+new[k:]
    out.append(src[p:i]);out.append(new);p=e
out.append(src[p:]);open(os.path.join(ROOT,'zukan-link.html'),'w',encoding='utf-8').write(''.join(out))
# 個別ページ
for f in glob.glob(os.path.join(ROOT,'link-*.html')): os.remove(f)
def li(it): return '<a href="%s" style="color:#2d5f94;border-bottom:0.5px solid #9db9d9;text-decoration:none">%s</a>'%(it['file'],html.escape(it['name']))
for it in info:
    t=html.escape(it['name'])
    title='%s は連携できる? | 連携チェック | AIマップ はじめの一歩'%t
    desc='%s がつながるかを、サービス側の公式ページに書かれていることで確認します。判定・条件・確認元の公式リンクつき。'%t
    h=head.replace('<title>サービス図鑑 連携チェック | AIマップ はじめの一歩</title>','<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s%s">'%(title,html.escape(desc,quote=True),BASE,it['file']))
    same=[x for x in info if x is not it and (x['ai']==it['ai'] or x['svc']==it['svc'])]
    rel=''.join('<div style="margin-top:6px">%s</div>'%li(x) for x in same)
    body=(wrap+'<div style="font-size:13px;line-height:1.7"><a href="zukan-link.html" style="color:#2d5f94;border-bottom:0.5px solid #9db9d9;text-decoration:none">← 連携チェックの一覧へ</a></div>'
      +it['card'].replace('margin-top: 26px','margin-top: 16px',1)
      +'<div style="margin-top:18px;background:#f3f7fb;border-left:2px solid #5b8fc9;padding:12px 16px;font-size:13px;line-height:1.7">分からないときは、自分のAIに確認元の公式ページを読ませて、「公式ページに書かれていないことは、書かれていないと答えて」と頼んでみてください。判定は、サービス側の公式ページに書かれていることで決めています。書かれていない=できない、ではありません。料金・機能は変わるので、最後は公式ページで確認してください。</div>'
      +'<div style="margin-top:32px;display:flex;gap:10px"><a href="zukan-link.html" style="flex:1 1 0;text-align:center;padding:12px 8px;font-size:14px;line-height:1.5;color:#2d5f94;background:#eef4fb;border:0.5px solid #9db9d9;border-radius:4px;text-decoration:none">ほかの連携も見る</a><a href="index.html" style="flex:1 1 0;text-align:center;padding:12px 8px;font-size:14px;line-height:1.5;color:#1f2a30;background:#fff;border:0.5px solid #c9d0d3;border-radius:4px;text-decoration:none">AIマップのトップへ</a></div>'
      +'</div></body></html>')
    open(os.path.join(ROOT,it['file']),'w',encoding='utf-8').write(h+body)
# sitemap
urls=[BASE]+[BASE+x for x in ['zukan-video.html','zukan-slides.html','zukan-ai.html','zukan-agent.html','zukan-link.html','start7.html','setup.html','templates.html','checklist.html','tips.html']]+[BASE+it['file'] for it in info]
open(os.path.join(ROOT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>%s</loc></url>\n'%u for u in urls)+'</urlset>\n')
open(os.path.join(ROOT,'robots.txt'),'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n'%BASE)
print(len(info),'pairs')
