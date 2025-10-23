// web/components/FrequencyEngine.js
export class FrequencyEngine {
  constructor(){
    this.audioCtx = null; this.osc1=null; this.osc2=null; this.gain=null; this.targetIntensity=0.2; this.isRunning=false;
  }
  init(){
    if(this.audioCtx) return;
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    this.osc1 = this.audioCtx.createOscillator(); this.osc2 = this.audioCtx.createOscillator(); this.gain = this.audioCtx.createGain();
    this.osc1.frequency.value = 432; this.osc2.frequency.value = 528;
    this.osc1.connect(this.gain); this.osc2.connect(this.gain); this.gain.connect(this.audioCtx.destination);
    this.gain.gain.value = 0; this.osc1.start(); this.osc2.start(); this.isRunning=true; this.animate();
  }
  setIntensity(v){ this.targetIntensity = Math.max(0,Math.min(1,v)); }
  triggerEvent(type){ if(type==="draw") this.setIntensity(0.6); if(type==="full") this.setIntensity(1.0); setTimeout(()=>this.setIntensity(0.2),2200); }
  animate(){ const loop=()=>{ if(!this.audioCtx) return; this.gain.gain.value += (this.targetIntensity - this.gain.gain.value)*0.08; document.querySelectorAll(".focus").forEach(el=>{ el.style.opacity = 0.3 + this.gain.gain.value*0.7; el.style.transform = `scale(${1+this.gain.gain.value*0.6})`; }); requestAnimationFrame(loop);} ; loop(); }
  stop(){ if(!this.audioCtx) return; this.gain.gain.setValueAtTime(0,this.audioCtx.currentTime); this.audioCtx.close(); this.audioCtx=null; }
}
