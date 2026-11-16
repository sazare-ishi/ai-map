# 「AIの動向」(index.html)の「代表的な動き」の下に、役割で記事を絞り込むボタンを入れる。
# 毎週 index.html を書き直したあとに `python3 tools/add_filter.py` を実行する(何度実行しても同じ結果)。
import re
ROLES=[('調べる','#5b8fc9'),('作る','#d27a58'),('整理する','#3f9d86'),('代わりに動く','#8579cf'),('判断','#c19a3b')]
def block():
    allb='<button type="button" data-role="all" aria-pressed="true" style="--c:#8a949b;width:100%">すべて</button>'
    chips=allb+'</div><div class="row" style="margin-top:6px;flex-wrap:nowrap">'+''.join('<button type="button" data-role="%s" aria-pressed="false" style="--c:%s;%s">%s</button>'%(n,c,'flex:0 0 auto' if n=='判断' else 'flex:1 1 auto',n) for n,c in ROLES)
    css=('<style>#sel{margin:0 0 6px}#sel .row{display:flex;flex-wrap:wrap;gap:6px}'
         '#sel button{flex:1 1 auto;font:inherit;font-size:13px;font-weight:600;color:#1f2a30;cursor:pointer;padding:6px 8px;white-space:nowrap;min-width:0;'
         'border:0.5px solid #dfe5e9;border-left:4px solid var(--c);border-radius:0 10px 10px 0;background:color-mix(in srgb,var(--c) 10%,#fff)}'
         '#sel button[aria-pressed="true"]{border-color:var(--c);box-shadow:inset 0 0 0 1px var(--c);background:color-mix(in srgb,var(--c) 22%,#fff)}'
         '#sel .cnt{font-size:12px;color:#64717a;margin-top:6px}@media(max-width:379px){#sel .row{gap:4px}#sel button{font-size:11.5px;padding:6px 4px}}</style>')
    html='<div id="sel"><div style="font-size:12px;font-weight:700;color:#64717a;margin-bottom:6px">役割で絞り込む</div><div class="row">%s</div><div class="cnt" id="selcnt"></div></div>'%chips
    js=('<script id="selscript">(function(){var bar=document.getElementById("sel");if(!bar)return;var arts=[].slice.call(document.querySelectorAll("article"));'
        'function role(a){var m=a.querySelector(".meta span");return m?m.textContent.trim():""}'
        'function apply(r){arts.forEach(function(a){a.style.display=(r==="all"||role(a)===r)?"":"none"});'
        '[].forEach.call(bar.querySelectorAll("button"),function(b){b.setAttribute("aria-pressed",b.getAttribute("data-role")===r?"true":"false")});'
        'var n=arts.filter(function(a){return a.style.display!=="none"}).length;'
        'document.getElementById("selcnt").textContent=r==="all"?"":"「"+r+"」の記事: "+n+"件";}'
        'bar.addEventListener("click",function(e){var b=e.target.closest("button");if(b)apply(b.getAttribute("data-role"))});})();</script>')
    return '<!--sel-->'+css+html+'<!--/sel-->',js
def apply(s):
    s=re.sub(r'<!--sel-->.*?<!--/sel-->','',s,flags=re.S)
    s=re.sub(r'<script id="selscript">.*?</script>\n?','',s,flags=re.S)
    b,js=block()
    k='<h2>代表的な動き</h2>'; assert k in s
    s=s.replace(k,k+b,1)
    assert '</main>' in s
    return s.replace('</main>',js+'</main>',1)
if __name__=='__main__':
    p='docs/index.html'; s=open(p).read(); s=apply(s); open(p,'w').write(s)
