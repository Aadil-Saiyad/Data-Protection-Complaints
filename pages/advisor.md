[comment]: <> (Title of the page)
<h1><span style="color:#Ff5000">Data Protection Complaints</span> <span style="color:black">GDPR Compliance Advisor</span></h1>

[comment]: <> (Setting the columns for subtitles)
<|layout|columns = 1 1 6|
<h5>Sector</h5>
<h5>Sub-Sector</h5>
<h5>Sector-Specific Mitigation Recommendations</h5>
|>

[comment]: <> (Setting the columns for the sector and subsector dropdowns and recommendations)
<|layout|columns = 1 1 6|

[comment]: <> (Sector dropdown)
<| {sector_sel}|selector|lov={sectors}|type=Sector|adapter={lambda u:(u.sectorName)}|>

[comment]: <> (Subsector dropdown)
<| {subSector_sel}|selector|lov={subSectors}|type=SubSector|adapter={lambda u:(u.subSectorName)}|>

[comment]: <> (Recommendations section)
<|card card-bg|

[comment]: <> (Recommendations 1 article name)
<| {articleIdentifier} |text|class_name=h2|>
<br/>

[comment]: <> (Recommendations 1 article description)
<| {articleDescription} |text|class_name=h5|>
<br/>

[comment]: <> (Recommendations 1 first recommendation)
<| {articleRecommendations} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 1 second recommendation)
<| {articleRecommendations2} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 1 third recommendation)
<| {articleRecommendations3} |text|class_name=small|>
<br/>
<br/>
<br/>

[comment]: <> (Recommendations 2 article name)
<| {article2Identifier} |text|class_name=h2|>
<br/>

[comment]: <> (Recommendations 2 article description)
<| {article2Description} |text|class_name=h5|>
<br/>

[comment]: <> (Recommendations 2 first recommendation)
<| {article2Recommendations} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 2 second recommendation)
<| {article2Recommendations2} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 2 third recommendation)
<| {article2Recommendations3} |text|class_name=small|>
<br/>
<br/>
<br/>

[comment]: <> (Recommendations 3 article name)
<| {article3Identifier} |text|class_name=h2|>
<br/>

[comment]: <> (Recommendations 3 article description)
<| {article3Description} |text|class_name=h5|>
<br/>

[comment]: <> (Recommendations 3 first recommendation)
<| {article3Recommendations} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 3 second recommendation)
<| {article3Recommendations2} |text|class_name=small|>
<br/>
<br/>

[comment]: <> (Recommendations 3 third recommendation)
<| {article3Recommendations3} |text|class_name=small|>

|>

|>