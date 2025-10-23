// web/components/ArchitectWorkshop.jsx
import React, {useEffect, useState} from "react";
import { FrequencyEngine } from "../components/FrequencyEngine";
import io from "socket.io-client";
let socket;

export default function ArchitectWorkshop(){
  const [cards, setCards] = useState([]);
  const [mode,setMode] = useState("single");
  const [manual,setManual] = useState("");
  const [loading,setLoading] = useState(false);
  const engineRef = React.useRef();

  useEffect(()=>{ engineRef.current = new FrequencyEngine(); engineRef.current.init(); socket = io(process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"); return ()=> { engineRef.current.stop(); socket.disconnect(); } },[]);

  async function draw(){
    setLoading(true);
    engineRef.current.triggerEvent(mode==="full"?"full":"draw");
    const body = {mode};
    const manualIds = manual.split(",").map(s=>parseInt(s.trim())).filter(n=>!isNaN(n));
    if(manualIds.length) body.manual_cards = manualIds;
    const res = await fetch((process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000") + "/api/draw", {method:"POST", headers:{"Content-Type":"application/json","Authorization": "Bearer " + localStorage.getItem("token")}, body: JSON.stringify(body)});
    const j = await res.json();
    setCards(j.cards || j.cards || []);
    setLoading(false);
  }

  return (
    <div style={{padding:20,color:"#eae6d0"}}>
      <h2>Taller del Arquitecto</h2>
      <div>
        <select value={mode} onChange={e=>setMode(e.target.value)}>
          <option value="single">1 Carta</option>
          <option value="triple">3 Cartas</option>
          <option value="cross">Cruz (5)</option>
          <option value="full">Todo</option>
        </select>
        <input placeholder="IDs: 1,5,10" value={manual} onChange={e=>setManual(e.target.value)} />
        <button onClick={draw} disabled={loading}>{loading?"Tirando...":"Tirar"}</button>
      </div>

      <div style={{display:"flex",gap:12,flexWrap:"wrap",marginTop:18}}>
        {cards.map((c,i)=>(
          <div key={i} style={{width:220,background:"#151515",padding:12,borderRadius:6}}>
            <img src={c.image_url} style={{width:"100%",height:120,objectFit:"cover"}}/>
            <h3>{c.title}{c.inverted?" (Invertida)":""}</h3>
            <p style={{fontSize:13}}>{c.protocol}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
