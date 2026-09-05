#!/usr/bin/env python3
"""Validate an Architecture Council decision record JSON file."""
from __future__ import annotations
import argparse,json,re,sys
from datetime import date
from pathlib import Path
from typing import Any,Iterable
ALLOWED_MODES={"quick","duo","full"}; ALLOWED_EXECUTION_MODELS={"single-model structured deliberation","verified isolated agents","verified multi-provider"}; ALLOWED_RESULTS={"recommended","split","defer","reject"}; ALLOWED_STATUSES={"proposed","approved","implemented","confirmed","revised","reversed","inconclusive"}; ALLOWED_CONFIDENCE={"high","medium","low"}; ALLOWED_SCHEMA_VERSIONS={"1.0","1.1"}; ALLOWED_INTERVENTIONS={"insufficient_dissent","novelty_failure","premature_consensus","missing_stance","evidence_gap"}
SECRET_PATTERNS=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"\bAKIA[0-9A-Z]{16}\b"),re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")]
def walk_strings(v:Any)->Iterable[str]:
    if isinstance(v,str): yield v
    elif isinstance(v,dict):
        for k,c in v.items(): yield str(k); yield from walk_strings(c)
    elif isinstance(v,list):
        for c in v: yield from walk_strings(c)
def ns(v): return isinstance(v,str) and bool(v.strip())
def sl(v,empty=False): return isinstance(v,list) and (empty or bool(v)) and all(ns(x) for x in v)
def vd(v):
    if v is None:return True
    if not ns(v):return False
    try: date.fromisoformat(v);return True
    except ValueError:return False

def validate(path:Path)->list[str]:
    try:data=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:return[f"file not found: {path}"]
    except json.JSONDecodeError as exc:return[f"invalid JSON: {exc}"]
    if not isinstance(data,dict):return["top-level JSON value must be an object"]
    e=[]; req=("decision_id","result","recommended_option","decision_authority","mode","execution_model","panel","domain_weight_seat","reviewer_stances","evidence_summary","recommendation","rationale","acceptable_compromises","vote_tally","minority_position","unresolved_questions","kill_criteria","concrete_next_action","implementation_action","owner","due_or_trigger","prediction","review_date","review_condition","success_evidence","reversal_evidence","expected_cost_of_reversal","status","confidence","limitations")
    for k in req:
        if k not in data:e.append(f"missing required field: {k}")
    schema=data.get("schema_version","1.0")
    if schema not in ALLOWED_SCHEMA_VERSIONS:e.append(f"schema_version must be one of {sorted(ALLOWED_SCHEMA_VERSIONS)}")
    if schema=="1.1" and "protocol_interventions" not in data:e.append("missing required field for schema_version 1.1: protocol_interventions")
    if "protocol_interventions" in data and schema!="1.1":e.append("protocol_interventions requires schema_version 1.1")
    if "protocol_interventions" in data:
        pi=data.get("protocol_interventions")
        if not isinstance(pi,dict):e.append("protocol_interventions must be an object")
        else:
            if set(pi)!={"total","breakdown"}:e.append("protocol_interventions must contain exactly total and breakdown")
            total=pi.get("total"); breakdown=pi.get("breakdown")
            if not isinstance(total,int) or isinstance(total,bool) or total<0:e.append("protocol_interventions.total must be a non-negative integer")
            if not isinstance(breakdown,dict):e.append("protocol_interventions.breakdown must be an object")
            else:
                if set(breakdown)!=ALLOWED_INTERVENTIONS:e.append(f"protocol_interventions.breakdown must contain exactly {sorted(ALLOWED_INTERVENTIONS)}")
                valid_counts=True
                for k,v in breakdown.items():
                    if not isinstance(v,int) or isinstance(v,bool) or v<0:e.append(f"protocol_interventions.breakdown.{k} must be a non-negative integer");valid_counts=False
                if isinstance(total,int) and not isinstance(total,bool) and total>=0 and valid_counts and total!=sum(breakdown.values()):e.append("protocol_interventions.total must equal the sum of breakdown counts")
    if isinstance(data.get("decision_id"),str) and not re.fullmatch(r"DEC-\d{4}-\d{3,}",data["decision_id"]):e.append("decision_id must match DEC-YYYY-NNN")
    for k in ("decision_id","decision_authority","recommendation","minority_position","concrete_next_action","implementation_action","owner","due_or_trigger","prediction","expected_cost_of_reversal"):
        if k in data and not ns(data[k]):e.append(f"{k} must be a non-empty string")
    if data.get("result") not in ALLOWED_RESULTS:e.append(f"result must be one of {sorted(ALLOWED_RESULTS)}")
    if data.get("mode") not in ALLOWED_MODES:e.append(f"mode must be one of {sorted(ALLOWED_MODES)}")
    if data.get("execution_model") not in ALLOWED_EXECUTION_MODELS:e.append(f"execution_model must be one of {sorted(ALLOWED_EXECUTION_MODELS)}")
    if data.get("status") not in ALLOWED_STATUSES:e.append(f"status must be one of {sorted(ALLOWED_STATUSES)}")
    if data.get("confidence") not in ALLOWED_CONFIDENCE:e.append(f"confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
    panel=data.get("panel")
    if not isinstance(panel,list) or not all(ns(x) for x in panel):e.append("panel must be a non-empty array of reviewer names")
    else:
        expected={"quick":3,"duo":2,"full":6}.get(data.get("mode"),1)
        if len(panel)!=expected:e.append(f"panel must contain exactly {expected} reviewers for {data.get('mode')} mode")
        if len(panel)!=len(set(panel)):e.append("panel contains duplicate reviewers")
        seat=data.get("domain_weight_seat")
        if seat is not None and seat not in panel:e.append("domain_weight_seat must be null or a reviewer in panel")
    stances=data.get("reviewer_stances")
    if not isinstance(stances,list) or not stances:e.append("reviewer_stances must be a non-empty array")
    else:
        seen=set()
        for i,s in enumerate(stances):
            if not isinstance(s,dict):e.append(f"reviewer_stances[{i}] must be an object");continue
            for k in ("reviewer","option","confidence","dealbreaker"):
                if not ns(s.get(k)):e.append(f"reviewer_stances[{i}].{k} is required")
            if s.get("confidence") not in ALLOWED_CONFIDENCE:e.append(f"reviewer_stances[{i}].confidence is invalid")
            if s.get("reviewer") in seen:e.append(f"duplicate reviewer stance: {s.get('reviewer')}")
            seen.add(s.get("reviewer"))
        if isinstance(panel,list) and set(panel)!=seen:e.append("reviewer_stances must contain exactly one stance for each panel reviewer")
    es=data.get("evidence_summary")
    if not isinstance(es,dict):e.append("evidence_summary must be an object")
    else:
        for k in ("facts","inferences","assumptions","unknowns"):
            if not sl(es.get(k),empty=True):e.append(f"evidence_summary.{k} must be an array of non-empty strings")
        if not any(es.get(k) for k in ("facts","inferences","assumptions","unknowns")):e.append("evidence_summary must contain at least one item")
    for k in ("rationale","acceptable_compromises","unresolved_questions","success_evidence","reversal_evidence","limitations"):
        if not sl(data.get(k),empty=(k in {"acceptable_compromises","unresolved_questions","limitations"})):e.append(f"{k} must be an array of non-empty strings")
    tally=data.get("vote_tally")
    if not isinstance(tally,dict) or not tally:e.append("vote_tally must be a non-empty object")
    elif not all(ns(k) and isinstance(v,(int,float)) and not isinstance(v,bool) and v>=0 for k,v in tally.items()):e.append("vote_tally values must be non-negative numbers")
    if isinstance(stances,list) and isinstance(panel,list):
        factors={"high":1.0,"medium":0.75,"low":0.5}; calc={}; total=0.0; seat=data.get("domain_weight_seat")
        for s in stances:
            if not isinstance(s,dict) or s.get("confidence") not in factors or not ns(s.get("option")) or s.get("reviewer") not in panel:continue
            base=1.5 if s.get("reviewer")==seat else 1.0; total+=base; calc[s["option"]]=calc.get(s["option"],0)+base*factors[s["confidence"]]
        if isinstance(tally,dict) and tally and (set(tally)!=set(calc) or any(abs(float(tally[k])-calc[k])>0.001 for k in calc)):e.append("vote_tally does not match reviewer_stances and domain weighting")
        threshold=(2/3)*total if total else 0; winners=[o for o,w in calc.items() if w+1e-9>=threshold]
        result=data.get("result"); rec=data.get("recommended_option")
        if result=="recommended":
            if len(winners)!=1:e.append("recommended result requires exactly one option to reach the two-thirds threshold")
            elif rec!=winners[0]:e.append("recommended_option must equal the threshold winner")
        elif result=="split" and winners:e.append("split result is invalid when an option reaches the two-thirds threshold")
        elif result in {"defer","reject"} and rec is not None:e.append("recommended_option must be null for defer or reject")
    kc=data.get("kill_criteria")
    if not isinstance(kc,list) or not kc:e.append("kill_criteria must be a non-empty array")
    else:
        for i,c in enumerate(kc):
            if not isinstance(c,dict):e.append(f"kill_criteria[{i}] must be an object");continue
            for k in ("condition","measure","trigger","response","decision_authority"):
                if not ns(c.get(k)):e.append(f"kill_criteria[{i}].{k} is required")
    action=data.get("concrete_next_action")
    if isinstance(action,str) and ("\n" in action.strip() or len(action.strip())<5):e.append("concrete_next_action must contain exactly one clear action on one line")
    rd=data.get("review_date"); rc=data.get("review_condition")
    if not vd(rd):e.append("review_date must be YYYY-MM-DD or null")
    if rd is None and not ns(rc):e.append("review_condition is required when review_date is null")
    if rd is not None and rc is not None and not ns(rc):e.append("review_condition must be a non-empty string or null")
    for text in walk_strings(data):
        if any(p.search(text) for p in SECRET_PATTERNS):e.append("possible secret or credential detected")
    return sorted(set(e))

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("path",type=Path);a=p.parse_args();e=validate(a.path)
    if e:
        print("Decision record validation failed:",file=sys.stderr)
        for x in e:print(f"- {x}",file=sys.stderr)
        return 1
    print(f"Decision record is valid: {a.path}");return 0
if __name__=="__main__":raise SystemExit(main())
