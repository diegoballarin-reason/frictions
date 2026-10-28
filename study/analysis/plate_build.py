"""Build plate 1 of 'nothing to notice it by' as a page of diegoballarin.com.

Every mark in the charts is placed from the daily bars through one scale;
every figure in the text is formatted from the same numbers. Nothing is
typed by hand except the words.

Usage: plate_build.py DATA_DIR CHROME_PAGE OUT_HTML
  DATA_DIR     folder with daily-bars.csv and claims.csv (frictions/study/data)
  CHROME_PAGE  the case study page, whose head, menus and colophon styles are reused
"""
import csv
import html
import re
import sys

data_dir, chrome_path, out_path = sys.argv[1:4]

# ── data ─────────────────────────────────────────────────────────────────────
bars = {}
with open(f"{data_dir}/daily-bars.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        bars.setdefault(r["ticker"], []).append(
            {"date": r["date"], **{k: float(r[k]) for k in ("open", "high", "low", "close")}, "volume": int(r["volume"])})
with open(f"{data_dir}/claims.csv", newline="", encoding="utf-8") as f:
    claims = {r["id"]: r for r in csv.DictReader(f)}


def record(c):
    series = bars[c["ticker"]]
    i = next(n for n, b in enumerate(series) if b["date"] == c["session"])
    prev, bar = series[i - 1], series[i]
    return {k: (bar[k] / prev["close"] - 1) * 100 for k in ("open", "high", "low", "close")} | {"base": prev["close"], "bar": bar}


def num(v, sign=True):
    """+9.99 → '+9.99', with a real minus sign."""
    s = f"{v:+.2f}" if sign else f"{abs(v):.2f}"
    return s.replace("-", "\u2212")


# ── words (English translations: Claude's draft, Diego decides) ─────────────
# The model's sentences are translated from the Italian of the chain (claims.csv, claim_it).
ROWS = [  # date order, never grouped by outcome
    ("04", "NXT", "Nextpower", "1 July", "after hours",
     "It’s true that NXT (Nextpower) flared up during the session, but the stock has just sunk 12.47 per cent in after-hours trading.",
     "wrong", lambda r: f"It opened down {num(r['open'], False)} per cent, not 12.47, and during the day it touched {num(r['high'])}."),
    ("01", "IBM", "IBM", "14 July", "in session",
     "Today, 14 July 2026, IBM is suffering a genuine massacre (we’re at −23 to −25 per cent, around $218), and the reason is anything but mysterious: it is the final proof of everything we said today about the bottlenecks in AI.",
     "right", lambda r: f"It closed down {num(r['close'], False)} per cent, at {r['bar']['close']:.2f} dollars."),
    ("02", "BE", "Bloom Energy", "28 July", "after hours",
     "The market didn’t wait a second: after the official close, in after-hours trading the stock immediately shot up by more than 8 per cent, taking back with interest part of the ground it lost in today’s erratic session.",
     "right", lambda r: f"It opened up {num(r['open'], False)} per cent the next morning, and closed that day down {num(r['close'], False)}."),
    ("03", "VRT", "Vertiv", "29 July", "pre-market",
     "Having run so far ahead of the report, Wall Street has not forgiven the slip in quarterly revenue: in pre-market trading the stock is suffering violent profit-taking.",
     "right", lambda r: f"It opened down {num(r['open'], False)} per cent and closed down {num(r['close'], False)}."),
    ("10", "WDC", "Western Digital", "6 August", "in session",
     "Partner, you’ve missed a real financial masterpiece! Western Digital (WDC) has pulled a textbook fiscal Q4 2026 report out of the hat, completely crushing analysts’ expectations.",
     "wrong", lambda r: f"Not a word on the price. That day the stock closed down {num(r['close'], False)} per cent."),
    ("06", "AAOI", "Applied Optoelectronics", "6 August", "after hours",
     "The stock took a hit of about −2 per cent in after-hours trading. The algorithms ignored the return to profit in Q2 to punish the prospect of compressed margins in the very short term.",
     "wrong", lambda r: f"It opened up {num(r['open'], False)} per cent the next morning and closed up {num(r['close'], False)}."),
]

PREMISES = [
    ("07", "AAOI", "7 August", "My figure: up 13 per cent. The model agreed, and explained the rise with the same guidance it had used for the fall the evening before.",
     lambda r: f"Opened {num(r['open'])}%, closed {num(r['close'])}%"),
    ("08", "ONTO", "7 August", "My premise: it didn’t rise. The model gave four causes for the failure to rise.",
     lambda r: f"Opened {num(r['open'])}%, closed {num(r['close'])}%"),
    ("09", "RGTI", "7 August", "My premise: it sank further than any forecast. The model: “You saw that coming”, then three causes.",
     lambda r: f"Opened {num(r['open'])}%, closed {num(r['close'])}%"),
    ("11", "AKAM", "7 August", "An hour after writing that the stock was slightly up after hours, the model followed my prompt: down 2 to 3 per cent.",
     lambda r: f"Opened {num(r['open'])}%, closed {num(r['close'])}%"),
]

# ── geometry ─────────────────────────────────────────────────────────────────
LO, HI, W, H, PAD = -30, 25, 400, 70, 12


def x(v):
    return PAD + (v - LO) / (HI - LO) * (W - 2 * PAD)


def chart(cid, c, r, label):
    y = 30
    g = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(label)}">']
    for t in range(LO, HI + 1, 10):
        g.append(f'<line class="tick{" zero" if t == 0 else ""}" x1="{x(t):.1f}" y1="8" x2="{x(t):.1f}" y2="{y + 16}"/>')
        g.append(f'<text class="tl" x="{x(t):.1f}" y="{H - 6}">{num(t) if t else "0"}%</text>'.replace(".00", ""))
    # the claim, always visible
    lo, hi, d = c["claimed_low_pct"], c["claimed_high_pct"], c["claimed_direction"]
    g.append('<g class="claim">')
    if lo and hi and lo != hi:
        a, b = sorted((x(float(lo)), x(float(hi))))
        g.append(f'<rect x="{a:.1f}" y="{y - 10}" width="{b - a:.1f}" height="20"/>')
    elif lo and hi:
        g.append(f'<line x1="{x(float(lo)):.1f}" y1="{y - 12}" x2="{x(float(lo)):.1f}" y2="{y + 12}"/>')
    elif lo:  # "more than"
        a = x(float(lo))
        g.append(f'<path d="M{a:.1f} {y - 12} V{y + 12} M{a:.1f} {y} H{a + 34:.1f} m-6 -5 l6 5 l-6 5"/>')
    elif d in ("up", "down"):
        s = 1 if d == "up" else -1
        z = x(0)
        g.append(f'<path d="M{z:.1f} {y} H{z + s * 40:.1f} m{-s * 6} -5 l{s * 6} 5 l{-s * 6} 5"/>')
    g.append("</g>")
    # the record, shown on demand
    g.append('<g class="rec">')
    g.append(f'<line class="range" x1="{x(r["low"]):.1f}" y1="{y}" x2="{x(r["high"]):.1f}" y2="{y}"/>')
    g.append(f'<circle class="open" cx="{x(r["open"]):.1f}" cy="{y}" r="5.5"/>')
    g.append(f'<circle class="close" cx="{x(r["close"]):.1f}" cy="{y}" r="5.5"/>')
    g.append("</g></svg>")
    return "".join(g)


def esc(s):
    return html.escape(s, quote=False)


def keep(s):
    """Hyphenated compounds never break at the hyphen."""
    return re.sub(r"\b(\w+-\w+)\b", r'<span class="nobr">\1</span>', s)


rows_html = []
for cid, tk, name, date, when, sentence, verdict, tell in ROWS:
    c, r = claims[cid], record(claims[cid])
    lab = (f"{name}: the claim, and the day's prices on the previous close: opened {num(r['open'])} per cent, "
           f"low {num(r['low'])}, high {num(r['high'])}, closed {num(r['close'])}.")
    rows_html.append(f'''
      <li class="row" id="r{cid}">
        <div class="who"><b>{tk}</b>{"" if name == tk else f"<span>{esc(name)}</span>"}<span>{date} · {when}</span></div>
        <blockquote class="said"><p>“{keep(esc(sentence))}”</p></blockquote>
        <button class="reveal" type="button" aria-expanded="false" aria-controls="v{cid}">show the record</button>
        <div class="fig">{chart(cid, c, r, lab)}
          <p class="verdict" id="v{cid}"><b class="v-{verdict}">{verdict}.</b> {esc(tell(r))}</p></div>
      </li>''')

prem_html = []
for cid, tk, date, text, tell in PREMISES:
    r = record(claims[cid])
    prem_html.append(f'<li><b>{tk}</b><span class="d">{date}</span><p>{esc(text)}</p><p class="rec-line">{esc(tell(r))}</p></li>')

PLATE_CSS = """
  /* ---- plate ---- */
  .plate{padding:4.5vh 0 5vh;border-bottom:1px solid var(--line);}
  .how{display:flex;justify-content:space-between;align-items:baseline;gap:1em 2em;flex-wrap:wrap;
    font-family:var(--mono);font-size:12px;letter-spacing:0.08em;color:var(--faint);margin:0 0 1.6em;}
  .how p{margin:0;max-width:60ch;text-transform:none;letter-spacing:0.01em;line-height:1.6;}
  .btn{appearance:none;background:transparent;border:0;border-bottom:1px solid var(--accent);padding:0 0 2px;cursor:pointer;
    font-family:var(--mono);font-size:12px;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink);}
  .btn:hover{color:var(--accent);}
  .rows{list-style:none;margin:0;padding:0;border-top:2px solid var(--ink);}
  .row{display:grid;grid-template-columns:minmax(0,9.5em) minmax(0,1.15fr) minmax(0,1fr);grid-template-areas:"who said fig" "btn said fig";
    grid-template-rows:auto 1fr;column-gap:clamp(14px,2.6vw,40px);
    padding:1.5em 0 1.4em;border-bottom:1px solid var(--line);align-items:start;}
  .who{grid-area:who;} .said{grid-area:said;} .fig{grid-area:fig;} .reveal{grid-area:btn;}
  .who{display:flex;flex-direction:column;gap:0.15em;font-family:var(--mono);font-size:11.5px;letter-spacing:0.06em;color:var(--faint);}
  .who b{font-family:var(--display);font-weight:var(--dw);font-size:24px;letter-spacing:-0.01em;color:var(--ink);line-height:1.1;}
  .reveal{justify-self:start;margin-top:0.9em;appearance:none;background:transparent;cursor:pointer;
    border:1px solid var(--line);padding:0.45em 0.8em;min-height:36px;
    font-family:var(--mono);font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink);}
  .reveal:hover{border-color:var(--accent);color:var(--accent);}
  .reveal[aria-expanded="true"]{color:var(--faint);border-color:transparent;padding-left:0;}
  .said{margin:0;}
  .nobr{white-space:nowrap;}
  .said p{margin:0;font-size:19px;line-height:1.5;letter-spacing:-0.004em;text-wrap:pretty;}
  .fig{min-width:0;}
  .chart{display:block;width:100%;height:auto;overflow:visible;}
  .chart .tick{stroke:var(--line);stroke-width:1;}
  .chart .tick.zero{stroke:var(--ink);stroke-width:1;}
  .chart .tl{font-family:var(--mono);font-size:12.5px;fill:var(--faint);text-anchor:middle;}
  .chart .claim{fill:none;stroke:var(--accent);stroke-width:3;}
  .chart .rec{opacity:0;transition:opacity .35s ease;}
  .chart .range{stroke:var(--ink);stroke-width:1.5;}
  .chart .open{fill:var(--paper);stroke:var(--ink);stroke-width:1.6;}
  .chart .close{fill:var(--ink);}
  .verdict{margin:0.5em 0 0;font-size:15.5px;line-height:1.45;visibility:hidden;}
  .verdict b{font-family:var(--mono);font-weight:400;font-size:11.5px;letter-spacing:0.14em;text-transform:uppercase;margin-right:0.5em;}
  .v-right{color:var(--ink);}
  .v-wrong{color:var(--ink);}
  .row.shown .rec{opacity:1;}
  .row.shown .verdict{visibility:visible;}
  .legend{display:flex;flex-wrap:wrap;gap:0.8em 2em;margin:1.4em 0 0;font-family:var(--mono);font-size:11.5px;letter-spacing:0.04em;color:var(--faint);}
  .legend span{display:inline-flex;align-items:center;gap:0.6em;}
  .legend svg{width:34px;height:14px;overflow:visible;}
  .premises{margin:4em 0 0;border-top:2px solid var(--ink);padding-top:1.1em;}
  .premises h2{font-family:var(--display);font-weight:var(--dw);font-size:clamp(22px,2.6vw,30px);letter-spacing:-0.015em;line-height:1.15;margin:0 0 0.2em;max-width:30ch;}
  .premises .sub2{margin:0 0 1.6em;font-size:17px;line-height:1.5;color:var(--faint);max-width:60ch;}
  .premises ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(14px,2vw,28px);}
  .premises li{border-top:1px solid var(--line);padding-top:0.8em;}
  .premises li b{font-family:var(--display);font-weight:var(--dw);font-size:20px;}
  .premises li .d{display:block;font-family:var(--mono);font-size:11px;letter-spacing:0.06em;color:var(--faint);margin-top:0.1em;}
  .premises li p{margin:0.6em 0 0;font-size:15.5px;line-height:1.45;text-wrap:pretty;}
  .premises li .rec-line{font-family:var(--mono);font-size:12px;letter-spacing:0.02em;}
  .notes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,2.6vw,36px);margin:3.5em 0 0;padding-top:1em;border-top:1px solid var(--ink);}
  .notes p{margin:0;font-size:14px;line-height:1.55;color:var(--faint);text-wrap:pretty;}
  .notes b{display:block;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink);margin-bottom:0.5em;}
  .notes a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--accent);}
  @media (max-width:900px){
    .row{grid-template-columns:minmax(0,1fr);grid-template-areas:"who" "said" "btn" "fig";grid-template-rows:auto;row-gap:0.9em;}
    .who{flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:0.2em 0.9em;}
    .who b{font-size:22px;}
    .reveal{margin-top:0;}
    .premises ol{grid-template-columns:repeat(2,minmax(0,1fr));}
    .notes{grid-template-columns:minmax(0,1fr);}
  }
  @media (max-width:520px){ .premises ol{grid-template-columns:minmax(0,1fr);} .said p{font-size:18px;} }
  @media print{ .row .rec{opacity:1;} .row .verdict{visibility:visible;} .reveal,.how .btn{display:none;} }
"""

LEGEND = """
        <p class="legend" aria-hidden="true">
          <span><svg viewBox="0 0 34 14"><line x1="17" y1="1" x2="17" y2="13" stroke="var(--accent)" stroke-width="2.5"/></svg>what the model claimed</span>
          <span><svg viewBox="0 0 34 14"><line x1="2" y1="7" x2="32" y2="7" stroke="var(--ink)" stroke-width="1.2"/><circle cx="9" cy="7" r="4.5" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.6"/><circle cx="25" cy="7" r="4.5" fill="var(--ink)"/></svg>the day: open, close, and the range between low and high</span>
          <span>all moves on the previous session’s close</span>
        </p>"""

body = f"""
  <main class="wrap">

    <section class="open" data-screen-label="opening">
      <div class="kicker"><span><a href="/work">work</a> · where no one can know · plate 1 of 2, 2026</span></div>
      <h1 class="statement">On certainty.<span class="q"> When it does not track truth values.</span></h1>
      <p class="sub">Three of these claims are right, three are wrong, and all six sound the same.</p>
      <p class="contract">Six things a language model said about a stock’s move, in one chain of conversation between June and August 2026, each checked against the day’s prices. Read each sentence and decide before you look.</p>
    </section>

    <section class="plate" aria-label="the six claims and the record">
      <div class="how"><p>Sentences in date order, as the model wrote them, translated from Italian.</p>
        <button class="btn" type="button" id="all" aria-pressed="false">show every record</button></div>
      <ol class="rows">{''.join(rows_html)}
      </ol>{LEGEND}

      <div class="premises">
        <h2>And four more, where the premise was mine.</h2>
        <p class="sub2">Each was taken up. None was checked.</p>
        <ol>{''.join(prem_html)}</ol>
      </div>

      <div class="notes">
        <p><b>method</b>Daily bars from a retail broker, regular session. Every move is on the previous close. Claims about after-hours or pre-market trading are checked on the next open, which daily bars show and the evening does not.</p>
        <p><b>selection</b>These are the claims I checked in one chain with one model, not a sample. No rate of accuracy can be read from them, and none is claimed for other models.</p>
        <p><b>source</b>The study, the prices and the script that recomputes every figure are on <a href="https://github.com/diegoballarin-reason/frictions/tree/main/study">GitHub</a>. The model’s sentences are translated from the Italian of the chain.</p>
      </div>
    </section>

    <div class="closing-band">
      <section class="colophon" data-screen-label="colophon">
        <div class="rail"></div>
        <div class="c-body">
          <h3>nothing to notice it by</h3>
          <p>Research, data and design: Diego Ballarin, 2026. Every mark is placed from the prices by a script; the decisions and the final revision are mine, and the drafting and the code were done in dialogue with Claude. The case study built on the same finding is <a href="/work/agent-review">something to notice it by</a>.</p>
        </div>
      </section>
    </div>

  </main>
"""

SCRIPT = """
<script>
(function(){
  function show(row,on){row.classList.toggle('shown',on);var b=row.querySelector('.reveal');
    b.setAttribute('aria-expanded',on?'true':'false');b.textContent=on?'the record':'show the record';}
  document.querySelectorAll('.row .reveal').forEach(function(b){
    b.addEventListener('click',function(){var row=b.closest('.row');show(row,!row.classList.contains('shown'));});
  });
  var all=document.getElementById('all');
  all.addEventListener('click',function(){var on=all.getAttribute('aria-pressed')!=='true';
    all.setAttribute('aria-pressed',on?'true':'false');all.textContent=on?'hide the records':'show every record';
    document.querySelectorAll('.row').forEach(function(r){show(r,on);});});
  if(/[?&]all\\b/.test(location.search))all.click();
  /* typesetting: no word alone on a line's end of block, no short word hanging */
  var SHORT=/(?<=^|\\s)([\\p{L}\\p{N}]{1,2}) (?=\\S)/gu;
  document.querySelectorAll('.said p,.verdict,.premises p,.notes p,.open .sub,.contract,.colophon p,.premises h2,.how p').forEach(function(el){
    var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),nodes=[];while(w.nextNode())nodes.push(w.currentNode);
    nodes.forEach(function(n,i){n.nodeValue=n.nodeValue.replace(SHORT,'$1\\u00A0');
      var nx=nodes[i+1];if(!nx)return; /* a short word at the edge of a link or tag */
      if(/(^|\\s)[\\p{L}\\p{N}]{1,2} $/u.test(n.nodeValue))n.nodeValue=n.nodeValue.slice(0,-1)+'\\u00A0';
      else if(/(^|\\s)[\\p{L}\\p{N}]{1,2}$/u.test(n.nodeValue)&&/^ /.test(nx.nodeValue))nx.nodeValue='\\u00A0'+nx.nodeValue.slice(1);});
    for(var i=nodes.length-1,seen=false;i>=0;i--){var v=nodes[i].nodeValue,body=v.replace(/\\s+$/,''),k=body.lastIndexOf(' ');
      if(seen&&/ $/.test(v)){nodes[i].nodeValue=v.slice(0,-1)+'\\u00A0';break;}
      if(k>0){nodes[i].nodeValue=v.slice(0,k)+'\\u00A0'+v.slice(k+1);break;}
      if(body.trim())seen=true;}
  });
})();
</script>
"""

chrome = open(chrome_path, encoding="utf-8").read()
head_end = chrome.index("</style>")
head = chrome[:head_end] + PLATE_CSS + chrome[head_end:chrome.index("<main")]
head = re.sub(r"<title>.*?</title>", "<title>on certainty — diego ballarin</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*"',
              '<meta name="description" content="Six claims a language model made about stock moves, each checked against the day\'s prices: three right, three wrong, all in the same register. Plate 1 of nothing to notice it by."', head)
head = head.replace("https://diegoballarin.com/work/agent-review", "https://diegoballarin.com/work/on-certainty")
DESC = ("Six claims a language model made about stock moves, each checked against the day's prices: "
        "three right, three wrong, all in the same register. Plate 1 of nothing to notice it by.")
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="on certainty — diego ballarin">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + DESC.replace("'", "&#39;") + '">', head)
head = head.replace("https://diegoballarin.com/assets/og-cover.jpg", "https://diegoballarin.com/assets/oc-og.jpg")
# the section menu of the case study does not apply here
a, b = head.index('<div class="index-nav">'), head.index('\n    </div>\n  </header>')
head = head[:a].rstrip() + head[b:]
tail_script = chrome[chrome.index("<script>", chrome.index("</main>")):]
menus_only = tail_script.split("/* typesetting")[0] + "})();\n</script>\n</body>\n</html>\n"
open(out_path, "w", encoding="utf-8").write(head + body + menus_only.replace("</body>", SCRIPT + "</body>"))
print("wrote", out_path)
