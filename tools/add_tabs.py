# トップ(index.html)に、下段メニュー「総評 / 代表的な動き / 発表済み変更点(未実施分)」を入れる(連携チェックなどの下段メニューと同じ見た目)。
# 毎週 index.html を更新したあと、add_cats.py → add_filter.py → add_upcoming.py → このスクリプトの順に実行する。何度実行しても同じ結果になる。
import re
P='docs/index.html'
ON='padding:10px 0 8px;font-size:min(13px,calc((50vw - 14px)/14));line-height:1.4;text-decoration:none;color:#1f2a30;font-weight:700;border-bottom:2px solid #1f2a30;'
OFF='padding:10px 0 8px;font-size:min(13px,calc((50vw - 14px)/14));line-height:1.4;text-decoration:none;color:#64717a;'
LN=';background:linear-gradient(#cfd6da,#cfd6da) left 22%/1px 56% no-repeat'
X1=';flex:8 1 0;text-align:center;padding-left:0;padding-right:0'
X2=';flex:12 1 0;text-align:center;padding-left:0;padding-right:0'+LN
X3=';flex:20 1 0;text-align:center;padding-left:0;padding-right:0'+LN
def apply(s):
    # 前回の入れ物・メニュー・スクリプトを外す
    s=re.sub(r'<div id="subtabs".*?</div><!--/subtabs-->','',s,flags=re.S)
    s=re.sub(r'<script id="tabscript">.*?</script>','',s,flags=re.S)
    s=re.sub(r'<style id="tabstyle">.*?</style>','',s,flags=re.S)
    s=re.sub(r'<div id="pane-(sohyo|ugoki|shin)"[^>]*>','',s); s=s.replace('</div><!--/pane-->','')
    # 前回の「発表済み変更点」の欄を、元の位置(「代表的な動き」の見出しの前)にもどす
    m=re.search(r'<!--up-->.*?<!--/up-->',s,flags=re.S)
    if m:
        blk=m.group(0).replace(' open ',' ',1); s=s.replace(m.group(0),'',1)
        s=s.replace('<h2>代表的な動き</h2>',blk+'<h2>代表的な動き</h2>',1)
    s=re.sub(r'<p style="color:#64717a">いまのところ、発表済みで、まだ実施されていない変更はありません。</p>','',s)
    a=s.find('<h2 style="margin-top:'); assert a>=0
    h=s.find('<h2>代表的な動き</h2>',a); assert h>a
    u=s.find('<!--up-->',a); has_up=0<=u<h
    if not has_up: u=h
    last=s.rfind('</article>'); assert last>h
    e=last+len('</article>')
    if has_up:
        up=s[u:h]
    else:
        up='<p style="color:#64717a">いまのところ、発表済みで、まだ実施されていない変更はありません。</p>'
    s=(s[:a]+'<div id="pane-sohyo" style="margin-top:28px">'+s[a:u]+'</div><!--/pane-->'
       +'<div id="pane-ugoki" hidden style="margin-top:28px">'+s[h:e]+'</div><!--/pane-->'
       +'<div id="pane-shin" hidden style="margin-top:28px">'+up+'</div><!--/pane-->'+s[e:])
    # 下段メニュー(帯の中、上段メニューの下)
    tabs=('<div id="subtabs" style="display:flex;gap:0;margin:0 -20px;border-bottom:0.5px solid #dfe5e9">'
          '<a href="#sohyo" data-tab="sohyo" data-x="%s" style="%s%s">総　評</a><a href="#ugoki" data-tab="ugoki" data-x="%s" style="%s%s">代表的な動き</a><a href="#shin" data-tab="shin" data-x="%s" style="%s%s">発表済み変更点(未実施分)</a></div><!--/subtabs-->')%(X1,ON,X1,X2,OFF,X2,X3,OFF,X3)
    n=s.find('</nav>'); assert n>0
    s=s[:n+6]+tabs+s[n+6:]
    js=('<script id="tabscript">(function(){var T={sohyo:document.getElementById("pane-sohyo"),ugoki:document.getElementById("pane-ugoki"),shin:document.getElementById("pane-shin")};'
        'var L=[].slice.call(document.querySelectorAll("#subtabs a"));var ON=%r,OFF=%r;'
        'function show(k){if(!T[k])k="sohyo";for(var i in T)T[i].hidden=(i!==k);L.forEach(function(a){a.setAttribute("style",(a.getAttribute("data-tab")===k?ON:OFF)+a.getAttribute("data-x"))})}'
        'L.forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var k=a.getAttribute("data-tab");show(k);try{history.replaceState(null,"","#"+k)}catch(x){}})});'
        'show((location.hash||"").slice(1));window.addEventListener("hashchange",function(){show((location.hash||"").slice(1))})})();</script>')%(ON,OFF)
    css=('<style id="tabstyle">#pane-ugoki>h2{display:none}'
         '#pane-sohyo>h2{font-size:0!important;margin:0 0 12px!important;padding:0!important;border:0!important;font-weight:400}'
         '#pane-sohyo>h2 span{font-size:12px!important}#upcoming>div:first-child{margin-top:0!important}</style>')
    return s.replace('</main>',css+js+'</main>',1)
if __name__=='__main__':
    s=open(P).read(); open(P,'w').write(apply(s))
