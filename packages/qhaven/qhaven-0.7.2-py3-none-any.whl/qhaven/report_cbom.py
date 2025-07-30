from __future__ import annotations

import datetime, json, uuid
from pathlib import Path
from typing import Dict, List

_CBOM_FORMAT="CycloneDX"; _CBOM_SCHEMA_VERSION="1.4"; _CBOM_SPEC_VERSION="1.0"

def write_cbom(findings:List[Dict],sys_meta:Dict,out_path:Path)->None:
    bom={
        "bomFormat":_CBOM_FORMAT,
        "specVersion":_CBOM_SCHEMA_VERSION,
        "serialNumber":f"urn:uuid:{uuid.uuid4()}",
        "version":1,
        "metadata":{"properties":[
            {"name":"specVersion","value":_CBOM_SPEC_VERSION},
            {"name":"generated","value":datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z"},
            {"name":"tool","value":"QHaven"},
        ]},
        "components":[]
    }
    for f in findings:
        props=[
            {"name":"fismaId","value":sys_meta.get("fisma_id","")},
            {"name":"fips199","value":sys_meta.get("fips199","")},
            {"name":"hvaId","value":sys_meta.get("hva_id","")},
            {"name":"vendorType","value":sys_meta.get("vendor_type","")},
            {"name":"operatingSystem","value":sys_meta.get("operating_system","")},
            {"name":"hosting","value":sys_meta.get("hosting","")},
            {"name":"deadline","value":f.get("deadline","")},
            {"name":"replacement","value":f.get("replacement","")},
            {"name":"fileLocation","value":f.get("file","")},
            {"name":"lineNumber","value":str(f.get("line",""))},
        ]
        bom["components"].append({
            "type":"application","name":f"{f.get('algorithm','')}-{uuid.uuid4().hex[:8]}",
            "version":"0.0.1","properties":props
        })
    out_path.write_text(json.dumps(bom,indent=2))