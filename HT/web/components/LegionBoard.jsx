// web/components/LegionBoard.jsx
import { useEffect, useState } from "react";
import io from "socket.io-client";
let socket;
export default function LegionBoard(){
  const [messages,setMessages]=useState([]);
  const [text,setText]=useState("");
  const [manifests,setManifests]=useState([]);
  useEffect(()=>{ socket = io(process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"); socket.on("broadcast_message", m=> setMessages(prev=>[...prev,m])); socket.on("new_manifest", m=> setManifests(prev=>[m,...prev])); fetch((process.env.NEXT_PUBLIC_API_URL||"http://localhost:5000") + "/api/manifests").then(r=>r.json()).then(d=>setManifests(d)); return ()=> socket.disconnect(); },[]);
  const send = ()=>{ if(!text) return; socket.emit("send_message",{user:localStorage.getItem("user")||"Anónimo", text}); setText(""); }
  const publish = async ()=>{ const title = prompt("Título"); const content = prompt("Contenido"); if(!title||!content) return; await fetch((process.env.NEXT_PUBLIC_API_URL||"http://localhost:5000")+"/api/manifest",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+localStorage.getItem("token")}, body: JSON.stringify({intention:content,mask:"Narrador"})}); }
  return (
    <div style={{padding:12,color:"#eae6d0"}}>
      <h3>Legión Resonante</h3>
      <div style={{display:"flex",gap:12}}>
        <div style={{flex:1}}>
          <div style={{height:200,overflowY:"auto",background:"#111",padding:8}}>{messages.map((m,i)=><div key={i}><b>{m.user}</b>: {m.text}</div>)}</div>
          <input value={text} onChange={e=>setText(e.target.value)} />
          <button onClick={send}>Enviar</button>
          <button onClick={publish}>Publicar Manifestación</button>
        </div>
        <div style={{width:360}}>
          <h4>Tablón</h4>
          <div style={{maxHeight:300,overflow:"auto",background:"#111",padding:8}}>{manifests.map((m,i)=>(<div key={i} style={{borderBottom:"1px solid #222",padding:8}}><b>{m.title}</b><p>{m.content}</p><small>{m.author} • {m.timestamp}</small></div>))}</div>
        </div>
      </div>
    </div>
  )
}
