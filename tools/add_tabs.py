# トップ(index.html)に、下段メニュー「総評 / 代表的な動き」を入れる(連携チェックなどの下段メニューと同じ見た目)。
# 毎週 index.html を更新したあと、add_cats.py → add_filter.py → add_upcoming.py → このスクリプトの順に実行する。何度実行しても同じ結果になる。
import re
P='docs/index.html'
ON='padding:10px 0 8px;font-size:13px;line-height:1.4;text-decoration:none;color:#1f2a30;font-weight:700;border-bottom:2px solid #1f2a30;'
OFF='padding:10px 0 8px;font-size:13px;line-height:1.4;text-decoration:none;color:#64717a;'
def apply(s):
    # 前回の入れ物・メニュー・スクリプトを外す
    s=re.sub(r'<div id="subtabs".*?</div><!--/subtabs-->','',s,flags=re.S)
    s=re.sub(r'<script id="tabscript">.*?</script>','',s,flags=re.S)
    s=re.sub(r'<div id="pane-(sohyo|ugoki)"[^>]*>','',s); s=s.replace('</div><!--/pane-->','')
    a=s.find('<h2 style="margin-top:'); assert a>=0
    u=s.find('<!--up-->',a)
    if u<0: u=s.find('<h2>代表的な動き</h2>',a)
    assert u>a
    last=s.rfind('</article>'); assert last>u
    e=last+len('</article>')
    s=(s[:a]+'<div id="pane-sohyo">'+s[a:u]+'</div><!--/pane-->'
       +'<div id="pane-ugoki" hidden style="margin-top:10px">'+s[u:e]+'</div><!--/pane-->'+s[e:])
    # 下段メニュー(帯の中、上段メニューの下)
    tabs=('<div id="subtabs" style="display:flex;gap:32px;justify-content:center;border-bottom:0.5px solid #dfe5e9">'
          '<a href="#sohyo" data-tab="sohyo" style="%s">総評</a><a href="#ugoki" data-tab="ugoki" style="%s">代表的な動き</a></div><!--/subtabs-->')%(ON,OFF)
    n=s.find('</nav>'); assert n>0
    s=s[:n+6]+tabs+s[n+6:]
    js=('<script id="tabscript">(function(){var T={sohyo:document.getElementById("pane-sohyo"),ugoki:document.getElementById("pane-ugoki")};'
        'var L=[].slice.call(document.querySelectorAll("#subtabs a"));var ON=%r,OFF=%r;'
        'function show(k){if(!T[k])k="sohyo";for(var i in T)T[i].hidden=(i!==k);L.forEach(function(a){a.setAttribute("style",a.getAttribute("data-tab")===k?ON:OFF)})}'
        'L.forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var k=a.getAttribute("data-tab");show(k);try{history.replaceState(null,"","#"+k)}catch(x){}})});'
        'show((location.hash||"").slice(1))})();</script>')%(ON,OFF)
    return s.replace('</main>',js+'</main>',1)
if __name__=='__main__':
    s=open(P).read(); open(P,'w').write(apply(s))
