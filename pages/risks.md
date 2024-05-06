[comment]: <> (Title of the page)
<h1><span style="color:#Ff5000">Data Protection Complaints</span> <span style="color:black">Organisational Risk</span></h1>

[comment]: <> (Risks Legend)
<h6>
<span style="color:black">Risks Legend: </span>
<span style="color:#5bda5b">Low </span>, 
<span style="color:#d9d982">Moderate </span>, 
<span style="color:#ffb347">High </span>, 
<span style="color:#ff6961">Critical</span>
</h6>

[comment]: <> (Orgnaisation dropdown)
<| {data_merged_filtered}|selector|value={selected_companyname}|lov={unique_companyname}|dropdown|>

[comment]: <> (Organisation filter)
<| {data_merged_filtered}|table|style[Scaled Risk Factor]=risk_style|>

