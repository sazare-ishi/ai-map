import sys; sys.path.insert(0,'tools')
from build_zukan_new import card,OF,NG,CD,D
VID=('Google Vids','https://workspace.google.com/products/vids/','Googleの、AIで動画を作れる動画編集ツール。',[
 ('できること',OF,'台本を作り、ナレーションや動画クリップに使えます。公式の発表では、Googleアカウントがあれば、AIで動画を作る機能を無料で試せます。新しいモデルでは、月に3本まで、15秒の動画を無料で作れると案内されています。'),
 ('条件',CD,'動画の作成は、パソコンのブラウザから使う案内です。AIナレーションなどは、アカウントの種類(個人・Workspace・Google AIプラン)で、回数や使えるプランが変わります。公式ヘルプの表で確認してください。'),
 ('日本',NG,'日本語の公式ヘルプはあります。ただ、AIナレーションが日本語に対応しているかは、今回読めた範囲では確認できませんでした。')],
 [('AI動画の発表(無料の範囲)','https://blog.google/products-and-platforms/products/workspace/omni-1-2-flash-google-vids/'),('AIナレーションのヘルプ','https://support.google.com/docs/answer/15070345?hl=ja'),('機能の提供状況','https://support.google.com/docs/answer/15609411?hl=ja')])
FLOW=('Google Flow','https://labs.google/fx/ja/tools/flow','Googleの、映画のような動画やシーンを作るAI映像制作ツール。',[
 ('できること',OF,'一貫性のあるクリップ・シーン・ストーリーを作れます。パソコンでは高度な編集、スマホでは外出先での制作と、使い分けられます。'),
 ('費用',OF,'Google AIの有料プランに入っていなくても、基本的な動画生成と編集を使えます。お試し用に、1日50クレジットが付きます。有料プランでは、月ごとのクレジットが加わります。'),
 ('条件',CD,'18歳以上で、Flowの対象地域に住んでいる必要があります。サブスクリプションがないと、混み合う時間帯(UTCの午後2時〜5時ごろ)は動画を生成できないことがあります。'),
 ('日本',NG,'日本向けのGeminiの料金ページにFlowのクレジットが載っています。ただ、対象地域の一覧は今回読めず、日本が入っているかは確認できませんでした。')],
 [('Flowを使ってみる(ヘルプ)','https://support.google.com/flow/answer/16353333?hl=ja'),('クレジットの管理','https://support.google.com/flow/answer/16526234?hl=ja'),('Geminiの料金(日本)','https://gemini.google/jp/subscriptions/?hl=ja')])
NB=('Gemini Notebook(旧NotebookLM)','https://support.google.com/notebooklm/answer/16164461?hl=ja','自分の資料をもとに、質問に答えたり、まとめたりしてくれるGoogleのAI。',[
 ('できること',OF,'PDF・Webサイト・YouTube動画・音声・Googleドキュメントやスライドを入れると、その資料をもとに、引用つきで答えてくれます。学習ガイド・概要説明資料・音声概要・マインドマップにも変換できます。'),
 ('条件',CD,'利用にはGoogleアカウントでの年齢確認が必要です。学校や職場のアカウントでは、組織の管理者が有効にする必要があります。動画解説は、Google AI Ultraの契約者だけが使えます。上限はGoogle AIプランで引き上げられます。'),
 ('日本',OF,'音声概要が日本語を含む50以上の言語で使えると、日本語の公式ブログにあります。ヘルプには、80以上の言語に対応とあります。')],
 [('詳細(ヘルプ)','https://support.google.com/notebooklm/answer/16164461?hl=ja'),('音声解説','https://support.google.com/notebooklm/answer/16212820?hl=ja'),('日本語の公式ブログ','https://blog.google/intl/ja-jp/company-news/technology/notebooklm-50/')])
M='<div style="margin-top: 28px; background: #eef4fb'
def add(page,cards,color):
    f=D+'zukan-%s.html'%page; s=open(f).read(); i=s.find(M)
    s=s[:i]+''.join(card(color,*c) for c in cards)+'\n'+s[i:]; open(f,'w').write(s)
add('video',[VID,FLOW],'#d27a58'); add('ai',[NB],'#5b8fc9')
