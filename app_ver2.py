HTML = r"""<!doctype html>
"""

LOGIN_HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>道後温泉｜ログイン</title>
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
  <p>道後温泉 霊の湯3階個室 空き部屋管理</p>
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
<title>道後温泉｜霊の湯3階個室 空き部屋管理</title>
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
      <div class="wa-header-title">道後温泉｜霊の湯三階個室　空き部屋管理</div>
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
  // メニューが開いている
  if(document.querySelector('.inline-menu[style*="block"]')) return true;
  if(document.querySelector('.room-menu-panel[style*="block"]')) return true;
  // 部屋選択モード中
  if(PICK_REQ) return true;
  // 退出時間を編集中
  if(_editingEta) return true;
  // input / select にフォーカス中
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
  if(diffMs < 0) return null;              // ★過去は警告しない
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
  const startMinutes = 5 * 60 + 45;   // 05:45 JST
  const endMinutes = 22 * 60 + 15;    // 22:15 JST
  return nowMinutes >= startMinutes && nowMinutes <= endMinutes;
}

async function keepRenderAwake(){
  if(document.hidden) return;
  if(!isWithinKeepAliveWindow()) return;
  try{
    await fetch(API + '/api/snapshot', {
      cache: 'no-store',
      credentials: 'same-origin'
    });
  }catch(e){
  }
}

/* ========= スナップショット読込 ========= */
async function load(){
  if(isUIBusy()) return;

  const snap = await fetchJSON('/api/snapshot');

  // 通信中にメニューを開いた・入力中になった場合もDOM再構築をスキップ
  if(isUIBusy()) return;

  SNAP = snap;
  const {rooms, pending, heading, free_count, remain} = snap;
  const waiting = pending.filter(x => !x.calling);
  const calling = pending.filter(x => x.calling);

  // ★ 満室かどうかを判定
  const usableRooms   = rooms.filter(r => r.status !== 'disabled').length;   // 使える部屋の数
  const occupiedRooms = rooms.filter(r => r.status === 'occupied').length;   // 使用中の部屋数
  const activeCount   = heading.length + calling.length;                      // 呼び出し中+移動中
  const isFull = (occupiedRooms + activeCount) >= usableRooms;               // 満室なら true

  /* ---- KPI ---- */
  document.getElementById('kpiFree').textContent    = free_count;
  document.getElementById('kpiHeading').textContent = heading.length;

  const fourFree = rooms.filter(r => r.capacity === 4 && r.status === 'available').length;
  const room5    = rooms.find(r => /五号室/.test(r.name));
  const room7    = rooms.find(r => /七号室/.test(r.name));

  document.getElementById('kpiCap4').textContent = fourFree;
  // 清掃中の部屋数をカウント
  const cleaningCount = rooms.filter(r => r.status === 'cleaning').length;


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

  // すぐに通すボタンの可否
  document.getElementById('btnQuick').disabled = (remain <= 0 || activeCount >= free_count);

  /* ---- 待機中 ---- */
  const pEl = document.getElementById('pending');
  pEl.innerHTML = '';

  // #順（seq順）に、待ち時間を加算したマップを事前に作る
  const waitMap = buildPendingWaitMap(pending, rooms);

  waiting.forEach(x=>{
    const li = document.createElement('li');
    li.className='item';
    // 待ち時間 & 呼び出し予定時刻（2行表示＋数字を少し大きく）
    const wait = waitMap[x.id];
    let waitLine = '';

    if(wait == null){
      waitLine = `
        <div class="pending-wait">
          概算待ち時間：<span class="pending-number">-</span><br>
          呼び出し予定：<span class="pending-number">-</span>
        </div>`;
    }else{
      const d = new Date();
      d.setMinutes(d.getMinutes() + wait);
      waitLine = `
        <div class="pending-wait">
          概算待ち時間：約 <span class="pending-number">${wait}</span> 分<br>
          呼び出し予定：<span class="pending-number">${hhmm(d)}</span>
        </div>`;
    }



    const left = document.createElement('div');
    left.innerHTML =
      `<div><span class="badge">#${x.seq_label || x.seq}</span> <b>${x.headcount}名</b> <span class="muted">待機中</span></div>${waitLine}`;

    const box = document.createElement('span');

    // 呼び出しボタン
    const callBtn = document.createElement('button');
    callBtn.className = 'btn btn-mini btn-outline';
    callBtn.textContent = '呼び出し中にする';
    callBtn.onclick = ()=> toggleCalling(x.id, true);
    callBtn.disabled = isFull;



    // ハンバーガーメニュー（取り消し用：インライン）
    const menuContainer = document.createElement('span');
    menuContainer.className = 'inline-menu-container pending-menu-container';

        const menuBtn = document.createElement('button');
    menuBtn.className = 'btn btn-mini btn-outline pending-menu-btn';
    menuBtn.textContent = '︙';
    menuBtn.onclick = (e)=>{
      e.stopPropagation();
      const menu = menuContainer.querySelector('.inline-menu');
      const isOpen = menu && menu.style.display === 'block';
      // いったん他のメニューを全部閉じる
      closeAllMenus();
      if(menu){
        menu.style.display = isOpen ? 'none' : 'block';
      }
    };

    const menu = document.createElement('div');
    menu.className = 'inline-menu pending-menu';
    menu.style.display = 'none';

    const mChangeSeq = document.createElement('button');
    mChangeSeq.textContent = '番号を変更';
    mChangeSeq.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await changeSeqLabel(x.id, x.seq_label || String(x.seq));
    };
    menu.appendChild(mChangeSeq);

    const mChange = document.createElement('button');
    mChange.textContent = '人数を変更';
    mChange.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await changeHeadcount(x.id, x.headcount);
    };
    menu.appendChild(mChange);

    const m1 = document.createElement('button');
    m1.textContent = '取り消し';
    m1.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await confirmCancel(x.id);
    };
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

    // 「移動中へ」は常に表示
    const moveBtn = document.createElement('button');
    moveBtn.className = 'btn btn-mini';
    moveBtn.textContent = '移動中へ';
    moveBtn.onclick = (e)=>{ e.stopPropagation(); toHeading(x.id); };

    // ︙メニュー（戻す・取り消しのみ）
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
    const waitText =
      wait === 0 ? 'すぐにご案内できます' :
      wait ? `概算待ち時間：約 ${wait} 分` :
      '概算待ち時間：-';

    const li = document.createElement('li');

    // カード（クリックで部屋選択モード）
    const card = document.createElement('button');
    card.className = 'req';
    card.type = 'button';
    card.onclick = ()=> startAssignOnBoard(req, card);

    const left = document.createElement('div');
    left.innerHTML = `
      <div class="title">#${req.seq_label || req.seq} / ${req.headcount}名</div>
      <div class="sub">${waitText}</div>
    `;
    const right = document.createElement('div');
    right.innerHTML = `<span class="pill">部屋を選択</span>`;

    card.appendChild(left);
    card.appendChild(right);

    // インラインメニュー（待機中に戻す／取り消し）
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
      if(menu){
        menu.style.display = isOpen ? 'none' : 'block';
      }
    };

    const menu = document.createElement('div');
    menu.className = 'inline-menu heading-menu';
    menu.style.display = 'none';
    const mChangeSeq2 = document.createElement('button');
    mChangeSeq2.textContent = '番号を変更';
    mChangeSeq2.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await changeSeqLabel(req.id, req.seq_label || String(req.seq));
    };

    const mChange = document.createElement('button');
    mChange.textContent = '人数を変更';
    mChange.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await changeHeadcount(req.id, req.headcount);
    };

    const m1 = document.createElement('button');
    m1.textContent = '待機中に戻す';
    m1.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await headingToPending(req.id);
    };

    const m2 = document.createElement('button');
    m2.textContent = '取り消し';
    m2.onclick = async (ev)=>{
      ev.stopPropagation();
      menu.style.display='none';
      await confirmCancel(req.id);
    };

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

    if(r.status === 'cleaning'){
      div.classList.add('room-card-cleaning');
    }

    // 退出予定時刻の5分前〜過ぎても橙枠を表示し続ける
    if(r.eta_at && r.status === 'occupied'){
      const mins = minutesUntil(r.eta_at);
      if(mins === null || mins <= 5){
        div.classList.add('room-warning');
      }
    }



    const statusClass = `status ${r.status}`;

    // 「使用中」ではここに退出予定の時刻を出さない（下の time 入力で管理）
    let etaText = '';
    if (r.status === 'occupied' && r.eta_at){
  etaText = ` / 空き予定 ${fromISOtoHHMM(r.eta_at)}⌚`;
}else if (r.status === 'cleaning' && r.eta_at){
  etaText = ` / 空き予定 ${fromISOtoHHMM(r.eta_at)}⌚`;
}else if(r.status === 'available'){
  etaText = ' / すぐ案内可';
}


    const line1 = `
      <div class="between">
        <div>
          <span style="font-size:20px; font-weight:700">${r.name}</span>
          <span class="muted" style="font-size:12px">（目安 ${r.capacity}人）</span>
        </div>
        <button type="button"
                class="btn-ghost btn-mini room-menu-button"
                data-room-id="${r.id}">
          ︙
        </button>
      </div>
    `;
    const line2 = `<div class="${statusClass}">${roomStatusLabel(r.status)}<span class="muted">${etaText}</span></div>`;

    div.innerHTML = `
      ${line1}
      ${line2}
      <div id="room-${r.id}" style="margin-top:8px"></div>
    `;

    const inner = div.querySelector('#room-'+r.id);

    // 部屋用ミニメニュー枠
    const menuPanel = document.createElement('div');
    menuPanel.className = 'room-menu-panel';
    menuPanel.id = `room-menu-${r.id}`;
    menuPanel.style.display = 'none';
    div.appendChild(menuPanel);

    const menuBtn = div.querySelector('.room-menu-button');
    if(menuBtn){
      menuBtn.addEventListener('click', ev=>{
        ev.stopPropagation();
        openRoomMenu(r);
      });
    }

    // 使用中
    if (r.status === 'occupied' && r.currentRequestId) {
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
      etaInput.id   = `eta-${r.id}`;
      etaInput.value = fromISOtoHHMM(r.eta_at) || '';

      etaInput.addEventListener('focus', ()=>{
        _editingEta = true;
        if(_etaBlurTimer){ clearTimeout(_etaBlurTimer); _etaBlurTimer = null; }
      });
      etaInput.addEventListener('change', ()=>{
        if(etaInput.value){ saveEta(r.id, etaInput.value); }
      });
      etaInput.addEventListener('blur', ()=>{
        if(etaInput.value){ saveEta(r.id, etaInput.value); }
        // blur後も800ms待ってからフラグ解除（ピッカーUI操作中の一瞬のblurを無視）
        if(_etaBlurTimer) clearTimeout(_etaBlurTimer);
        _etaBlurTimer = setTimeout(()=>{ _editingEta = false; _etaBlurTimer = null; }, 800);
      });

      eta.appendChild(etaLabel);
      eta.appendChild(etaInput);
      inner.appendChild(eta);


      // 清掃中にするボタン：清掃完了と同じくらい大きく
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

    // 清掃中：清掃完了ボタン
    if(r.status === 'cleaning'){
      const cleanBtn = document.createElement('button');
      cleanBtn.className = 'btn btn-wide';
      cleanBtn.textContent = '清掃完了';
      cleanBtn.style.marginTop = '10px';
      cleanBtn.onclick = ()=> cleanDone(r.id);
      inner.appendChild(cleanBtn);
    }


    // 最後にこの部屋カードを一覧に追加
    rEl.appendChild(div);
  }); // ← forEach の終わり

} // ← ここで load() 関数の終わり

// ここから下はそのままでOK
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
  const CLEAN_MIN = 15;   // ★清掃時間（仕様に合わせて15分に）
  return rooms.map(r=>{
    let at = 0;

    if(r.status === 'available'){
      at = 0;

    }else if(r.status === 'occupied' && r.eta_at){
      // 退出予定までの残り + 清掃時間
      const diff = (new Date(r.eta_at) - now) / 60000;
      at = Math.max(0, Math.ceil(diff)) + CLEAN_MIN;

    }else if(r.status === 'cleaning' && r.eta_at){
      // 清掃完了予定までの残り（eta_atが「清掃完了時刻」なので清掃時間は足さない）
      const diff = (new Date(r.eta_at) - now) / 60000;
      at = Math.max(0, Math.ceil(diff));

    }else if(r.status === 'cleaning'){
      // eta_at が無い場合の保険
      at = CLEAN_MIN;

    }else{
      at = 99999;
    }
    return { id:r.id, capacity:r.capacity, at };
  });
}


function estimateWaitMinutesForGroup(size, rooms){
  const slots = buildRoomSlots(rooms).sort((a,b)=>a.at-b.at);

  const slot4 = slots.filter(s=>s.capacity === 4);
  const slot6 = slots.filter(s=>s.capacity === 6);
  const slot2 = slots.filter(s=>s.capacity === 2);

  if(size >= 9){
    const big = [...slot4, ...slot6].sort((a,b)=>a.at-b.at);
    if(big.length < 2) return null;
    return Math.max(big[0].at, big[1].at);
  }

  if(size >= 5){
    if(slot6.length === 0) return null;
    return slot6[0].at;
  }

  if(size >= 3){
    const cand = [...slot4, ...slot6].sort((a,b)=>a.at-b.at);
    if(cand.length === 0) return null;
    return cand[0].at;
  }

  const cand = [...slot2, ...slot4, ...slot6].sort((a,b)=>a.at-b.at);
  if(cand.length === 0) return null;
  return cand[0].at;
}

// 待機中の依頼全体について、# の小さい順に待ち時間を「加算」していくマップを作る
function buildPendingWaitMap(pending, rooms){
  // 現在の部屋のスロット情報を作る（参照を共有する配列）
  const slots = buildRoomSlots(rooms);

  // #（seq）が小さい順に並べ替え
  const sorted = pending.slice().sort((a,b)=> a.seq - b.seq);

  const waitMap = {};
  sorted.forEach(req=>{
    const w = estimateWaitMinutesForGroupAndConsume(req.headcount, slots);
    waitMap[req.id] = w;
  });

  return waitMap;
}

// 1つのグループについて待ち時間を計算し、そのグループが部屋を使う分だけスロットに加算する
function estimateWaitMinutesForGroupAndConsume(size, slots){
  const SERVICE_MIN = 90 + 15; // ★利用90分 + 清掃15分


  // 現在の状態で「いつ空くか」を早い順に並べる
  const sorted = slots.slice().sort((a,b)=> a.at - b.at);

  const slot4 = sorted.filter(s=>s.capacity === 4);
  const slot6 = sorted.filter(s=>s.capacity === 6);
  const slot2 = sorted.filter(s=>s.capacity === 2);

  let chosen = [];

  if(size >= 9){
    const big = [...slot4, ...slot6].sort((a,b)=>a.at-b.at);
    if(big.length < 2) return null;
    chosen = [big[0], big[1]];
  }else if(size >= 5){
    if(slot6.length === 0) return null;
    chosen = [slot6[0]];
  }else if(size >= 3){
    const cand = [...slot4, ...slot6].sort((a,b)=>a.at-b.at);
    if(cand.length === 0) return null;
    chosen = [cand[0]];
  }else{
    const cand = [...slot2, ...slot4, ...slot6].sort((a,b)=>a.at-b.at);
    if(cand.length === 0) return null;
    chosen = [cand[0]];
  }

  // このグループの待ち時間は、選ばれた部屋の中で一番遅く空くもの
  const wait = chosen.reduce((max, s)=> Math.max(max, s.at), 0);

  // このグループが利用した分だけ、その部屋の「次に空く時間」を押し出す
  chosen.forEach(s=>{
    s.at = wait + SERVICE_MIN;
  });

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
    // まず現在のスナップショットを取得
    const snap = await fetchJSON('/api/snapshot');
    const free = snap.free_count;
    const activeCount = snap.heading.length + snap.pending.filter(x=> x.calling).length;

    // 空室数以上は「移動中」を増やせない
    if(activeCount >= free){
      alert('入室可能な部屋数を超えるため、「移動中」をこれ以上作成できません。');
      return;
    }

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

/* ========= 依頼操作 ========= */

/* ========= 番号変更 ========= */
async function changeSeqLabel(requestId, currentSeqLabel){
  const v = prompt('新しい番号を入力してください', currentSeqLabel);
  if(v === null) return;
  const label = v.trim();
  if(label === ''){
    alert('番号を入力してください。');
    return;
  }
  try{
    await post('/api/requests/update_seq_label', {requestId, seq_label: label});
    await load();
  }catch(e){
    alert(e.message || '番号の変更に失敗しました');
  }
}

/* ========= 人数変更 ========= */
async function changeHeadcount(requestId, currentHeadcount){
  const v = prompt('新しい人数を入力してください', currentHeadcount);
  if(v === null) return;  // キャンセル

  const n = parseInt(v, 10);
  if(!Number.isFinite(n) || n < 1){
    alert('1以上の数字を入力してください。');
    return;
  }

  try{
    await post('/api/requests/update_headcount', {requestId, headcount:n});
    await load();
  }catch(e){
    alert(e.message || '人数の変更に失敗しました');
  }
}


async function toggleCalling(requestId, calling){
  try{
    await post('/api/requests/calling', {requestId, calling});
    await load();
  }catch(e){ alert(e.message); }
}
async function confirmCancel(requestId){
  if(!confirm('本当に取り消しますか？')) return;
  try{
    await post('/api/requests/cancel', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}
async function toHeading(requestId){
  try{
    const snap = await fetchJSON('/api/snapshot');
    const free = snap.free_count;
    const activeCount = snap.heading.length + snap.pending.filter(x=> x.calling).length;

    if(activeCount > free){
      alert('入室可能な部屋数を超えるため、「移動中」に移動できません。');
      return;
    }

    await post('/api/requests/heading', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}

async function headingToPending(requestId){
  try{
    await post('/api/requests/heading_to_pending', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}

/* ========= 割当（画面上で部屋選択） ========= */
// 「移動中」の枠をクリックした時の処理
function startAssignOnBoard(req, card){
  // すでにこの依頼が選択されている → 選択解除
  if (PICK_REQ && PICK_REQ.id === req.id){
    PICK_REQ = null;
    clearRoomHighlights();
    clearReqHighlights();
    return;
  }

  // この依頼を選択状態にする
  PICK_REQ = req;

  // まず他の依頼のハイライトを消す
  clearReqHighlights();

  // 今クリックした枠をハイライト
  card.classList.add('req-selected');

  // 空室の部屋をハイライト
  highlightRoomsForSelection();
}


// 部屋の枠を押したときの処理（ボード割り当て用）
async function assignFromBoard(roomId){
  if (!PICK_REQ) return;

  try{
    await assign(roomId, PICK_REQ.id);
    PICK_REQ = null;
    clearRoomHighlights();
    clearReqHighlights();
    await load();               // このあとすぐ最新状態を読み込み
  }catch(e){
    alert(e.message || '割当に失敗しました');
  }
}
// 共通 assign ヘルパー
async function assign(roomId, requestId){
  const res = await post('/api/assign', {roomId, requestId});
  if(!res.ok){
    // サーバー側が {"ok": False, "msg": "..."} を返している場合
    throw new Error(res.msg || '割当に失敗しました（サーバー側エラー）');
  }
}


/* ========= 旧モーダル方式（未使用） ========= */
function openRoomPicker(req){
  // 残しておくだけ
}
function closeRoomPicker(){
  document.getElementById('overlayRoom').style.display='none';
  document.getElementById('roomPicker').style.display='none';
  PICK_REQ = null;
}

/* ========= 部屋メニュー（ミニ） ========= */
function openRoomMenu(room){
  const panel = document.getElementById(`room-menu-${room.id}`);
  if(!panel) return;

  const isVisible = panel.style.display === 'block';
  document.querySelectorAll('.room-menu-panel').forEach(p=> p.style.display='none');

  if(isVisible){
    panel.style.display = 'none';
    return;
  }

  panel.innerHTML = '';
  const inner = document.createElement('div');
  inner.className = 'room-menu-inner';

  const isDisabled = room.status === 'disabled';
  const btnDisable = document.createElement('button');
  btnDisable.textContent = isDisabled ? '使用停止を解除' : '使用停止にする';
  btnDisable.onclick = async ()=>{
    await toggleRoomDisabled(room.id, !isDisabled);
    panel.style.display = 'none';
  };
  inner.appendChild(btnDisable);

  if(room.status === 'occupied' && room.currentRequestId){
    const btnChange = document.createElement('button');
    btnChange.textContent = '人数を変更';
    btnChange.onclick = async ()=>{
      await changeHeadcount(room.currentRequestId, room.currentHeadcount || 1);
      panel.style.display = 'none';
    };
    inner.appendChild(btnChange);

    const btnBack = document.createElement('button');
    btnBack.textContent = '「移動中」に戻す';
    btnBack.onclick = async ()=>{
      await requeueToHeading(room.currentRequestId);
      panel.style.display = 'none';
    };
    inner.appendChild(btnBack);
  }


  panel.appendChild(inner);
  panel.style.display = 'block';
}


async function toggleRoomDisabled(roomId, disabled){
  try{
    await post('/api/rooms/disable', {roomId, disabled});
    await load();
  }catch(e){ alert(e.message); }
}

/* ========= 部屋操作 ========= */
async function saveEta(roomId, hhmm){
  try{
    await post('/api/rooms/eta', {roomId, hhmm});
    await load();
  }catch(e){ alert(e.message); }
}
async function requeueToHeading(requestId){
  try{
    await post('/api/requeue_to_heading', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}
async function confirmCheckout(roomName, requestId){
  if(!confirm(`${roomName}の鍵を確認しましたか？`)) return;
  try{
    await post('/api/checkout', {requestId});
    await load();
  }catch(e){ alert(e.message); }
}
async function cleanDone(roomId){
  try{
    await post('/api/rooms/clean_done', {roomId});
    await load();
  }catch(e){ alert(e.message); }
}

async function logout(){
  try{
    await post('/api/logout', {});
  }catch(e){
  }
  window.location.href = '/';
}

/* ========= 管理 ========= */
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
  const [hist, canceled] = await Promise.all([
    fetchJSON('/api/history'),
    fetchJSON('/api/canceled_history')
  ]);

  const wrap = document.getElementById('adminContent');
  wrap.innerHTML = '';

  // --- 入室履歴 ---
  const hTitle = document.createElement('h4');
  hTitle.textContent = '入室履歴（最近50件）';
  wrap.appendChild(hTitle);

  const ul = document.createElement('ul');
  ul.className = 'list';

  hist.forEach(x=>{
    const li = document.createElement('li');
    li.className = 'item';

    const left = document.createElement('span');
    left.innerHTML = `#${x.seq} / ${x.headcount}名 / ${x.room_name||'-'} / ${x.updated_at}`;

    const box = document.createElement('span');

    const btn = document.createElement('button');
    btn.className = 'btn btn-mini btn-outline';
    btn.textContent = '「移動中」に復元（#そのまま）';
    btn.onclick = async ()=>{
      try{
        await post('/api/requests/restore', {requestId:x.id});
        await load();
        await loadAdmin();
      }catch(e){ alert(e.message); }
    };
    box.appendChild(btn);

    li.appendChild(left);
    li.appendChild(box);
    ul.appendChild(li);
  });
  wrap.appendChild(ul);

  // --- 取り消し履歴 ---
  const cTitle = document.createElement('h4');
  cTitle.textContent = '取り消し履歴（最近50件）';
  wrap.appendChild(cTitle);

  const cul = document.createElement('ul');
  cul.className = 'list';

  canceled.forEach(x=>{
    const li = document.createElement('li');
    li.className = 'item';

    const left = document.createElement('span');
    left.innerHTML = `#${x.seq} / ${x.headcount}名 / ${x.room_name||'-'} / ${x.updated_at}`;

    const box = document.createElement('span');

    const toHeading = document.createElement('button');
    toHeading.className = 'btn btn-mini btn-outline';
    toHeading.textContent = '「移動中」に復元（#そのまま）';
    toHeading.onclick = async ()=>{
      try{
        await post('/api/cancel_restore', {requestId:x.id, target:'heading'});
        await load();
        await loadAdmin();
      }catch(e){ alert(e.message); }
    };

    const toPending = document.createElement('button');
    toPending.className = 'btn btn-mini btn-outline';
    toPending.textContent = '待機中に復元（#そのまま）';
    toPending.onclick = async ()=>{
      try{
        await post('/api/cancel_restore', {requestId:x.id, target:'pending'});
        await load();
        await loadAdmin();
      }catch(e){ alert(e.message); }
    };

    box.appendChild(toHeading);
    box.appendChild(toPending);

    li.appendChild(left);
    li.appendChild(box);
    cul.appendChild(li);
  });

  wrap.appendChild(cul);
}



/* ========= ハイライト系 ========= */
// 「移動中」の依頼枠のハイライトを全部消す
function clearReqHighlights(){
  document.querySelectorAll('.req-selected').forEach(el=>{
    el.classList.remove('req-selected');
  });
}

// 空室の部屋枠をハイライト
function highlightRoomsForSelection(){
  clearRoomHighlights();

  const cards = document.querySelectorAll('.room-card');
  cards.forEach(card=>{
    const statusEl = card.querySelector('.status.available');
    if(statusEl){
      card.classList.add('room-selectable');
      const roomId = parseInt(card.dataset.roomId || '0', 10);
      card.onclick = ()=> assignFromBoard(roomId);
    }
  });
}

// 全ての部屋枠のハイライトを消す
function clearRoomHighlights(){
  document.querySelectorAll('.room-card').forEach(card=>{
    card.classList.remove('room-selectable');
    card.onclick = null;
  });
}

/* ========= メニュー共通：外側クリックで閉じる ========= */
function closeAllMenus(){
  document.querySelectorAll('.inline-menu').forEach(m=> m.style.display='none');
  document.querySelectorAll('.room-menu-panel').forEach(p=> p.style.display='none');
}

document.addEventListener('click', (e)=>{
  if(e.target.closest('.inline-menu-container') ||
     e.target.closest('.inline-menu') ||
     e.target.closest('.room-menu-panel') ||
     e.target.closest('.room-menu-button')
  ){
    return;
  }
  closeAllMenus();
});

// 画面のどこかをクリックしたときの共通ハンドラ
document.addEventListener('click', e=>{
  // 部屋選択中でなければ何もしない
  if(!PICK_REQ) return;

  // 依頼カード or 部屋カード上のクリックなら解除しない
  if(e.target.closest('.req') || e.target.closest('.room-card')) return;

  // それ以外の場所をクリックしたら選択解除
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

# ========================
# ここから Python(FastAPI)
# ========================
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from datetime import datetime, timedelta, timezone
from typing import Dict, List
from zoneinfo import ZoneInfo
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
import uuid

app = FastAPI()

try:
    TZ = ZoneInfo("Asia/Tokyo")
except Exception:
    # tzdata が無い環境でも JST として動かせるようにする
    TZ = timezone(timedelta(hours=9))

SESSION_COOKIE = "dogo_session"
SESSION_MAX_AGE = 60 * 60 * 17 + 60 * 30
LOGIN_WINDOW_SECONDS = 30 * 60
LOGIN_MAX_ATTEMPTS = 5
PERMANENT_BAN_THRESHOLD = 40
APP_USERNAME = os.getenv("DOGO_APP_USERNAME", "staff")
APP_PASSWORD = os.getenv("DOGO_APP_PASSWORD", "ChangeMe123!")
SESSION_SECRET = os.getenv("DOGO_SESSION_SECRET", "change-this-session-secret")
ALLOWED_HOST_SUFFIXES = tuple(
    x.strip() for x in os.getenv("DOGO_ALLOWED_HOSTS", "localhost,127.0.0.1,.workers.dev").split(",") if x.strip()
)
LOGIN_ATTEMPTS: Dict[str, List[float]] = {}
PERMANENT_BANS: set = set()
TOTAL_FAILURES: Dict[str, int] = {}


# メモリ上の簡易データベース
ROOMS: Dict[int, dict] = {
    1: {"id": 1, "name": "一号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    2: {"id": 2, "name": "二号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    3: {"id": 3, "name": "三号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    4: {"id": 4, "name": "五号室", "capacity": 2,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    5: {"id": 5, "name": "六号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    6: {"id": 6, "name": "七号室", "capacity": 6,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    7: {"id": 7, "name": "八号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    8: {"id": 8, "name": "十号室", "capacity": 4,
        "status": "available", "eta_at": None,
        "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
}

REQUESTS: Dict[str, dict] = {}
PENDING: List[str] = []
HEADING: List[str] = []

HISTORY: List[dict] = []
CANCELED: List[dict] = []


SEQ_COUNTER = 1

# ── データ永続化（Cloudflare KV）────────────────────────────
_STATE_LOADED = False

def _state_data():
    return {
        "rooms": {str(k): v for k, v in ROOMS.items()},
        "requests": REQUESTS,
        "pending": PENDING,
        "heading": HEADING,
        "history": HISTORY,
        "canceled": CANCELED,
        "seq_counter": SEQ_COUNTER,
        "permanent_bans": list(PERMANENT_BANS),
        "total_failures": TOTAL_FAILURES,
    }

def _apply_state(d):
    global SEQ_COUNTER
    ROOMS.clear()
    ROOMS.update({int(k): v for k, v in d["rooms"].items()})
    REQUESTS.clear()
    REQUESTS.update(d["requests"])
    PENDING[:] = d["pending"]
    HEADING[:] = d["heading"]
    HISTORY[:] = d["history"]
    CANCELED[:] = d["canceled"]
    SEQ_COUNTER = d["seq_counter"]
    PERMANENT_BANS.clear()
    PERMANENT_BANS.update(d.get("permanent_bans", []))
    TOTAL_FAILURES.clear()
    TOTAL_FAILURES.update(d.get("total_failures", {}))

def _get_kv(request: Request):
    env = request.scope.get("cloudflare.workers.env") or request.scope.get("env")
    if env is None:
        return None
    return getattr(env, "STATE_KV", None)

async def save_state(request: Request):
    kv = _get_kv(request)
    if kv is None:
        return
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    try:
        data = json.dumps({"saved_date": today, "data": _state_data()}, ensure_ascii=False)
        await kv.put("state", data)
    except Exception:
        pass

async def load_state(request: Request):
    kv = _get_kv(request)
    if kv is None:
        return
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    try:
        raw = await kv.get("state")
        if not raw:
            return
        saved = json.loads(raw)
        if saved.get("saved_date") != today:
            return
        _apply_state(saved["data"])
    except Exception:
        pass
# ─────────────────────────────────────────────────────────────

def now_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")



def ceil_to_5min(dt: datetime) -> datetime:
    """dt を「次の5分」に切り上げる（日本時間で統一）"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    else:
        dt = dt.astimezone(TZ)

    minute = ((dt.minute + 4) // 5) * 5
    if minute >= 60:
        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        dt = dt.replace(minute=minute, second=0, microsecond=0)
    return dt



def build_request(headcount: int) -> dict:
    global SEQ_COUNTER
    rid = str(uuid.uuid4())
    seq = SEQ_COUNTER

    req = {
        "id": rid,
        "seq": seq,                 # 数値としての受付番号（元番号）
        "seq_label": f"{seq}",      # 表示用（通常は "12"）
        "seq_part": None,           # 分割されたとき 1 / 2
        "seq_parts": None,          # 分割されたとき 2
        "headcount": headcount,
        "calling": False,
        "updated_at": now_str(),
        "room_id": None,
    }
    REQUESTS[rid] = req
    SEQ_COUNTER += 1
    return req



def move_request(rid: str, src: List[str], dst: List[str]):
    if rid in src:
        src.remove(rid)
    if rid not in dst:
        dst.append(rid)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def make_session_value(username: str) -> tuple[str, str]:
    csrf_token = secrets.token_urlsafe(24)
    payload = {
        "u": username,
        "csrf": csrf_token,
        "iat": int(time.time()),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_b64 = _b64url_encode(payload_bytes)
    sig = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}", csrf_token


def parse_session_value(raw_value: str | None) -> dict | None:
    if not raw_value or "." not in raw_value:
        return None
    payload_b64, sig = raw_value.rsplit(".", 1)
    expected = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    except Exception:
        return None
    if int(payload.get("iat", 0)) + SESSION_MAX_AGE < int(time.time()):
        return None
    return payload


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def prune_login_attempts(ip: str) -> List[float]:
    now = time.time()
    recent = [ts for ts in LOGIN_ATTEMPTS.get(ip, []) if now - ts <= LOGIN_WINDOW_SECONDS]
    LOGIN_ATTEMPTS[ip] = recent
    return recent


def is_authenticated(request: Request) -> bool:
    return bool(getattr(request.state, "session", None))


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    global _STATE_LOADED
    if not _STATE_LOADED:
        await load_state(request)
        _STATE_LOADED = True

    host = (request.headers.get("host") or "").split(":")[0]
    if host and not any(host == allowed or host.endswith(allowed) for allowed in ALLOWED_HOST_SUFFIXES):
        return JSONResponse({"ok": False, "msg": "invalid host"}, status_code=400)

    request.state.session = parse_session_value(request.cookies.get(SESSION_COOKIE))

    if request.url.path.startswith("/api/") and request.url.path not in ("/api/login",):
        if not is_authenticated(request):
            return JSONResponse({"ok": False, "msg": "authentication required"}, status_code=401)

    if request.method == "POST" and request.url.path.startswith("/api/") and request.url.path not in ("/api/login",):
        session = getattr(request.state, "session", None) or {}
        csrf_header = request.headers.get("x-csrf-token", "")
        if not csrf_header or csrf_header != session.get("csrf"):
            return JSONResponse({"ok": False, "msg": "invalid csrf token"}, status_code=403)

    if request.url.path == "/" and not is_authenticated(request):
        response = HTMLResponse(LOGIN_HTML)
    else:
        response = await call_next(request)

    # データ変更POSTのあとに状態をKVへ保存
    if (request.method == "POST"
            and request.url.path.startswith("/api/")
            and request.url.path not in ("/api/login", "/api/logout")
            and response.status_code < 400):
        await save_state(request)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    return response


@app.post("/api/login")
async def login_api(request: Request, body: dict):
    ip = get_client_ip(request)

    if ip in PERMANENT_BANS:
        return JSONResponse({"ok": False, "msg": "このアクセス元は永久にブロックされています。"}, status_code=403)

    attempts = prune_login_attempts(ip)
    if len(attempts) >= LOGIN_MAX_ATTEMPTS:
        return JSONResponse({"ok": False, "msg": "試行回数が多すぎます。しばらく待ってから再試行してください。"}, status_code=429)

    username = str(body.get("username", ""))
    password = str(body.get("password", ""))
    if username != APP_USERNAME or password != APP_PASSWORD:
        attempts.append(time.time())
        LOGIN_ATTEMPTS[ip] = attempts
        TOTAL_FAILURES[ip] = TOTAL_FAILURES.get(ip, 0) + 1
        if TOTAL_FAILURES[ip] >= PERMANENT_BAN_THRESHOLD:
            PERMANENT_BANS.add(ip)
            await save_state(request)
            return JSONResponse({"ok": False, "msg": "このアクセス元は永久にブロックされています。"}, status_code=403)
        return JSONResponse({"ok": False, "msg": "ユーザー名またはパスワードが違います。"}, status_code=401)

    LOGIN_ATTEMPTS[ip] = []
    session_value, _csrf = make_session_value(username)
    response = JSONResponse({"ok": True})
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_value,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="strict",
        max_age=SESSION_MAX_AGE,
        path="/",
    )
    return response


@app.post("/api/logout")
async def logout_api():
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    session = getattr(request.state, "session", None)
    if not session:
        return HTMLResponse(LOGIN_HTML)
    return HTMLResponse(HTML.replace("__CSRF_TOKEN__", session["csrf"]))


@app.get("/api/snapshot")
def snapshot():
    rooms = list(ROOMS.values())
    pending = [REQUESTS[rid] for rid in PENDING if rid in REQUESTS]
    heading = [REQUESTS[rid] for rid in HEADING if rid in REQUESTS]

    free_count = sum(1 for r in rooms if r["status"] == "available")
    remain = free_count

    return {
        "rooms": rooms,
        "pending": pending,
        "heading": heading,
        "free_count": free_count,
        "remain": remain,
    }


@app.post("/api/requests")
async def create_request(body: dict):
    headcount = int(body.get("headcount", 1))
    status = body.get("status", "pending")
    seq_label = body.get("seq_label")

    req = build_request(headcount)
    if seq_label is not None:
        req["seq_label"] = str(seq_label).strip()

    if status == "pending":
        PENDING.append(req["id"])
    else:
        HEADING.append(req["id"])

    return {"ok": True}


@app.post("/api/requests/update_seq_label")
async def update_seq_label(body: dict):
    rid = body["requestId"]
    new_label = str(body.get("seq_label", "")).strip()
    if not new_label:
        return {"ok": False, "msg": "seq_label is required"}
    req = REQUESTS.get(rid)
    if not req:
        return {"ok": False, "msg": "request not found"}
    req["seq_label"] = new_label
    req["updated_at"] = now_str()
    return {"ok": True}


@app.post("/api/requests/calling")
async def set_calling(body: dict):
    rid = body["requestId"]
    calling = bool(body["calling"])
    if rid in REQUESTS:
        REQUESTS[rid]["calling"] = calling
        REQUESTS[rid]["updated_at"] = now_str()
    return {"ok": True}


@app.post("/api/requests/cancel")
async def cancel_request(body: dict):
    rid = body["requestId"]
    req = REQUESTS.get(rid)
    if not req:
        return {"ok": False, "msg": "not found"}

    if rid in PENDING:
        PENDING.remove(rid)
    if rid in HEADING:
        HEADING.remove(rid)
    REQUESTS.pop(rid, None)


    room_name = "-"
    if req.get("room_id") and req["room_id"] in ROOMS:
        room_name = ROOMS[req["room_id"]]["name"]

    CANCELED.insert(0, {
        "id": rid,
        "seq": req["seq"],
        "headcount": req["headcount"],
        "room_name": room_name,
        "updated_at": now_str(),
    })

    return {"ok": True}


@app.post("/api/requests/heading")
async def pending_to_heading(body: dict):
    rid = body["requestId"]
    move_request(rid, PENDING, HEADING)
    return {"ok": True}


@app.post("/api/requests/heading_to_pending")
async def heading_to_pending_api(body: dict):
    rid = body["requestId"]
    move_request(rid, HEADING, PENDING)
    return {"ok": True}

@app.post("/api/requests/update_headcount")
async def update_headcount(body: dict):
    rid = body["requestId"]
    new_headcount = int(body.get("headcount", 1))

    if new_headcount < 1:
        return {"ok": False, "msg": "headcount must be >= 1"}

    req = REQUESTS.get(rid)
    if not req:
        return {"ok": False, "msg": "request not found"}

    req["headcount"] = new_headcount
    req["updated_at"] = now_str()

    # もし部屋に入っている依頼なら、部屋側の人数も更新
    room_id = req.get("room_id")
    if room_id and room_id in ROOMS:
        ROOMS[room_id]["currentHeadcount"] = new_headcount

    return {"ok": True}


@app.post("/api/assign")
async def assign_room(body: dict):
    room_id = int(body["roomId"])
    request_id = body["requestId"]

    room = ROOMS.get(room_id)
    req = REQUESTS.get(request_id)
    if not room or not req:
        return {"ok": False, "msg": "not found"}

    # ① 空室でない部屋には割り当てしない
    if room["status"] != "available":
        return {"ok": False, "msg": "room not available"}

    # ② ここで部屋を「使用中」にする ←★一番大事
    room["status"] = "occupied"
    room["currentRequestId"] = request_id
    room["currentSeq"] = req.get("seq_label") or str(req["seq"])
    room["currentHeadcount"] = req["headcount"]

    # ③ 退出予定時刻をセット（今のロジックのままでOK）
    base = ceil_to_5min(datetime.now(TZ))
    eta = base + timedelta(minutes=90)
    room["eta_at"] = eta.isoformat()

    # ④ 依頼側にも部屋IDを記録
    req["room_id"] = room_id
    req["updated_at"] = now_str()

    # ⑤ 「移動中」リストから外す
    if request_id in HEADING:
        HEADING.remove(request_id)

    return {"ok": True}



@app.post("/api/requeue_to_heading")
async def requeue_to_heading_api(body: dict):
    request_id = body["requestId"]

    for room in ROOMS.values():
        if room["currentRequestId"] == request_id:
            room["currentRequestId"] = None
            room["currentSeq"] = None
            room["currentHeadcount"] = None
            room["status"] = "available"
            room["eta_at"] = None

    move_request(request_id, PENDING, HEADING)
    if request_id not in HEADING:
        HEADING.append(request_id)

    return {"ok": True}


@app.post("/api/checkout")
async def checkout(body: dict):
    request_id = body["requestId"]
    req = REQUESTS.get(request_id)
    if not req:
        return {"ok": False, "msg": "not found"}

    for room in ROOMS.values():
        if room["currentRequestId"] == request_id:

            room["currentRequestId"] = None
            room["currentSeq"] = None
            room["currentHeadcount"] = None
            room["status"] = "cleaning"

            # 現在時刻を5分刻みにしてから、10分後＝清掃完了時刻をセット
            base = ceil_to_5min(datetime.now(TZ))
            eta = base + timedelta(minutes=15)

            room["eta_at"] = eta.isoformat()

            HISTORY.insert(0, {
                "id": request_id,
                "seq": req["seq"],
                "headcount": req["headcount"],
                "room_name": room["name"],
                "updated_at": now_str(),
            })
            break

    return {"ok": True}


@app.post("/api/rooms/eta")
async def save_eta_api(body: dict):
    room_id = int(body["roomId"])
    hhmm = body["hhmm"]
    room = ROOMS.get(room_id)
    if not room:
        return {"ok": False, "msg": "room not found"}

    hour, minute = map(int, hhmm.split(":"))
    now = datetime.now(TZ)

    eta = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # ★入力した時刻が「いま」より過去なら、翌日にする（表示ズレ防止）
    if eta < now:
        eta = eta + timedelta(days=1)

    room["eta_at"] = eta.isoformat()
    return {"ok": True}



@app.post("/api/rooms/clean_done")
async def clean_done_api(body: dict):
    room_id = int(body["roomId"])
    room = ROOMS.get(room_id)
    if not room:
        return {"ok": False, "msg": "room not found"}

    room["status"] = "available"
    room["eta_at"] = None
    return {"ok": True}


@app.get("/api/history")
async def get_history():
    return HISTORY[:50]


@app.get("/api/canceled_history")
async def get_canceled_history():
    return CANCELED[:50]


@app.get("/api/rooms")
async def get_rooms():
    return list(ROOMS.values())

@app.post("/api/rooms/disable")
async def disable_room(body: dict):
    room_id = int(body["roomId"])
    disabled = bool(body["disabled"])
    room = ROOMS.get(room_id)
    if not room:
        return {"ok": False, "msg": "room not found"}

    if disabled:
        room["status"] = "disabled"
        room["currentRequestId"] = None
        room["currentSeq"] = None
        room["currentHeadcount"] = None
        room["eta_at"] = None
    else:
        room["status"] = "available"

    return {"ok": True}


@app.post("/api/requests/restore")
async def restore_from_history(body: dict):
    original_id = body["requestId"]
    hist = next((h for h in HISTORY if h["id"] == original_id), None)
    if not hist:
        return {"ok": False, "msg": "not found"}

    req = build_request(hist["headcount"])
    req["seq"] = hist["seq"]
    req["seq_label"] = f"{req['seq']}"


    HEADING.append(req["id"])
    return {"ok": True}


@app.post("/api/cancel_restore")
async def cancel_restore(body: dict):
    original_id = body["requestId"]
    target = body.get("target", "heading")

    hist = next((h for h in CANCELED if h["id"] == original_id), None)
    if not hist:
        return {"ok": False, "msg": "not found"}

    req = build_request(hist["headcount"])
    req["seq"] = hist["seq"]

    if target == "pending":
        PENDING.append(req["id"])
    else:
        HEADING.append(req["id"])

    return {"ok": True}





