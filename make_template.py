"""Derive template.html (generic flipbook with {{PLACEHOLDERS}}) from base_flipbook.html."""
import re, sys
src = open('base_flipbook.html', encoding='utf-8').read()
s = src

def rep(old, new, count=1):
    global s
    if old not in s:
        sys.exit('missing: ' + old[:60])
    s = s.replace(old, new, count)

rep('<title>WinWinTrip × TGV Lyria</title>', '<title>{{TITLE}}</title>')
rep('aspect-ratio:7040/1980;', 'aspect-ratio:{{W2}}/{{H}};')
rep('width:min(100cqw, 355.56cqh);', 'width:min(100cqw, {{CQH}}cqh);')
rep('aspect-ratio:3520/1980;', 'aspect-ratio:{{W}}/{{H}};')
rep('<span class="title"><b>WinWinTrip</b> <span>× TGV Lyria</span><small>Catalogue numérique</small></span>',
    '<span class="title"><b>{{TITLE}}</b><small>{{SUBTITLE}}</small></span>')
rep('<span id="totPage">7</span>', '<span id="totPage">{{TOTAL}}</span>')

# pages come from the generator (data URIs or relative paths)
s = re.sub(r'  var TOTAL = 7;\n  var pages = \[\];\n  for \(var i = 1; i <= TOTAL; i\+\+\) pages\.push\([^\n]*\n',
           '  var pages = {{PAGES_JSON}};\n  var TOTAL = pages.length;\n  // last index reachable as the LEFT page of a spread (or the lone back cover)\n  var LAST = TOTAL % 2 === 1 ? TOTAL - 2 : TOTAL - 1;\n  if (LAST < 0) LAST = 0;\n', s)
rep('var SPREAD_AR = (3520 * 2) / 1980;', 'var SPREAD_AR = ({{W}} * 2) / {{H}};')
rep('smoother downscaling of the 3520px sources', 'smoother downscaling of the large sources')

# end-of-book handling for odd/even page counts
rep('var pct = (curIdx / (TOTAL - 1)) * 100;', 'var pct = LAST > 0 ? (curIdx / LAST) * 100 : 0;')
rep('document.getElementById("btnNext").disabled = curIdx >= TOTAL - 2;', 'document.getElementById("btnNext").disabled = curIdx >= LAST;')
rep('''  function setCover(on){ bookMountEl.classList.toggle("is-cover", !!on); }''',
    '''  function setCover(on){ bookMountEl.classList.toggle("is-cover", !!on); }
  function setBack(on){ bookMountEl.classList.toggle("is-back", !!on); }''')
rep('if (!pageFlip || ready) setCover(curIdx === 0);',
    'if (!pageFlip || ready){ setCover(curIdx === 0); setBack(TOTAL > 2 && TOTAL % 2 === 0 && curIdx === TOTAL - 1); }')
rep('if (e.data === "read") setCover(curIdx === 0);\n      else if (e.data === "flipping" || e.data === "user_fold") setCover(false);',
    'if (e.data === "read"){ setCover(curIdx === 0); setBack(TOTAL > 2 && TOTAL % 2 === 0 && curIdx === TOTAL - 1); }\n      else if (e.data === "flipping" || e.data === "user_fold"){ setCover(false); setBack(false); }')
rep('.book-mount.is-cover{', '.book-mount.is-back{transform:translateX(25%);clip-path:inset(-40px 50% -40px 0);}\n  .book-mount.is-cover{')

# the page-flip library is inlined so the exported file works offline
rep('<script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>',
    '<script>{{PAGEFLIP_LIB}}</script>')

for bad in ('WinWinTrip', 'TGV', '7040', '3520', '1980'):
    if bad in s:
        sys.exit('leftover: ' + bad)
open('template.html', 'w', encoding='utf-8').write(s)
print('template.html ok', len(s))
