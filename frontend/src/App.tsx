import {useState} from "react";

type Message={role:"user"|"assistant";text:string;verified?:boolean;proposalId?:string;requiresConfirmation?:boolean};
const API="http://localhost:8000/api";

export default function App(){
 const [messages,setMessages]=useState<Message[]>([{role:"assistant",text:"Hi! I can help you search products, check order status, estimate delivery, and prepare purchases."}]);
 const [input,setInput]=useState(""); const [loading,setLoading]=useState(false);

 async function sendMessage(text=input){
  if(!text.trim()||loading)return;
  setMessages(p=>[...p,{role:"user",text}]); setInput(""); setLoading(true);
  try{
   const r=await fetch(`${API}/chat`,{method:"POST",headers:{"Content-Type":"application/json"},
     body:JSON.stringify({message:text,session_id:"demo-session"})});
   if(!r.ok)throw new Error();
   const d=await r.json();
   setMessages(p=>[...p,{role:"assistant",text:d.message,verified:d.verified,
     proposalId:d.proposal_id,requiresConfirmation:d.requires_confirmation}]);
  }catch{
   setMessages(p=>[...p,{role:"assistant",text:"I couldn't reach the shopping service. Please make sure the backend is running."}]);
  }finally{setLoading(false);}
 }

 async function confirmPurchase(proposalId:string){
  setLoading(true);
  try{
   const r=await fetch(`${API}/purchase/confirm`,{method:"POST",headers:{"Content-Type":"application/json"},
     body:JSON.stringify({proposal_id:proposalId})});
   const d=await r.json();
   setMessages(p=>[...p,{role:"assistant",text:d.message||d.detail||"Purchase could not be completed.",verified:d.verified}]);
  }catch{
   setMessages(p=>[...p,{role:"assistant",text:"Purchase confirmation failed. Please try again."}]);
  }finally{setLoading(false);}
 }

 return <main className="page"><section className="app">
  <header className="header"><div><h1>🛍 AI Shopping Assistant</h1><p>Products, orders and purchases — backed by verified data.</p></div><span className="status">● Demo</span></header>
  <div className="quick-actions">
   <button onClick={()=>sendMessage("What Nike t shirts are available?")}>Nike T-Shirts</button>
   <button onClick={()=>sendMessage("What is the status of order 1001?")}>Track Order</button>
   <button onClick={()=>sendMessage("When will order 1001 be delivered?")}>Delivery</button>
  </div>
  <section className="messages" aria-live="polite">
   {messages.map((m,i)=><div key={i} className={`row ${m.role}`}><div className={`bubble ${m.role}`}>
    <div>{m.text}</div>
    {m.verified&&<div className="verified">✓ Verified backend data</div>}
    {m.requiresConfirmation&&m.proposalId&&<div className="confirm-box"><strong>Purchase confirmation required</strong>
      <button disabled={loading} onClick={()=>confirmPurchase(m.proposalId!)}>Confirm Purchase</button></div>}
   </div></div>)}
   {loading&&<div className="row assistant"><div className="bubble assistant">Checking verified information…</div></div>}
  </section>
  <form className="composer" onSubmit={e=>{e.preventDefault();sendMessage();}}>
   <label htmlFor="message" className="sr-only">Message</label>
   <input id="message" value={input} onChange={e=>setInput(e.target.value)} placeholder="Ask about products or orders…" disabled={loading}/>
   <button type="submit" disabled={loading||!input.trim()}>Send</button>
  </form>
  <footer><span>Backend tools are the source of truth.</span><span>👍 Helpful &nbsp; 👎 Not helpful</span></footer>
 </section></main>
}
