import re,html
D='/home/claude/ai-map/docs/'
CH="display:block;box-sizing:border-box;font-size:12px;line-height:1.5;padding:4px 10px;border:0.5px solid #c9d0d3;border-radius:14px;color:#64717a;text-decoration:none;margin-top:6px"
CUR=";border-color:#1f2a30;background:#f4f6f7;color:#1f2a30"
def chip(spans,href,cur):
    inner=''.join('<span style="display:inline-block">%s</span>'%x for x in spans)
    if cur: return '<span style="%s%s">%s</span>'%(CH,CUR,inner)
    return '<a href="%s" style="%s">%s</a>'%(href,CH,inner)
def col(name,color,desc,chips):
    d='・'.join('<span style="display:inline-block">%s</span>'%x for x in desc)
    return ('<div class="rc"><div class="rn" style="color:%s;border-color:%s;background:%s1a">%s</div>'
            '<div class="rr"><div class="rd" style="font-size:13.5px;line-height:1.8;color:#1f2a30">%s</div><div class="cs">%s</div></div></div>')%(color,color,color,name,d,chips)
def roles(page):
    c=lambda spans,href,key: chip(spans,href,page==key)
    cols=[
     col('調べる','#5b8fc9',['探す','まとめる'],c(['AIに聞く・','書く'],'zukan-ai.html','ai')),
     col('作る','#d27a58',['動画','資料','画像','文章'],c(['動画'],'zukan-video.html','video')+c(['資料'],'zukan-slides.html','slides')+c(['画像'],'zukan-image.html','image')),
     col('整理する','#3f9d86',['表','フォルダ','メモ'],c(['表・メモ','を整える'],'zukan-organize.html','organize')),
     col('代わりに動く','#8579cf',['手順を踏んで','進める'],c(['代わりに動く'],'zukan-agent.html','agent')),
     col('判断','#c19a3b',['AIに頼まない','自分の役割'],chip(['AIと向き合うために →'],'checklist.html',False)),
    ]
    return ('<div class="rs" style="margin-top:12px">'+''.join(cols)+'</div><!--re-->')
END='<!--re-->'
def swap(s,page):
    a=s.find('<div class="rs"'); b=s.find(END,a)+len(END)
    return s[:a]+roles(page)+s[b:]
# ---- cards
LINK="display:inline-block;margin:2px 0 0 4px;font-size:11.5px;font-weight:400;line-height:1.6;color:#2d5f94;border:0.5px solid #9db9d9;border-radius:10px;padding:0 9px;text-decoration:none;vertical-align:middle;white-space:nowrap"
def row(color,label,tag,text):
    return ('<div style="margin-top: 18px"><div style="display: flex; align-items: center; flex-wrap: wrap; gap: 4px 10px; border-bottom: 0.5px solid #e3e8eb; padding-bottom: 4px">'
     '<span style="font-size: 13px; font-weight: 700; color: %s">%s</span><span style="font-size: 11.5px; color: #64717a">(%s)</span></div>'
     '<div style="margin-top: 6px; font-size: 14.5px; line-height: 1.9">%s</div></div>')%(color,label,tag,text)
def src(links):
    a=''.join('<a href="%s" target="_blank" rel="noopener" style="color:#2d5f94;border-bottom:0.5px solid #9db9d9;text-decoration:none">%s</a>'%(u,t) for t,u in links)
    return '<div style="display:flex;gap:12px;margin-top:10px;font-size:13px;line-height:1.8"><span style="width:44px;flex:none;color:#64717a;font-size:11.5px">確認元</span><span style="display:flex;flex-wrap:wrap;gap:2px 14px">%s</span></div>'%a
def card(color,name,url,one,rows,links):
    r=''.join(row(color,*x) for x in rows)
    return ('<div style="margin-top: 26px; border-left: 2px solid %s; padding: 2px 0 2px 14px"><div style="font-size: 16px; font-weight: 700; line-height: 1.5; color: #1f2a30">%s '
     '<a href="%s" target="_blank" rel="noopener" style="%s">公式サイト ↗</a></div><div style="font-size: 12.5px; line-height: 1.6; color: #64717a; margin-top: 2px">%s</div>%s%s</div>')%(color,name,url,LINK,one,r,src(links))
OF='確認元:公式ページ'; NG='確認できず'; CD='条件あり'
IMG=[
 ('ChatGPT(画像生成)','https://chatgpt.com/','会話しながら、画像を作ったり直したりできるAI。',[
  ('できること',OF,'ChatGPTの中で、文章から画像を作れます。公式の発表では、最新の「Images 2.6」で生成が速くなり、GIFの作成と、細かい編集にも対応したとあります。'),
  ('費用',OF,'無料プランでも使えますが、画像生成には別の回数制限があり、上限に達すると画面で知らせてくれます。有料プランでは上限が上がります。回数は変わるので、画面と公式ページで確認してください。'),
  ('日本',NG,'Images 2.6は「すべての有料プランで世界的に提供」と公式にありますが、日本が名指しされた記載は確認できませんでした。')],
  [('Images 2.6の発表','https://openai.com/index/introducing-images-2-6/'),('無料プランの案内','https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq')]),
 ('Gemini(画像生成)','https://gemini.google/jp/','GoogleのAIアプリ。画像の生成と編集ができる。',[
  ('できること',OF,'Geminiアプリで、画像を作ったり、写真を直したりできます。日本語での画像生成は、公式ブログで対応が案内されています。'),
  ('費用',OF,'無料で使えます。生成できる枚数には上限があり、毎日リセットされますが、需要によって頻繁に変わると公式ヘルプにあります。有料のGoogle AIプランでは上限が大きくなります。'),
  ('条件',CD,'画像の生成・編集は、18歳以上が対象と公式ヘルプにあります。学校用アカウントでは、制限が異なる場合があります。')],
  [('画像を生成・編集するヘルプ','https://support.google.com/gemini/answer/14286560?hl=ja'),('使用量の上限','https://support.google.com/gemini/answer/16275805?hl=ja'),('日本向けの案内','https://gemini.google/jp/overview/image-generation/?hl=ja-JP')]),
 ('Canva','https://www.canva.com/ja_jp/','チラシやSNS用の画像を、テンプレートからつくれるデザインのサービス。',[
  ('できること',OF,'「マジック生成」で、文章を入力すると画像ができます。作った画像は、そのままチラシやポスターのデザインに使えます。'),
  ('費用',OF,'無料プランがあり、AI画像生成は月に50回まで試せると、Canva公式の解説ページにあります。一部の機能は有料で、AIブラシは無料だと1日25回までです。'),
  ('日本',OF,'日本語の公式ページで、使い方と無料での利用が案内されています。')],
  [('AI画像生成の解説','https://www.canva.com/ja_jp/learn/what-is-generative-ai/'),('AIポスター','https://www.canva.com/ja_jp/features/ai-poster/')]),
 ('Adobe Firefly','https://www.adobe.com/jp/products/firefly.html','Adobeの画像・動画づくりのサービス。',[
  ('できること',OF,'文章から画像や動画を作れます。Adobe自身のモデルは、使用許諾のある素材などで学習されていて、商用利用できると公式にあります。'),
  ('費用',OF,'無料プランに、1日あたりの無料生成回数が含まれます。上限を超えると有料プランが必要です。'),
  ('条件',CD,'他社(パートナー)のモデルで作った画像は、利用条件が異なる場合があります。ベータ版の機能は、商用利用の対象外になることがあります。')],
  [('Fireflyの公式ページ','https://www.adobe.com/jp/products/firefly.html'),('商用利用のFAQ','https://www.adobe.com/jp/products/firefly/features/image-to-image.html')]),
]
ORG=[
 ('Claude Sheets','https://claude.com/','Claudeの中で、AIと一緒に編集できる表計算。',[
  ('できること',OF,'表や数式をClaudeに頼んで作り、人とClaudeが同じセルを編集できます。Excelなど本格的な機能が要るときは、.xlsxやCSVで書き出せます。同じ場所のWhiteboards(共有の書き込みボード)も同じベータです。'),
  ('条件',CD,'ベータ版で、有料プラン(Pro・Max・Ultra・Team・Enterprise)が対象です。無料プランは対象外です。連携したアプリの最新データは取り込めず、スマホでは見るだけです。'),
  ('日本',NG,'日本での提供や画面の言語について、公式ページで名指しの記載は確認できませんでした。')],
  [('使い始めガイド','https://support.claude.com/en/articles/18324300-get-started-with-claude-sheets'),('発表','https://claude.com/resources/articles/sheets-whiteboards-data')]),
 ('Gemini in Google スプレッドシート','https://workspace.google.com/products/sheets/','Googleの表計算に、Geminiが入ったもの。',[
  ('できること',OF,'表や数式を作る、データを分析する、グラフを作る、といったことを、文章で頼めます。Excelのファイルは、Googleスプレッドシート形式で保存すると使えます。'),
  ('条件',CD,'対象のGoogle WorkspaceまたはGoogle AIのプランが必要です。スマホでは、分析はできますが、表の直接の編集はできません。'),
  ('日本',OF,'日本語の公式ヘルプがあります。一部の言語ではAI機能が使えないことがあると、公式に書かれています。')],
  [('スプレッドシートでの使い方','https://support.google.com/docs/answer/14356410?hl=ja'),('サービスの紹介','https://workspace.google.com/products/sheets/')]),
 ('Excel の Copilot','https://www.microsoft.com/microsoft-365/excel','Microsoftの表計算に、AIのCopilotが入ったもの。',[
  ('できること',OF,'ワークシートの編集、データの生成と変換、強調表示・並べ替え・フィルター、Webからの情報の取得ができると、公式のよくある質問にあります。'),
  ('条件',CD,'AIクレジットを含むMicrosoft 365 Personal・Family、Premium、商用のCopilot、Copilot Chat対象のビジネス向けプランのどれかが必要です。使えるかは、ライセンスと(組織の場合は)管理者の設定で変わります。'),
  ('費用',NG,'日本円の料金は、今回確認できた公式ページでは読み取れませんでした。日本の料金ページで確認してください。')],
  [('Excel の Copilot よくある質問','https://support.microsoft.com/ja-jp/office/excel-%E3%81%AE-copilot-%E3%81%AB%E9%96%A2%E3%81%97%E3%81%A6%E3%82%88%E3%81%8F%E5%AF%84%E3%81%9B%E3%82%89%E3%82%8C%E3%82%8B%E8%B3%AA%E5%95%8F-7a13758f-d61e-4a56-8440-f2c9a07802ec')]),
 ('Notion','https://www.notion.com/','メモ・表・予定を、1つの場所にまとめて整理するサービス。',[
  ('できること',OF,'メモや表を1か所にまとめられます。無料のFreeプランは、個人が自分の予定やメモを整理する用途向けと、公式ヘルプにあります。'),
  ('費用',CD,'AI機能は、FreeとPlusでは回数が限られ、お試し向けと公式ヘルプにあります。AIを続けて使うには、上のプランが必要です。料金ページは米ドル表記で、日本円の料金は確認できませんでした。'),
  ('日本',NG,'日本での提供や、日本語の画面について、今回確認できた公式ページに名指しの記載はありませんでした。')],
  [('プランの変更','https://www.notion.com/help/upgrade-or-downgrade-your-plan'),('料金','https://www.notion.com/pricing')]),
]
def build(page,title,cards,color,extra=''):
    s=open(D+'zukan-slides.html').read()
    s=s.replace('サービス図鑑 資料 |','サービス図鑑 %s |'%title)
    s=swap(s,page)
    a=s.find('\n<div style="margin-top: 18px; background: #fbf6e7')
    b=s.find('<div style="margin-top: 28px; background: #eef4fb')
    body=extra+''.join(card(color,*c) for c in cards)
    s=s[:a]+'\n'+body+'\n'+s[b:]
    open(D+'zukan-%s.html'%page,'w').write(s)
NOTE='<div style="margin-top: 18px; background: #fbf6e7; border-left: 2px solid #c19a3b; padding: 12px 16px; font-size: 13px; line-height: 1.7">フォルダの整理をAIに頼む方法は、<a href="templates.html" style="color:#2d5f94;border-bottom:0.5px solid #9db9d9">テンプレ集の「フォルダの整理を頼む」</a>にあります。ここでは、表とメモを整えるサービスを載せています。</div>'
if __name__=='__main__':
    build('image','画像',IMG,'#d27a58')
    build('organize','整理',ORG,'#3f9d86',NOTE)
    for p in ['video','slides','ai','agent']:
        f=D+'zukan-%s.html'%p; s=open(f).read(); open(f,'w').write(swap(s,p))
