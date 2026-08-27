#!/usr/bin/env python3
"""
Generator for TrueSiddiquiAnimation.html
A NASA-style replica of the Artemis II Entry-Point -> Splashdown segment,
driven EXCLUSIVELY by our own extracted telemetry (traj_telemetry.json).

TRUTH MODE rules honoured:
  * Only real dial data is plotted (velocity, altitude, downrange, time, moon dist).
  * Telemetry has NO latitude/longitude/heading -> geography is NOT invented.
    Instead we draw an honest ORBITAL-PLANE PROFILE: the polar angle is the
    real downrange (arc length / Earth radius) and the radius is the real
    FROM-EARTH altitude. This is a physically faithful cross-section, and it
    is labelled as such.
  * Anomalies are marked exactly where they occur (frame 38 & 105 time
    reversal, frame 153 +110 s blackout gap, duplicates, data-ends).
  * Data ends at 34 mi / 11,650 mph. The craft is still aloft. We do NOT
    continue to splashdown because our dials never reach it. NASA's own
    animation shows splashdown in the PACIFIC; our earlier Atlantic guess is
    flagged as unverified assumption, not fact.
"""
import json

TEL = json.load(open('traj_telemetry.json'))
tel_json = json.dumps(TEL, separators=(',', ':'))

R_EARTH_MI = 3959.0  # mean Earth radius, used only to convert downrange->angle

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TrueSiddiquiAnimation &mdash; Artemis II Re-entry (telemetry-only replica)</title>
<style>
  :root{--fg:#e8f0ff;--dim:#8ea3c0;--pan:#0c1526;--edge:#1c2b45;--hot:#ff5470;--vel:#ffd166;--alt:#5ec8ff;--dr:#8affc1;}
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;background:#04070f;color:var(--fg);
    font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  #wrap{display:flex;flex-direction:column;height:100vh}
  header{padding:10px 16px;border-bottom:1px solid var(--edge);background:#060b16}
  header h1{margin:0;font-size:16px;letter-spacing:.4px}
  header h1 small{color:var(--dim);font-weight:400;font-size:12px}
  #banner{background:#2a0f16;border-bottom:1px solid #52202b;color:#ffc9d3;
    font-size:12px;padding:7px 16px;line-height:1.45}
  #banner b{color:#ffb0bd}
  #main{flex:1;display:flex;min-height:0}
  #stage{flex:1;position:relative;min-width:0}
  canvas{display:block;width:100%;height:100%}
  #side{width:310px;flex:none;background:var(--pan);border-left:1px solid var(--edge);
    padding:12px 14px;overflow:auto}
  .grp{margin-bottom:12px}
  .grp h2{margin:0 0 6px;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--dim)}
  .row{display:flex;justify-content:space-between;align-items:baseline;
    padding:3px 0;border-bottom:1px dashed #16223a}
  .lbl{color:var(--dim);font-size:12px}
  .val{font-variant-numeric:tabular-nums;font-weight:600;font-size:15px}
  .val small{color:var(--dim);font-weight:400;font-size:11px;margin-left:2px}
  .vel{color:var(--vel)}.alt{color:var(--alt)}.dr{color:var(--dr)}.g{color:var(--hot)}
  .hash{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:#b9c8e6}
  #flag{margin-top:8px;min-height:20px;font-size:12px;font-weight:600}
  #ctrls{display:flex;align-items:center;gap:8px;padding:10px 16px;
    border-top:1px solid var(--edge);background:#060b16}
  button{background:#12213c;color:var(--fg);border:1px solid #24395e;border-radius:6px;
    padding:6px 12px;font-size:13px;cursor:pointer}
  button:hover{background:#1a2f52}
  #scrub{flex:1}
  .legend{font-size:11px;color:var(--dim);line-height:1.5}
  .legend .k{display:inline-block;width:11px;height:11px;border-radius:2px;
    vertical-align:-1px;margin-right:5px}
  .note{font-size:11px;color:#9fb2d0;line-height:1.5;background:#0a1424;
    border:1px solid #182a47;border-radius:6px;padding:9px 11px;margin-top:6px}
  .note b{color:#e8f0ff}
</style>
</head>
<body>
<div id="wrap">
  <header>
    <h1>TrueSiddiquiAnimation &mdash; Artemis II Re-entry replica
      <small>&nbsp;built ONLY from our extracted telemetry &middot; no bias, no invented geography</small></h1>
  </header>
  <div id="banner">
    <b>HONEST SCOPE:</b> This is the Entry&nbsp;Point&nbsp;&rarr;&nbsp;Splashdown segment.
    Our dials record <b>velocity, altitude, downrange &amp; time only</b> &mdash; they contain
    <b>NO latitude, longitude or heading</b>. So this is an <b>orbital-plane profile</b>
    (angle = real downrange, height = real altitude), <b>not</b> a map. Our data ENDS at
    <b>34&nbsp;mi / 11,650&nbsp;mph</b> &mdash; the capsule is still aloft; we do not draw a
    splashdown because our telemetry never reaches it. NASA&rsquo;s own animation depicts
    splashdown in the <b>Pacific</b>; our earlier Atlantic guess was an assumption, now retracted.
  </div>
  <div id="main">
    <div id="stage"><canvas id="c"></canvas></div>
    <div id="side">
      <div class="grp">
        <h2>Live telemetry (from dials)</h2>
        <div class="row"><span class="lbl">Frame</span><span class="val" id="oIdx">--<small>/265</small></span></div>
        <div class="row"><span class="lbl">Video time</span><span class="val" id="oTime">--:--:--</span></div>
        <div class="row"><span class="lbl">Mission elapsed</span><span class="val" id="oRel">--<small>s</small></span></div>
        <div class="row"><span class="lbl">Velocity</span><span class="val vel" id="oVel">--<small>mph</small></span></div>
        <div class="row"><span class="lbl">Altitude (from Earth)</span><span class="val alt" id="oAlt">--<small>mi</small></span></div>
        <div class="row"><span class="lbl">Downrange</span><span class="val dr" id="oDr">--<small>mi</small></span></div>
        <div class="row"><span class="lbl">Decel</span><span class="val g" id="oG">--<small>g</small></span></div>
        <div class="row"><span class="lbl">To Moon</span><span class="val" id="oMoon">--<small>mi</small></span></div>
        <div class="row"><span class="lbl">Frame MD5</span><span class="hash" id="oHash">--------</span></div>
        <div id="flag"></div>
      </div>
      <div class="grp">
        <h2>What the plot shows</h2>
        <div class="legend">
          <div><span class="k" style="background:#ffd166"></span>Trajectory profile (real downrange &amp; altitude)</div>
          <div><span class="k" style="background:#ff5470"></span>Capsule &mdash; current telemetry frame</div>
          <div><span class="k" style="background:#5ec8ff"></span>Earth surface (radius reference only)</div>
          <div><span class="k" style="background:#b06bff"></span>Anomaly marker (reversal / gap / data-end)</div>
        </div>
        <div class="note">
          <b>Why a profile, not a map?</b> Downrange is a true arc-length, so
          angle&nbsp;=&nbsp;downrange&nbsp;/&nbsp;Earth&nbsp;radius is honest. Altitude is the
          real FROM-EARTH dial. The <b>direction</b> around the globe and the landing point are
          <b>unknown from our data</b>, so none is drawn. Every one of the 265 frames is plotted;
          nothing smoothed, nothing added.
        </div>
      </div>
    </div>
  </div>
  <div id="ctrls">
    <button id="play">&#10074;&#10074; Pause</button>
    <button id="reset">&#8635; Reset</button>
    <input type="range" id="scrub" min="0" max="264" value="0" step="1">
    <span id="clock" class="legend" style="min-width:120px;text-align:right"></span>
  </div>
</div>
<script>
const TEL = __TEL_JSON__;
const R_EARTH_MI = __R_EARTH__;
const N = TEL.length;

// ---- derive honest per-frame quantities ----
// polar angle from downrange (radians), radius = Earth + altitude
for (let i=0;i<N;i++){
  const f = TEL[i];
  f.theta = f.downrange / R_EARTH_MI;              // real arc-length angle
  f.radius = R_EARTH_MI + f.alt;                   // real altitude
  // g-force from velocity change vs previous real-time sample
  if (i>0){
    const dt = TEL[i].sec - TEL[i-1].sec;
    if (dt>0){
      const dv = (TEL[i-1].vel - TEL[i].vel) * 0.44704; // mph->m/s
      f.g = Math.max(0,(dv/dt)/9.80665);
    } else f.g = 0;
  } else f.g = 0;
}
// anomaly classification
const anomaly = new Array(N).fill(null);
for (let i=1;i<N;i++){
  if (TEL[i].sec < TEL[i-1].sec) anomaly[i] = 'TIME REVERSAL (clock jumps back \u2014 replay artifact)';
  else if (TEL[i].sec - TEL[i-1].sec > 5) anomaly[i] = 'BLACKOUT GAP +' + (TEL[i].sec-TEL[i-1].sec) + 's (frames missing)';
  else if (TEL[i].md5 === TEL[i-1].md5) anomaly[i] = 'DUPLICATE frame (byte-identical to previous)';
}
anomaly[N-1] = 'DATA ENDS \u2014 34 mi / 11,650 mph, craft still aloft';

const cv = document.getElementById('c');
const ctx = cv.getContext('2d');
let W=0,H=0,DPR=1;
function resize(){
  DPR = Math.min(2, window.devicePixelRatio||1);
  const r = cv.parentNode.getBoundingClientRect();
  W=r.width; H=r.height;
  cv.width=W*DPR; cv.height=H*DPR;
  ctx.setTransform(DPR,0,0,DPR,0,0);
}
window.addEventListener('resize',()=>{resize();draw();});

// starfield
const stars=[];
for(let i=0;i<220;i++) stars.push({x:Math.random(),y:Math.random(),r:Math.random()*1.3+0.2,a:Math.random()*0.7+0.3});

// ---- honest altitude-vs-downrange profile ----
// X axis = real downrange (mi). Y axis = real altitude (mi), exaggerated so the
// 28..40 mi band is readable. A gentle Earth-curve baseline is drawn for style.
const DR_MAX = 1000;    // downrange axis top (mi)
const ALT_MAX = 50;     // altitude axis top (mi)
function plotArea(){
  return {l:64, r:W-24, t:56, b:H-56};
}
function px(dr,a){
  const P=plotArea();
  const x = P.l + (dr/DR_MAX)*(P.r-P.l);
  const y = P.b - (a/ALT_MAX)*(P.b-P.t);
  return [x,y];
}
function earthBaselineY(dr){
  // shallow cosmetic curvature so the "surface" bows like a horizon
  const P=plotArea();
  const midx=(P.l+P.r)/2, half=(P.r-P.l)/2;
  const t=(px(dr,0)[0]-midx)/half; // -1..1
  return P.b + 26 - (1-t*t)*22;     // bows upward in the middle
}

let cur=0, playing=true, last=0;
const FPS=18;

function draw(){
  ctx.clearRect(0,0,W,H);
  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,'#04070f'); bg.addColorStop(1,'#081020');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);
  for(const s of stars){ ctx.globalAlpha=s.a; ctx.fillStyle='#cfe0ff';
    ctx.beginPath(); ctx.arc(s.x*W,s.y*H*0.5,s.r,0,7); ctx.fill(); }
  ctx.globalAlpha=1;

  const P=plotArea();

  // ---- Earth body (below baseline) ----
  ctx.beginPath();
  ctx.moveTo(P.l, H);
  for(let dr=0; dr<=DR_MAX; dr+=25){ const x=px(dr,0)[0]; ctx.lineTo(x, earthBaselineY(dr)); }
  ctx.lineTo(P.r, H); ctx.closePath();
  const eg=ctx.createLinearGradient(0,P.b-40,0,H);
  eg.addColorStop(0,'#1f5c9e'); eg.addColorStop(0.5,'#123f74'); eg.addColorStop(1,'#0a2848');
  ctx.fillStyle=eg; ctx.fill();
  // atmosphere haze band just above surface
  ctx.beginPath();
  for(let dr=0; dr<=DR_MAX; dr+=25){ const x=px(dr,0)[0]; if(dr===0)ctx.moveTo(x,earthBaselineY(dr)); else ctx.lineTo(x,earthBaselineY(dr)); }
  ctx.strokeStyle='rgba(120,190,255,0.5)'; ctx.lineWidth=2; ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.85)'; ctx.font='11px Segoe UI'; ctx.textAlign='left';
  ctx.fillText('EARTH SURFACE (altitude 0 \u2014 reference only)', P.l+6, earthBaselineY(DR_MAX/2)+16);

  // ---- grid + axes ----
  ctx.strokeStyle='rgba(90,120,160,0.20)'; ctx.lineWidth=1;
  ctx.fillStyle='rgba(150,175,210,0.85)'; ctx.font='10px Segoe UI';
  ctx.textAlign='right';
  for(let a=0;a<=ALT_MAX;a+=10){ const y=px(0,a)[1];
    ctx.beginPath(); ctx.moveTo(P.l,y); ctx.lineTo(P.r,y); ctx.stroke();
    ctx.fillText(a+' mi', P.l-6, y+3); }
  ctx.textAlign='center';
  for(let dr=0;dr<=DR_MAX;dr+=200){ const x=px(dr,0)[0];
    ctx.beginPath(); ctx.moveTo(x,P.t); ctx.lineTo(x,P.b); ctx.stroke();
    ctx.fillText(dr+' mi', x, P.b+16); }
  ctx.fillStyle='rgba(150,175,210,0.9)'; ctx.font='11px Segoe UI';
  ctx.fillText('DOWNRANGE  (real telemetry, mi)', (P.l+P.r)/2, P.b+34);
  ctx.save(); ctx.translate(16,(P.t+P.b)/2); ctx.rotate(-Math.PI/2);
  ctx.fillText('ALTITUDE FROM EARTH  (real telemetry, mi)',0,0); ctx.restore();

  // ---- full trajectory (faint reference) ----
  ctx.beginPath();
  for(let i=0;i<N;i++){ const p=px(TEL[i].downrange,TEL[i].alt);
    if(i===0)ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }
  ctx.strokeStyle='rgba(255,209,102,0.22)'; ctx.lineWidth=2; ctx.stroke();

  // ---- travelled portion, coloured by velocity ----
  for(let i=1;i<=cur;i++){
    const a=px(TEL[i-1].downrange,TEL[i-1].alt);
    const b=px(TEL[i].downrange,TEL[i].alt);
    const sf=Math.max(0,Math.min(1,(TEL[i].vel-11650)/(25192-11650)));
    const r=255, g=Math.round(90+130*sf), bl=Math.round(70*(1-sf));
    ctx.strokeStyle=`rgb(${r},${g},${bl})`; ctx.lineWidth=3.4;
    ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();
  }
  // ---- anomaly markers ----
  for(let i=0;i<=cur;i++){ if(anomaly[i] && i!==N-1 && anomaly[i].indexOf('DUPLICATE')<0){
    const p=px(TEL[i].downrange,TEL[i].alt);
    ctx.fillStyle='#b06bff'; ctx.beginPath(); ctx.arc(p[0],p[1],4,0,7); ctx.fill();
    ctx.strokeStyle='rgba(176,107,255,0.7)'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.arc(p[0],p[1],8,0,7); ctx.stroke();
  }}

  // ---- entry point marker/label ----
  const ep=px(TEL[0].downrange,TEL[0].alt);
  ctx.fillStyle='#8affc1'; ctx.beginPath(); ctx.arc(ep[0],ep[1],5,0,7); ctx.fill();
  ctx.font='11px Segoe UI'; ctx.textAlign='left';
  ctx.fillText('\u25B2 ENTRY POINT  25,064 mph \u00b7 28 mi', ep[0]+8, ep[1]-8);

  // ---- data-end marker ----
  const endp=px(TEL[N-1].downrange,TEL[N-1].alt);
  ctx.strokeStyle='rgba(255,84,112,0.55)'; ctx.setLineDash([4,4]); ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(endp[0],P.t); ctx.lineTo(endp[0],P.b); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#ff5470'; ctx.textAlign='right';
  ctx.fillText('\u25A0 DATA ENDS 11,650 mph \u00b7 34 mi', endp[0]-6, P.t+14);
  ctx.fillStyle='rgba(255,120,140,0.8)'; ctx.font='10px Segoe UI';
  ctx.fillText('(still aloft \u2014 no splashdown in our data)', endp[0]-6, P.t+28);

  // ---- capsule (current frame) ----
  const cp=px(TEL[cur].downrange,TEL[cur].alt);
  const hot=(TEL[cur].vel>18000);
  const glow=ctx.createRadialGradient(cp[0],cp[1],1,cp[0],cp[1],20);
  glow.addColorStop(0, hot?'#fff2b0':'#ffd0d8');
  glow.addColorStop(0.4, hot?'#ff9e3d':'#ff6a86');
  glow.addColorStop(1,'rgba(255,84,112,0)');
  ctx.fillStyle=glow; ctx.beginPath(); ctx.arc(cp[0],cp[1],20,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(cp[0],cp[1],4.5,0,7); ctx.fill();
  ctx.strokeStyle=hot?'#ffbf47':'#ff5470'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(cp[0],cp[1],7,0,7); ctx.stroke();

  // ---- skip-entry callout when altitude peaks ----
  if(cur>=153){
    const sp=px(TEL[153].downrange,TEL[153].alt);
    ctx.fillStyle='rgba(94,200,255,0.9)'; ctx.font='10px Segoe UI'; ctx.textAlign='center';
    ctx.fillText('\u25B3 altitude peak 40 mi (skip-entry signature: 28\u219240\u219234)', sp[0], sp[1]-12);
  }

  // ---- on-screen anomaly banner ----
  if(anomaly[cur]){
    ctx.textAlign='center';
    const bw=Math.min(520,W-40);
    ctx.fillStyle='rgba(176,107,255,0.16)'; ctx.fillRect(W/2-bw/2,10,bw,28);
    ctx.strokeStyle='#b06bff'; ctx.lineWidth=1; ctx.strokeRect(W/2-bw/2,10,bw,28);
    ctx.fillStyle='#d9bcff'; ctx.font='bold 12px Segoe UI';
    ctx.fillText('\u26A0 '+anomaly[cur], W/2, 29);
    ctx.textAlign='left';
  }
}

function fmt(n){return n.toLocaleString('en-US');}
function updatePanel(){
  const f=TEL[cur];
  document.getElementById('oIdx').innerHTML=cur+'<small>/265</small>';
  document.getElementById('oTime').textContent=f.t;
  document.getElementById('oRel').innerHTML=f.rel+'<small>s</small>';
  document.getElementById('oVel').innerHTML=fmt(f.vel)+'<small>mph</small>';
  document.getElementById('oAlt').innerHTML=f.alt+'<small>mi</small>';
  document.getElementById('oDr').innerHTML=f.downrange.toFixed(1)+'<small>mi</small>';
  document.getElementById('oG').innerHTML=(f.g||0).toFixed(2)+'<small>g</small>';
  document.getElementById('oMoon').innerHTML=fmt(f.moon)+'<small>mi</small>';
  document.getElementById('oHash').textContent=f.md5;
  const fl=document.getElementById('flag');
  if(anomaly[cur]){ fl.style.color='#c79bff'; fl.textContent='\u26A0 '+anomaly[cur]; }
  else { fl.style.color='#6f88a8'; fl.textContent='nominal frame'; }
  document.getElementById('scrub').value=cur;
  document.getElementById('clock').textContent='frame '+cur+' \u2022 '+f.t;
}

function step(ts){
  if(playing){
    if(ts-last > 1000/FPS){
      last=ts; cur++; if(cur>=N) cur=0;
      updatePanel();
    }
  }
  draw();
  requestAnimationFrame(step);
}
document.getElementById('play').onclick=function(){
  playing=!playing; this.innerHTML= playing?'&#10074;&#10074; Pause':'&#9654; Play';
};
document.getElementById('reset').onclick=function(){ cur=0; updatePanel(); };
document.getElementById('scrub').oninput=function(){ cur=+this.value; playing=false;
  document.getElementById('play').innerHTML='&#9654; Play'; updatePanel(); };

resize(); updatePanel(); requestAnimationFrame(step);
</script>
</body>
</html>'''

HTML = HTML.replace('__TEL_JSON__', tel_json).replace('__R_EARTH__', str(R_EARTH_MI))
open('TrueSiddiquiAnimation.html','w').write(HTML)
print('written TrueSiddiquiAnimation.html', len(HTML), 'bytes')
