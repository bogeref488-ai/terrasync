const API="/api/v1",TOKEN_KEY="terrasync_coordinator_token";
let user=null;
const q=s=>document.querySelector(s),qa=s=>[...document.querySelectorAll(s)];
function headers(){return{"Authorization":`Bearer ${localStorage.getItem(TOKEN_KEY)||""}`,"Content-Type":"application/json"}}
async function api(path,opts={}){const r=await fetch(API+path,{...opts,headers:{...headers(),...(opts.headers||{})}});if(!r.ok){const b=await r.json().catch(()=>({detail:r.statusText}));throw new Error(typeof b.detail==="string"?b.detail:JSON.stringify(b.detail))}return r.json()}
function initials(n){return(n||"CO").split(/\s+/).map(x=>x[0]).join("").slice(0,2).toUpperCase()}
function show(id){qa(".view").forEach(v=>v.classList.toggle("active",v.id===id));qa(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.view===id));q("#title").textContent={home:"Dashboard",assignments:"Assignments",review:"AI Review Queue",templates:"Templates",devices:"Field Devices",profile:"Profile"}[id]}
function metric(label,value){return`<article class="metric"><span>${label}</span><strong>${value}</strong></article>`}
function row(title,sub,right=""){return`<div class="row"><div><h4>${title}</h4><p>${sub}</p></div><div>${right}</div></div>`}
function riskClass(score){return score>=70?"high":score>=30?"med":"low"}
async function loadDashboard(){
  const [dashboard,queue]=await Promise.all([api("/dashboard/coordinator"),api("/review-queue")]);
  q("#metrics").innerHTML=metric("Assigned",dashboard.assigned)+metric("In field",dashboard.in_field)+metric("Awaiting review",dashboard.awaiting_review)+metric("Critical",dashboard.critical);
  q("#recent").innerHTML=(dashboard.recent_reports||[]).map(r=>row(r.report_no,r.summary||r.status,`<span class="risk ${riskClass(r.risk||0)}">${r.risk||0}/100</span>`)).join("")||"<p class='muted'>No reports yet.</p>";
  q("#fieldStatus").innerHTML=`<div class="mini-grid"><div class="mini-card"><span>Active technicians</span><strong>${dashboard.active_technicians}</strong></div><div class="mini-card"><span>Registered devices</span><strong>${dashboard.registered_devices}</strong></div><div class="mini-card"><span>Review queue</span><strong>${queue.length}</strong></div><div class="mini-card"><span>Critical queue</span><strong>${queue.filter(r=>(r.ai_risk_score||0)>=70).length}</strong></div></div>`;
  renderReview(queue);
}
function renderReview(queue){
  q("#reviewList").innerHTML=queue.map(r=>`<div class="row">
    <div><h4>${r.report_no} · ${r.report_type}</h4><p>${r.ai_summary||"AI screening complete."}</p><p>Inspector: ${r.inspector_name} · Status: ${r.status}</p></div>
    <div class="review-actions">
      <span class="risk ${riskClass(r.ai_risk_score||0)}">${r.ai_risk_score||0}/100</span>
      <a href="${API}/reports/${r.id}/pdf" target="_blank"><button>PDF</button></a>
      <button class="approve" data-review="${r.id}" data-decision="approve">Approve</button>
      <button class="return" data-review="${r.id}" data-decision="return">Return</button>
    </div>
  </div>`).join("")||"<p class='muted'>No reports currently require coordinator review.</p>";
}

let templateCatalog=[];
function renderTemplates(){
  const sector=q("#templateSector")?.value||"";
  const list=sector?templateCatalog.filter(t=>t.sector===sector):templateCatalog;
  q("#templateList").innerHTML=list.map(t=>`<div class="row"><div><h4>${t.name}</h4><p>${t.sector} · ${t.category} · v${t.version}</p><p>${t.description}</p></div><div><span class="status">${t.section_count} sections</span><br><small class="muted">${t.minimum_evidence} min. photos</small></div></div>`).join("")||"<p class='muted'>No templates.</p>";
}
async function loadTemplates(){
  templateCatalog=await api("/inspection-templates");
  q("#reportType").innerHTML=templateCatalog.map(t=>`<option value="${t.name}">${t.name} · ${t.sector}</option>`).join("");
  const sectors=[...new Set(templateCatalog.map(t=>t.sector))].sort();
  q("#templateSector").innerHTML='<option value="">All sectors</option>'+sectors.map(s=>`<option>${s}</option>`).join("");
  renderTemplates();
}

async function loadOperations(){
  const [assignments,devices,techs,sites]=await Promise.all([api("/assignments"),api("/devices"),api("/users/technicians"),api("/sites")]);
  q("#assignmentList").innerHTML=assignments.map(x=>row(x.work_order_no,`${x.report_type} · ${x.assigned_to||"Unassigned"} · ${x.status}`,`<span class="status">${x.priority}</span>`)).join("")||"<p class='muted'>No assignments.</p>";
  q("#deviceList").innerHTML=devices.map(x=>row(x.device_name,`${x.platform||"Device"} · last seen ${new Date(x.last_seen_at).toLocaleString()}`,`<span class="status">${x.active?"Active":"Revoked"}</span>`)).join("")||"<p class='muted'>No registered devices.</p>";
  const options=techs.map(x=>`<option value="${x.id}">${x.full_name} · ${x.staff_no||x.username}</option>`).join("");
  q("#technicianId").innerHTML=options;q("#otpTech").innerHTML=options;
  q("#siteId").innerHTML=sites.map(x=>`<option value="${x.id}">${x.code} · ${x.name}</option>`).join("");
}
async function boot(){
  user=await api("/auth/me");
  if(!["COORDINATOR","ADMIN"].includes(user.role))throw new Error("Coordinator access required");
  q("#name").textContent=user.full_name;q("#role").textContent="Coordinator";q("#avatar").textContent=initials(user.full_name);
  q("#profileData").innerHTML=row("Staff number",user.staff_no||"—")+row("Company",user.company||"—")+row("Email",user.email||"—")+row("Role","Coordinator — assignment & human review");
  await Promise.all([loadDashboard(),loadOperations(),loadTemplates()]);
}
q("#loginForm").addEventListener("submit",async e=>{e.preventDefault();q("#loginMessage").textContent="Signing in…";try{const data=await api("/auth/staff-login",{method:"POST",headers:{"Content-Type":"application/json","Authorization":""},body:JSON.stringify({username:q("#username").value,password:q("#password").value})});localStorage.setItem(TOKEN_KEY,data.access_token);q("#login").classList.add("hidden");q("#shell").classList.remove("hidden");await boot()}catch(err){q("#loginMessage").textContent=err.message}});
q("#assignmentForm").addEventListener("submit",async e=>{e.preventDefault();q("#assignmentMessage").textContent="Publishing…";try{await api("/assignments",{method:"POST",body:JSON.stringify({work_order_no:q("#woNo").value.trim(),site_id:q("#siteId").value,report_type:q("#reportType").value,priority:q("#priority").value,technician_id:q("#technicianId").value})});q("#assignmentMessage").textContent="Assignment published to the technician.";q("#assignmentMessage").className="success wide";e.target.reset();await Promise.all([loadDashboard(),loadOperations()])}catch(err){q("#assignmentMessage").textContent=err.message;q("#assignmentMessage").className="error wide"}});
q("#otpForm").addEventListener("submit",async e=>{e.preventDefault();try{const data=await api("/auth/activation-codes",{method:"POST",body:JSON.stringify({user_id:q("#otpTech").value,expires_minutes:Number(q("#otpMinutes").value)})});q("#otpResult").innerHTML=`<div class="callout"><span class="muted">One-time activation code</span><h2>${data.code}</h2><p class="muted">Expires ${new Date(data.expires_at).toLocaleString()}. It can be used once only.</p></div>`}catch(err){q("#otpResult").innerHTML=`<p class="error">${err.message}</p>`}});
document.body.addEventListener("click",async e=>{const b=e.target.closest("[data-review]");if(!b)return;const decision=b.dataset.decision;let note=null;if(decision==="return"){note=prompt("What should the field technician correct or recapture?","Please review the flagged item and resubmit verified evidence.");if(note===null)return}if(decision==="approve"&&!confirm("Approve this inspection report?"))return;try{await api(`/reports/${b.dataset.review}/review`,{method:"POST",body:JSON.stringify({decision,note})});await Promise.all([loadDashboard(),loadOperations()])}catch(err){alert(err.message)}});
qa(".nav button").forEach(b=>b.addEventListener("click",()=>show(b.dataset.view)));
q("#logout").addEventListener("click",()=>{localStorage.removeItem(TOKEN_KEY);location.reload()});
if(localStorage.getItem(TOKEN_KEY)){q("#login").classList.add("hidden");q("#shell").classList.remove("hidden");boot().catch(()=>{localStorage.removeItem(TOKEN_KEY);location.reload()})}
q("#templateSector").addEventListener("change",renderTemplates);
