// web/pages/index.js
import Link from "next/link";
export default function Home(){
  return (
    <div style={{padding:40,color:"#eae6d0",background:"#0d0d0f",minHeight:"100vh",fontFamily:"JetBrains Mono"}}>
      <h1>HELL THEATER — Códex Público</h1>
      <p>Puerta al Taller, al Tablero y a la Legión.</p>
      <nav>
        <Link href="/workshop">Taller</Link> | <Link href="/dashboard">Dashboard</Link>
      </nav>
    </div>
  )
}
