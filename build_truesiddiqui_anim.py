#!/usr/bin/env python3
"""
TrueSiddiquiAnimation.html  — v2
Globe-style NASA replica with SIDE-BY-SIDE trajectory comparison:
  CYAN  = NASA trajectory (observed from video, no data behind it)
  ORANGE/RED = Our telemetry (real numbers; geographic position is illustrative)

Truth-mode: no invented geography, no modeled splashdown, every anomaly flagged.
"""
import json

# ── Telemetry ─────────────────────────────────────────────────────────────────
TEL = json.load(open('traj_telemetry.json'))
for i, f in enumerate(TEL):
    if i > 0:
        dt = TEL[i]['sec'] - TEL[i-1]['sec']
        dv = (TEL[i-1]['vel'] - TEL[i]['vel']) * 0.44704   # mph→m/s
        f['g'] = round(max(0, (dv/dt)/9.80665), 3) if dt > 0 else 0
    else:
        f['g'] = 0
tel_json = json.dumps(TEL, separators=(',',':'))

# ── Continent outlines (approximate, simplified Pacific-visible coastlines) ───
# Format: list of [lat_deg, lon_deg] going around each polygon
# Visible in orthographic projection centred ~35°N 148°W

SHAPES = {
    # North American Pacific coast (south to north)
    "na_coast": [
        [15,-92],[18,-97],[20,-105],[22,-106],[25,-109],[28,-115],[30,-116],
        [32,-117],[34,-120],[36,-122],[38,-123],[40,-124],[42,-124],[44,-124],
        [46,-124],[48,-124],[50,-128],[52,-131],[55,-130],[57,-133],[58,-148],
        [60,-148]
    ],
    # Alaska
    "alaska": [
        [60,-148],[62,-143],[64,-141],[66,-141],[68,-141],[70,-141],[71,-155],
        [70,-160],[68,-165],[66,-168],[64,-168],[62,-168],[60,-170],[58,-170],
        [56,-168],[54,-168],[55,-163],[57,-157],[58,-153],[58,-148],[60,-148]
    ],
    # Japan (Honshu + Hokkaido rough)
    "japan": [
        [33,131],[34,132],[35,133],[34,135],[33,135],[34,135],[35,136],
        [36,137],[37,138],[38,140],[39,141],[40,141],[41,141],[43,141],
        [44,144],[43,142],[41,140],[39,140],[38,138],[36,136],[35,134],[33,131]
    ],
    # Kamchatka Peninsula
    "kamchatka": [
        [51,156],[53,158],[55,160],[57,162],[59,163],[60,163],[61,166],
        [60,166],[58,163],[55,160],[52,157],[51,156]
    ],
    # Baja California (helps ID the NASA splashdown region)
    "baja": [
        [32,-117],[30,-116],[28,-115],[27,-114],[24,-110],[22,-106],[25,-109],[28,-115],[30,-116],[32,-117]
    ]
}
shapes_json = json.dumps(SHAPES, separators=(',',':'))

# ── Geographic anchors (from visual analysis of NASA video) ───────────────────
# Entry: observed glow emerges from western North Pacific, ~northern latitudes
ENTRY_LAT,  ENTRY_LON  = 48.0, -165.0   # ~48°N 165°W  (western N.Pacific)
# NASA splashdown: observed in Pacific off western North America
SPLASH_LAT, SPLASH_LON = 29.0, -120.0   # ~29°N 120°W  (off Baja California)
# Our telemetry endpoint: 948 mi downrange from entry, still aloft at 34mi
# (no splashdown, will be computed in JS using great-circle formula)

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TrueSiddiquiAnimation — NASA vs Telemetry Comparison</title>
<style>
:root{
  --bg:#04070f;--pan:#0b1525;--edge:#1a2d48;--fg:#dce8ff;--dim:#7a96ba;
  --nasa:#00e5ff;--tel:#ff7c2a;--ano:#b06bff;--hot:#ff5470;--green:#3dffb0;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--fg);
  font-family:"Segoe UI",system-ui,sans-serif;overflow:hidden}
#root{display:flex;flex-direction:column;height:100vh}

/* ── header ── */
#hdr{background:#060d1c;border-bottom:1px solid var(--edge);padding:8px 14px;flex:none}
#hdr h1{font-size:14px;font-weight:700;letter-spacing:.3px}
#hdr h1 small{font-weight:400;color:var(--dim);font-size:11px}
#banner{background:#130a03;border-bottom:1px solid #3a1e06;color:#ffc9a0;
  font-size:11px;padding:6px 14px;line-height:1.5;flex:none}

/* ── main area ── */
#main{flex:1;display:flex;min-height:0}
#stage{flex:1;position:relative;min-width:0}
canvas{display:block;width:100%;height:100%}

/* ── comparison panel ── */
#panel{width:340px;flex:none;background:var(--pan);border-left:1px solid var(--edge);
  display:flex;flex-direction:column;overflow:hidden}
#panel-hdr{background:#060d1c;border-bottom:1px solid var(--edge);padding:8px 10px;flex:none}
#panel-hdr .cols{display:flex;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px}
#panel-hdr .cn{flex:1;color:var(--nasa)}
#panel-hdr .ct{flex:1;color:var(--tel)}
#rows{flex:1;overflow-y:auto;padding:6px 0}
.crow{display:flex;align-items:flex-start;border-bottom:1px solid #111f35;padding:5px 8px}
.crow .lbl{width:76px;flex:none;color:var(--dim);font-size:10px;text-transform:uppercase;
  letter-spacing:.5px;padding-top:2px;line-height:1.4}
.crow .cn,.crow .ct{flex:1;font-size:12px;font-variant-numeric:tabular-nums;padding:0 3px}
.crow .cn{color:var(--nasa)}
.crow .ct{color:var(--tel)}
.crow .cn.nd{color:#406a72;font-style:italic}    /* no-data in NASA col */
.crow .ct.live{font-weight:700;font-size:14px}
.crow .ct.warn{color:var(--ano)}
.crow .ct.end{color:var(--hot)}
small{font-size:10px;opacity:.7;font-weight:400}
#ano-log{background:#0a0f1f;border-top:1px solid var(--edge);padding:6px 8px;flex:none;
  font-size:10px;color:var(--ano);max-height:100px;overflow-y:auto}
#ano-log .item{line-height:1.4;margin-bottom:2px}

/* ── controls ── */
#ctrls{flex:none;display:flex;align-items:center;gap:8px;
  padding:7px 12px;border-top:1px solid var(--edge);background:#060d1c}
button{background:#111f38;color:var(--fg);border:1px solid #1f3558;
  border-radius:5px;padding:5px 10px;font-size:12px;cursor:pointer}
button:hover{background:#1a2f52}
#scrub{flex:1;accent-color:var(--tel)}
#clk{font-size:11px;color:var(--dim);min-width:130px;text-align:right}
</style>
</head>
<body>
<div id="root">
<div id="hdr"><h1>TrueSiddiquiAnimation
  <small>&nbsp;— Artemis II Re-entry: NASA animation vs our telemetry data &nbsp;|&nbsp;
  CYAN = NASA observed trajectory &nbsp;|&nbsp; ORANGE/RED = Our telemetry (position illustrative)</small>
</h1></div>
<div id="banner">
  <b>TRUTH SCOPE:</b> NASA trajectory = what their video visually depicts (no numeric data behind it).
  Our telemetry = dial readings (velocity / altitude / downrange / time) <b>read off NASA's own broadcast
  graphics</b> — so BOTH sides here are NASA-produced. This is <b>NASA-vs-NASA</b>, not independent
  verification (see ISSUES_DEEPDIVE.md §0). Our dials carry
  <b>NO latitude, longitude or heading</b>, so the geographic position of our arc is
  <b>ILLUSTRATIVE</b>, not fact.  Our data ENDS at <b>34 mi / 11,650 mph — still aloft</b>.
  We do not draw a splashdown because our dials never record one.
  NASA depicts splashdown in the <b>Pacific</b>; our earlier Atlantic assumption is retracted.
</div>

<div id="main">
  <div id="stage"><canvas id="c"></canvas></div>

  <div id="panel">
    <div id="panel-hdr">
      <div style="font-size:11px;color:var(--dim);margin-bottom:4px">Side-by-side comparison — live data vs NASA animation</div>
      <div class="cols">
        <div class="cn">&#9632; NASA animation</div>
        <div class="ct">&#9632; Our telemetry</div>
      </div>
    </div>

    <div id="rows">
      <div class="crow"><div class="lbl">Type</div>
        <div class="cn">Stylised artistic render from NASA video</div>
        <div class="ct">Raw dial captures, 265 frames</div></div>
      <div class="crow"><div class="lbl">Speed</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct live" id="rVel">--</div></div>
      <div class="crow"><div class="lbl">Altitude</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct live" id="rAlt">--</div></div>
      <div class="crow"><div class="lbl">Downrange</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct live" id="rDr">--</div></div>
      <div class="crow"><div class="lbl">Decel</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct live" id="rG">--</div></div>
      <div class="crow"><div class="lbl">Time</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct live" id="rT">--</div></div>
      <div class="crow"><div class="lbl">To Moon</div>
        <div class="cn nd">NO DATA on screen</div>
        <div class="ct" id="rMoon" style="font-size:12px">--</div></div>
      <div class="crow"><div class="lbl">Position</div>
        <div class="cn">Pacific approach W→E (from video)</div>
        <div class="ct warn" id="rPos">ILLUSTRATIVE<br><small>no lat/lon in dials</small></div></div>
      <div class="crow"><div class="lbl">Splashdown</div>
        <div class="cn">Pacific shown (~29°N 120°W)</div>
        <div class="ct end" id="rSp">NOT IN DATA<br><small>ends at 34 mi, still aloft</small></div></div>
      <div class="crow"><div class="lbl">Arc style</div>
        <div class="cn">Smooth, continuous, artist-rendered</div>
        <div class="ct warn" id="rArc">Raw — 154 unique + 111 duplicates</div></div>
      <div class="crow"><div class="lbl">Anomalies</div>
        <div class="cn">None visible</div>
        <div class="ct warn" id="rAno">2 reversals · 110s gap · noise</div></div>
      <div class="crow"><div class="lbl">Frame MD5</div>
        <div class="cn nd">—</div>
        <div class="ct" id="rHash" style="font-family:monospace;font-size:11px;color:#8fb0d0">--------</div></div>
    </div>

    <div id="ano-log"><b style="color:#fff">Anomaly log</b></div>
  </div>
</div>

<div id="ctrls">
  <button id="play">&#10074;&#10074; Pause</button>
  <button id="reset">&#8635;</button>
  <input type="range" id="scrub" min="0" max="264" value="0" step="1">
  <span id="clk">frame 0 · 1:28:19</span>
</div>
</div><!-- root -->

<script>
"use strict";
// ─── data ──────────────────────────────────────────────────────────────────
const TEL    = __TEL__;
const SHAPES = __SHAPES__;
const N      = TEL.length;

// Geographic anchors (from visual analysis of NASA video — honest estimates)
const ENTRY_LAT   = __ELAT__,  ENTRY_LON  = __ELON__;   // deg
const SPLASH_LAT  = __SLAT__,  SPLASH_LON = __SLON__;   // deg
const R_EARTH_MI  = 3959.0;

// ─── anomaly classification ─────────────────────────────────────────────────
const anomaly = new Array(N).fill(null);
const anoLog  = [];
for (let i = 1; i < N; i++) {
  if (TEL[i].sec < TEL[i-1].sec) {
    anomaly[i] = {type:'REVERSAL', msg:`TIME REVERSAL frame ${i}: clock jumps back ${TEL[i-1].sec-TEL[i].sec}s — replay artifact`};
    anoLog.push(anomaly[i].msg);
  } else if (TEL[i].sec - TEL[i-1].sec > 5) {
    anomaly[i] = {type:'GAP', msg:`BLACKOUT GAP at frame ${i}: +${TEL[i].sec-TEL[i-1].sec}s missing`};
    anoLog.push(anomaly[i].msg);
  } else if (TEL[i].md5 === TEL[i-1].md5) {
    anomaly[i] = {type:'DUP', msg:`DUP frame ${i}`};
  }
}
anomaly[N-1] = {type:'END', msg:`DATA ENDS frame ${N-1}: ${TEL[N-1].alt} mi / ${TEL[N-1].vel.toLocaleString()} mph — still aloft`};
anoLog.push(anomaly[N-1].msg);

// ─── math helpers ──────────────────────────────────────────────────────────
const D2R = Math.PI/180, R2D = 180/Math.PI;

// Great-circle destination: from (lat1,lon1) in degrees, bearing deg, distance miles → [lat,lon] deg
function gc_dest(lat1, lon1, bearing, dist_mi) {
  const d = dist_mi / R_EARTH_MI;   // angular distance in radians
  const φ1 = lat1*D2R, λ1 = lon1*D2R, β = bearing*D2R;
  const φ2 = Math.asin(Math.sin(φ1)*Math.cos(d) + Math.cos(φ1)*Math.sin(d)*Math.cos(β));
  const λ2 = λ1 + Math.atan2(Math.sin(β)*Math.sin(d)*Math.cos(φ1),
                               Math.cos(d) - Math.sin(φ1)*Math.sin(φ2));
  return [φ2*R2D, λ2*R2D];
}

// Great-circle initial bearing from (lat1,lon1) to (lat2,lon2) — degrees
function gc_bearing(lat1, lon1, lat2, lon2) {
  const φ1=lat1*D2R, λ1=lon1*D2R, φ2=lat2*D2R, λ2=lon2*D2R;
  const dλ=λ2-λ1;
  return (Math.atan2(Math.sin(dλ)*Math.cos(φ2),
          Math.cos(φ1)*Math.sin(φ2)-Math.sin(φ1)*Math.cos(φ2)*Math.cos(dλ))*R2D+360)%360;
}

// Slerp two [lat,lon] points at fraction t → [lat,lon]
function gc_lerp(lat1,lon1,lat2,lon2,t){
  const v1=[Math.cos(lat1*D2R)*Math.cos(lon1*D2R),
            Math.cos(lat1*D2R)*Math.sin(lon1*D2R), Math.sin(lat1*D2R)];
  const v2=[Math.cos(lat2*D2R)*Math.cos(lon2*D2R),
            Math.cos(lat2*D2R)*Math.sin(lon2*D2R), Math.sin(lat2*D2R)];
  const dot=Math.min(1,Math.max(-1,v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]));
  const omega=Math.acos(dot);
  if(omega<1e-9) return [lat1,lon1];
  const s=Math.sin(omega);
  const a=Math.sin((1-t)*omega)/s, b=Math.sin(t*omega)/s;
  const vx=a*v1[0]+b*v2[0], vy=a*v1[1]+b*v2[1], vz=a*v1[2]+b*v2[2];
  return [Math.asin(vz)*R2D, Math.atan2(vy,vx)*R2D];
}

// Pre-compute NASA smooth arc (50 points)
const NASA_ARC = [];
for(let i=0;i<=200;i++){
  const p=gc_lerp(ENTRY_LAT,ENTRY_LON,SPLASH_LAT,SPLASH_LON,i/200);
  NASA_ARC.push(p);
}

// Pre-compute telemetry positions along great circle from entry, bearing toward splash
const TEL_BEARING = gc_bearing(ENTRY_LAT,ENTRY_LON,SPLASH_LAT,SPLASH_LON);
const TEL_POS = TEL.map(f => gc_dest(ENTRY_LAT,ENTRY_LON,TEL_BEARING,f.downrange));
// Endpoint of our data (for reference)
const TEL_END = TEL_POS[N-1];

// ─── orthographic projection ────────────────────────────────────────────────
// Globe centre: Pacific focus
const GLAT0 = 36*D2R, GLON0 = -148*D2R;

let globeR = 1;   // set in resize

function ortho(lat_deg, lon_deg) {
  const φ=lat_deg*D2R, λ=lon_deg*D2R;
  const visible = Math.sin(GLAT0)*Math.sin(φ) + Math.cos(GLAT0)*Math.cos(φ)*Math.cos(λ-GLON0);
  if (visible < 0) return null;           // behind globe
  const x =  globeR * Math.cos(φ)*Math.sin(λ-GLON0);
  const y = -globeR * (Math.cos(GLAT0)*Math.sin(φ) - Math.sin(GLAT0)*Math.cos(φ)*Math.cos(λ-GLON0));
  return [x, y];   // canvas coords relative to globe centre
}

// ─── canvas setup ──────────────────────────────────────────────────────────
const cv = document.getElementById('c');
const ctx = cv.getContext('2d');
let W=0,H=0,DPR=1,CX=0,CY=0;

function resize(){
  DPR=Math.min(2,window.devicePixelRatio||1);
  const r=cv.parentNode.getBoundingClientRect();
  W=r.width; H=r.height;
  cv.width=W*DPR; cv.height=H*DPR;
  ctx.setTransform(DPR,0,0,DPR,0,0);
  CX=W/2; CY=H/2;
  globeR=Math.min(W,H)*0.44;
}
window.addEventListener('resize',()=>{resize();draw();});

// ─── starfield ─────────────────────────────────────────────────────────────
const stars=[];
for(let i=0;i<280;i++)
  stars.push({x:Math.random(),y:Math.random(),r:Math.random()*1.4+0.3,a:Math.random()*0.6+0.4});

// ─── draw helpers ──────────────────────────────────────────────────────────
function project([lat,lon]){
  const p=ortho(lat,lon); if(!p) return null;
  return [CX+p[0], CY+p[1]];
}

function drawArc(pts, strokeFn, lw){
  // pts = [[lat,lon],...]; strokeFn called per segment for colour (receives index)
  let prev=null;
  for(let i=0;i<pts.length;i++){
    const sc=project(pts[i]);
    if(sc && prev){
      ctx.beginPath(); ctx.moveTo(prev[0],prev[1]); ctx.lineTo(sc[0],sc[1]);
      ctx.strokeStyle=strokeFn(i); ctx.lineWidth=lw; ctx.stroke();
    }
    prev=sc||null;
  }
}

function drawPoly(coords, fill, stroke, lw=0.8){
  ctx.beginPath();
  let first=true;
  for(const [lt,ln] of coords){
    const p=ortho(lt,ln); if(!p) continue;
    const sx=CX+p[0], sy=CY+p[1];
    if(first){ctx.moveTo(sx,sy);first=false;} else ctx.lineTo(sx,sy);
  }
  ctx.closePath();
  if(fill){ctx.fillStyle=fill;ctx.fill();}
  if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=lw;ctx.stroke();}
}

function dot(lat,lon,r,col,label,above){
  const p=ortho(lat,lon); if(!p) return;
  const sx=CX+p[0], sy=CY+p[1];
  ctx.fillStyle=col; ctx.beginPath(); ctx.arc(sx,sy,r,0,7); ctx.fill();
  if(label){
    ctx.font='11px Segoe UI'; ctx.fillStyle=col;
    ctx.textAlign='center';
    ctx.fillText(label, sx, sy+(above?-r-5:r+13));
  }
}

function glowDot(lat,lon,r,colOuter,colInner){
  const p=ortho(lat,lon); if(!p) return null;
  const sx=CX+p[0], sy=CY+p[1];
  const grd=ctx.createRadialGradient(sx,sy,1,sx,sy,r*4);
  grd.addColorStop(0,colInner); grd.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=grd; ctx.beginPath(); ctx.arc(sx,sy,r*4,0,7); ctx.fill();
  ctx.fillStyle=colInner; ctx.beginPath(); ctx.arc(sx,sy,r,0,7); ctx.fill();
  ctx.strokeStyle=colOuter; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(sx,sy,r+3,0,7); ctx.stroke();
  return [sx,sy];
}

// ─── draw globe shell ──────────────────────────────────────────────────────
function drawGlobe(){
  // ocean
  const grd=ctx.createRadialGradient(CX-globeR*0.2,CY-globeR*0.25,globeR*0.05,CX,CY,globeR);
  grd.addColorStop(0,'#1e5c9e'); grd.addColorStop(0.6,'#0e3a6a'); grd.addColorStop(1,'#070f22');
  ctx.fillStyle=grd; ctx.beginPath(); ctx.arc(CX,CY,globeR,0,7); ctx.fill();
  // atmosphere rim
  const atm=ctx.createRadialGradient(CX,CY,globeR*0.92,CX,CY,globeR*1.08);
  atm.addColorStop(0,'rgba(100,180,255,0.0)');
  atm.addColorStop(0.5,'rgba(100,180,255,0.25)');
  atm.addColorStop(1,'rgba(100,180,255,0.0)');
  ctx.fillStyle=atm; ctx.beginPath(); ctx.arc(CX,CY,globeR*1.08,0,7); ctx.fill();
  // clip subsequent drawing to globe
}

function drawLand(){
  ctx.save();
  ctx.beginPath(); ctx.arc(CX,CY,globeR,0,7); ctx.clip();
  const LAND='#2a5e38', COAST='#3a8050';
  drawPoly(SHAPES.alaska,    LAND, COAST);
  drawPoly(SHAPES.na_coast,  LAND, COAST);
  drawPoly(SHAPES.japan,     '#2a5038', '#3a7048');
  drawPoly(SHAPES.kamchatka, '#2a5038', '#3a7048');
  drawPoly(SHAPES.baja,      LAND, COAST, 0.5);
  ctx.restore();
}

function drawGrid(){
  ctx.save();
  ctx.beginPath(); ctx.arc(CX,CY,globeR,0,7); ctx.clip();
  ctx.strokeStyle='rgba(100,140,180,0.12)'; ctx.lineWidth=0.8;
  // lat lines 10° steps
  for(let lt=-80;lt<=80;lt+=20){
    ctx.beginPath(); let first=true;
    for(let ln=-180;ln<=180;ln+=3){
      const p=ortho(lt,ln); if(!p){first=true;continue;}
      const sx=CX+p[0],sy=CY+p[1];
      if(first){ctx.moveTo(sx,sy);first=false;} else ctx.lineTo(sx,sy);
    }
    ctx.stroke();
  }
  // lon lines 20° steps
  for(let ln=-180;ln<180;ln+=20){
    ctx.beginPath(); let first=true;
    for(let lt=-85;lt<=85;lt+=2){
      const p=ortho(lt,ln); if(!p){first=true;continue;}
      const sx=CX+p[0],sy=CY+p[1];
      if(first){ctx.moveTo(sx,sy);first=false;} else ctx.lineTo(sx,sy);
    }
    ctx.stroke();
  }
  ctx.restore();
}

// ─── velocity colour for our telemetry arc ─────────────────────────────────
function velColor(vel, alpha=1){
  const sf=Math.max(0,Math.min(1,(vel-11650)/(25192-11650)));
  const r=255, g=Math.round(70+140*sf), b=Math.round(20*(1-sf));
  return `rgba(${r},${g},${b},${alpha})`;
}

// ─── main draw ─────────────────────────────────────────────────────────────
let cur=0, playing=true, last=0;
const FPS=20;

function draw(){
  ctx.clearRect(0,0,W,H);

  // ---- starfield (full canvas, outside globe) ----
  for(const s of stars){
    ctx.globalAlpha=s.a;
    ctx.fillStyle='#c8d8f8';
    ctx.beginPath(); ctx.arc(s.x*W, s.y*H, s.r, 0,7); ctx.fill();
  }
  ctx.globalAlpha=1;

  // ---- globe shell ----
  drawGlobe();
  ctx.save(); ctx.beginPath(); ctx.arc(CX,CY,globeR,0,7); ctx.clip();
  drawGrid();
  drawLand();

  // ── NASA trajectory (CYAN): full arc, drawing progressively ────────────
  // NASA arc has 200 pts; we spread them over all 265 TEL frames
  const nasaFrac = cur/(N-1);   // 0→1
  const nasaEnd  = Math.round(nasaFrac*200);
  ctx.lineWidth=2.5; ctx.strokeStyle='rgba(0,229,255,0.35)';
  {  // faint full reference
    ctx.beginPath(); let first=true;
    for(const pt of NASA_ARC){
      const sc=project(pt); if(!sc){first=true;continue;}
      if(first){ctx.moveTo(sc[0],sc[1]);first=false;} else ctx.lineTo(sc[0],sc[1]);
    }
    ctx.stroke();
  }
  {  // bright travelled portion
    ctx.lineWidth=3; let prev=null;
    for(let i=0;i<=nasaEnd;i++){
      const sc=project(NASA_ARC[i]); if(!sc){prev=null;continue;}
      if(prev){
        ctx.beginPath(); ctx.moveTo(prev[0],prev[1]); ctx.lineTo(sc[0],sc[1]);
        ctx.strokeStyle=`rgba(0,229,255,${0.5+0.5*(i/nasaEnd)})`;
        ctx.stroke();
      }
      prev=sc;
    }
  }

  // ── Our telemetry arc (ORANGE→RED): real downrange-based positions ─────
  {  // faint full trail
    ctx.lineWidth=1.5; let prev=null;
    for(let i=0;i<N;i++){
      const sc=project(TEL_POS[i]); if(!sc){prev=null;continue;}
      if(prev){
        ctx.beginPath(); ctx.moveTo(prev[0],prev[1]); ctx.lineTo(sc[0],sc[1]);
        ctx.strokeStyle=velColor(TEL[i].vel,0.2); ctx.stroke();
      }
      prev=sc;
    }
  }
  {  // bright travelled portion
    ctx.lineWidth=3.5; let prev=null;
    for(let i=0;i<=cur;i++){
      const sc=project(TEL_POS[i]); if(!sc){prev=null;continue;}
      if(prev){
        ctx.beginPath(); ctx.moveTo(prev[0],prev[1]); ctx.lineTo(sc[0],sc[1]);
        ctx.strokeStyle=velColor(TEL[i].vel,0.9); ctx.stroke();
      }
      prev=sc;
    }
  }

  // ── Anomaly markers along our arc ──────────────────────────────────────
  for(let i=0;i<=cur;i++){
    if(!anomaly[i]||anomaly[i].type==='DUP') continue;
    const col = anomaly[i].type==='END'?'#ff5470':'#b06bff';
    const sc=project(TEL_POS[i]); if(!sc) continue;
    ctx.beginPath(); ctx.arc(sc[0],sc[1],5,0,7); ctx.fillStyle=col; ctx.fill();
    ctx.strokeStyle=col+'99'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.arc(sc[0],sc[1],10,0,7); ctx.stroke();
  }
  ctx.restore();  // end globe clip

  // ── Markers (outside clip so labels don't get cropped) ─────────────────
  // Entry point marker (shared by both arcs)
  dot(ENTRY_LAT, ENTRY_LON, 6, '#8affc1', '▲ ENTRY POINT\n25,064 mph · 28 mi', true);

  // NASA splashdown marker (cyan)
  const nsplash=project([SPLASH_LAT,SPLASH_LON]);
  if(nsplash){
    ctx.fillStyle='#00e5ff'; ctx.beginPath(); ctx.arc(nsplash[0],nsplash[1],5,0,7); ctx.fill();
    ctx.font='10px Segoe UI'; ctx.fillStyle='#00e5ff'; ctx.textAlign='center';
    ctx.fillText('NASA splashdown', nsplash[0], nsplash[1]+18);
    ctx.fillText('(from video ~29°N 120°W)', nsplash[0], nsplash[1]+30);
  }

  // Our data-end marker
  const tendsc=project(TEL_END);
  if(tendsc && cur>=N-1){
    ctx.fillStyle='#ff5470'; ctx.beginPath(); ctx.arc(tendsc[0],tendsc[1],5,0,7); ctx.fill();
    ctx.font='10px Segoe UI'; ctx.fillStyle='#ff5470'; ctx.textAlign='center';
    ctx.fillText('■ DATA ENDS', tendsc[0], tendsc[1]-14);
    ctx.fillText('34 mi · 11,650 mph · still aloft', tendsc[0], tendsc[1]-24);
  }

  // Capsule glow (our telemetry)
  {
    const hot=TEL[cur].vel>18000;
    glowDot(TEL_POS[cur][0],TEL_POS[cur][1], 6,
      hot?'#ffbf47':'#ff5470', hot?'#fff8c0':'#ffb070');
  }

  // ── On-screen anomaly banner ─────────────────────────────────────────────
  if(anomaly[cur] && anomaly[cur].type!=='DUP'){
    const colMap={REVERSAL:'#b06bff',GAP:'#b06bff',END:'#ff5470'};
    const col=colMap[anomaly[cur].type]||'#b06bff';
    const bw=Math.min(480,W-40);
    ctx.fillStyle=col+'22'; ctx.fillRect(W/2-bw/2,8,bw,28);
    ctx.strokeStyle=col; ctx.lineWidth=1; ctx.strokeRect(W/2-bw/2,8,bw,28);
    ctx.fillStyle=col; ctx.font='bold 12px Segoe UI'; ctx.textAlign='center';
    ctx.fillText('⚠ '+anomaly[cur].msg, W/2, 27);
    ctx.textAlign='left';
  }

  // ── Legend (bottom left) ─────────────────────────────────────────────────
  const lx=14, ly=H-70;
  ctx.font='11px Segoe UI'; ctx.textAlign='left';
  ctx.strokeStyle='#00e5ff'; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(lx,ly); ctx.lineTo(lx+28,ly); ctx.stroke();
  ctx.fillStyle='#00e5ff'; ctx.fillText('NASA trajectory (from video, no data)',lx+34,ly+4);
  ctx.strokeStyle='#ff7c2a'; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(lx,ly+18); ctx.lineTo(lx+28,ly+18); ctx.stroke();
  ctx.fillStyle='#ff7c2a'; ctx.fillText('Our telemetry (position ILLUSTRATIVE — no lat/lon in dials)',lx+34,ly+22);
  ctx.fillStyle='#b06bff';
  ctx.fillText('● Anomaly marker (reversal / gap / data-end)',lx+34,ly+40);
}

// ─── panel update ──────────────────────────────────────────────────────────
const anoLogEl=document.getElementById('ano-log');
let loggedAnoms=new Set();
function fmt(n){return Number(n).toLocaleString('en-US');}
function updatePanel(){
  const f=TEL[cur];
  document.getElementById('rVel').innerHTML   = fmt(f.vel)+'<small> mph</small>';
  document.getElementById('rAlt').innerHTML   = f.alt+'<small> mi</small>';
  document.getElementById('rDr').innerHTML    = f.downrange.toFixed(1)+'<small> mi</small>';
  document.getElementById('rG').innerHTML     = (f.g||0).toFixed(2)+'<small> g</small>';
  document.getElementById('rT').textContent   = f.t+' ('+f.rel+'s)';
  document.getElementById('rMoon').innerHTML  = fmt(f.moon)+'<small> mi</small>';
  document.getElementById('rHash').textContent= f.md5;
  // anomaly arc style
  const aEl=document.getElementById('rArc');
  if(anomaly[cur] && anomaly[cur].type==='DUP')
    aEl.innerHTML='<span style="color:#b06bff">⚠ DUPLICATE FRAME</span>';
  else if(anomaly[cur] && anomaly[cur].type==='REVERSAL')
    aEl.innerHTML='<span style="color:#b06bff">⚠ TIME REVERSAL — replay</span>';
  else if(anomaly[cur] && anomaly[cur].type==='GAP')
    aEl.innerHTML='<span style="color:#b06bff">⚠ BLACKOUT GAP +110s</span>';
  else if(anomaly[cur] && anomaly[cur].type==='END')
    aEl.innerHTML='<span style="color:#ff5470">■ DATA ENDS HERE</span>';
  else
    aEl.innerHTML='154 unique + 111 duplicates';
  // splashdown row
  const sEl=document.getElementById('rSp');
  if(cur>=N-1)
    sEl.innerHTML='<span style="color:#ff5470">■ DATA ENDS 34mi — NOT RECORDED</span>';
  // anomaly log
  if(anomaly[cur] && !loggedAnoms.has(cur)){
    loggedAnoms.add(cur);
    const d=document.createElement('div'); d.className='item';
    const colMap={REVERSAL:'#b06bff',GAP:'#b06bff',END:'#ff5470',DUP:'#5a6070'};
    d.style.color=colMap[anomaly[cur].type]||'#b06bff';
    d.textContent='['+f.t+'] '+anomaly[cur].msg;
    anoLogEl.appendChild(d);
    anoLogEl.scrollTop=anoLogEl.scrollHeight;
  }
  document.getElementById('scrub').value=cur;
  document.getElementById('clk').textContent='frame '+cur+' · '+f.t;
}

// ─── animation loop ─────────────────────────────────────────────────────────
function step(ts){
  if(playing){
    if(ts-last>1000/FPS){ last=ts; cur=(cur+1)%N; updatePanel(); }
  }
  draw();
  requestAnimationFrame(step);
}
document.getElementById('play').onclick=function(){
  playing=!playing; this.innerHTML=playing?'&#10074;&#10074; Pause':'&#9654; Play';
};
document.getElementById('reset').onclick=function(){ cur=0; loggedAnoms.clear();
  anoLogEl.innerHTML='<b style="color:#fff">Anomaly log</b>';
  document.getElementById('rSp').innerHTML='NOT IN DATA<br><small>ends at 34 mi, still aloft</small>';
  document.getElementById('rArc').innerHTML='Raw \u2014 154 unique + 111 duplicates';
  updatePanel(); playing=true; document.getElementById('play').innerHTML='&#10074;&#10074; Pause';
};
document.getElementById('scrub').oninput=function(){
  cur=+this.value; playing=false;
  document.getElementById('play').innerHTML='&#9654; Play'; updatePanel();
};
resize(); updatePanel(); requestAnimationFrame(step);
</script>
</body>
</html>'''

HTML = (HTML
  .replace('__TEL__',    tel_json)
  .replace('__SHAPES__', shapes_json)
  .replace('__ELAT__', str(ENTRY_LAT))
  .replace('__ELON__', str(ENTRY_LON))
  .replace('__SLAT__', str(SPLASH_LAT))
  .replace('__SLON__', str(SPLASH_LON))
)

with open('TrueSiddiquiAnimation.html','w') as fh:
    fh.write(HTML)
print(f'Written {len(HTML):,} bytes -> TrueSiddiquiAnimation.html')
