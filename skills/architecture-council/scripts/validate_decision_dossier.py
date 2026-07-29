#!/usr/bin/env python3
"""Validate an Architecture Council decision dossier JSON file."""
from __future__ import annotations
import argparse, json, re, sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

ALLOWED_LABELS={"FACT","INFERENCE","ASSUMPTION","UNKNOWN"}
ALLOWED_REVERSIBILITY={"reversible","partially-reversible","difficult-to-reverse","irreversible"}
ALLOWED_SENSITIVITY={"public","internal","confidential","restricted"}
SECRET_PATTERNS=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"\bAKIA[0-9A-Z]{16}\b"),re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),re.compile(r"(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[^\s,;]{8,}")]

def walk_strings(v:Any)->Iterable[str]:
    if isinstance(v,str): yield v
    elif isinstance(v,dict):
        for k,c in v.items(): yield str(k); yield from walk_strings(c)
    elif isinstance(v,list):
        for c in v: yield from walk_strings(c)

def nonempty_string(v:Any)->bool: return isinstance(v,str) and bool(v.strip())
def string_list(v:Any, allow_empty:bool=False)->bool: return isinstance(v,list) and (allow_empty or bool(v)) and all(nonempty_string(x) for x in v)
def valid_date(v:Any)->bool:
    if v is None: return True
    if not nonempty_string(v): return False
    try: date.fromisoformat(v); return True
    except ValueError: return False

def validate(path:Path)->list[str]:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError: return [f"file not found: {path}"]
    except json.JSONDecodeError as exc: return [f"invalid JSON: {exc}"]
    if not isinstance(data,dict): return ["top-level JSON value must be an object"]
    errors=[]
    required=("decision_id","title","question","required_outcome","options","constraints","success_criteria","evidence","no_material_unknowns","reversibility","deadline","decision_authority","risk_of_action","risk_of_inaction","sensitivity","external_provider_allowed","external_provider_approval","related_decisions","related_skills","related_lessons")
    for k in required:
        if k not in data: errors.append(f"missing required field: {k}")
    for k in ("decision_id","title","question","required_outcome","decision_authority"):
        if k in data and not nonempty_string(data[k]): errors.append(f"{k} must be a non-empty string")
    if isinstance(data.get("decision_id"),str) and not re.fullmatch(r"DEC-\d{4}-\d{3,}",data["decision_id"]): errors.append("decision_id must match DEC-YYYY-NNN")
    options=data.get("options")
    if not isinstance(options,list) or len(options)<2: errors.append("options must contain at least two entries")
    else:
        ids=set()
        for i,o in enumerate(options):
            if not isinstance(o,dict): errors.append(f"options[{i}] must be an object"); continue
            for k in ("id","name","description"):
                if not nonempty_string(o.get(k)): errors.append(f"options[{i}].{k} is required")
            oid=o.get("id")
            if isinstance(oid,str):
                if oid in ids: errors.append(f"duplicate option id: {oid}")
                ids.add(oid)
    for k in ("constraints","success_criteria","risk_of_action","risk_of_inaction"):
        if not string_list(data.get(k)): errors.append(f"{k} must be a non-empty array of strings")
    for k in ("related_decisions","related_skills","related_lessons"):
        if not string_list(data.get(k),allow_empty=True): errors.append(f"{k} must be an array of non-empty strings")
    evidence=data.get("evidence"); labels=set()
    if not isinstance(evidence,list) or not evidence: errors.append("evidence must be a non-empty array")
    else:
        for i,item in enumerate(evidence):
            if not isinstance(item,dict): errors.append(f"evidence[{i}] must be an object"); continue
            label=item.get("label"); statement=item.get("statement")
            if label not in ALLOWED_LABELS: errors.append(f"evidence[{i}].label must be one of {sorted(ALLOWED_LABELS)}")
            else: labels.add(label)
            if not nonempty_string(statement): errors.append(f"evidence[{i}].statement is required")
            if label in {"FACT","INFERENCE"} and not nonempty_string(item.get("source")): errors.append(f"evidence[{i}] {label} requires a source")
    no_unknowns=data.get("no_material_unknowns")
    if not isinstance(no_unknowns,bool): errors.append("no_material_unknowns must be a boolean")
    elif no_unknowns and "UNKNOWN" in labels: errors.append("no_material_unknowns cannot be true when UNKNOWN evidence exists")
    elif not no_unknowns and "UNKNOWN" not in labels: errors.append("evidence must include UNKNOWN unless no_material_unknowns is true")
    if data.get("reversibility") not in ALLOWED_REVERSIBILITY: errors.append(f"reversibility must be one of {sorted(ALLOWED_REVERSIBILITY)}")
    if not valid_date(data.get("deadline")): errors.append("deadline must be YYYY-MM-DD or null")
    sensitivity=data.get("sensitivity")
    if sensitivity not in ALLOWED_SENSITIVITY: errors.append(f"sensitivity must be one of {sorted(ALLOWED_SENSITIVITY)}")
    allowed=data.get("external_provider_allowed"); approval=data.get("external_provider_approval")
    if not isinstance(allowed,bool): errors.append("external_provider_allowed must be a boolean")
    if approval is not None and not nonempty_string(approval): errors.append("external_provider_approval must be a non-empty string or null")
    if sensitivity in {"confidential","restricted"} and allowed and not nonempty_string(approval): errors.append("confidential or restricted dossiers require documented external_provider_approval")
    if not allowed and approval is not None: errors.append("external_provider_approval must be null when external_provider_allowed is false")
    for text in walk_strings(data):
        if any(p.search(text) for p in SECRET_PATTERNS): errors.append("possible secret or credential detected")
    return sorted(set(errors))

def main()->int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("path",type=Path); a=p.parse_args(); e=validate(a.path)
    if e:
        print("Decision dossier validation failed:",file=sys.stderr)
        for x in e: print(f"- {x}",file=sys.stderr)
        return 1
    print(f"Decision dossier is valid: {a.path}"); return 0
if __name__=="__main__": raise SystemExit(main())
