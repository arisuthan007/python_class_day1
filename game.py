
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SHADOW RUN | Offline Survival</title>

<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--cyan:#4cecff;--pink:#ff397e;--bg:#050712}
body{
  background:var(--bg);color:white;
  font-family:Segoe UI,Arial,sans-serif;
  min-height:100vh;overflow:hidden;
}
#game{position:relative;width:100%;height:100vh;overflow:hidden;
  background:radial-gradient(ellipse at 50% 75%,#14264a 0%,#090c1b 42%,#03040a 100%)}
canvas{position:absolute;inset:0;width:100%;height:100%}
.scanlines{position:absolute;inset:0;pointer-events:none;z-index:2;
 background:repeating-linear-gradient(0deg,transparent 0px,
 rgba(255,255,255,.018) 1px,transparent 3px)}
.vignette{position:absolute;inset:0;pointer-events:none;z-index:2;
 background:radial-gradient(ellipse,transparent 40%,rgba(0,0,0,.72) 100%)}
.topbar{position:absolute;z-index:5;top:25px;left:5%;right:5%;
 display:flex;justify-content:space-between;align-items:center;gap:15px}
.brand{font-size:13px;letter-spacing:5px;color:var(--cyan);font-weight:800}
.brand span{color:white}
.status{font-size:10px;letter-spacing:2px;color:#a2b7d4}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;
 background:#40ffb0;box-shadow:0 0 12px #40ffb0;margin-right:7px}
.hud{position:absolute;top:90px;left:5%;z-index:4;display:flex;gap:30px}
.stat label{font-size:9px;letter-spacing:3px;color:#91a6c9;display:block}
.stat strong{display:block;font-size:25px;letter-spacing:2px;margin-top:5px}
.stat strong em{font-size:11px;color:var(--cyan);font-style:normal}
#energy{position:absolute;top:95px;right:5%;width:125px;z-index:4}
#energy label{font-size:9px;letter-spacing:2px;color:#91a6c9}
.track{height:4px;background:#1b2740;margin-top:10px}
#energyBar{height:100%;width:100%;background:var(--cyan);
 box-shadow:0 0 12px var(--cyan);transition:width .15s}
.center{position:absolute;z-index:6;left:50%;top:47%;transform:translate(-50%,-50%);
 text-align:center;width:min(90%,650px)}
.eyebrow{font-size:10px;letter-spacing:6px;color:var(--cyan);margin-bottom:20px}
h1{font-size:clamp(48px,10vw,105px);font-weight:900;line-height:.9;
 letter-spacing:-4px;text-shadow:0 0 35px #3152a9}
h1 span{color:var(--cyan)}
.subtitle{font-size:11px;letter-spacing:4px;color:#9aabc6;margin-top:24px}
.description{font-size:13px;color:#94a4bf;line-height:1.8;margin:17px auto 28px}
button{cursor:pointer;color:white;background:rgba(15,27,50,.85);
 border:1px solid #39516f;padding:14px 24px;font-size:10px;
 letter-spacing:3px;font-weight:bold;transition:.2s}
button:hover{border-color:var(--cyan);box-shadow:0 0 22px #29caff35}
.primary{background:var(--cyan);color:#03101b;border:1px solid var(--cyan);
 min-width:190px}
.primary:hover{background:white;color:#03101b}
.actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.hidden{display:none!important}
#message{font-size:11px;letter-spacing:3px;color:var(--pink);margin-top:20px}
.controls{position:absolute;bottom:25px;left:5%;right:5%;z-index:5;
 display:flex;justify-content:space-between;align-items:end;color:#8293b1}
.hint{font-size:10px;letter-spacing:2px;line-height:2}
.key{border:1px solid #3c4c6a;padding:5px 8px;color:var(--cyan);margin-right:5px}
#jumpBtn{display:none;min-width:95px}
#pauseBtn{padding:10px 13px}
footer{position:absolute;bottom:6px;left:0;right:0;text-align:center;
 font-size:8px;letter-spacing:3px;color:#34435c;z-index:5}
@media(max-width:600px){
 .topbar{top:18px}.brand{letter-spacing:3px}
 .hud{top:75px;gap:18px}.stat strong{font-size:20px}
 #energy{top:80px;width:90px}.center{top:45%}
 .controls{bottom:32px}.hint{font-size:8px;letter-spacing:1px}
 #jumpBtn{display:block}.subtitle{letter-spacing:2px}
}
</style>
</head>
<body>
<div id="game">
 <canvas id="scene"></canvas>
 <div class="scanlines"></div><div class="vignette"></div>

 <div class="topbar">
  <div class="brand">NEXUS <span>/ SHADOW RUN</span></div>
  <div class="status"><i class="dot"></i>LOCAL SYSTEM // OFFLINE</div>
 </div>

 <div class="hud">
  <div class="stat"><label>DISTANCE</label><strong><span id="score">0000</span><em> M</em></strong></div>
  <div class="stat"><label>ENERGY CORES</label><strong id="cores">00</strong></div>
 </div>

 <div id="energy"><label>SUIT ENERGY</label><div class="track"><div id="energyBar"></div></div></div>

 <div class="center" id="intro">
  <div class="eyebrow">YEAR 2099 // SECTOR 07</div>
  <h1>SHADOW<br><span>RUN.</span></h1>
  <div class="subtitle">THE CITY HAS GONE DARK.</div>
  <p class="description">
   The grid has collapsed. The city is hunting you.<br>
   Run through the ruins. Collect energy. Survive the night.
  </p>
  <div class="actions">
   <button class="primary" id="startBtn">INITIALISE RUN ↗</button>
   <button id="howBtn">HOW TO PLAY</button>
  </div>
  <p id="message"></p>
 </div>

 <div class="center hidden" id="gameover">
  <div class="eyebrow">SIGNAL LOST // MISSION FAILED</div>
  <h1>GAME<br><span>OVER.</span></h1>
  <p class="description">The city claimed another runner.</p>
  <div class="stat" style="margin-bottom:25px">
   <label>FINAL DISTANCE</label><strong id="finalScore">0000 M</strong>
  </div>
  <div class="actions">
   <button class="primary" id="retryBtn">RETRY MISSION ↗</button>
   <button id="homeBtn">MAIN MENU</button>
  </div>
 </div>

 <div class="center hidden" id="paused">
  <div class="eyebrow">SYSTEM SUSPENDED</div><h1>PAUSE<span>.</span></h1>
  <p class="description">Take a breath. The city is still waiting.</p>
  <button class="primary" id="resumeBtn">RESUME MISSION</button>
 </div>

 <div class="controls">
  <div class="hint">
   <span class="key">SPACE</span><span class="key">↑</span> JUMP<br>
   <span style="color:#435779">AVOID THE RED // COLLECT THE CYAN</span>
  </div>
  <div style="display:flex;gap:8px">
   <button id="jumpBtn">JUMP ↑</button>
   <button id="pauseBtn" class="hidden">Ⅱ PAUSE</button>
  </div>
 </div>
 <footer>SHADOW RUN © 2099 &nbsp; • &nbsp; SURVIVE THE DARK</footer>
</div>

<script>
const canvas = document.getElementById('scene');
const ctx = canvas.getContext('2d');
const $ = id => document.getElementById(id);

let W,H,ground,stars=[],buildings=[],obstacles=[],orbs=[],particles=[];
let running=false,paused=false,over=false,started=false;
let score=0,cores=0,speed=5,energy=100,spawn=0,orbSpawn=0;
let last=0,elapsed=0,highScore=Number(localStorage.getItem('shadowHigh')||0);
let player={x:100,y:0,w:28,h:48,vy:0,jumping:false};
const rand=(a,b)=>Math.random()*(b-a)+a;

function resize(){
 W=canvas.width=innerWidth*devicePixelRatio;
 H=canvas.height=innerHeight*devicePixelRatio;
 ctx.setTransform(1,0,0,1,0,0);
 ctx.scale(devicePixelRatio,devicePixelRatio);
 W=innerWidth;H=innerHeight;ground=H*.79;
 player.x=Math.max(55,W*.13);
 makeWorld();
}
function makeWorld(){
 stars=Array.from({length:100},()=>({x:rand(0,W),y:rand(0,ground*.8),r:rand(.5,1.8),a:rand(.2,.9)}));
 buildings=[];let x=0;
 while(x<W+100){
  let w=rand(35,90),h=rand(50,ground*.55);
  buildings.push({x,w,h,seed:Math.random()});x+=w+rand(4,13);
 }
}
addEventListener('resize',resize);
resize();

function text(str,x,y,size,color,align='left'){
 ctx.font=`${size}px Segoe UI, Arial`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(str,x,y);
}
function drawWorld(dt){
 let sky=ctx.createLinearGradient(0,0,0,H);
 sky.addColorStop(0,'#03050e');sky.addColorStop(.7,'#101b37');sky.addColorStop(1,'#080c18');
 ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

 // distant moon
 let moon=ctx.createRadialGradient(W*.78,H*.24,2,W*.78,H*.24,100);
 moon.addColorStop(0,'#b7f8ff');moon.addColorStop(.15,'#628dca66');
 moon.addColorStop(1,'#18254800');
 ctx.fillStyle=moon;ctx.fillRect(W*.78-110,H*.24-110,220,220);
 ctx.beginPath();ctx.arc(W*.78,H*.24,20,0,Math.PI*2);
 ctx.fillStyle='#b8d9ee';ctx.globalAlpha=.65;ctx.fill();ctx.globalAlpha=1;

 stars.forEach(s=>{
  ctx.globalAlpha=s.a*(.7+.3*Math.sin(elapsed*2+s.x));
  ctx.fillStyle='#c8f7ff';ctx.fillRect(s.x,s.y,s.r,s.r);
 });
 ctx.globalAlpha=1;

 // city skyline
 buildings.forEach(b=>{
  ctx.fillStyle='#080d1c';ctx.fillRect(b.x,ground-b.h,b.w,b.h);
  ctx.strokeStyle='#22365a';ctx.lineWidth=1;
  ctx.strokeRect(b.x,ground-b.h,b.w,b.h);
  for(let yy=ground-b.h+10;yy<ground-8;yy+=13){
   for(let xx=b.x+7;xx<b.x+b.w-4;xx+=12){
    if(Math.sin(xx*13+yy*7+b.seed*20)>.35){
     ctx.fillStyle=Math.sin(xx+yy)>.2?'#32cce9':'#ff397e';
     ctx.globalAlpha=.2+Math.abs(Math.sin(xx*yy))*.4;
     ctx.fillRect(xx,yy,3,4);
    }
   }
  }
 });
 ctx.globalAlpha=1;

 // distant horizon and ground
 ctx.fillStyle='#080d1b';ctx.fillRect(0,ground,W,H-ground);
 ctx.strokeStyle='#34c8f5';ctx.globalAlpha=.7;
 ctx.beginPath();ctx.moveTo(0,ground);ctx.lineTo(W,ground);ctx.stroke();
 ctx.globalAlpha=1;
 ctx.strokeStyle='#17314d';ctx.lineWidth=1;
 let shift=(elapsed*speed*18)%75;
 for(let x=-shift;x<W;x+=75){
  ctx.beginPath();ctx.moveTo(x,ground);ctx.lineTo(x-45,H);ctx.stroke();
 }
 for(let y=ground+20;y<H;y+=Math.max(12,(y-ground)*.22)){
  ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
 }
 ctx.fillStyle='#37dfff';ctx.globalAlpha=.18;
 ctx.fillRect(0,ground,W,2);ctx.globalAlpha=1;
}

function drawPlayer(){
 const x=player.x,y=player.y-player.h;
 ctx.save();
 ctx.shadowBlur=20;ctx.shadowColor='#36dcff';
 // shadow on ground
 ctx.globalAlpha=Math.max(.15,1-Math.abs(player.y-ground)/160);
 ctx.fillStyle='#37dfff';ctx.beginPath();
 ctx.ellipse(x+player.w/2,ground,player.w,4,0,0,Math.PI*2);ctx.fill();
 ctx.globalAlpha=1;
 // glowing running silhouette
 ctx.strokeStyle='#5beaff';ctx.fillStyle='#0d2540';ctx.lineWidth=2.5;
 ctx.beginPath();ctx.arc(x+15,y+8,7,0,Math.PI*2);ctx.fill();ctx.stroke();
 ctx.fillStyle='#dffcff';ctx.fillRect(x+17,y+5,7,2);
 ctx.beginPath();ctx.moveTo(x+13,y+16);ctx.lineTo(x+7,y+34);
 ctx.lineTo(x+20,y+36);ctx.lineTo(x+22,y+17);ctx.closePath();ctx.fill();ctx.stroke();
 let swing=running&&!paused?Math.sin(elapsed*16)*8:0;
 ctx.beginPath();ctx.moveTo(x+12,y+20);ctx.lineTo(x+2,y+29+swing);ctx.stroke();
 ctx.beginPath();ctx.moveTo(x+19,y+20);ctx.lineTo(x+29,y+27-swing);ctx.stroke();
 ctx.beginPath();ctx.moveTo(x+10,y+34);ctx.lineTo(x+7+swing,y+47);ctx.stroke();
 ctx.beginPath();ctx.moveTo(x+18,y+34);ctx.lineTo(x+22-swing,y+47);ctx.stroke();
 ctx.restore();
}

function drawObstacle(o){
 ctx.save();ctx.shadowBlur=17;ctx.shadowColor='#ff397e';
 ctx.fillStyle='#291126';ctx.strokeStyle='#ff397e';ctx.lineWidth=2;
 ctx.fillRect(o.x,ground-o.h,o.w,o.h);
 ctx.strokeRect(o.x,ground-o.h,o.w,o.h);
 ctx.strokeStyle='#ff8fb7';ctx.lineWidth=2;
 ctx.beginPath();ctx.moveTo(o.x+5,ground-o.h+5);ctx.lineTo(o.x+o.w-5,ground-5);ctx.stroke();
 ctx.restore();
}
function drawOrb(o){
 ctx.save();ctx.shadowBlur=20;ctx.shadowColor='#4cecff';
 ctx.fillStyle='#4cecff';ctx.beginPath();ctx.arc(o.x,o.y,o.r,0,Math.PI*2);ctx.fill();
 ctx.strokeStyle='white';ctx.lineWidth=1;ctx.beginPath();
 ctx.arc(o.x,o.y,o.r+5+Math.sin(elapsed*5)*2,0,Math.PI*2);ctx.stroke();
 ctx.restore();
}
function burst(x,y,color){
 for(let i=0;i<12;i++)particles.push({
  x,y,vx:rand(-3,3),vy:rand(-4,2),life:rand(.3,.7),color
 });
}
function drawParticles(dt){
 particles.forEach(p=>{
  p.x+=p.vx*dt*60;p.y+=p.vy*dt*60;p.vy+=.12*dt*60;p.life-=dt;
  ctx.globalAlpha=Math.max(0,p.life*2);ctx.fillStyle=p.color;
  ctx.fillRect(p.x,p.y,3,3);
 });
 ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);
}
function hud(){
 $('score').textContent=String(Math.floor(score)).padStart(4,'0');
 $('cores').textContent=String(cores).padStart(2,'0');
 $('energyBar').style.width=energy+'%';
 $('energyBar').style.background=energy<25?'#ff397e':'#4cecff';
}
function reset(){
 score=0;cores=0;speed=5;energy=100;spawn=35;orbSpawn=25;
 elapsed=0;obstacles=[];orbs=[];particles=[];
 player.y=ground;player.vy=0;player.jumping=false;
 hud();
}
function begin(){
 reset();running=true;paused=false;over=false;started=true;
 $('intro').classList.add('hidden');
 $('gameover').classList.add('hidden');$('paused').classList.add('hidden');
 $('pauseBtn').classList.remove('hidden');last=performance.now();
}
function endGame(){
 running=false;over=true;
 $('finalScore').textContent=Math.floor(score)+' M';
 $('gameover').classList.remove('hidden');
 $('pauseBtn').classList.add('hidden');
 if(score>highScore){
  highScore=Math.floor(score);localStorage.setItem('shadowHigh',highScore);
  $('message').textContent='NEW DISTANCE RECORD // '+highScore+' M';
 }
}
function jump(){
 if(!running||paused||over)return;
 if(!player.jumping){
  player.vy=-14;player.jumping=true;
  burst(player.x+15,player.y-10,'#4cecff');
 }
}
function togglePause(){
 if(!running||over)return;
 paused=!paused;
 $('paused').classList.toggle('hidden',!paused);
 $('pauseBtn').textContent=paused?'▶ RESUME':'Ⅱ PAUSE';
 if(!paused)last=performance.now();
}
addEventListener('keydown',e=>{
 if(['Space','ArrowUp','ArrowDown'].includes(e.code))e.preventDefault();
 if((e.code==='Space'||e.code==='ArrowUp')&&!e.repeat)jump();
 if(e.code==='Escape'||e.code==='KeyP')togglePause();
});
$('startBtn').onclick=begin;
$('retryBtn').onclick=begin;
$('pauseBtn').onclick=togglePause;
$('resumeBtn').onclick=togglePause;
$('jumpBtn').onclick=jump;
$('homeBtn').onclick=()=>{
 running=false;paused=false;over=false;
 $('gameover').classList.add('hidden');$('intro').classList.remove('hidden');
 $('pauseBtn').classList.add('hidden');
};
$('howBtn').onclick=()=>{
 $('message').textContent='SPACE / UP = JUMP  •  DODGE RED OBSTACLES  •  COLLECT CYAN CORES';
};
canvas.addEventListener('pointerdown',()=>{if(running)jump()});

function update(dt){
 elapsed+=dt;
 if(!running||paused){return}
 score+=speed*dt*3;
 speed=Math.min(11,5+score/1500);
 energy=Math.max(0,energy-dt*.8);
 if(energy<=0){endGame();return}

 player.y+=player.vy*dt*60;
 player.vy+=.65*dt*60;
 if(player.y>=ground){player.y=ground;player.vy=0;player.jumping=false}

 spawn-=dt*60;
 if(spawn<=0){
  let h=rand(30,65),w=rand(22,36);
  obstacles.push({x:W+20,w,h});
  spawn=rand(65,110)/Math.min(1.8,speed/5);
 }
 orbSpawn-=dt*60;
 if(orbSpawn<=0){
  orbs.push({x:W+20,y:ground-rand(65,145),r:7});
  orbSpawn=rand(75,140);
 }
 obstacles.forEach(o=>o.x-=speed*dt*60);
 orbs.forEach(o=>o.x-=speed*dt*60);
 obstacles=obstacles.filter(o=>o.x+o.w>-20);
 orbs=orbs.filter(o=>o.x>-20);

 for(let o of obstacles){
  if(player.x+player.w-5>o.x&&player.x+5<o.x+o.w&&
     player.y>ground-o.h+8){
   burst(player.x+15,player.y-20,'#ff397e');endGame();return;
  }
 }
 for(let i=orbs.length-1;i>=0;i--){
  let o=orbs[i];
  if(Math.abs(player.x+15-o.x)<24&&Math.abs(player.y-23-o.y)<30){
   cores++;energy=Math.min(100,energy+18);burst(o.x,o.y,'#4cecff');
   orbs.splice(i,1);
  }
 }
 drawParticles(dt);hud();
}

function render(now){
 const dt=Math.min((now-last)/1000,.035||0.035);
 last=now;
 drawWorld(dt);
 if(running&&!paused){
  update(dt);
 }else{
  drawParticles(dt);
 }
 obstacles.forEach(drawObstacle);orbs.forEach(drawOrb);
 drawPlayer();
 if(running&&paused){
  // Keep the world visible while paused.
 }
 requestAnimationFrame(render);
}
reset();player.y=ground;requestAnimationFrame(t=>{last=t;requestAnimationFrame(render)});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
