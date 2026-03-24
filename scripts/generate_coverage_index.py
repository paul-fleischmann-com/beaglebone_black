#!/usr/bin/env python3
import os
import json

output_dir = os.environ["OUTPUT_DIR"]
html_dir = os.path.join(output_dir, "html")
reports = [{"label": "All Tests", "url": "combined/index.html"}]
cov_dir = os.path.join(output_dir, "coverage")
if os.path.isdir(cov_dir):
    for name in sorted(os.listdir(cov_dir)):
        if os.path.isdir(os.path.join(cov_dir, name)):
            reports.append({"label": name, "url": f"{name}/index.html"})

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>C Coverage</title><style>
body{{font-family:sans-serif;margin:2em}}
.tabs{{display:flex;gap:8px;margin-bottom:1em;flex-wrap:wrap}}
.tab{{padding:8px 16px;background:#eee;border:1px solid #ccc;border-radius:4px;cursor:pointer;text-decoration:none;color:#333}}
.tab:hover{{background:#ddd}}.tab.active{{background:#4a90d9;color:white;border-color:#4a90d9}}
iframe{{width:100%;height:85vh;border:1px solid #ccc;border-radius:4px}}
</style></head><body><h2>C Coverage Report</h2>
<div class="tabs" id="tabs"></div>
<iframe id="frame" src="combined/index.html"></iframe>
<script>
const reports={json.dumps(reports)};
const tabs=document.getElementById('tabs');
const frame=document.getElementById('frame');
reports.forEach((r,i)=>{{
  const a=document.createElement('a');
  a.className='tab'+(i===0?' active':'');
  a.textContent=r.label;a.href='#';
  a.onclick=e=>{{e.preventDefault();
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    a.classList.add('active');frame.src=r.url;}};
  tabs.appendChild(a);
}});</script></body></html>"""

with open(os.path.join(html_dir, "index.html"), "w") as f:
    f.write(html)
