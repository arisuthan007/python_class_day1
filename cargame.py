
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>APEX | Supercar Racing</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#050712;color:#fff;font-family:Arial,sans-serif;overflow:hidden}
#game{width:100vw;height:100vh;position:relative}
canvas{display:block}
.hud{position:absolute;inset:0;pointer-events:none}
.top{position:absolute;top:22px;left:4%;right:4%;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:25px;font-weight:900;letter-spacing:5px}
.logo span,.cyan{color:#00e5ff}
.small{font-size:10px;color:#91a6bf;letter-spacing:2px;margin-top:7px}
.stats{display:flex;gap:23px;text-align:right}
.stat label{display:block;font-size:9px;color:#91a6bf;letter-spacing:2px}
.stat strong{display:block;font-size:21px;margin-top:6px}
.panel{position:absolute;left:4%;top:23%;width:min(420px,91%);
background:linear-gradient(135deg,#071321f5,#080b13e8);
border:1px solid #30455b;padding:25px;backdrop-filter:blur(12px);
pointer-events:auto;max-height:72vh;overflow:auto}
.tag{font-size:10px;color:#00e5ff;letter-spacing:4px}
h1{font-size:clamp(38px,5vw,66px);line-height:.95;margin:18px 0;letter-spacing:-2px}
p{font-size:12px;line-height:1.8;color:#a7b8ca}
button,select{padding:13px;background:#101d2b;color:#fff;border:1px solid #3b5369;
cursor:pointer;font-size:11px;letter-spacing:1px}
button:hover{border-color:#00e5ff}
.primary{background:#00e5ff;color:#03121a;border-color:#00e5ff;font-weight:bold}
select{width:100%;margin:9px 0 14px}
label{font-size:10px;color:#00e5ff;letter-spacing:2px}
.hidden{display:none!important}
.bottom{position:absolute;bottom:20px;left:4%;right:4%;display:flex;justify-content:space-between;align-items:end}
.hint{font-size:10px;line-height:2;color:#9bb0c6;letter-spacing:1px}
.key{border:1px solid #40546a;padding:5px;color:#00e5ff}
#mobile{display:none;gap:5px;pointer-events:auto}
#mobile button{font-size:18px;min-width:48px}
#speedLine{position:absolute;bottom:0;left:0;height:3px;background:#00e5ff;width:0}
#notice{color:#ff557c;font-size:11px;min-height:15px}
@media(max-width:650px){
 .top{top:12px}.logo{font-size:18px;letter-spacing:3px}
 .stats{gap:10px}.stat strong{font-size:15px}
 .panel{top:22%;left:5%;padding:18px}
 .bottom{bottom:12px}#mobile{display:flex}.hint{font-size:8px}
}
</style>
</head>
<body>
<div id="game">
 <div class="hud">
  <div class="top">
   <div><div class="logo">APEX<span>.</span></div>
   <div class="small">HYPERCAR DIVISION / 2099</div></div>
   <div class="stats">
    <div class="stat"><label>SPEED</label><strong><span id="speed">0</span> <small>KM/H</small></strong></div>
    <div class="stat"><label>DISTANCE</label><strong id="distance">0 M</strong></div>
    <div class="stat"><label>LEVEL</label><strong id="level">01 / 03</strong></div>
   </div>
  </div>
  <div class="bottom">
   <div class="hint">
    <span class="key">A</span> <span class="key">D</span> STEER
    <span class="key">↑</span> ACCELERATE<br>
    <span class="key">↓</span> BRAKE &nbsp; AVOID RED BARRIERS
   </div>
   <div id="mobile">
    <button id="left">←</button><button id="brake">▼</button>
    <button id="gas">▲</button><button id="right">→</button>
   </div>
  </div>
 </div>

 <div class="panel" id="menu">
  <div class="tag">WORLD SERIES / CHAMPIONSHIP</div>
  <h1>OWN THE<br>ROAD<span class="cyan">.</span></h1>
  <p>Three supercars. Three stages. Five environments.
  Complete races to unlock faster and more powerful cars.</p>
  <label for="environment">ENVIRONMENT</label>
  <select id="environment">
   <option value="snow">ARCTIC SNOW</option>
   <option value="mud">MUDLAND</option>
   <option value="road" selected>ASPHALT ROAD</option>
   <option value="highway">NEON HIGHWAY</option>
   <option value="mix">EXTREME MIX</option>
  </select>
  <label for="carSelect">SELECT YOUR UNLOCKED CAR</label>
  <select id="carSelect"></select>
  <button class="primary" id="start" style="width:100%">START RACE ↗</button>
  <p id="notice"></p>
  <div class="small">LEVEL 1 GT / LEVEL 2 TRACK SPEC / LEVEL 3 HYPERCAR</div>
 </div>

 <div class="panel hidden" id="result">
  <div class="tag" id="resultTag">LEVEL COMPLETE</div>
  <h1 id="resultTitle">CAR<br>UPGRADED<span class="cyan">.</span></h1>
  <p id="resultText">Your next supercar is ready.</p>
  <button class="primary" id="next" style="width:100%">UNLOCK NEXT CAR ↗</button>
  <button id="garage" style="width:100%;margin-top:9px">RETURN TO GARAGE</button>
 </div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.185.0/build/three.module.js';

const $=id=>document.getElementById(id);
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.1,500);
camera.position.set(0,5.2,10);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.2;
$('game').prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xc4e4ff,0x382d29,2));
const sun=new THREE.DirectionalLight(0xffe6ca,3);
sun.position.set(-8,14,8);sun.castShadow=true;scene.add(sun);

const material=(c,r=.5,m=0)=>new THREE.MeshStandardMaterial({
 color:c,roughness:r,metalness:m
});
const M={
 road:material('#252b35',.9),snow:material('#e1edf5',.9),
 mud:material('#493326',1),grass:material('#193c36',1),
 glass:material('#071321',.18,.6),rubber:material('#090b10',.8),
 rim:material('#a4b4c2',.25,.8),white:material('#eafaff',.2,.3),
 dark:material('#10141e',.4,.5),cyan:material('#00e5ff',.2,.5),
 gold:material('#ffb52e',.2,.4),red:material('#ff3158',.3,.3)
};

let car,road,ground,roadObjects=[],obstacles=[],wheels=[];
let running=false,level=1,unlocked=1,dist=0,speed=0;
let carX=0,spawn=0,elapsed=0,last=0,env='road',keys={};
const LIMIT=4.4;
const targets={1:250,2:350,3:450};
const names={1:'GT SUPERCAR',2:'TRACK SPEC',3:'ULTIMATE HYPERCAR'};
const colours={1:0xff6828,2:0xe31d45,3:0x05dfff};

function box(parent,w,h,d,mat,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;
 parent.add(o);return o;
}

function makeCar(n){
 if(car)scene.remove(car);
 wheels=[];
 car=new THREE.Group();scene.add(car);
 const paint=material(colours[n],.2,.55);
 const black=material('#151d29',.25,.7);

 // Low, wide supercar body
 box(car,1.85,.38,3.9,paint,0,.57,0);
 box(car,1.7,.2,1.3,paint,0,.79,-1.2);
 box(car,1.65,.16,1.05,paint,0,.76,1.25);

 // Sloped windscreen and cockpit
 const cabin=box(car,1.23,.48,1.65,M.glass,0,.94,.02);
 cabin.rotation.x=-.10;
 box(car,1.32,.09,.62,black,0,1.18,.45);
 box(car,1.95,.08,.48,black,0,.35,-1.9);

 for(const side of [-1,1]){
  const lamp=box(car,.36,.09,.07,M.white,side*.61,.68,-1.98);
  lamp.material.emissive=new THREE.Color('#9cf6ff');
  lamp.material.emissiveIntensity=2;
  box(car,.10,.13,1.3,black,side*.91,.40,0);

  for(const z of [-1.25,1.25]){
   const wheel=new THREE.Group();
   const tyre=new THREE.Mesh(new THREE.CylinderGeometry(.36,.36,.23,24),M.rubber);
   tyre.rotation.z=Math.PI/2;wheel.add(tyre);
   const rim=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,.245,16),M.rim);
   rim.rotation.z=Math.PI/2;wheel.add(rim);
   wheel.position.set(side*.97,.36,z);car.add(wheel);wheels.push(wheel);
  }
 }
 if(n>=2){
  box(car,1.8,.10,.15,black,0,1.20,1.7);
  for(const s of [-1,1])box(car,.08,.3,.1,black,s*.72,1.03,1.58);
 }
 if(n>=3){
  box(car,1.65,.09,.5,paint,0,.95,1.55);
  box(car,2.0,.08,.12,black,0,1.42,1.65);
  box(car,.12,.15,.25,M.cyan,-.7,.7,-1.9);
  box(car,.12,.15,.25,M.cyan,.7,.7,-1.9);
 }
 car.position.set(0,0,3.2);
}

function clearWorld(){
 if(road)scene.remove(road);
 if(ground)scene.remove(ground);
 roadObjects.forEach(o=>scene.remove(o));
 roadObjects=[];
 obstacles.forEach(o=>scene.remove(o.group));
 obstacles=[];
}

function setEnvironment(name){
 clearWorld();env=name;
 let groundMat=name==='snow'?M.snow:name==='mud'?M.mud:M.grass;
 ground=new THREE.Mesh(new THREE.PlaneGeometry(500,500),groundMat);
 ground.rotation.x=-Math.PI/2;ground.position.y=-.12;
 ground.receiveShadow=true;scene.add(ground);

 let roadMat=name==='snow'?material('#aabdc9'):
 name==='mud'?material('#382920'):M.road;
 road=new THREE.Mesh(new THREE.PlaneGeometry(11,420),roadMat);
 road.rotation.x=-Math.PI/2;road.position.set(0,0,-195);
 road.receiveShadow=true;scene.add(road);

 const lineMat=name==='snow'?M.white:
 name==='mud'?material('#d0b18d'):M.white;
 for(let z=-400;z<20;z+=8){
  for(const x of [-1.8,1.8]){
   const line=box(scene,.08,.025,3,lineMat,x,.025,z);
   roadObjects.push(line);
  }
 }
 for(let z=-380;z<20;z+=17){
  for(const x of [-6.2,6.2]){
   const post=box(scene,.11,.8,.11,name==='highway'?M.cyan:lineMat,x,.3,z);
   roadObjects.push(post);
  }
 }
 if(name==='highway'){
  scene.background=new THREE.Color('#040718');
  sun.color.set('#91baff');
 }else if(name==='snow'){
  scene.background=new THREE.Color('#9db7cd');
  sun.color.set('#e9f6ff');
 }else if(name==='mud'){
  scene.background=new THREE.Color('#514033');
  sun.color.set('#ffc18c');
 }else{
  scene.background=new THREE.Color('#101b2b');
  sun.color.set('#ffe5cb');
 }
 scene.fog=new THREE.Fog(scene.background,35,180);

 // Mountain silhouettes
 const mountainMat=material(name==='snow'?'#718ba2':
 name==='mud'?'#3b3029':'#192b3a');
 for(let i=0;i<24;i++){
  const h=5+Math.random()*12;
  const m=new THREE.Mesh(new THREE.ConeGeometry(5+Math.random()*5,h,5),mountainMat);
  m.position.set((i%2?1:-1)*(13+Math.random()*22),h/2-.1,-45-i*10);
  scene.add(m);roadObjects.push(m);
 }
}

function spawnObstacle(){
 const group=new THREE.Group();
 const coin=Math.random()<.25;
 const obj=new THREE.Mesh(
  coin?new THREE.TorusGeometry(.48,.12,10,22):
  new THREE.BoxGeometry(1.35,1,1.1),
  coin?M.gold:M.red
 );
 obj.position.y=coin?1.25:.5;
 obj.castShadow=true;group.add(obj);
 group.position.set((Math.floor(Math.random()*3)-1)*3,0,-170);
 scene.add(group);obstacles.push({group,coin,hit:false});
}

function updateGarage(){
 $('carSelect').innerHTML='';
 for(let n=1;n<=3;n++){
  const option=document.createElement('option');
  option.value=n;
  option.disabled=n>unlocked;
  option.textContent='LEVEL '+n+' — '+names[n]+(n>unlocked?' 🔒':' ✓');
  $('carSelect').appendChild(option);
 }
 $('carSelect').value=String(Math.min(unlocked,3));
}

function resetRace(){
 dist=0;speed=0;carX=0;spawn=.5;elapsed=0;
 obstacles.forEach(o=>scene.remove(o.group));obstacles=[];
 car.position.x=0;car.rotation.z=0;
 $('speed').textContent='0';
 $('distance').textContent='0 M';
 $('level').textContent='0'+level+' / 03';
 $('speedLine').style.width='0%';
}

function startRace(){
 level=Number($('carSelect').value);
 level=Math.min(level,unlocked);
 setEnvironment($('environment').value);
 makeCar(level);resetRace();
 $('menu').classList.add('hidden');
 $('result').classList.add('hidden');
 running=true;last=performance.now();
}

function finishRace(){
 running=false;
 unlocked=Math.max(unlocked,Math.min(3,level+1));
 localStorage.setItem('apexUnlocked',String(unlocked));
 updateGarage();

 $('result').classList.remove('hidden');
 if(level<3){
  $('resultTag').textContent='LEVEL '+level+' COMPLETE';
  $('resultTitle').innerHTML='CAR<br>UPGRADED<span class="cyan">.</span>';
  $('resultText').textContent='You unlocked '+names[level+1]+
   '. Your next supercar has more power and a new design.';
  $('next').classList.remove('hidden');
  $('next').textContent='UNLOCK / DRIVE LEVEL '+(level+1)+' ↗';
 }else{
  $('resultTag').textContent='CHAMPIONSHIP COMPLETE';
  $('resultTitle').innerHTML='APEX<br>LEGEND<span class="cyan">.</span>';
  $('resultText').textContent='All three supercars unlocked. Return to the garage to select any car.';
  $('next').classList.add('hidden');
 }
}

$('start').onclick=startRace;

$('next').onclick=()=>{
 level=Math.min(3,level+1);
 $('carSelect').value=String(level);
 makeCar(level);
 resetRace();
 $('result').classList.add('hidden');
 running=true;last=performance.now();
};

$('garage').onclick=()=>{
 running=false;
 $('result').classList.add('hidden');
 $('menu').classList.remove('hidden');
 updateGarage();
};

function bindHold(id,key){
 const el=$(id);
 el.addEventListener('pointerdown',e=>{
  e.preventDefault();keys[key]=true;
 });
 ['pointerup','pointerleave','pointercancel'].forEach(ev=>
  el.addEventListener(ev,()=>keys[key]=false));
}
bindHold('left','ArrowLeft');bindHold('right','ArrowRight');
bindHold('gas','ArrowUp');bindHold('brake','ArrowDown');

addEventListener('keydown',e=>{
 keys[e.key]=true;
 if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(e.key))
  e.preventDefault();
});
addEventListener('keyup',e=>keys[e.key]=false);
addEventListener('blur',()=>keys={});

function update(dt){
 elapsed+=dt;
 if(keys.ArrowUp||keys.w||keys.W)speed+=27*dt;
 else speed-=7*dt;
 if(keys.ArrowDown||keys.s||keys.S)speed-=38*dt;
 speed=THREE.MathUtils.clamp(speed,0,level===1?160:level===2?230:320);

 const steer=(keys.ArrowRight||keys.d||keys.D?1:0)-
 (keys.ArrowLeft||keys.a||keys.A?1:0);
 carX=THREE.MathUtils.clamp(carX+steer*dt*(2.3+speed/65),-LIMIT,LIMIT);
 car.position.x=THREE.MathUtils.lerp(car.position.x,carX,.16);
 car.rotation.z=THREE.MathUtils.lerp(car.rotation.z,-steer*.12,.1);
 wheels.forEach(w=>w.rotation.x+=speed*dt*.05);

 dist+=speed*dt/3.6;
 spawn-=dt;
 if(spawn<=0&&speed>20){
  spawn=1.0+Math.random()*1.4;
  spawnObstacle();
 }
 roadObjects.forEach(o=>{
  o.position.z+=speed*dt*.23;
  if(o.position.z>15)o.position.z-=420;
 });

 for(let i=obstacles.length-1;i>=0;i--){
  const o=obstacles[i];
  o.group.position.z+=speed*dt*.23;
  o.group.rotation.y+=dt;
  if(!o.hit&&o.group.position.z>2&&o.group.position.z<5&&
     Math.abs(car.position.x-o.group.position.x)<1.25){
   o.hit=true;
   if(o.coin){
    dist+=30;
    scene.remove(o.group);obstacles.splice(i,1);
    continue;
   }else{
    speed*=.45;
    $('notice').textContent='COLLISION! SPEED REDUCED';
    setTimeout(()=>$('notice').textContent='',1000);
   }
  }
  if(o.group.position.z>12){
   scene.remove(o.group);obstacles.splice(i,1);
  }
 }

 camera.position.x=THREE.MathUtils.lerp(camera.position.x,car.position.x*.4,.05);
 camera.position.y=5.2+Math.sin(elapsed*2)*.03;
 camera.lookAt(car.position.x*.2,.5,-5);

 $('speed').textContent=Math.round(speed);
 $('distance').textContent=Math.floor(dist)+' M';
 $('level').textContent='0'+level+' / 03';
 $('speedLine').style.width=(speed/320*100)+'%';

 if(dist>=targets[level])finishRace();
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-last)/1000,.04);
 last=now;
 if(running)update(dt);
 renderer.render(scene,camera);
}

unlocked=Math.max(1,Math.min(3,Number(localStorage.getItem('apexUnlocked')||1)));
updateGarage();
makeCar(1);
setEnvironment('road');
resetRace();
requestAnimationFrame(animate);

addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
