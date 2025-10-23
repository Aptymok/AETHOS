// web/components/LegionNetwork.jsx
import { useEffect, useRef } from "react";
import * as d3 from "d3";
export default function LegionNetwork({nodes}) {
  const ref = useRef();
  useEffect(()=>{
    if(!nodes || !nodes.length) return;
    const svg = d3.select(ref.current); svg.selectAll("*").remove();
    const width = window.innerWidth, height = window.innerHeight;
    svg.attr("viewBox",[0,0,width,height]);
    const sim = d3.forceSimulation(nodes).force("charge", d3.forceManyBody().strength(-200)).force("center", d3.forceCenter(width/2,height/2));
    const circles = svg.selectAll("circle").data(nodes).enter().append("circle").attr("r", d=>10 + (d.coherence||0)*10).attr("fill", d => d.coherence>=1 ? "#ffd700" : "#00ffff").attr("stroke","#222").attr("stroke-width",1.5);
    sim.on("tick", ()=>{ circles.attr("cx",d=>d.x).attr("cy",d=>d.y) })
  },[nodes]);
  return <svg ref={ref} style={{width:"100%",height:"100%",background:"#0b0b0c"}}></svg>
}
