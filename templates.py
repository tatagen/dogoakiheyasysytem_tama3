LOGIN_HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>温泉休憩室管理｜ログイン</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root{ --line:#e6e6e6; --ink:#111; --muted:#666; }
  *{box-sizing:border-box}
  body{
    margin:0;
    min-height:100vh;
    display:grid;
    place-items:center;
    padding:24px;
    background:linear-gradient(135deg,#f7f4ee,#ffffff 60%);
    color:var(--ink);
    font-family:system-ui,-apple-system,Segoe UI,Roboto;
  }
  .panel{
    width:min(420px,100%);
    background:#fff;
    border:1px solid var(--line);
    border-radius:20px;
    padding:24px;
    box-shadow:0 12px 30px rgba(0,0,0,.06);
  }
  h1{font-size:24px; margin:0 0 6px}
  p{margin:0 0 16px; color:var(--muted); line-height:1.6}
  label{display:block; font-size:13px; margin:12px 0 6px}
  input{
    width:100%;
    padding:12px 14px;
    border-radius:12px;
    border:1px solid #ccc;
    font-size:14px;
  }
  button{
    width:100%;
    margin-top:16px;
    padding:12px 14px;
    border:none;
    border-radius:12px;
    background:#222;
    color:#fff;
    font-size:14px;
    cursor:pointer;
  }
  .error{
    display:none;
    margin-top:12px;
    padding:10px 12px;
    border-radius:12px;
    background:#fff0f0;
    color:#9b1c1c;
    font-size:13px;
  }
  .note{
    margin-top:14px;
    font-size:12px;
    color:var(--muted);
  }
</style>
<div class="panel">
  <h1>ログイン</h1>
  <p>温泉休憩室 空き部屋管理</p>
  <form id="loginForm">
    <label for="username">ユーザー名</label>
    <input id="username" name="username" autocomplete="username" required>
    <label for="password">パスワード</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required>
    <button type="submit">ログイン</button>
  </form>
  <div id="errorBox" class="error"></div>
  <div class="note">社内利用向けに認証を有効化しています。</div>
</div>
<script>
document.getElementById('loginForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const errorBox = document.getElementById('errorBox');
  errorBox.style.display = 'none';
  errorBox.textContent = '';

  const payload = {
    username: document.getElementById('username').value,
    password: document.getElementById('password').value
  };

  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json().catch(()=>({ ok:false, msg:'ログインに失敗しました' }));
  if(res.ok && data.ok){
    location.href = '/';
    return;
  }

  errorBox.textContent = data.msg || 'ログインに失敗しました';
  errorBox.style.display = 'block';
});
</script>
"""

HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>温泉休憩室｜空き部屋管理</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  /* ===== パターンC：和風・温かみ ===== */
  *{box-sizing:border-box; margin:0; padding:0;}
  body{
    font-family:'Hiragino Sans','Meiryo',system-ui,sans-serif;
    background:#faf7f2;
    color:#2c1f0e;
    font-size:14px;
  }

  /* ヘッダー */
  .wa-header{
    background:#2c1f0e;
    color:#f5efe6;
    padding:12px 20px;
    display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;
    border-bottom:3px solid #8b6914;
  }
  .wa-header-logo{display:flex; align-items:center; gap:10px;}
  .wa-header-mark{font-size:22px;}
  .wa-header-title{font-size:15px; font-weight:700; letter-spacing:.06em;}
  .wa-header-sub{font-size:11px; opacity:.55; margin-top:2px;}
  .wa-kpi-row{display:flex; gap:6px; flex-wrap:wrap; align-items:center;}
  .kpi-pill{
    background:rgba(245,239,230,.1);
    border:1px solid rgba(245,239,230,.2);
    border-radius:6px;
    padding:5px 10px;
    text-align:center;
    min-width:58px;
  }
  .kpi-pill.accent{background:rgba(212,160,23,.25); border-color:rgba(212,160,23,.4);}
  .kpi-pill-val{font-size:19px; font-weight:700; line-height:1;}
  .kpi-pill-lbl{font-size:10px; opacity:.65; margin-top:2px; letter-spacing:.03em;}
  .wa-header-actions{display:flex; gap:8px; align-items:center;}

  /* メインレイアウト */
  .grid{
    display:grid;
    grid-template-columns:1fr 360px;
    gap:14px;
    padding:14px;
  }
  @media(max-width:1100px){.grid{grid-template-columns:1fr}}

  /* カード */
  .card{
    background:#fff;
    border:1px solid #e8ddd0;
    border-radius:4px;
    padding:18px;
    box-shadow:0 2px 8px rgba(44,31,14,.05);
  }
  .soft{background:#fdf9f4;}

  /* セクションタイトル */
  h2{
    font-size:15px; font-weight:700; letter-spacing:.08em;
    padding-bottom:10px;
    border-bottom:2px solid #8b6914;
    margin-bottom:12px;
    display:flex; align-items:center; gap:8px;
  }
  h2::before{content:''; display:inline-block; width:4px; height:17px; background:#8b6914; border-radius:2px; flex-shrink:0;}
  h3{
    font-size:12px; font-weight:700; letter-spacing:.1em; color:#8b6914;
    padding:8px 0 6px;
    border-bottom:1px solid #e8ddd0;
    margin:14px 0 8px;
  }

  .section-lead{font-size:12px; color:#8b7355; margin-bottom:12px; line-height:1.8;}
  .muted{color:#a89070; font-size:12px;}
  .row{display:flex; gap:8px; align-items:center; flex-wrap:wrap;}
  .between{display:flex; gap:8px; align-items:center; justify-content:space-between; flex-wrap:wrap;}

  /* ボタン */
  .btn{
    padding:9px 16px; border-radius:4px;
    border:1px solid #2c1f0e; background:#2c1f0e; color:#f5efe6;
    font-size:13px; font-weight:600; cursor:pointer; font-family:inherit;
    letter-spacing:.03em;
  }
  .btn:active{transform:translateY(1px);}
  .btn[disabled]{opacity:.45; cursor:not-allowed;}
  .btn-outline{background:#fff; color:#2c1f0e; border-color:#c8b89a;}
  .btn-outline:hover{background:#faf7f2;}
  .btn-ghost{background:transparent; border-color:transparent; color:#a89070;}
  .btn-danger{background:#7c1d1d; border-color:#7c1d1d; color:#fff;}
  .btn-wide{width:100%;}
  .btn-mini{font-size:12px; padding:6px 10px;}

  /* 入力 */
  .num{font-size:20px; padding:9px; width:90px; text-align:center; border-radius:4px; border:1px solid #c8b89a; background:#fff; font-family:inherit;}
  .num:focus{border-color:#8b6914; outline:none; box-shadow:0 0 0 2px rgba(139,105,20,.15);}

  /* バッジ */
  .badge{font-size:12px; padding:2px 8px; border-radius:3px; background:#2c1f0e; color:#f5efe6; font-weight:700;}
  .badge-calling{background:#b45309; color:#fff;}
  .pill{font-size:12px; padding:3px 8px; border-radius:3px; border:1px solid #e8ddd0; background:#fff;}

  /* ステータス（部屋用） */
  .status{font-weight:700; font-size:11px; padding:1px 8px; border-radius:2px; letter-spacing:.05em; display:inline-block;}
  .status.available{background:#c6e9ca; color:#2d6a31;}
  .status.occupied{background:#fde68a; color:#7c5c00;}
  .status.cleaning{background:#c7d9f5; color:#1e4080;}
  .status.disabled{background:#e5e5e5; color:#888;}

  /* 部屋グリッド */
  .rooms-grid{
    display:grid;
    grid-template-columns:repeat(4, minmax(110px,1fr));
    gap:10px;
    direction:rtl;
  }
  @media(max-width:800px){.rooms-grid{grid-template-columns:repeat(2,minmax(130px,1fr));}}
  @media(max-width:420px){.rooms-grid{grid-template-columns:1fr;}}

  /* 部屋カード */
  .room-card{
    border-radius:6px;
    padding:12px 8px;
    text-align:center;
    direction:ltr;
    border:2px solid #e8ddd0;
    background:#fff;
    position:relative;
  }
  .room-card.available{background:#f0f9f4; border-color:#6aab72;}
  .room-card.occupied{background:#fefce8; border-color:#c9a227;}
  .room-card.cleaning{background:#f0f4fe; border-color:#7b9fd4;}
  .room-card.disabled{background:#f5f5f5; border-color:#ddd; opacity:.5;}
  .room-card-cleaning{border:2px solid #7b9fd4 !important; box-shadow:0 0 0 2px rgba(123,159,212,.2);}
  .room-warning{border:2px solid #d97706 !important; box-shadow:0 0 0 2px rgba(217,119,6,.2);}
  .room-selectable{outline:3px solid #8b6914;}
  .req-selected{border:2px solid #6aab72 !important; background:#f0f9f4 !important;}

  /* 部屋カード内テキスト */
  .current-info{font-size:15px; font-weight:700; color:#2c1f0e; margin-top:4px;}
  .room-eta{margin-top:6px; font-size:13px; display:flex; align-items:center; gap:4px; justify-content:center;}
  .room-eta input[type="time"]{font-size:15px; padding:3px 5px; border:1px solid #c8b89a; border-radius:3px; font-family:inherit;}

  /* 部屋カード内メニュー */
  .room-menu-panel{position:absolute; top:32px; right:6px; z-index:20;}
  .room-menu-inner{
    background:#fff; border-radius:4px;
    box-shadow:0 4px 14px rgba(44,31,14,.18);
    border:1px solid #e8ddd0; padding:4px;
    display:flex; flex-direction:column; min-width:150px;
  }
  .room-menu-inner button{border:none; background:transparent; padding:6px 10px; text-align:left; font-size:13px; cursor:pointer; width:100%; font-family:inherit;}
  .room-menu-inner button:hover{background:#faf7f2;}

  /* リストアイテム */
  .list{list-style:none; padding:0; margin:0;}
  .item{
    display:flex; justify-content:space-between; align-items:center;
    padding:9px 10px;
    border-radius:4px;
    margin-bottom:5px;
    gap:8px;
    background:#fdf9f4;
    border:1px solid #e8ddd0;
  }

  /* 点滅（呼び出し中） */
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}
  .blink{animation:blink 1.2s ease-in-out infinite; background:#fff5eb !important; border:2px solid #d97706 !important;}

  /* 待ち時間表示 */
  .pending-wait{font-size:13px; color:#6b5240; margin-top:3px; line-height:1.6;}
  .pending-number{font-size:14px; font-weight:700; color:#2c1f0e;}

  /* 依頼カード（移動中） */
  .req{
    padding:10px;
    border:1px solid #e8ddd0;
    border-radius:4px;
    background:#fdf9f4;
    display:flex; justify-content:space-between; align-items:center; gap:10px;
    cursor:pointer; width:100%;
    font-family:inherit;
  }
  .req:hover{background:#f5ede0;}
  .req .title{font-weight:700;}
  .req .sub{font-size:12px; color:#a89070;}
  .req-row{display:flex; align-items:flex-start; justify-content:space-between; gap:8px;}

  /* インラインメニュー */
  .inline-menu-container{position:relative;}
  .inline-menu{
    position:absolute; right:0; top:110%;
    background:#fff; border:1px solid #e8ddd0;
    border-radius:4px;
    box-shadow:0 4px 14px rgba(44,31,14,.18);
    padding:4px; min-width:155px; z-index:50;
  }
  .inline-menu button{border:none; background:transparent; padding:7px 10px; text-align:left; font-size:13px; cursor:pointer; width:100%; font-family:inherit;}
  .inline-menu button:hover{background:#faf7f2;}

  /* モーダル */
  .overlay{position:fixed; inset:0; background:rgba(44,31,14,.45); display:none;}
  .modal{
    position:fixed; left:50%; top:50%; transform:translate(-50%,-50%);
    width:min(760px,94vw); max-height:85vh; overflow:auto;
    background:#fff; border-radius:4px; border:1px solid #e8ddd0; padding:18px; display:none;
    box-shadow:0 8px 32px rgba(44,31,14,.2);
  }
  .modal h3{margin-top:0; font-size:15px; letter-spacing:.06em; border-bottom:2px solid #8b6914; padding-bottom:8px; margin-bottom:14px;}
  .roomOption{border:1px solid #e8ddd0; border-radius:4px; padding:10px; display:flex; justify-content:space-between; align-items:center; gap:10px; background:#fdf9f4;}
  .roomOption[disabled]{opacity:.55; pointer-events:none;}
  .roomOption .cap{font-size:12px; color:#a89070;}
  .hint{font-size:12px; color:#a89070; margin:6px 0 0;}
</style>

<div class="wa-header">
  <div class="wa-header-logo">
    <div class="wa-header-mark">♨</div>
    <div>
      <div class="wa-header-title">温泉休憩室｜空き部屋管理</div>
    </div>
  </div>
  <div class="wa-kpi-row">
    <div class="kpi-pill accent"><div class="kpi-pill-val" id="kpiFree">-</div><div class="kpi-pill-lbl">空　室</div></div>
    <div class="kpi-pill"><div class="kpi-pill-val" id="kpiHeading">-</div><div class="kpi-pill-lbl">移動中</div></div>
    <div class="kpi-pill"><div class="kpi-pill-val" id="kpiCap4">-</div><div class="kpi-pill-lbl">4人部屋</div></div>
    <div class="kpi-pill"><div class="kpi-pill-val" id="kpiRoom5">-</div><div class="kpi-pill-lbl">五号室</div></div>
    <div class="kpi-pill"><div class="kpi-pill-val" id="kpiRoom7">-</div><div class="kpi-pill-lbl">七号室</div></div>
  </div>
  <div class="wa-header-actions">
    <button class="btn btn-mini btn-outline" style="color:#f5efe6;border-color:rgba(245,239,230,.3);background:transparent;" onclick="openAdmin()">︙ 管理</button>
    <button class="btn btn-mini btn-danger" onclick="logout()">ログアウト</button>
  </div>
</div>

<div class="grid">
  <!-- 左：部屋一覧 -->
  <section class="card">
    <h2>個室一覧</h2>
    <p class="section-lead">空室・使用中・清掃中をリアルタイムで確認いただけます。橙枠は退出予定が近い部屋です。</p>
    <div id="rooms" class="rooms-grid"></div>
  </section>

  <!-- 右：受付 -->
  <section class="card soft">
    <h2>受付登録</h2>
    <p class="section-lead">番号と人数を入力して登録します。</p>

    <!-- 番号入力 -->
    <div class="row" style="margin-bottom:8px">
      <label style="min-width:3em; color:#6b5240; font-size:13px;">番号：</label>
      <input id="seq_label_input" type="text" placeholder="例：12"
        style="width:80px;padding:8px 10px;border-radius:4px;border:1px solid #c8b89a;font-size:14px;font-family:inherit;background:#fff;">
    </div>

    <!-- 人数入力 -->
    <div class="row">
      <label style="min-width:3em; color:#6b5240; font-size:13px;">人数：</label>
      <button class="btn btn-outline" onclick="dec()">－</button>
      <input id="headcount" type="number" min="1" value="1" class="num">
      <button class="btn btn-outline" onclick="inc()">＋</button>
    </div>

    <!-- 依頼ボタン -->
    <div class="row" style="margin-top:10px">
      <button id="btnQuick" class="btn" onclick="createRequestQuick()">移動中に追加</button>
      <button class="btn btn-outline" onclick="createRequestPending()">待機中に追加</button>
    </div>
    <p class="muted" style="margin-top:8px">※ 空室がないと「移動中」には追加できません。</p>

    <!-- 移動中 -->
    <h3>移　動　中</h3>
    <ul id="heading" class="list" style="display:grid; gap:6px"></ul>

    <!-- 呼び出し中 -->
    <h3>呼び出し中</h3>
    <ul id="calling" class="list" style="display:grid; gap:6px"></ul>

    <!-- 待機中 -->
    <h3>待　機　中</h3>
    <ul id="pending" class="list"></ul>

  </section>
</div>

<!-- 管理モーダル -->
<div id="overlay" class="overlay" onclick="closeAdmin()"></div>
<div id="adminModal" class="modal">
  <h3>管理メニュー</h3>
  <div id="adminContent"></div>
  <div class="row" style="justify-content:flex-end;margin-top:12px">
    <button class="btn btn-outline" onclick="closeAdmin()">閉じる</button>
  </div>
</div>

<!-- 部屋選択モーダル（旧フロー用：今は未使用だが残しておく） -->
<div id="overlayRoom" class="overlay" onclick="closeRoomPicker()"></div>
<div id="roomPicker" class="modal">
  <h3>部屋を選択</h3>
  <div id="roomPickerBody"></div>
  <p class="hint">※ 空室のみ選択できます。使用中の部屋は「退出予定」をご確認ください。</p>
  <div class="row" style="justify-content:flex-end;margin-top:12px">
    <button class="btn btn-outline" onclick="closeRoomPicker()">キャンセル</button>
  </div>
</div>

<script>
const API = location.origin;
const CSRF_TOKEN = "__CSRF_TOKEN__";
let SNAP = null;
let PICK_REQ = null;
let _pauseRefresh = false;
let _editingEta = false;
let _etaBlurTimer = null;

function isUIBusy(){
  if(document.querySelector('.inline-menu[style*="block"]')) return true;
  if(document.querySelector('.room-menu-panel[style*="block"]')) return true;
  if(PICK_REQ) return true;
  if(_editingEta) return true;
  const tag = document.activeElement && document.activeElement.tagName;
  if(tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return true;
  return false;
}

async function fetchJSON(path){
  const res = await fetch(API + path, { cache: "no-store" });
  if(res.status === 401){
    window.location.href = '/';
    throw new Error('認証が必要です');
  }
  if(!res.ok){
    const text = await res.text();
    throw new Error(`GET ${path} failed: ${res.status} ${text}`);
  }
  return await res.json();
}

async function post(path, data){
  const res = await fetch(API + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": CSRF_TOKEN
    },
    body: JSON.stringify(data || {})
  });
  if(res.status === 401){
    window.location.href = '/';
    throw new Error('認証が必要です');
  }
  if(!res.ok){
    const text = await res.text();
    throw new Error(`POST ${path} failed: ${res.status} ${text}`);
  }
  return await res.json();
}

/* ========= 汎用 ========= */
function v(el){ return parseInt(document.getElementById(el).value||"1"); }
function setv(el, val){ document.getElementById(el).value = val; }
function inc(){ setv("headcount", Math.max(1, v("headcount")+1)); }
function dec(){ setv("headcount", Math.max(1, v("headcount")-1)); }
function hhmm(d){ const p=n=>String(n).padStart(2,'0'); return p(d.getHours())+':'+p(d.getMinutes()); }
function fromISOtoHHMM(iso){
  if(!iso) return '';
  const d = new Date(iso);
  if(isNaN(d)) return '';
  return new Intl.DateTimeFormat('ja-JP', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Tokyo'
  }).format(d);
}
function minutesUntil(iso){
  if(!iso) return null;
  const d = new Date(iso);
  if(isNaN(d)) return null;
  const diffMs = d - new Date();
  if(diffMs < 0) return null;
  return Math.ceil(diffMs / 60000);
}

function getJstParts(){
  const fmt = new Intl.DateTimeFormat('ja-JP', {
    timeZone: 'Asia/Tokyo',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
  const parts = fmt.formatToParts(new Date());
  const hour = parseInt(parts.find(p=> p.type === 'hour')?.value || '0', 10);
  const minute = parseInt(parts.find(p=> p.type === 'minute')?.value || '0', 10);
  return { hour, minute };
}

function isWithinKeepAliveWindow(){
  const { hour, minute } = getJstParts();
  const nowMinutes = hour * 60 + minute;
  const startMinutes = 5 * 60 + 45;
  const endMinutes = 22 * 60 + 15;
  return nowMinutes >= startMinutes && nowMinutes <= endMinutes;
}

async function keepRenderAwake(){
  if(document.hidden) return;
  if(!isWithinKeepAliveWindow()) return;
  try{
    await fetch(API + '/api/snapshot', { cache: 'no-store', credentials: 'same-origin' });
  }catch(e){}
}

/* ========= スナップショット読込 ========= */
async function load(){
  if(isUIBusy()) return;
  const snap = await fetchJSON('/api/snapshot');
  if(isUIBusy()) return;
  SNAP = snap;
  const {rooms, pending, heading, free_count, remain} = snap;
  const waiting = pending.filter(x => !x.calling);
  const calling = pending.filter(x => x.calling);

  const usableRooms   = rooms.filter(r => r.status !== 'disabled').length;
  const occupiedRooms = rooms.filter(r => r.status === 'occupied').length;
  const activeCount   = heading.length + calling.length;
  const isFull = (occupiedRooms + activeCount) >= usableRooms;

  document.getElementById('kpiFree').textContent    = free_count;
  document.getElementById('kpiHeading').textContent = heading.length;

  const fourFree = rooms.filter(r => r.capacity === 4 && r.status === 'available').length;
  const room5    = rooms.find(r => /五号室/.test(r.name));
  const room7    = rooms.find(r => /七号室/.test(r.name));

  document.getElementById('kpiCap4').textContent = fourFree;

  function labelRoomState(r){
    if(!r) return '-';
    switch(r.status){
      case 'available': return '空き';
      case 'occupied':  return '使用中';
      case 'cleaning':  return '清掃中';
      case 'disabled':  return '停止';
      default:          return r.status;
    }
  }
  document.getElementById('kpiRoom5').textContent = labelRoomState(room5);
  document.getElementById('kpiRoom7').textContent = labelRoomState(room7);

  document.getElementById('btnQuick').disabled = (remain <= 0 || activeCount >= free_count);

  /* ---- 待機中 ---- */
  const pEl = document.getElementById('pending');
  pEl.innerHTML = '';
  const waitMap = buildPendingWaitMap(pending, rooms);

  waiting.forEach(x=>{
    const li = document.createElement('li');
    li.className='item';
    const wait = waitMap[x.id];
    let waitLine = '';
    if(wait == null){
      waitLine = `<div class="pending-wait">概算待ち時間：<span class="pending-number">-</span><br>呼び出し予定：<span class="pending-number">-</span></div>`;
    }else{
      const d = new Date();
      d.setMinutes(d.getMinutes() + wait);
      waitLine = `<div class="pending-wait">概算待ち時間：約 <span class="pending-number">${wait}</span> 分<br>呼び出し予定：<span class="pending-number">${hhmm(d)}</span></div>`;
    }

    const left = document.createElement('div');
    left.innerHTML = `<div><span class="badge">#${x.seq_label || x.seq}</span> <b>${x.headcount}名</b> <span class="muted">待機中</span></div>${waitLine}`;

    const box = document.createElement('span');
    const callBtn = document.createElement('button');
    callBtn.className = 'btn btn-mini btn-outline';
    callBtn.textContent = '呼び出し中にする';
    callBtn.onclick = ()=> toggleCalling(x.id, true);
    callBtn.disabled = isFull;

    const menuContainer = document.createElement('span');
    menuContainer.className = 'inline-menu-container pending-menu-container';
    const menuBtn = document.createElement('button');
    menuBtn.className = 'btn btn-mini btn-outline pending-menu-btn';
    menuBtn.textContent = '︙';
    menuBtn.onclick = (e)=>{
      e.stopPropagation();
      const menu = menuContainer.querySelector('.inline-menu');
      const isOpen = menu && menu.style.display === 'block';
      closeAllMenus();
      if(menu){ menu.style.display = isOpen ? 'none' : 'block'; }
    };

    const menu = document.createElement('div');
    menu.className = 'inline-menu pending-menu';
    menu.style.display = 'none';

    const mChangeSeq = document.createElement('button');
    mChangeSeq.textContent = '番号を変更';
    mChangeSeq.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await changeSeqLabel(x.id, x.seq_label || String(x.seq)); };
    menu.appendChild(mChangeSeq);

    const mChange = document.createElement('button');
    mChange.textContent = '人数を変更';
    mChange.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await changeHeadcount(x.id, x.headcount); };
    menu.appendChild(mChange);

    const m1 = document.createElement('button');
    m1.textContent = '取り消し';
    m1.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await confirmCancel(x.id); };
    menu.appendChild(m1);

    menuContainer.appendChild(menuBtn);
    menuContainer.appendChild(menu);
    box.appendChild(callBtn);
    box.appendChild(menuContainer);
    li.appendChild(left);
    li.appendChild(box);
    pEl.appendChild(li);
  });

  /* ---- 呼び出し中 ---- */
  const cEl = document.getElementById('calling');
  cEl.innerHTML = '';
  calling.forEach(x=>{
    const li = document.createElement('li');
    li.className = 'item blink';
    const left = document.createElement('div');
    left.innerHTML = `<div><span class="badge">#${x.seq_label || x.seq}</span> <b>${x.headcount}名</b> <span class="badge badge-calling">呼び出し中</span></div>`;
    const right = document.createElement('span');
    right.style.cssText = 'display:flex;gap:6px;align-items:center;';

    const moveBtn = document.createElement('button');
    moveBtn.className = 'btn btn-mini';
    moveBtn.textContent = '移動中へ';
    moveBtn.onclick = (e)=>{ e.stopPropagation(); toHeading(x.id); };

    const menuContainer = document.createElement('span');
    menuContainer.className = 'inline-menu-container calling-menu-container';
    const menuBtn = document.createElement('button');
    menuBtn.className = 'btn btn-mini btn-outline calling-menu-btn';
    menuBtn.textContent = '︙';
    menuBtn.onclick = (e)=>{
      e.stopPropagation();
      const menu = menuContainer.querySelector('.inline-menu');
      const isOpen = menu && menu.style.display === 'block';
      closeAllMenus();
      if(menu){ menu.style.display = isOpen ? 'none' : 'block'; }
    };

    const menu = document.createElement('div');
    menu.className = 'inline-menu calling-menu';
    menu.style.display = 'none';
    const mBack = document.createElement('button');
    mBack.textContent = '待機中へ戻す';
    mBack.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await toggleCalling(x.id, false); };
    const mCancel = document.createElement('button');
    mCancel.textContent = '取り消し';
    mCancel.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await confirmCancel(x.id); };

    menu.appendChild(mBack);
    menu.appendChild(mCancel);
    menuContainer.appendChild(menuBtn);
    menuContainer.appendChild(menu);
    right.appendChild(moveBtn);
    right.appendChild(menuContainer);
    li.appendChild(left);
    li.appendChild(right);
    cEl.appendChild(li);
  });

  /* ---- 移動中 ---- */
  const hEl = document.getElementById('heading');
  hEl.innerHTML = '';
  heading.forEach(req=>{
    const wait = estimateWaitMinutesForGroup(req.headcount, rooms);
    const waitText = wait === 0 ? 'すぐにご案内できます' : wait ? `概算待ち時間：約 ${wait} 分` : '概算待ち時間：-';
    const li = document.createElement('li');
    const card = document.createElement('button');
    card.className = 'req';
    card.type = 'button';
    card.onclick = ()=> startAssignOnBoard(req, card);
    const left = document.createElement('div');
    left.innerHTML = `<div class="title">#${req.seq_label || req.seq} / ${req.headcount}名</div><div class="sub">${waitText}</div>`;
    const right = document.createElement('div');
    right.innerHTML = `<span class="pill">部屋を選択</span>`;
    card.appendChild(left);
    card.appendChild(right);

    const menuContainer = document.createElement('div');
    menuContainer.className = 'inline-menu-container heading-menu-container';
    const menuBtn = document.createElement('button');
    menuBtn.textContent = "︙";
    menuBtn.className = "btn btn-mini btn-outline heading-menu-btn";
    menuBtn.onclick = (e)=>{
      e.stopPropagation();
      const menu = menuContainer.querySelector('.inline-menu');
      const isOpen = menu && menu.style.display === 'block';
      closeAllMenus();
      if(menu){ menu.style.display = isOpen ? 'none' : 'block'; }
    };

    const menu = document.createElement('div');
    menu.className = 'inline-menu heading-menu';
    menu.style.display = 'none';

    const mChangeSeq2 = document.createElement('button');
    mChangeSeq2.textContent = '番号を変更';
    mChangeSeq2.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await changeSeqLabel(req.id, req.seq_label || String(req.seq)); };
    const mChange = document.createElement('button');
    mChange.textContent = '人数を変更';
    mChange.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await changeHeadcount(req.id, req.headcount); };
    const m1 = document.createElement('button');
    m1.textContent = '待機中に戻す';
    m1.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await headingToPending(req.id); };
    const m2 = document.createElement('button');
    m2.textContent = '取り消し';
    m2.onclick = async (ev)=>{ ev.stopPropagation(); menu.style.display='none'; await confirmCancel(req.id); };

    menu.appendChild(mChangeSeq2);
    menu.appendChild(mChange);
    menu.appendChild(m1);
    menu.appendChild(m2);
    menuContainer.appendChild(menuBtn);
    menuContainer.appendChild(menu);

    const rowWrap = document.createElement('div');
    rowWrap.className = 'req-row';
    rowWrap.appendChild(card);
    rowWrap.appendChild(menuContainer);
    li.appendChild(rowWrap);
    hEl.appendChild(li);
  });

  /* ---- 部屋一覧 ---- */
  const rEl = document.getElementById('rooms');
  rEl.innerHTML = '';
  const orderedRooms = rooms.slice().sort((a,b)=> roomOrderIndex(a) - roomOrderIndex(b));

  orderedRooms.forEach(r=>{
    const div = document.createElement('div');
    div.className = 'card room-card';
    div.dataset.roomId = r.id;
    div.dataset.roomStatus = r.status;
    if(r.status === 'cleaning') div.classList.add('room-card-cleaning');
    if(r.eta_at && r.status === 'occupied'){
      const mins = minutesUntil(r.eta_at);
      if(mins === null || mins <= 5) div.classList.add('room-warning');
    }

    const statusClass = `status ${r.status}`;
    let etaText = '';
    if(r.status === 'occupied' && r.eta_at) etaText = ` / 空き予定 ${fromISOtoHHMM(r.eta_at)}⌚`;
    else if(r.status === 'cleaning' && r.eta_at) etaText = ` / 空き予定 ${fromISOtoHHMM(r.eta_at)}⌚`;
    else if(r.status === 'available') etaText = ' / すぐ案内可';

    const line1 = `<div class="between"><div><span style="font-size:20px; font-weight:700">${r.name}</span><span class="muted" style="font-size:12px">（目安 ${r.capacity}人）</span></div><button type="button" class="btn-ghost btn-mini room-menu-button" data-room-id="${r.id}">︙</button></div>`;
    const line2 = `<div class="${statusClass}">${roomStatusLabel(r.status)}<span class="muted">${etaText}</span></div>`;

    div.innerHTML = `${line1}${line2}<div id="room-${r.id}" style="margin-top:8px"></div>`;

    const inner = div.querySelector('#room-'+r.id);
    const menuPanel = document.createElement('div');
    menuPanel.className = 'room-menu-panel';
    menuPanel.id = `room-menu-${r.id}`;
    menuPanel.style.display = 'none';
    div.appendChild(menuPanel);

    const menuBtn = div.querySelector('.room-menu-button');
    if(menuBtn) menuBtn.addEventListener('click', ev=>{ ev.stopPropagation(); openRoomMenu(r); });

    if(r.status === 'occupied' && r.currentRequestId){
      const info = document.createElement('div');
      info.className = 'current-info';
      info.textContent = `${r.currentHeadcount}人 / #${r.currentSeq}`;
      inner.appendChild(info);

      const eta = document.createElement('div');
      eta.className = 'room-eta';
      const etaLabel = document.createElement('span');
      etaLabel.textContent = '退出予定：';
      const etaInput = document.createElement('input');
      etaInput.type = 'time';
      etaInput.id = `eta-${r.id}`;
      etaInput.value = fromISOtoHHMM(r.eta_at) || '';
      etaInput.addEventListener('focus', ()=>{ _editingEta = true; if(_etaBlurTimer){ clearTimeout(_etaBlurTimer); _etaBlurTimer = null; } });
      etaInput.addEventListener('change', ()=>{ if(etaInput.value) saveEta(r.id, etaInput.value); });
      etaInput.addEventListener('blur', ()=>{
        if(etaInput.value) saveEta(r.id, etaInput.value);
        if(_etaBlurTimer) clearTimeout(_etaBlurTimer);
        _etaBlurTimer = setTimeout(()=>{ _editingEta = false; _etaBlurTimer = null; }, 800);
      });
      eta.appendChild(etaLabel);
      eta.appendChild(etaInput);
      inner.appendChild(eta);

      const row = document.createElement('div');
      row.className = 'row';
      row.style.marginTop = '6px';
      const outBtn = document.createElement('button');
      outBtn.className = 'btn btn-wide';
      outBtn.textContent = `清掃中にする（#${r.currentSeq}）`;
      outBtn.onclick = ()=> confirmCheckout(r.name, r.currentRequestId);
      row.appendChild(outBtn);
      inner.appendChild(row);
    }

    if(r.status === 'cleaning'){
      const cleanBtn = document.createElement('button');
      cleanBtn.className = 'btn btn-wide';
      cleanBtn.textContent = '清掃完了';
      cleanBtn.style.marginTop = '10px';
      cleanBtn.onclick = ()=> cleanDone(r.id);
      inner.appendChild(cleanBtn);
    }

    rEl.appendChild(div);
  });
}

function roomStatusLabel(s){
  switch(s){
    case 'available': return '空室';
    case 'occupied':  return '使用中';
    case 'cleaning':  return '清掃中';
    case 'disabled':  return '使用停止中';
    default:          return s;
  }
}

/* ==== 待ち時間計算 ==== */
function buildRoomSlots(rooms){
  const now = new Date();
  const CLEAN_MIN = 15;
  return rooms.map(r=>{
    let at = 0;
    if(r.status === 'available') at = 0;
    else if(r.status === 'occupied' && r.eta_at){ const diff = (new Date(r.eta_at) - now) / 60000; at = Math.max(0, Math.ceil(diff)) + CLEAN_MIN; }
    else if(r.status === 'cleaning' && r.eta_at){ const diff = (new Date(r.eta_at) - now) / 60000; at = Math.max(0, Math.ceil(diff)); }
    else if(r.status === 'cleaning') at = CLEAN_MIN;
    else at = 99999;
    return { id:r.id, capacity:r.capacity, at };
  });
}

function estimateWaitMinutesForGroup(size, rooms){
  const slots = buildRoomSlots(rooms).sort((a,b)=>a.at-b.at);
  const slot4 = slots.filter(s=>s.capacity === 4);
  const slot6 = slots.filter(s=>s.capacity === 6);
  const slot2 = slots.filter(s=>s.capacity === 2);
  if(size >= 9){ const big = [...slot4,...slot6].sort((a,b)=>a.at-b.at); if(big.length < 2) return null; return Math.max(big[0].at, big[1].at); }
  if(size >= 5){ if(slot6.length === 0) return null; return slot6[0].at; }
  if(size >= 3){ const cand = [...slot4,...slot6].sort((a,b)=>a.at-b.at); if(cand.length === 0) return null; return cand[0].at; }
  const cand = [...slot2,...slot4,...slot6].sort((a,b)=>a.at-b.at);
  if(cand.length === 0) return null;
  return cand[0].at;
}

function buildPendingWaitMap(pending, rooms){
  const slots = buildRoomSlots(rooms);
  const sorted = pending.slice().sort((a,b)=> a.seq - b.seq);
  const waitMap = {};
  sorted.forEach(req=>{ waitMap[req.id] = estimateWaitMinutesForGroupAndConsume(req.headcount, slots); });
  return waitMap;
}

function estimateWaitMinutesForGroupAndConsume(size, slots){
  const SERVICE_MIN = 90 + 15;
  const sorted = slots.slice().sort((a,b)=> a.at - b.at);
  const slot4 = sorted.filter(s=>s.capacity === 4);
  const slot6 = sorted.filter(s=>s.capacity === 6);
  const slot2 = sorted.filter(s=>s.capacity === 2);
  let chosen = [];
  if(size >= 9){ const big = [...slot4,...slot6].sort((a,b)=>a.at-b.at); if(big.length < 2) return null; chosen = [big[0], big[1]]; }
  else if(size >= 5){ if(slot6.length === 0) return null; chosen = [slot6[0]]; }
  else if(size >= 3){ const cand = [...slot4,...slot6].sort((a,b)=>a.at-b.at); if(cand.length === 0) return null; chosen = [cand[0]]; }
  else { const cand = [...slot2,...slot4,...slot6].sort((a,b)=>a.at-b.at); if(cand.length === 0) return null; chosen = [cand[0]]; }
  const wait = chosen.reduce((max, s)=> Math.max(max, s.at), 0);
  chosen.forEach(s=>{ s.at = wait + SERVICE_MIN; });
  return wait;
}

/* ==== 並び順 ==== */
function extractRoomNo(name){
  const kanjiMap = {'一':1,'二':2,'三':3,'五':5,'六':6,'七':7,'八':8,'十':10};
  const m = name.match(/^([一二三五六七八十]+)号室/);
  if(m) return kanjiMap[m[1]] ?? null;
  const n = name.match(/(\d+)号室/);
  return n ? parseInt(n[1], 10) : null;
}
function roomOrderIndex(room){
  const roomNo = extractRoomNo(room.name);
  const order = [10, 8, 7, 6, 1, 2, 3, 5];
  const idx = order.indexOf(roomNo);
  return idx === -1 ? 999 : idx;
}

/* ========= 依頼作成 ========= */
async function createRequestQuick(){
  try{
    const snap = await fetchJSON('/api/snapshot');
    const free = snap.free_count;
    const activeCount = snap.heading.length + snap.pending.filter(x=> x.calling).length;
    if(activeCount >= free){ alert('入室可能な部屋数を超えるため、「移動中」をこれ以上作成できません。'); return; }
    const seqLabel = document.getElementById('seq_label_input').value.trim();
    await post('/api/requests', {headcount:v('headcount'), status:'heading', seq_label: seqLabel || null});
    document.getElementById('seq_label_input').value = '';
    await load();
  }catch(e){ alert(e.message); }
}

async function createRequestPending(){
  try{
    const seqLabel = document.getElementById('seq_label_input').value.trim();
    await post('/api/requests', {headcount:v('headcount'), status:'pending', seq_label: seqLabel || null});
    document.getElementById('seq_label_input').value = '';
    await load();
  }catch(e){ alert(e.message); }
}

async function changeSeqLabel(requestId, currentSeqLabel){
  const val = prompt('新しい番号を入力してください', currentSeqLabel);
  if(val === null) return;
  const label = val.trim();
  if(label === ''){ alert('番号を入力してください。'); return; }
  try{ await post('/api/requests/update_seq_label', {requestId, seq_label: label}); await load(); }
  catch(e){ alert(e.message || '番号の変更に失敗しました'); }
}

async function changeHeadcount(requestId, currentHeadcount){
  const val = prompt('新しい人数を入力してください', currentHeadcount);
  if(val === null) return;
  const n = parseInt(val, 10);
  if(!Number.isFinite(n) || n < 1){ alert('1以上の数字を入力してください。'); return; }
  try{ await post('/api/requests/update_headcount', {requestId, headcount:n}); await load(); }
  catch(e){ alert(e.message || '人数の変更に失敗しました'); }
}

async function toggleCalling(requestId, calling){
  try{ await post('/api/requests/calling', {requestId, calling}); await load(); }catch(e){ alert(e.message); }
}
async function confirmCancel(requestId){
  if(!confirm('本当に取り消しますか？')) return;
  try{ await post('/api/requests/cancel', {requestId}); await load(); }catch(e){ alert(e.message); }
}
async function toHeading(requestId){
  try{
    const snap = await fetchJSON('/api/snapshot');
    const free = snap.free_count;
    const activeCount = snap.heading.length + snap.pending.filter(x=> x.calling).length;
    if(activeCount > free){ alert('入室可能な部屋数を超えるため、「移動中」に移動できません。'); return; }
    await post('/api/requests/heading', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}
async function headingToPending(requestId){
  try{ await post('/api/requests/heading_to_pending', {requestId}); await load(); }catch(e){ alert(e.message); }
}

function startAssignOnBoard(req, card){
  if(PICK_REQ && PICK_REQ.id === req.id){ PICK_REQ = null; clearRoomHighlights(); clearReqHighlights(); return; }
  PICK_REQ = req;
  clearReqHighlights();
  card.classList.add('req-selected');
  highlightRoomsForSelection();
}

async function assignFromBoard(roomId){
  if(!PICK_REQ) return;
  try{
    await assign(roomId, PICK_REQ.id);
    PICK_REQ = null;
    clearRoomHighlights();
    clearReqHighlights();
    await load();
  }catch(e){ alert(e.message || '割当に失敗しました'); }
}
async function assign(roomId, requestId){
  const res = await post('/api/assign', {roomId, requestId});
  if(!res.ok) throw new Error(res.msg || '割当に失敗しました（サーバー側エラー）');
}

function openRoomPicker(req){}
function closeRoomPicker(){
  document.getElementById('overlayRoom').style.display='none';
  document.getElementById('roomPicker').style.display='none';
  PICK_REQ = null;
}

function openRoomMenu(room){
  const panel = document.getElementById(`room-menu-${room.id}`);
  if(!panel) return;
  const isVisible = panel.style.display === 'block';
  document.querySelectorAll('.room-menu-panel').forEach(p=> p.style.display='none');
  if(isVisible){ panel.style.display = 'none'; return; }
  panel.innerHTML = '';
  const inner = document.createElement('div');
  inner.className = 'room-menu-inner';

  const isDisabled = room.status === 'disabled';
  const btnDisable = document.createElement('button');
  btnDisable.textContent = isDisabled ? '使用停止を解除' : '使用停止にする';
  btnDisable.onclick = async ()=>{ await toggleRoomDisabled(room.id, !isDisabled); panel.style.display = 'none'; };
  inner.appendChild(btnDisable);

  if(room.status === 'occupied' && room.currentRequestId){
    const btnChange = document.createElement('button');
    btnChange.textContent = '人数を変更';
    btnChange.onclick = async ()=>{ await changeHeadcount(room.currentRequestId, room.currentHeadcount || 1); panel.style.display = 'none'; };
    inner.appendChild(btnChange);
    const btnBack = document.createElement('button');
    btnBack.textContent = '「移動中」に戻す';
    btnBack.onclick = async ()=>{ await requeueToHeading(room.currentRequestId); panel.style.display = 'none'; };
    inner.appendChild(btnBack);
  }

  panel.appendChild(inner);
  panel.style.display = 'block';
}

async function toggleRoomDisabled(roomId, disabled){
  try{ await post('/api/rooms/disable', {roomId, disabled}); await load(); }catch(e){ alert(e.message); }
}
async function saveEta(roomId, hhmm){
  try{ await post('/api/rooms/eta', {roomId, hhmm}); await load(); }catch(e){ alert(e.message); }
}
async function requeueToHeading(requestId){
  try{ await post('/api/requeue_to_heading', {requestId}); await load(); }catch(e){ alert(e.message); }
}
async function confirmCheckout(roomName, requestId){
  if(!confirm(`${roomName}の鍵を確認しましたか？`)) return;
  try{ await post('/api/checkout', {requestId}); await load(); }catch(e){ alert(e.message); }
}
async function cleanDone(roomId){
  try{ await post('/api/rooms/clean_done', {roomId}); await load(); }catch(e){ alert(e.message); }
}
async function logout(){
  try{ await post('/api/logout', {}); }catch(e){}
  window.location.href = '/';
}

function openAdmin(){
  document.getElementById('overlay').style.display='block';
  document.getElementById('adminModal').style.display='block';
  loadAdmin();
}
function closeAdmin(){
  document.getElementById('overlay').style.display='none';
  document.getElementById('adminModal').style.display='none';
}

async function loadAdmin(){
  const [hist, canceled] = await Promise.all([fetchJSON('/api/history'), fetchJSON('/api/canceled_history')]);
  const wrap = document.getElementById('adminContent');
  wrap.innerHTML = '';

  const hTitle = document.createElement('h4');
  hTitle.textContent = '入室履歴（最近50件）';
  wrap.appendChild(hTitle);
  const ul = document.createElement('ul');
  ul.className = 'list';
  hist.forEach(x=>{
    const li = document.createElement('li'); li.className = 'item';
    const left = document.createElement('span');
    left.innerHTML = `#${x.seq} / ${x.headcount}名 / ${x.room_name||'-'} / ${x.updated_at}`;
    const box = document.createElement('span');
    const btn = document.createElement('button');
    btn.className = 'btn btn-mini btn-outline';
    btn.textContent = '「移動中」に復元（#そのまま）';
    btn.onclick = async ()=>{ try{ await post('/api/requests/restore', {requestId:x.id}); await load(); await loadAdmin(); }catch(e){ alert(e.message); } };
    box.appendChild(btn);
    li.appendChild(left); li.appendChild(box); ul.appendChild(li);
  });
  wrap.appendChild(ul);

  const cTitle = document.createElement('h4');
  cTitle.textContent = '取り消し履歴（最近50件）';
  wrap.appendChild(cTitle);
  const cul = document.createElement('ul');
  cul.className = 'list';
  canceled.forEach(x=>{
    const li = document.createElement('li'); li.className = 'item';
    const left = document.createElement('span');
    left.innerHTML = `#${x.seq} / ${x.headcount}名 / ${x.room_name||'-'} / ${x.updated_at}`;
    const box = document.createElement('span');
    const toHeadingBtn = document.createElement('button');
    toHeadingBtn.className = 'btn btn-mini btn-outline';
    toHeadingBtn.textContent = '「移動中」に復元（#そのまま）';
    toHeadingBtn.onclick = async ()=>{ try{ await post('/api/cancel_restore', {requestId:x.id, target:'heading'}); await load(); await loadAdmin(); }catch(e){ alert(e.message); } };
    const toPendingBtn = document.createElement('button');
    toPendingBtn.className = 'btn btn-mini btn-outline';
    toPendingBtn.textContent = '待機中に復元（#そのまま）';
    toPendingBtn.onclick = async ()=>{ try{ await post('/api/cancel_restore', {requestId:x.id, target:'pending'}); await load(); await loadAdmin(); }catch(e){ alert(e.message); } };
    box.appendChild(toHeadingBtn); box.appendChild(toPendingBtn);
    li.appendChild(left); li.appendChild(box); cul.appendChild(li);
  });
  wrap.appendChild(cul);
}

function clearReqHighlights(){ document.querySelectorAll('.req-selected').forEach(el=>{ el.classList.remove('req-selected'); }); }
function highlightRoomsForSelection(){
  clearRoomHighlights();
  document.querySelectorAll('.room-card').forEach(card=>{
    const statusEl = card.querySelector('.status.available');
    if(statusEl){
      card.classList.add('room-selectable');
      const roomId = parseInt(card.dataset.roomId || '0', 10);
      card.onclick = ()=> assignFromBoard(roomId);
    }
  });
}
function clearRoomHighlights(){ document.querySelectorAll('.room-card').forEach(card=>{ card.classList.remove('room-selectable'); card.onclick = null; }); }

function closeAllMenus(){
  document.querySelectorAll('.inline-menu').forEach(m=> m.style.display='none');
  document.querySelectorAll('.room-menu-panel').forEach(p=> p.style.display='none');
}
document.addEventListener('click', (e)=>{
  if(e.target.closest('.inline-menu-container') || e.target.closest('.inline-menu') || e.target.closest('.room-menu-panel') || e.target.closest('.room-menu-button')) return;
  closeAllMenus();
});
document.addEventListener('click', e=>{
  if(!PICK_REQ) return;
  if(e.target.closest('.req') || e.target.closest('.room-card')) return;
  PICK_REQ = null;
  clearRoomHighlights();
  clearReqHighlights();
});

/* ========= 起動 ========= */
load();
setInterval(load, 1000);
keepRenderAwake();
setInterval(keepRenderAwake, 10 * 60 * 1000);
</script>
"""
