#!/usr/bin/env python3
"""Regression tests for Architecture Council validators."""
from __future__ import annotations
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'scripts'/'validate_decision_dossier.py'; R=ROOT/'scripts'/'validate_decision_record.py'; B=ROOT/'scripts'/'validate_skill_bundle.py'
def run(script,target,expected):
    x=subprocess.run([sys.executable,str(script),str(target)],capture_output=True,text=True)
    if x.returncode!=expected:raise AssertionError(f"{script.name}: {x.returncode}!={expected}\n{x.stdout}\n{x.stderr}")
def dossier():
 return {'decision_id':'DEC-2026-001','title':'Select target architecture','question':'Which option?','required_outcome':'Supportable secure architecture','options':[{'id':'a','name':'A','description':'Centralized'},{'id':'b','name':'B','description':'Distributed'}],'constraints':['Rollback required'],'success_criteria':['Acceptance tests pass'],'evidence':[{'label':'FACT','statement':'Inventory approved','source':'inventory'},{'label':'INFERENCE','statement':'A reduces variation','source':'operating data'},{'label':'ASSUMPTION','statement':'Team can support A','source':None},{'label':'UNKNOWN','statement':'Adoption rate unknown','source':None}],'no_material_unknowns':False,'reversibility':'partially-reversible','deadline':'2026-08-15','decision_authority':'Architecture owner','risk_of_action':['Disruption'],'risk_of_inaction':['Inconsistency'],'sensitivity':'internal','external_provider_allowed':False,'external_provider_approval':None,'related_decisions':[],'related_skills':[],'related_lessons':[]}
def record():
 return {'decision_id':'DEC-2026-001','result':'recommended','recommended_option':'a','decision_authority':'Architecture owner','mode':'full','execution_model':'single-model structured deliberation','panel':['strategy','technical','delivery','risk','operations','stakeholder'],'domain_weight_seat':'technical','reviewer_stances':[{'reviewer':'strategy','option':'a','confidence':'high','dealbreaker':'ROI fails'},{'reviewer':'technical','option':'a','confidence':'high','dealbreaker':'Security fails'},{'reviewer':'delivery','option':'a','confidence':'high','dealbreaker':'No rollback'},{'reviewer':'risk','option':'a','confidence':'medium','dealbreaker':'Control fails'},{'reviewer':'operations','option':'b','confidence':'medium','dealbreaker':'Support load high'},{'reviewer':'stakeholder','option':'a','confidence':'medium','dealbreaker':'Customer rejects'}],'evidence_summary':{'facts':['fact'],'inferences':['inference'],'assumptions':['assumption'],'unknowns':['unknown']},'recommendation':'Proceed with A.','rationale':['Secure','Supportable'],'acceptable_compromises':['Phased rollout'],'vote_tally':{'a':5.0,'b':0.75},'minority_position':'Choose B if support capacity fails.','unresolved_questions':['Final support capacity'],'kill_criteria':[{'condition':'Support load exceeds threshold','measure':'More than 10 incidents','trigger':'First 30 days','response':'Pause rollout','decision_authority':'Architecture owner'}],'concrete_next_action':'Validate operating capacity against the target support model.','implementation_action':'Run a controlled pilot.','owner':'Architecture owner','due_or_trigger':'Before production approval','prediction':'A will reduce variation without breaching support thresholds.','review_date':'2026-08-15','review_condition':None,'success_evidence':['Acceptance tests pass'],'reversal_evidence':['Support capacity is insufficient'],'expected_cost_of_reversal':'One maintenance window and rollback effort.','status':'proposed','confidence':'medium','limitations':['Single-model structured deliberation']}
def main():
 with tempfile.TemporaryDirectory() as td:
  p=Path(td); cases=[(D,dossier(),0,'valid dossier')]
  for key in ['success_criteria','deadline','related_decisions','related_skills','related_lessons','no_material_unknowns','external_provider_approval']:
   x=dossier();x.pop(key);cases.append((D,x,1,f'missing {key}'))
  x=dossier();x['deadline']='15/08/2026';cases.append((D,x,1,'bad deadline'))
  x=dossier();x['evidence']=[i for i in x['evidence'] if i['label']!='UNKNOWN'];cases.append((D,x,1,'unknown missing'))
  x=dossier();x['sensitivity']='restricted';x['external_provider_allowed']=True;cases.append((D,x,1,'missing provider approval'))
  cases.append((R,record(),0,'valid record'))
  for key in ['result','recommended_option','decision_authority','acceptable_compromises','prediction','implementation_action','success_evidence','expected_cost_of_reversal','review_date']:
   x=record();x.pop(key);cases.append((R,x,1,f'missing {key}'))
  x=record();x['vote_tally']={};cases.append((R,x,1,'empty tally'))
  x=record();x['vote_tally']={'a':999,'b':0};cases.append((R,x,1,'incorrect tally'))
  x=record();x['domain_weight_seat']='chair';cases.append((R,x,1,'seat not panel'))
  x=record();x['result']='split';cases.append((R,x,1,'split despite threshold'))
  x=record();x['evidence_summary']={'facts':[],'inferences':[],'assumptions':[],'unknowns':[]};cases.append((R,x,1,'empty evidence'))
  for idx,(s,obj,code,name) in enumerate(cases):
   f=p/f'{idx}.json';f.write_text(json.dumps(obj,indent=2),encoding='utf-8');run(s,f,code)
 run(B,ROOT,0);print(f'All {len(cases)} Architecture Council validator tests passed.');return 0
if __name__=='__main__':raise SystemExit(main())
