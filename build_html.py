#!/usr/bin/env python3
"""Assemble the final narnia_study_tool.html from data.json + grammar.json +
comprehension.json + summary_data.json."""
import json
import sys

def main():
    data = json.load(open('data.json', encoding='utf-8'))
    grammar = json.load(open('grammar.json', encoding='utf-8'))
    comprehension = json.load(open('comprehension.json', encoding='utf-8'))
    summary = json.load(open('summary_data.json', encoding='utf-8'))
    kotest = json.load(open('kotest.json', encoding='utf-8'))

    vocab_json = json.dumps(data['vocab'], ensure_ascii=False)
    underline_json = json.dumps(data['underline'], ensure_ascii=False)
    quiz_json = json.dumps(data['quiz'], ensure_ascii=False)
    grammar_json = json.dumps(grammar, ensure_ascii=False)
    comprehension_json = json.dumps(comprehension, ensure_ascii=False)
    summary_json = json.dumps(summary, ensure_ascii=False)
    kotest_json = json.dumps(kotest, ensure_ascii=False)

    html = TEMPLATE.replace('__VOCAB_JSON__', vocab_json) \
                    .replace('__UNDERLINE_JSON__', underline_json) \
                    .replace('__QUIZ_JSON__', quiz_json) \
                    .replace('__GRAMMAR_JSON__', grammar_json) \
                    .replace('__COMPREHENSION_JSON__', comprehension_json) \
                    .replace('__SUMMARY_JSON__', summary_json) \
                    .replace('__KOTEST_JSON__', kotest_json)

    outpath = sys.argv[1] if len(sys.argv) > 1 else 'narnia_study_tool.html'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'wrote {outpath} ({len(html)} bytes)')


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ナルニア国物語 期末試験対策ツール</title>
<style>
  :root{
    --bg:#faf8f4;
    --card:#ffffff;
    --ink:#2b2b28;
    --sub:#6b6b64;
    --line:#e4e0d6;
    --accent:#8a5a3b;
    --accent-bg:#f3e6d8;
    --good:#3b6d11;
    --good-bg:#eaf3de;
    --bad:#a32d2d;
    --bad-bg:#fcebeb;
    --mark:#fde68a;
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
  }
  *{box-sizing:border-box;}
  body{margin:0; background:var(--bg); color:var(--ink); line-height:1.7;}
  .wrap{max-width:780px; margin:0 auto; padding:24px 16px 60px;}
  h1{font-size:20px; font-weight:600; margin:0 0 4px;}
  .lead{color:var(--sub); font-size:13px; margin:0 0 20px;}
  .tabs{display:flex; gap:8px; margin-bottom:20px; border-bottom:1px solid var(--line); flex-wrap:wrap;}
  .tab{padding:10px 14px; font-size:14px; cursor:pointer; color:var(--sub); border-bottom:2px solid transparent; user-select:none; transition:color 0.2s, border-color 0.2s;}
  .tab:hover{color:var(--accent);}
  .tab.active{color:var(--accent); border-bottom-color:var(--accent); font-weight:600;}
  .subtabs{display:flex; gap:6px; margin-bottom:14px; flex-wrap:wrap;}
  .subtab{padding:6px 12px; font-size:12.5px; cursor:pointer; color:var(--sub); border:1px solid var(--line); border-radius:20px; background:var(--card); transition:all 0.2s;}
  .subtab:hover{background:var(--accent-bg);}
  .subtab.active{background:var(--accent); color:#fff; border-color:var(--accent);}
  .panel{display:none;}
  .panel.active{display:block;}
  .card{background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px; margin-bottom:16px; animation:fadeInUp 0.35s ease;}
  @keyframes fadeInUp{ from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:translateY(0);} }
  @keyframes shakeX{ 10%,90%{transform:translateX(-2px);} 20%,80%{transform:translateX(3px);} 30%,50%,70%{transform:translateX(-5px);} 40%,60%{transform:translateX(5px);} }
  @keyframes popScale{ 0%{transform:scale(1);} 45%{transform:scale(1.035);} 100%{transform:scale(1);} }
  @keyframes confettiFall{ to{ transform:translateY(70px) rotate(320deg); opacity:0; } }
  @keyframes floaty{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
  .statrow{display:flex; gap:10px; margin-bottom:16px; flex-wrap:wrap;}
  .stat{background:var(--card); border:1px solid var(--line); border-radius:10px; padding:10px 14px; font-size:13px; flex:1; min-width:100px; transition:transform 0.15s;}
  .stat:hover{transform:translateY(-2px);}
  .stat b{display:block; font-size:20px; font-weight:600; margin-top:2px;}
  mark{background:var(--mark); color:#3a2c00; padding:0 2px; border-radius:2px;}
  u{text-decoration-color:var(--accent); text-decoration-thickness:2px;}
  .en{font-size:16px; margin-bottom:14px;}
  .jp{font-size:15px; color:var(--sub); border-top:1px dashed var(--line); padding-top:12px; margin-top:12px;}
  .btnrow{display:flex; gap:10px; flex-wrap:wrap; margin-top:14px;}
  button{font-family:inherit; font-size:14px; padding:9px 16px; border-radius:8px; border:1px solid var(--line); background:var(--card); cursor:pointer; color:var(--ink); transition:background 0.15s, transform 0.1s;}
  button:hover{background:var(--accent-bg);}
  button:active{transform:scale(0.96);}
  button.primary{background:var(--accent); color:#fff; border-color:var(--accent);}
  button.primary:hover{opacity:0.9;}
  button.good{background:var(--good-bg); color:var(--good); border-color:var(--good);}
  button.bad{background:var(--bad-bg); color:var(--bad); border-color:var(--bad);}
  .term{font-size:22px; font-weight:600; margin-bottom:6px;}
  .flip-outer{cursor:pointer; padding:0; overflow:hidden;}
  .flip-3d{perspective:1400px;}
  .flip-inner{display:grid; transition:transform 0.6s cubic-bezier(.5,.05,.15,1); transform-style:preserve-3d;}
  .flip-inner.flipped{transform:rotateY(180deg);}
  .flip-face{grid-area:1/1; backface-visibility:hidden; -webkit-backface-visibility:hidden; padding:34px 20px; text-align:center;}
  .flip-face.back{transform:rotateY(180deg); text-align:left; padding:26px 24px;}
  .flip-face .hint{color:var(--sub); font-size:13px; margin-top:10px;}
  .gloss-big{font-size:21px; font-weight:700; color:var(--accent); margin:4px 0 4px;}
  .srsbadge{display:inline-block; font-size:11px; color:var(--sub); margin-top:6px;}
  .context-toggle{margin-top:12px;}
  .context-box{margin-top:14px; text-align:left; border-top:1px dashed var(--line); padding-top:12px;}
  .context-box.hidden{display:none;}
  .progress{font-size:13px; color:var(--sub); margin-bottom:10px;}
  textarea{width:100%; min-height:70px; font-family:inherit; font-size:15px; padding:10px; border-radius:8px; border:1px solid var(--line); resize:vertical;}
  .choice{display:block; width:100%; text-align:left; margin-bottom:8px; padding:12px 14px;}
  .choice.correct{background:var(--good-bg); border-color:var(--good); color:var(--good); animation:popScale 0.35s;}
  .choice.wrong{background:var(--bad-bg); border-color:var(--bad); color:var(--bad); animation:shakeX 0.4s;}
  .choice:disabled{cursor:default; opacity:1;}
  .filterrow{display:flex; gap:8px; margin-bottom:14px; align-items:center; flex-wrap:wrap;}
  select{font-family:inherit; font-size:13px; padding:6px 10px; border-radius:8px; border:1px solid var(--line); background:var(--card);}
  input[type=text]{font-family:inherit; font-size:13px; padding:6px 10px; border-radius:8px; border:1px solid var(--line); background:var(--card);}
  .badge{display:inline-block; font-size:12px; padding:2px 8px; border-radius:20px; background:var(--accent-bg); color:var(--accent); margin-left:8px;}
  .point-badge{display:inline-block; font-size:12px; padding:3px 10px; border-radius:20px; background:var(--accent-bg); color:var(--accent); margin-bottom:12px; font-weight:600;}
  .explain{background:var(--accent-bg); border-radius:8px; padding:12px 14px; font-size:13px; margin-top:14px; color:var(--ink); line-height:1.6;}
  .reveal{margin-top:14px;}
  .empty{text-align:center; color:var(--sub); padding:30px 10px;}
  .wronglist{margin-top:10px;}
  .wrongitem{padding:10px 0; border-top:1px dashed var(--line); font-size:14px;}
  .subhead{font-size:15px; font-weight:600; margin:0 0 10px;}
  .reviewSection{margin-bottom:20px;}
  .reviewSection:last-child{margin-bottom:0;}
  /* vocab list view */
  .vlistRow{display:flex; justify-content:space-between; gap:10px; padding:10px 0; border-top:1px dashed var(--line); font-size:14px;}
  .vlistRow:first-child{border-top:none;}
  .vlistTerm{font-weight:600; min-width:120px;}
  .vlistGloss{color:var(--sub); text-align:right; flex:1;}
  .vlistChap{font-size:11px; color:var(--sub); background:var(--accent-bg); border-radius:10px; padding:1px 7px; align-self:center;}
  /* match game (Quizlet-style: all tiles visible, click two to pair them off) */
  .matchTop{display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; font-size:13px; color:var(--sub); flex-wrap:wrap; gap:8px;}
  .matchGrid{display:grid; grid-template-columns:repeat(auto-fill, minmax(110px,1fr)); gap:10px;}
  .matchTile{min-height:64px; padding:12px 10px; border-radius:10px; border:1px solid var(--line); background:var(--card);
    display:flex; align-items:center; justify-content:center; text-align:center; font-size:13px; line-height:1.35;
    cursor:pointer; user-select:none; transition:background 0.25s ease, border-color 0.25s ease, color 0.25s ease, opacity 0.5s ease;}
  .matchTile:hover{background:var(--accent-bg);}
  .matchTile.selected{background:var(--accent); color:#fff; border-color:var(--accent);}
  .matchTile.wrong{background:var(--bad-bg); border-color:var(--bad); color:var(--bad);}
  .matchTile.clearing{opacity:0; transition:opacity 0.5s ease;}
  .matchTile.cleared{opacity:0; pointer-events:none; cursor:default; border-color:transparent; background:transparent;}
  .confetti{position:relative; height:50px; width:220px; margin:0 auto 6px;}
  .confetti span{position:absolute; top:-6px; width:8px; height:8px; border-radius:2px; animation:confettiFall 1.1s ease-in forwards;}
  /* summary tab */
  .banner{width:100%; border-radius:10px; margin-bottom:14px; display:block;}
  .charGrid{display:grid; grid-template-columns:repeat(auto-fill, minmax(140px,1fr)); gap:12px; margin-bottom:20px;}
  .charCard{background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px; text-align:center; transition:transform 0.15s;}
  .charCard:hover{transform:translateY(-3px);}
  .charCard svg{width:56px; height:56px; margin-bottom:8px; animation:floaty 3s ease-in-out infinite;}
  .charName{font-weight:600; font-size:13px;}
  .charNameEn{font-size:11px; color:var(--sub); margin-bottom:6px;}
  .charDesc{font-size:12px; color:var(--sub); line-height:1.5;}
  .chapTitle{font-size:17px; font-weight:700; margin-bottom:2px;}
  .chapTitleEn{font-size:12px; color:var(--sub); margin-bottom:12px; font-style:italic;}
  .summaryText{font-size:14.5px; line-height:1.85; margin-bottom:16px;}
  .miniHead{font-size:13px; font-weight:600; color:var(--accent); margin:14px 0 8px;}
  .chip{display:inline-block; font-size:12.5px; background:var(--accent-bg); color:var(--accent); border-radius:20px; padding:4px 10px; margin:0 6px 6px 0;}
  .gpointRow{padding:8px 0; border-top:1px dashed var(--line); font-size:13px;}
  .gpointRow:first-child{border-top:none;}
  .gpointName{font-weight:600; margin-bottom:2px;}
  .toc{display:flex; gap:8px; flex-wrap:wrap; margin-bottom:18px;}
  .toc a{font-size:12.5px; color:var(--accent); background:var(--accent-bg); border-radius:20px; padding:5px 12px; text-decoration:none;}
  .toc a:hover{opacity:0.8;}
</style>
</head>
<body>
<div class="wrap">
  <h1>ナルニア国物語 期末試験対策ツール</h1>
  <p class="lead">授業でマーカーが引かれた語句・表現と、一緒に訳読・読解の練習ができます。間隔反復と苦手問題の自動復習つき。</p>

  <div class="statrow" id="statrow"></div>

  <div class="tabs">
    <div class="tab active" data-tab="vocab">単語・熟語</div>
    <div class="tab" data-tab="underline">下線部訳</div>
    <div class="tab" data-tab="quiz">読解クイズ</div>
    <div class="tab" data-tab="grammar">文法問題</div>
    <div class="tab" data-tab="kotest">小テスト対策</div>
    <div class="tab" data-tab="summary">まとめ</div>
    <div class="tab" data-tab="review">復習<span class="badge" id="reviewBadge" style="display:none"></span></div>
  </div>

  <div class="panel active" id="panel-vocab">
    <div class="subtabs" id="vocabSubtabs">
      <div class="subtab active" data-vmode="card">カード</div>
      <div class="subtab" data-vmode="list">一覧</div>
      <div class="subtab" data-vmode="match">マッチ</div>
    </div>
    <div class="filterrow">
      <select id="vocabChapter"></select>
      <select id="vocabFilter">
        <option value="all">すべて表示</option>
        <option value="due">復習が必要な語のみ</option>
        <option value="exam">小テストの語のみ</option>
      </select>
      <span class="progress" id="vocabProgress"></span>
    </div>
    <div id="vocabArea"></div>
  </div>

  <div class="panel" id="panel-underline">
    <div class="filterrow">
      <select id="underlineChapter"></select>
    </div>
    <div id="underlineArea"></div>
  </div>

  <div class="panel" id="panel-quiz">
    <div class="subtabs" id="quizSubtabs">
      <div class="subtab active" data-qmode="translate">日本語訳を選ぶ</div>
      <div class="subtab" data-qmode="comprehension">内容理解</div>
    </div>
    <div class="filterrow">
      <select id="quizChapter"></select>
    </div>
    <div id="quizArea"></div>
  </div>

  <div class="panel" id="panel-grammar">
    <div id="grammarArea"></div>
  </div>

  <div class="panel" id="panel-kotest">
    <p class="lead" style="margin-top:0">授業の小テストで実際に出た穴埋め問題です。期末試験に出やすい重要表現なので優先的に押さえましょう。</p>
    <div id="kotestArea"></div>
  </div>

  <div class="panel" id="panel-summary">
    <div id="summaryArea"></div>
  </div>

  <div class="panel" id="panel-review">
    <div id="reviewArea"></div>
  </div>
</div>

<script>
const VOCAB = __VOCAB_JSON__;
const UNDERLINE = __UNDERLINE_JSON__;
const QUIZ = __QUIZ_JSON__;
const GRAMMAR = __GRAMMAR_JSON__;
const COMPREHENSION = __COMPREHENSION_JSON__;
const SUMMARY = __SUMMARY_JSON__;
const KOTEST = __KOTEST_JSON__;
</script>
<script>
(function(){

const STORAGE_KEY = 'narnia-progress';
const CHAPTER_COUNT = Math.max(...VOCAB.map(v=>v.chapter), ...QUIZ.map(q=>q.chapter));

function defaultData(){
  return {
    version: 4,
    vocab: {},               // idx -> {box, due}
    underlineDone: {},       // idx -> true
    underlineWrong: {},      // idx -> true
    quizWrong: {},           // idx -> true
    quizScore: {correct:0, total:0},
    grammarWrong: {},        // idx -> true
    grammarScore: {correct:0, total:0},
    comprehensionWrong: {},  // idx -> true
    comprehensionScore: {correct:0, total:0},
    kotestWrong: {},         // idx -> true
    kotestScore: {correct:0, total:0},
  };
}

const store = {
  data: defaultData(),
  async load(){
    // Prefer window.storage when the page is hosted inside an environment
    // that provides it; otherwise (a normal browser / GitHub Pages) fall
    // back to localStorage, which is what actually persists on a plain
    // deployed site.
    try{
      if(window.storage && window.storage.get){
        const r = await window.storage.get(STORAGE_KEY);
        if(r && r.value){
          const parsed = JSON.parse(r.value);
          if(parsed && parsed.version === 4){ this.data = parsed; return; }
        }
      }
    }catch(e){}
    try{
      const raw = localStorage.getItem(STORAGE_KEY);
      if(raw){
        const parsed = JSON.parse(raw);
        if(parsed && parsed.version === 4) this.data = parsed;
      }
    }catch(e){}
  },
  async save(){
    const json = JSON.stringify(this.data);
    try{
      if(window.storage && window.storage.set){ await window.storage.set(STORAGE_KEY, json); }
    }catch(e){}
    try{ localStorage.setItem(STORAGE_KEY, json); }catch(e){}
  }
};

function shuffle(arr){
  const a = arr.slice();
  for(let i=a.length-1;i>0;i--){
    const j = Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function chapterSelectHtml(includeAllLabel){
  let opts = `<option value="all">${includeAllLabel}</option>`;
  for(let c=1;c<=CHAPTER_COUNT;c++) opts += `<option value="${c}">第${c}章</option>`;
  return opts;
}

function fireConfetti(container){
  const colors = ['#8a5a3b','#c9793f','#3b6d11','#a32d2d','#7891a8','#dbb35a'];
  const wrap = document.createElement('div');
  wrap.className = 'confetti';
  for(let i=0;i<14;i++){
    const s = document.createElement('span');
    s.style.left = (Math.random()*100)+'%';
    s.style.background = colors[i % colors.length];
    s.style.animationDelay = (Math.random()*0.3)+'s';
    s.style.transform = `rotate(${Math.random()*360}deg)`;
    wrap.appendChild(s);
  }
  container.appendChild(wrap);
}

// ---------- Leitner spaced repetition (vocab) ----------
const BOX_INTERVAL_DAYS = [0, 0, 1, 2, 4, 7, 14];
const MS_DAY = 86400000;

function vocabState(idx){
  return store.data.vocab[idx] || {box:0, due:0};
}
function isDue(state){
  return !state.due || state.due <= Date.now();
}
function markVocab(idx, correct){
  const cur = vocabState(idx);
  let box = cur.box || 0;
  box = correct ? Math.min(box+1, BOX_INTERVAL_DAYS.length-1) : 0;
  const due = correct ? Date.now() + BOX_INTERVAL_DAYS[box]*MS_DAY : Date.now();
  store.data.vocab[idx] = {box, due};
  store.save();
  updateStats();
}

function updateStats(){
  const learned = Object.values(store.data.vocab).filter(s=>s.box>0).length;
  const dueCount = VOCAB.reduce((n,_,i)=> n + (isDue(vocabState(i)) ? 1 : 0), 0);
  const underDone = Object.keys(store.data.underlineDone).length;
  const qs = store.data.quizScore;
  const gs = store.data.grammarScore;
  const cs = store.data.comprehensionScore;
  const ks = store.data.kotestScore;
  const wrongTotal = Object.keys(store.data.quizWrong).length + Object.keys(store.data.underlineWrong).length + Object.keys(store.data.grammarWrong).length + Object.keys(store.data.comprehensionWrong).length + Object.keys(store.data.kotestWrong).length;
  document.getElementById('statrow').innerHTML = `
    <div class="stat">習得した語彙<b>${learned} / ${VOCAB.length}</b></div>
    <div class="stat">復習が必要な語<b>${dueCount}</b></div>
    <div class="stat">下線部訳 練習済み<b>${underDone} / ${UNDERLINE.length}</b></div>
    <div class="stat">クイズ正答率<b>${qs.total? Math.round(qs.correct/qs.total*100):0}%</b></div>
    <div class="stat">文法問題正答率<b>${gs.total? Math.round(gs.correct/gs.total*100):0}%</b></div>
    <div class="stat">小テスト正答率<b>${ks.total? Math.round(ks.correct/ks.total*100):0}%</b></div>
  `;
  const badge = document.getElementById('reviewBadge');
  if(wrongTotal > 0){ badge.style.display='inline-block'; badge.textContent = wrongTotal; }
  else{ badge.style.display='none'; }
}

// ================= VOCAB TAB =================
let vocabMode = 'card';
let vocabOrder = [];
let vocabIdx = 0;
let vocabFlipped = false;
let vocabShowContext = false;
let vocabChapter = 'all';
let vocabFilterMode = 'all';

function vocabPool(){
  let idxs = VOCAB.map((_,i)=>i);
  if(vocabChapter !== 'all'){
    idxs = idxs.filter(i => VOCAB[i].chapter === Number(vocabChapter));
  }
  return idxs;
}

function vocabPoolWithDueFilter(){
  let idxs = vocabPool();
  if(vocabFilterMode === 'due'){
    idxs = idxs.filter(i => isDue(vocabState(i)));
  } else if(vocabFilterMode === 'exam'){
    idxs = idxs.filter(i => VOCAB[i].exam);
  }
  return idxs;
}

function buildVocabOrder(){
  const pool = vocabPoolWithDueFilter();
  const due = pool.filter(i=>isDue(vocabState(i)));
  const notDue = pool.filter(i=>!isDue(vocabState(i)));
  const grouped = {};
  due.forEach(i=>{ const b=vocabState(i).box; (grouped[b]=grouped[b]||[]).push(i); });
  let dueOrdered = [];
  Object.keys(grouped).sort((a,b)=>a-b).forEach(b=>{ dueOrdered = dueOrdered.concat(shuffle(grouped[b])); });
  notDue.sort((a,b)=> (vocabState(a).due||0) - (vocabState(b).due||0));
  vocabOrder = dueOrdered.concat(notDue);
  vocabIdx = 0;
}

function renderVocabRoot(){
  document.getElementById('vocabFilter').style.display = (vocabMode==='card') ? '' : 'none';
  document.getElementById('vocabProgress').style.display = (vocabMode==='card') ? '' : 'none';
  if(vocabMode === 'card') renderVocabCard();
  else if(vocabMode === 'list') renderVocabList();
  else if(vocabMode === 'match') renderVocabMatch();
}

document.getElementById('vocabSubtabs').querySelectorAll('.subtab').forEach(t=>{
  t.onclick = ()=>{
    document.getElementById('vocabSubtabs').querySelectorAll('.subtab').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    vocabMode = t.dataset.vmode;
    if(vocabMode==='match') buildMatchGame();
    renderVocabRoot();
  };
});

function renderVocabCard(){
  // Full rebuild: only called when the card itself changes (new term / filter
  // change). Flipping and the context-toggle mutate the existing DOM nodes
  // afterwards (see below) so their CSS transitions actually get to animate --
  // replacing the whole subtree on every interaction skips the transition.
  const area = document.getElementById('vocabArea');
  document.getElementById('vocabProgress').textContent = vocabOrder.length ? `${Math.min(vocabIdx+1,vocabOrder.length)} / ${vocabOrder.length}` : '';
  if(vocabOrder.length===0){
    area.innerHTML = `<div class="card empty">この条件のカードはありません。すべて覚えました！</div>`;
    return;
  }
  if(vocabIdx>=vocabOrder.length) vocabIdx = 0;
  const gi = vocabOrder[vocabIdx];
  const item = VOCAB[gi];
  const st = vocabState(gi);
  const boxLabel = st.box>0 ? `習熟度 ${st.box} / ${BOX_INTERVAL_DAYS.length-1}` : '未学習';
  area.innerHTML = `
    <div class="card flip-outer flip-3d" id="flipOuter">
      <div class="flip-inner" id="flipInner">
        <div class="flip-face front">
          <div class="term">${item.term}</div>
          <div class="hint">タップして意味を確認</div>
          <div class="srsbadge">第${item.chapter}章・${boxLabel}${item.exam ? ' <span class="badge">小テスト</span>' : ''}</div>
        </div>
        <div class="flip-face back">
          <div class="term" style="margin-bottom:2px">${item.term}</div>
          <div class="gloss-big">${item.gloss || ''}</div>
          <div class="srsbadge">第${item.chapter}章・${boxLabel}${item.exam ? ' <span class="badge">小テスト</span>' : ''}</div>
          <div class="context-toggle"><button id="toggleContext">例文を見る</button></div>
          <div class="context-box hidden" id="ctxBox">
            <div class="en">${item.enHtml}</div>
            <div class="jp">${item.jp}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="btnrow">
      <button id="prevVocab">前へ</button>
      <button class="bad" id="markUnknown">まだ</button>
      <button class="good" id="markKnown">覚えた</button>
      <button class="primary" id="nextVocab">次へ</button>
    </div>
  `;
  vocabFlipped = false;
  vocabShowContext = false;
  document.getElementById('flipOuter').onclick = ()=>{
    vocabFlipped = !vocabFlipped;
    document.getElementById('flipInner').classList.toggle('flipped', vocabFlipped);
  };
  document.getElementById('toggleContext').onclick = (e)=>{
    e.stopPropagation();
    vocabShowContext = !vocabShowContext;
    const box = document.getElementById('ctxBox');
    box.classList.toggle('hidden', !vocabShowContext);
    e.currentTarget.textContent = vocabShowContext ? '例文を隠す' : '例文を見る';
  };
  const advance = (correct)=>{
    if(correct!==null) markVocab(gi, correct);
    vocabIdx++;
    renderVocabCard();
  };
  document.getElementById('nextVocab').onclick = (e)=>{ e.stopPropagation(); advance(null); };
  document.getElementById('prevVocab').onclick = (e)=>{ e.stopPropagation(); vocabIdx=Math.max(0,vocabIdx-1); renderVocabCard(); };
  document.getElementById('markKnown').onclick = (e)=>{ e.stopPropagation(); advance(true); };
  document.getElementById('markUnknown').onclick = (e)=>{ e.stopPropagation(); advance(false); };
}

// ---- vocab list view ----
let vocabListSearch = '';
function renderVocabList(){
  const area = document.getElementById('vocabArea');
  let idxs = vocabPoolWithDueFilter();
  if(vocabListSearch.trim()){
    const q = vocabListSearch.trim().toLowerCase();
    idxs = idxs.filter(i => VOCAB[i].term.toLowerCase().includes(q) || (VOCAB[i].gloss||'').includes(q));
  }
  const rows = idxs.map(i=>{
    const item = VOCAB[i];
    return `<div class="vlistRow"><span class="vlistTerm">${item.term}${item.exam ? ' <span class="badge">小テスト</span>' : ''}</span><span class="vlistGloss">${item.gloss||''}</span><span class="vlistChap">第${item.chapter}章</span></div>`;
  }).join('');
  area.innerHTML = `
    <div class="card">
      <input type="text" id="vlistSearch" placeholder="検索（英語 or 日本語）" style="width:100%; margin-bottom:12px;" value="${escapeHtml(vocabListSearch)}">
      <div class="progress">${idxs.length} 件</div>
      ${rows || '<div class="empty">該当する語がありません</div>'}
    </div>
  `;
  const input = document.getElementById('vlistSearch');
  input.oninput = (e)=>{ vocabListSearch = e.target.value; renderVocabList(); };
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
}

// ---- vocab match game (Quizlet Match: every tile is visible from the start;
// tap two tiles that form a term/meaning pair and they clear off the board) ----
let matchCards = [];       // {uid, vocabIdx, side, text, cleared, clearing}
let matchSelected = [];    // up to 2 uids currently selected
let matchWrongIds = [];    // uids currently flashing red
let matchMoves = 0;
let matchLocked = false;
let matchStartTs = 0;
let matchTimerHandle = null;

function buildMatchGame(){
  const pool = vocabPoolWithDueFilter().filter(i => VOCAB[i].gloss);
  const n = Math.min(6, pool.length);
  const chosen = shuffle(pool).slice(0, n);
  const cards = [];
  chosen.forEach((vi, i)=>{
    cards.push({uid:'t'+i, vocabIdx:vi, side:'term', text:VOCAB[vi].term, cleared:false, clearing:false});
    cards.push({uid:'g'+i, vocabIdx:vi, side:'gloss', text:VOCAB[vi].gloss, cleared:false, clearing:false});
  });
  matchCards = shuffle(cards);
  matchSelected = [];
  matchWrongIds = [];
  matchMoves = 0;
  matchLocked = false;
  matchStartTs = Date.now();
  if(matchTimerHandle) clearInterval(matchTimerHandle);
  matchTimerHandle = setInterval(()=>{
    if(vocabMode==='match'){
      const el = document.getElementById('matchTimer');
      if(el) el.textContent = Math.floor((Date.now()-matchStartTs)/1000) + '秒';
    }
  }, 1000);
}

// Builds the match-game DOM exactly once per game (new game / mode switch /
// filter change / restart). Taps afterwards only toggle classes on the
// existing tile elements via syncMatchTiles() -- rebuilding the whole
// innerHTML on every tap was recreating the outer .card wrapper each time,
// which replays its mount animation (fadeInUp) and reads as a "bounce" on
// every interaction.
function renderVocabMatch(){
  const area = document.getElementById('vocabArea');
  if(matchCards.length===0){
    area.innerHTML = `<div class="card empty">この条件では6語未満しかないため、マッチゲームを作成できません。章の範囲を広げてみてください。</div>`;
    return;
  }
  area.innerHTML = `
    <div class="card">
      <div class="matchTop">
        <span>ペアになる「英語」と「意味」のタイルを2枚タップして選んでください</span>
        <span>手数: <span id="matchMovesLabel">0</span>　経過時間: <span id="matchTimer">0秒</span></span>
      </div>
      <div class="empty" id="matchDone" style="display:none"></div>
      <div class="matchGrid" id="matchGrid"></div>
    </div>
  `;
  const grid = document.getElementById('matchGrid');
  matchCards.forEach(c=>{
    const tile = document.createElement('div');
    tile.className = 'matchTile';
    tile.dataset.uid = c.uid;
    tile.textContent = c.text;
    tile.onclick = ()=> onMatchTileClick(c.uid);
    grid.appendChild(tile);
  });
  syncMatchTiles();
}

function syncMatchTiles(){
  const movesEl = document.getElementById('matchMovesLabel');
  if(movesEl) movesEl.textContent = matchMoves;
  matchCards.forEach(c=>{
    const tile = document.querySelector(`.matchTile[data-uid="${c.uid}"]`);
    if(!tile) return;
    tile.classList.toggle('selected', matchSelected.includes(c.uid));
    tile.classList.toggle('wrong', matchWrongIds.includes(c.uid));
    tile.classList.toggle('clearing', !!c.clearing);
    tile.classList.toggle('cleared', !!c.cleared);
  });
  const allCleared = matchCards.every(c=>c.cleared);
  const doneEl = document.getElementById('matchDone');
  if(!doneEl) return;
  if(allCleared){
    if(doneEl.dataset.shown !== '1'){
      doneEl.dataset.shown = '1';
      doneEl.style.display = '';
      doneEl.innerHTML = `🎉 全ペア達成！ お見事です。<div class="btnrow" style="justify-content:center"><button class="primary" id="matchAgain">もう一度</button></div>`;
      fireConfetti(doneEl);
      document.getElementById('matchAgain').onclick = ()=>{ buildMatchGame(); renderVocabMatch(); };
    }
  } else {
    doneEl.dataset.shown = '0';
    doneEl.style.display = 'none';
  }
}

function onMatchTileClick(uid){
  if(matchLocked) return;
  const card = matchCards.find(c=>c.uid===uid);
  if(!card || card.cleared) return;
  if(matchSelected.includes(uid)){
    matchSelected = matchSelected.filter(id=>id!==uid);
    syncMatchTiles();
    return;
  }
  if(matchSelected.length>=2) return;
  matchSelected.push(uid);
  syncMatchTiles();
  if(matchSelected.length===2){
    matchLocked = true;
    matchMoves++;
    const [a,b] = matchSelected.map(id=>matchCards.find(c=>c.uid===id));
    const isMatch = a.vocabIdx===b.vocabIdx && a.side!==b.side;
    if(isMatch){
      setTimeout(()=>{
        a.clearing = true; b.clearing = true;
        syncMatchTiles();
        setTimeout(()=>{
          a.cleared = true; b.cleared = true;
          matchSelected = [];
          matchLocked = false;
          syncMatchTiles();
        }, 500);
      }, 220);
    } else {
      matchWrongIds = [a.uid, b.uid];
      syncMatchTiles();
      setTimeout(()=>{
        matchWrongIds = [];
        matchSelected = [];
        matchLocked = false;
        syncMatchTiles();
      }, 550);
    }
  }
}

document.getElementById('vocabChapter').innerHTML = chapterSelectHtml('すべての章');
document.getElementById('vocabChapter').onchange = (e)=>{
  vocabChapter = e.target.value; vocabFlipped=false; vocabShowContext=false;
  buildVocabOrder();
  if(vocabMode==='match') buildMatchGame();
  renderVocabRoot();
};
document.getElementById('vocabFilter').onchange = (e)=>{ vocabFilterMode = e.target.value; vocabFlipped=false; vocabShowContext=false; buildVocabOrder(); renderVocabRoot(); };

// ================= UNDERLINE TAB =================
let underlineOrder = [];
let underlineIdx = 0;
let underlineChapter = 'all';

function buildUnderlineOrder(){
  let idxs = UNDERLINE.map((_,i)=>i);
  if(underlineChapter !== 'all'){
    idxs = idxs.filter(i => UNDERLINE[i].chapter === Number(underlineChapter));
  }
  underlineOrder = shuffle(idxs);
  underlineIdx = 0;
}

function renderUnderline(){
  const area = document.getElementById('underlineArea');
  if(underlineOrder.length===0){
    area.innerHTML = `<div class="card empty">この条件の下線部はありません。</div>`;
    return;
  }
  if(underlineIdx >= underlineOrder.length) underlineIdx = 0;
  const gi = underlineOrder[underlineIdx];
  const item = UNDERLINE[gi];
  area.innerHTML = `
    <div class="progress">${underlineIdx+1} / ${underlineOrder.length}（第${item.chapter}章）：下線部を日本語に訳してみましょう。</div>
    <div class="card">
      <div class="en">${item.enHtml}</div>
      <textarea id="ansBox" placeholder="下線部の日本語訳を入力"></textarea>
      <div class="btnrow">
        <button class="primary" id="showAns">答えを見る</button>
      </div>
      <div class="reveal" id="revealArea" style="display:none">
        <div class="jp"><b style="color:var(--ink)">全体の日本語訳：</b><br>${item.jp}</div>
        <div class="btnrow">
          <button class="good" id="selfGood">できた</button>
          <button class="bad" id="selfBad">もう一度復習</button>
          <button id="nextUnderline">次の問題</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById('showAns').onclick = ()=>{
    document.getElementById('revealArea').style.display = 'block';
  };
  document.getElementById('selfGood').onclick = ()=>{
    store.data.underlineDone[gi] = true;
    delete store.data.underlineWrong[gi];
    store.save(); updateStats();
    underlineIdx++; renderUnderline();
  };
  document.getElementById('selfBad').onclick = ()=>{
    store.data.underlineWrong[gi] = true;
    store.save(); updateStats();
    underlineIdx++; renderUnderline();
  };
  const nb = document.getElementById('nextUnderline');
  if(nb) nb.onclick = ()=>{ underlineIdx++; renderUnderline(); };
}

document.getElementById('underlineChapter').innerHTML = chapterSelectHtml('すべての章');
document.getElementById('underlineChapter').onchange = (e)=>{ underlineChapter = e.target.value; buildUnderlineOrder(); renderUnderline(); };

// ================= QUIZ TAB (translate + comprehension) =================
let quizMode = 'translate';
let quizOrder = [];
let quizIdx = 0;
let quizAnswered = false;
let quizChapter = 'all';

let compOrder = [];
let compIdx = 0;

function buildQuizOrder(){
  let idxs = QUIZ.map((_,i)=>i);
  if(quizChapter !== 'all'){
    idxs = idxs.filter(i => QUIZ[i].chapter === Number(quizChapter));
  }
  quizOrder = shuffle(idxs).slice(0, 30);
  quizIdx = 0;
}

function buildCompOrder(){
  let idxs = COMPREHENSION.map((_,i)=>i);
  if(quizChapter !== 'all'){
    idxs = idxs.filter(i => COMPREHENSION[i].chapter === Number(quizChapter));
  }
  compOrder = shuffle(idxs);
  compIdx = 0;
}

function buildChoices(correctIdx){
  const pool = QUIZ.filter((_,i)=>i!==correctIdx).map(q=>q.jp);
  const decoys = shuffle(pool).slice(0,3);
  const options = shuffle([QUIZ[correctIdx].jp, ...decoys]);
  return options;
}

function renderQuizRoot(){
  document.getElementById('quizChapter').querySelector('option[value="all"]').textContent =
    quizMode==='translate' ? 'すべての章（ランダム30問）' : 'すべての章';
  if(quizMode==='translate') renderQuiz();
  else renderComprehension();
}

document.getElementById('quizSubtabs').querySelectorAll('.subtab').forEach(t=>{
  t.onclick = ()=>{
    document.getElementById('quizSubtabs').querySelectorAll('.subtab').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    quizMode = t.dataset.qmode;
    renderQuizRoot();
  };
});

function renderQuiz(){
  const area = document.getElementById('quizArea');
  if(quizOrder.length===0){
    area.innerHTML = `<div class="card empty">この条件の問題はありません。</div>`;
    return;
  }
  if(quizIdx >= quizOrder.length){
    area.innerHTML = `<div class="card empty" id="quizDoneCard">クイズ終了です。お疲れ様でした。<div class="btnrow" style="justify-content:center"><button class="primary" id="restartQuiz">もう一度</button></div></div>`;
    fireConfetti(document.getElementById('quizDoneCard'));
    document.getElementById('restartQuiz').onclick = ()=>{ buildQuizOrder(); renderQuiz(); };
    return;
  }
  const qi = quizOrder[quizIdx];
  const item = QUIZ[qi];
  const options = buildChoices(qi);
  quizAnswered = false;
  area.innerHTML = `
    <div class="progress">${quizIdx+1} / ${quizOrder.length}（第${item.chapter}章）：正しい日本語訳を選んでください</div>
    <div class="card">
      <div class="en">${item.en}</div>
      <div id="choiceArea"></div>
    </div>
  `;
  const choiceArea = document.getElementById('choiceArea');
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(quizAnswered) return;
      quizAnswered = true;
      const correct = opt === item.jp;
      store.data.quizScore.total++;
      if(correct){ store.data.quizScore.correct++; delete store.data.quizWrong[qi]; }
      else{ store.data.quizWrong[qi] = true; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.jp) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ quizIdx++; renderQuiz(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

function renderComprehension(){
  const area = document.getElementById('quizArea');
  if(compOrder.length===0){
    area.innerHTML = `<div class="card empty">この条件の問題はありません。</div>`;
    return;
  }
  if(compIdx >= compOrder.length){
    area.innerHTML = `<div class="card empty" id="compDoneCard">内容理解クイズ終了です。お疲れ様でした。<div class="btnrow" style="justify-content:center"><button class="primary" id="restartComp">もう一度</button></div></div>`;
    fireConfetti(document.getElementById('compDoneCard'));
    document.getElementById('restartComp').onclick = ()=>{ buildCompOrder(); renderComprehension(); };
    return;
  }
  const ci = compOrder[compIdx];
  const item = COMPREHENSION[ci];
  let answered = false;
  area.innerHTML = `
    <div class="progress">${compIdx+1} / ${compOrder.length}（第${item.chapter}章）：本文の内容として正しいものを選んでください</div>
    <div class="card">
      <div class="en" style="font-size:16.5px; font-weight:600">${item.q}</div>
      <div id="compChoiceArea"></div>
    </div>
  `;
  const choiceArea = document.getElementById('compChoiceArea');
  const options = shuffle(item.choices);
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(answered) return;
      answered = true;
      const correct = opt === item.answer;
      store.data.comprehensionScore.total++;
      if(correct){ store.data.comprehensionScore.correct++; delete store.data.comprehensionWrong[ci]; }
      else{ store.data.comprehensionWrong[ci] = true; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const ex = document.createElement('div');
      ex.className = 'explain';
      ex.textContent = item.explain;
      choiceArea.appendChild(ex);
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ compIdx++; renderComprehension(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

document.getElementById('quizChapter').innerHTML = chapterSelectHtml('すべての章（ランダム30問）');
document.getElementById('quizChapter').onchange = (e)=>{
  quizChapter = e.target.value;
  buildQuizOrder(); buildCompOrder();
  renderQuizRoot();
};

// ================= GRAMMAR TAB =================
let grammarOrder = [];
let grammarIdx = 0;
let grammarAnswered = false;
let grammarHintShown = false;

function buildGrammarOrder(){
  grammarOrder = shuffle(GRAMMAR.map((_,i)=>i));
  grammarIdx = 0;
}

function renderGrammar(){
  const area = document.getElementById('grammarArea');
  if(grammarIdx >= grammarOrder.length){
    area.innerHTML = `<div class="card empty" id="gramDoneCard">文法問題は以上です。お疲れ様でした。<div class="btnrow" style="justify-content:center"><button class="primary" id="restartGrammar">もう一度</button></div></div>`;
    fireConfetti(document.getElementById('gramDoneCard'));
    document.getElementById('restartGrammar').onclick = ()=>{ buildGrammarOrder(); renderGrammar(); };
    return;
  }
  const gi = grammarOrder[grammarIdx];
  const item = GRAMMAR[gi];
  grammarAnswered = false;
  grammarHintShown = false;
  area.innerHTML = `
    <div class="progress">${grammarIdx+1} / ${grammarOrder.length}</div>
    <div class="card">
      <div id="gHintArea">
        <button id="gShowHint">💡 ヒント（文法ポイント）を見る</button>
      </div>
      <div class="en" style="margin-top:14px">${item.en}</div>
      <div id="gChoiceArea"></div>
      <div id="gExplain" style="display:none" class="explain"></div>
    </div>
  `;
  document.getElementById('gShowHint').onclick = ()=>{
    grammarHintShown = true;
    document.getElementById('gHintArea').innerHTML = `<div class="point-badge">${item.point}</div>`;
  };
  const choiceArea = document.getElementById('gChoiceArea');
  const options = shuffle(item.choices);
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(grammarAnswered) return;
      grammarAnswered = true;
      const correct = opt === item.answer;
      store.data.grammarScore.total++;
      if(correct){ store.data.grammarScore.correct++; delete store.data.grammarWrong[gi]; }
      else{ store.data.grammarWrong[gi] = true; }
      store.save(); updateStats();
      if(!grammarHintShown){
        document.getElementById('gHintArea').innerHTML = `<div class="point-badge">${item.point}</div>`;
      }
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const ex = document.getElementById('gExplain');
      ex.style.display = 'block';
      ex.textContent = item.explain;
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ grammarIdx++; renderGrammar(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

// ================= KOTEST TAB (weekly pop-quiz fill-in-the-blank) =================
let kotestOrder = [];
let kotestIdx = 0;
let kotestAnswered = false;

function buildKotestOrder(){
  kotestOrder = shuffle(KOTEST.map((_,i)=>i));
  kotestIdx = 0;
}

function kotestChoices(item){
  const ans = item.answer;
  const isShort = ans.split(' ').length === 1 && ans.length <= 6;
  const sameBucket = [...new Set(KOTEST.map(x=>x.answer))].filter(a=>{
    const aShort = a.split(' ').length === 1 && a.length <= 6;
    return aShort === isShort && a.toLowerCase() !== ans.toLowerCase();
  });
  const decoys = shuffle(sameBucket).slice(0,3);
  return shuffle([ans, ...decoys]);
}

function renderKotest(){
  const area = document.getElementById('kotestArea');
  if(kotestIdx >= kotestOrder.length){
    area.innerHTML = `<div class="card empty" id="kotestDoneCard">小テスト対策は以上です。お疲れ様でした。<div class="btnrow" style="justify-content:center"><button class="primary" id="restartKotest">もう一度</button></div></div>`;
    fireConfetti(document.getElementById('kotestDoneCard'));
    document.getElementById('restartKotest').onclick = ()=>{ buildKotestOrder(); renderKotest(); };
    return;
  }
  const ki = kotestOrder[kotestIdx];
  const item = KOTEST[ki];
  kotestAnswered = false;
  area.innerHTML = `
    <div class="progress">${kotestIdx+1} / ${kotestOrder.length}：空欄に入る語句を選んでください</div>
    <div class="card">
      <div class="en" style="font-size:17px">${item.en}</div>
      <div id="kChoiceArea"></div>
    </div>
  `;
  const choiceArea = document.getElementById('kChoiceArea');
  kotestChoices(item).forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(kotestAnswered) return;
      kotestAnswered = true;
      const correct = opt === item.answer;
      store.data.kotestScore.total++;
      if(correct){ store.data.kotestScore.correct++; delete store.data.kotestWrong[ki]; }
      else{ store.data.kotestWrong[ki] = true; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ kotestIdx++; renderKotest(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

// ================= SUMMARY TAB =================
const CHAR_ICON = {
  peter:   {bg:'#8a5a3b', mark:`<polygon points="62,10 65,17 72,18 66,23 68,30 62,26 56,30 58,23 52,18 59,17" fill="#f3e6d8"/>`},
  susan:   {bg:'#a9776a', mark:`<circle cx="63" cy="16" r="5" fill="#f3e6d8"/><path d="M52 18 Q58 12 63 16 Q68 12 74 18" stroke="#f3e6d8" stroke-width="2" fill="none"/>`},
  edmund:  {bg:'#6b6b64', mark:`<rect x="55" y="9" width="15" height="15" rx="3" fill="#f3e6d8"/><rect x="55" y="9" width="15" height="15" rx="3" fill="none" stroke="#c9793f" stroke-width="1.5"/>`},
  lucy:    {bg:'#c9793f', mark:`<circle cx="63" cy="16" r="4" fill="#fff7e6"/><circle cx="55" cy="20" r="3" fill="#fff7e6"/><circle cx="71" cy="20" r="3" fill="#fff7e6"/><circle cx="63" cy="24" r="3" fill="#fff7e6"/>`},
  tumnus_icon: {bg:'#7a5c3e', mark:`<path d="M50 20 Q46 8 54 6" stroke="#f3e6d8" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M76 20 Q80 8 72 6" stroke="#f3e6d8" stroke-width="3" fill="none" stroke-linecap="round"/>`},
  witch_icon: {bg:'#7891a8', mark:`<polygon points="63,6 70,20 56,20" fill="#dbe8f0"/><circle cx="63" cy="6" r="3" fill="#dbe8f0"/>`},
  professor: {bg:'#5c4a3a', mark:`<circle cx="55" cy="14" r="6" fill="none" stroke="#f3e6d8" stroke-width="2"/><circle cx="71" cy="14" r="6" fill="none" stroke="#f3e6d8" stroke-width="2"/><line x1="61" y1="14" x2="65" y2="14" stroke="#f3e6d8" stroke-width="2"/>`},
  macready:  {bg:'#8a6d5a', mark:`<circle cx="64" cy="14" r="5" fill="none" stroke="#f3e6d8" stroke-width="2.5"/><rect x="68" y="12" width="7" height="3.5" fill="#f3e6d8"/>`},
  dwarf_icon: {bg:'#5f6b5a', mark:`<polygon points="63,3 74,22 52,22" fill="#f3e6d8"/><circle cx="63" cy="3" r="2.5" fill="#c9793f"/>`},
  servants:  {bg:'#a89a8a', mark:`<circle cx="52" cy="14" r="4" fill="#f3e6d8"/><circle cx="64" cy="10" r="4" fill="#f3e6d8"/><circle cx="76" cy="14" r="4" fill="#f3e6d8"/>`},
};

function avatarSvg(key, initial){
  const cfg = CHAR_ICON[key] || {bg:'#8a5a3b', mark:''};
  return `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="40" fill="${cfg.bg}"/>
    <text x="40" y="52" font-size="28" text-anchor="middle" fill="#fff" font-family="'Hiragino Sans', sans-serif" font-weight="700">${initial}</text>
    ${cfg.mark}
  </svg>`;
}

const BANNER_SVG = {
  wardrobe: `<svg viewBox="0 0 320 130" xmlns="http://www.w3.org/2000/svg">
    <rect width="320" height="130" fill="#f3e6d8"/>
    <rect x="120" y="15" width="90" height="100" rx="4" fill="#8a5a3b"/>
    <rect x="120" y="15" width="90" height="100" rx="4" fill="none" stroke="#5f3d27" stroke-width="2"/>
    <line x1="165" y1="15" x2="165" y2="115" stroke="#5f3d27" stroke-width="2"/>
    <circle cx="155" cy="65" r="2.5" fill="#f3e6d8"/><circle cx="175" cy="65" r="2.5" fill="#f3e6d8"/>
    <path d="M210 15 L245 25 L245 105 L210 115 Z" fill="#2b3a4a"/>
    <circle cx="228" cy="55" r="2" fill="#fff"/><circle cx="220" cy="70" r="1.5" fill="#fff"/><circle cx="235" cy="80" r="1.5" fill="#fff"/>
    <line x1="228" y1="40" x2="228" y2="95" stroke="#dbe8f0" stroke-width="1.5"/>
    <rect x="223" y="35" width="10" height="6" fill="#dbe8f0"/>
    <circle cx="60" cy="30" r="2" fill="#c9d9e4"/><circle cx="80" cy="55" r="1.5" fill="#c9d9e4"/>
    <circle cx="45" cy="75" r="2" fill="#c9d9e4"/><circle cx="270" cy="30" r="2" fill="#c9d9e4"/><circle cx="290" cy="60" r="1.5" fill="#c9d9e4"/>
  </svg>`,
  tumnus: `<svg viewBox="0 0 320 130" xmlns="http://www.w3.org/2000/svg">
    <rect width="320" height="130" fill="#f3e6d8"/>
    <path d="M0 130 C 40 40, 280 40, 320 130 Z" fill="#7a5c3e" opacity="0.22"/>
    <path d="M150 115 q10 -30 0 -40 q10 10 5 25 q10 -20 -2 -35 q12 8 8 30 q8 -10 2 -22 q6 15 -3 42 Z" fill="#c9793f"/>
    <ellipse cx="150" cy="118" rx="26" ry="5" fill="#5f3d27"/>
    <ellipse cx="220" cy="95" rx="35" ry="8" fill="#8a5a3b"/>
    <rect x="215" y="95" width="10" height="18" fill="#5f3d27"/>
    <rect x="205" y="82" width="10" height="10" rx="2" fill="#faf8f4"/>
    <rect x="228" y="82" width="10" height="10" rx="2" fill="#faf8f4"/>
    <path d="M70 90 a25 25 0 0 1 50 0 Z" fill="#a32d2d"/>
    <line x1="95" y1="90" x2="95" y2="120" stroke="#5f3d27" stroke-width="3"/>
  </svg>`,
  sledge: `<svg viewBox="0 0 320 130" xmlns="http://www.w3.org/2000/svg">
    <rect width="320" height="130" fill="#eaf1f6"/>
    <path d="M0 110 Q80 85 160 105 T320 100 V130 H0 Z" fill="#ffffff"/>
    <path d="M110 95 Q130 70 190 80 L200 95 Z" fill="#8a5a3b"/>
    <path d="M100 100 Q150 108 210 100" stroke="#5f3d27" stroke-width="4" fill="none" stroke-linecap="round"/>
    <polygon points="150,60 156,75 144,75" fill="#dbb35a"/>
    <polygon points="140,64 146,75 134,75" fill="#dbb35a"/>
    <polygon points="160,64 166,75 154,75" fill="#dbb35a"/>
    <path d="M60 60 l-10 -15 M60 60 l-2 -18 M60 60 l8 -14" stroke="#7a5c3e" stroke-width="2" fill="none"/>
    <path d="M85 60 l-10 -15 M85 60 l-2 -18 M85 60 l8 -14" stroke="#7a5c3e" stroke-width="2" fill="none"/>
    <circle cx="30" cy="30" r="2" fill="#c9d9e4"/><circle cx="250" cy="25" r="2" fill="#c9d9e4"/>
    <circle cx="280" cy="50" r="1.5" fill="#c9d9e4"/><circle cx="20" cy="60" r="1.5" fill="#c9d9e4"/>
  </svg>`,
  witch: `<svg viewBox="0 0 320 130" xmlns="http://www.w3.org/2000/svg">
    <rect width="320" height="130" fill="#dfe9f0"/>
    <path d="M20 0 L26 22 L32 0 Z" fill="#b9d3e0"/><path d="M60 0 L64 15 L68 0 Z" fill="#b9d3e0"/>
    <path d="M250 0 L256 26 L262 0 Z" fill="#b9d3e0"/><path d="M290 0 L294 14 L298 0 Z" fill="#b9d3e0"/>
    <polygon points="160,35 172,65 148,65" fill="#7891a8"/>
    <polygon points="140,45 150,65 130,65" fill="#7891a8"/>
    <polygon points="180,45 190,65 170,65" fill="#7891a8"/>
    <circle cx="160" cy="35" r="4" fill="#dbe8f0"/>
    <path d="M110 65 Q160 100 210 65 L220 118 Q160 130 100 118 Z" fill="#5c7186"/>
    <line x1="230" y1="70" x2="255" y2="115" stroke="#dbe8f0" stroke-width="3" stroke-linecap="round"/>
    <polygon points="230,63 236,72 224,72" fill="#dbe8f0"/>
  </svg>`,
  hideseek: `<svg viewBox="0 0 320 130" xmlns="http://www.w3.org/2000/svg">
    <rect width="320" height="130" fill="#f3e6d8"/>
    <rect x="30" y="15" width="70" height="100" rx="3" fill="#faf8f4" stroke="#8a5a3b" stroke-width="3"/>
    <circle cx="88" cy="65" r="2.5" fill="#8a5a3b"/>
    <rect x="220" y="30" width="60" height="80" rx="3" fill="#8a5a3b"/>
    <line x1="250" y1="30" x2="250" y2="110" stroke="#5f3d27" stroke-width="2"/>
    <circle cx="150" cy="95" r="10" fill="#c9793f"/><circle cx="180" cy="100" r="8" fill="#a9776a"/>
    <text x="140" y="45" font-size="26" fill="#8a5a3b" font-family="sans-serif" font-weight="700">?</text>
    <text x="185" y="60" font-size="18" fill="#c9793f" font-family="sans-serif" font-weight="700">?</text>
  </svg>`,
};

function renderSummary(){
  const area = document.getElementById('summaryArea');
  let html = '';

  html += `<div class="toc">`;
  SUMMARY.chapters.forEach(c=>{ html += `<a href="#sum-ch${c.chapter}">第${c.chapter}章</a>`; });
  html += `<a href="#sum-chars">登場人物</a></div>`;

  html += `<div class="card" id="sum-chars"><div class="subhead">登場人物</div><div class="charGrid">`;
  SUMMARY.characters.forEach(ch=>{
    html += `
      <div class="charCard">
        ${avatarSvg(ch.svg, ch.name_jp[0])}
        <div class="charName">${ch.name_jp}</div>
        <div class="charNameEn">${ch.name_en}</div>
        <div class="charDesc">${ch.desc}</div>
      </div>
    `;
  });
  html += `</div></div>`;

  SUMMARY.chapters.forEach(c=>{
    const gpoints = GRAMMAR.filter(g => g.chapter === c.chapter);
    const vocabTerms = VOCAB.filter(v => v.chapter === c.chapter && v.term.split(' ').length > 1).slice(0, 8);
    const vocabFallback = vocabTerms.length ? vocabTerms : VOCAB.filter(v => v.chapter === c.chapter).slice(0, 8);
    html += `
      <div class="card" id="sum-ch${c.chapter}">
        ${BANNER_SVG[c.svg] || ''}
        <div class="chapTitle">第${c.chapter}章　${c.title_jp}</div>
        <div class="chapTitleEn">${c.title}</div>
        <div class="summaryText">${c.summary}</div>
        <div class="miniHead">この章の重要文法ポイント</div>
        ${gpoints.map(g=>`<div class="gpointRow"><div class="gpointName">${g.point}</div><div>${g.explain}</div></div>`).join('') || '<div class="progress">なし</div>'}
        <div class="miniHead">この章のキーワード</div>
        ${vocabFallback.map(v=>`<span class="chip">${v.term}: ${v.gloss}</span>`).join('')}
      </div>
    `;
  });

  area.innerHTML = html;
}

// ================= REVIEW TAB =================
function renderReview(){
  const area = document.getElementById('reviewArea');
  const qWrong = Object.keys(store.data.quizWrong).map(Number).filter(i=>QUIZ[i]);
  const uWrong = Object.keys(store.data.underlineWrong).map(Number).filter(i=>UNDERLINE[i]);
  const gWrong = Object.keys(store.data.grammarWrong).map(Number).filter(i=>GRAMMAR[i]);
  const cWrong = Object.keys(store.data.comprehensionWrong).map(Number).filter(i=>COMPREHENSION[i]);
  const kWrong = Object.keys(store.data.kotestWrong).map(Number).filter(i=>KOTEST[i]);

  if(qWrong.length===0 && uWrong.length===0 && gWrong.length===0 && cWrong.length===0 && kWrong.length===0){
    area.innerHTML = `<div class="card empty">苦手問題はありません。素晴らしい！<br>クイズ・下線部訳・文法問題・内容理解・小テスト対策で間違えると、ここに自動で表示されます。</div>`;
    return;
  }

  area.innerHTML = `
    <div class="reviewSection">
      <div class="subhead">小テスト対策の苦手問題（${kWrong.length}件）</div>
      <div id="reviewKotestArea"></div>
    </div>
    <div class="reviewSection">
      <div class="subhead">読解クイズ（日本語訳）の苦手問題（${qWrong.length}件）</div>
      <div id="reviewQuizArea"></div>
    </div>
    <div class="reviewSection">
      <div class="subhead">内容理解の苦手問題（${cWrong.length}件）</div>
      <div id="reviewCompArea"></div>
    </div>
    <div class="reviewSection">
      <div class="subhead">下線部訳の苦手問題（${uWrong.length}件）</div>
      <div id="reviewUnderlineArea"></div>
    </div>
    <div class="reviewSection">
      <div class="subhead">文法問題の苦手問題（${gWrong.length}件）</div>
      <div id="reviewGrammarArea"></div>
    </div>
  `;
  renderReviewKotest(kWrong);
  renderReviewQuiz(qWrong);
  renderReviewComp(cWrong);
  renderReviewUnderline(uWrong);
  renderReviewGrammar(gWrong);
}

function renderReviewKotest(list){
  const area = document.getElementById('reviewKotestArea');
  if(list.length===0){ area.innerHTML = `<div class="card empty" style="padding:16px">なし</div>`; return; }
  const ki = list[0];
  const item = KOTEST[ki];
  let answered = false;
  area.innerHTML = `<div class="card"><div class="en" style="font-size:17px">${item.en}</div><div id="rkChoiceArea"></div></div>`;
  const choiceArea = document.getElementById('rkChoiceArea');
  kotestChoices(item).forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(answered) return;
      answered = true;
      const correct = opt === item.answer;
      if(correct){ delete store.data.kotestWrong[ki]; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ renderReview(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

function renderReviewQuiz(list){
  const area = document.getElementById('reviewQuizArea');
  if(list.length===0){ area.innerHTML = `<div class="card empty" style="padding:16px">なし</div>`; return; }
  const qi = list[0];
  const item = QUIZ[qi];
  const options = buildChoices(qi);
  let answered = false;
  area.innerHTML = `<div class="card"><div class="en">${item.en}</div><div id="rqChoiceArea"></div></div>`;
  const choiceArea = document.getElementById('rqChoiceArea');
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(answered) return;
      answered = true;
      const correct = opt === item.jp;
      if(correct){ delete store.data.quizWrong[qi]; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.jp) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ renderReview(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

function renderReviewComp(list){
  const area = document.getElementById('reviewCompArea');
  if(list.length===0){ area.innerHTML = `<div class="card empty" style="padding:16px">なし</div>`; return; }
  const ci = list[0];
  const item = COMPREHENSION[ci];
  let answered = false;
  area.innerHTML = `<div class="card"><div class="en" style="font-weight:600">${item.q}</div><div id="rcChoiceArea"></div></div>`;
  const choiceArea = document.getElementById('rcChoiceArea');
  const options = shuffle(item.choices);
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(answered) return;
      answered = true;
      const correct = opt === item.answer;
      if(correct){ delete store.data.comprehensionWrong[ci]; }
      store.save(); updateStats();
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const ex = document.createElement('div');
      ex.className = 'explain';
      ex.textContent = item.explain;
      choiceArea.appendChild(ex);
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ renderReview(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

function renderReviewUnderline(list){
  const area = document.getElementById('reviewUnderlineArea');
  if(list.length===0){ area.innerHTML = `<div class="card empty" style="padding:16px">なし</div>`; return; }
  const gi = list[0];
  const item = UNDERLINE[gi];
  area.innerHTML = `
    <div class="card">
      <div class="en">${item.enHtml}</div>
      <div class="btnrow"><button class="primary" id="rUShowAns">答えを見る</button></div>
      <div class="reveal" id="rURevealArea" style="display:none">
        <div class="jp">${item.jp}</div>
        <div class="btnrow">
          <button class="good" id="rUGood">できた</button>
          <button class="bad" id="rUBad">もう一度復習</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById('rUShowAns').onclick = ()=>{ document.getElementById('rURevealArea').style.display='block'; };
  document.getElementById('rUGood').onclick = ()=>{
    delete store.data.underlineWrong[gi];
    store.data.underlineDone[gi] = true;
    store.save(); updateStats(); renderReview();
  };
  document.getElementById('rUBad').onclick = ()=>{ renderReview(); };
}

function renderReviewGrammar(list){
  const area = document.getElementById('reviewGrammarArea');
  if(list.length===0){ area.innerHTML = `<div class="card empty" style="padding:16px">なし</div>`; return; }
  const gi = list[0];
  const item = GRAMMAR[gi];
  let answered = false;
  area.innerHTML = `
    <div class="card">
      <div id="rgHintArea"><button id="rgShowHint">💡 ヒント（文法ポイント）を見る</button></div>
      <div class="en" style="margin-top:14px">${item.en}</div>
      <div id="rgChoiceArea"></div>
      <div id="rgExplain" style="display:none" class="explain"></div>
    </div>
  `;
  document.getElementById('rgShowHint').onclick = ()=>{
    document.getElementById('rgHintArea').innerHTML = `<div class="point-badge">${item.point}</div>`;
  };
  const choiceArea = document.getElementById('rgChoiceArea');
  const options = shuffle(item.choices);
  options.forEach(opt=>{
    const b = document.createElement('button');
    b.className = 'choice';
    b.textContent = opt;
    b.onclick = ()=>{
      if(answered) return;
      answered = true;
      const correct = opt === item.answer;
      if(correct){ delete store.data.grammarWrong[gi]; }
      store.save(); updateStats();
      document.getElementById('rgHintArea').innerHTML = `<div class="point-badge">${item.point}</div>`;
      Array.from(choiceArea.children).forEach(c=>{
        c.disabled = true;
        if(c.textContent === item.answer) c.classList.add('correct');
        else if(c===b) c.classList.add('wrong');
      });
      const ex = document.getElementById('rgExplain');
      ex.style.display = 'block';
      ex.textContent = item.explain;
      const nextBtn = document.createElement('button');
      nextBtn.className = 'primary';
      nextBtn.textContent = '次へ';
      nextBtn.style.marginTop = '14px';
      nextBtn.onclick = ()=>{ renderReview(); };
      choiceArea.appendChild(nextBtn);
    };
    choiceArea.appendChild(b);
  });
}

// ================= TABS =================
document.querySelectorAll('.tab').forEach(tab=>{
  tab.onclick = ()=>{
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('panel-'+tab.dataset.tab).classList.add('active');
    if(tab.dataset.tab === 'review') renderReview();
    if(tab.dataset.tab === 'summary') renderSummary();
  };
});

(async function init(){
  await store.load();
  updateStats();
  buildVocabOrder(); renderVocabRoot();
  buildUnderlineOrder(); renderUnderline();
  buildQuizOrder(); buildCompOrder(); renderQuiz();
  buildGrammarOrder(); renderGrammar();
  buildKotestOrder(); renderKotest();
})();

})();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
