from __future__ import annotations
import json, math, random, re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

SEED = 20260910
random.seed(SEED)
np.random.seed(SEED)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
SRC = ROOT / 'src'
OUT = ROOT / 'outputs'
for p in (DATA, SRC, OUT): p.mkdir(parents=True, exist_ok=True)

FIRST = ['Ahsan','Ali','Areeba','Bilal','Danish','Eman','Farhan','Fatima','Hamza','Hira','Hussain','Iqra','Laiba','Mahnoor','Mariam','Muhammad','Nimra','Noor','Rida','Saad','Sajid','Sana','Shayan','Sidra','Talha','Usman','Yasir','Zain','Zara']
LAST = ['Ahmed','Ali','Ansari','Baloch','Bhatti','Chandio','Khan','Malik','Memon','Mirza','Qureshi','Rind','Shah','Shaikh','Siddiqui','Soomro','Syed','Abbasi','Rajput','Jatoi']
CITIES = {
    'Sindh': ['Karachi','Hyderabad','Sukkur','Khairpur','Nawabshah','Larkana'],
    'Punjab': ['Lahore','Rawalpindi','Faisalabad','Multan','Gujranwala'],
    'Khyber Pakhtunkhwa': ['Peshawar','Abbottabad','Mardan'],
    'Balochistan': ['Quetta'],
    'Islamabad Capital Territory': ['Islamabad'],
}
UNIS = ['Shah Abdul Latif University','University of Karachi','NED University','Mehran University','FAST NUCES','COMSATS University','University of Sindh','IBA Karachi','NUST','LUMS','Punjab University','Bahria University']
EDU = ['BS Information Technology','BS Computer Science','BS Software Engineering','BBA','BS Data Science','BS Statistics','BS Economics']
DEPTS = ['Data Analytics','Business Intelligence','Software Development','Human Resources','Marketing','Finance','Product']
SOURCES = ['LinkedIn','University Portal','Referral','Internee.pk','Indeed','Direct']
GENDERS = ['Male','Female','Prefer not to say']
CANON_SKILLS = ['Python','SQL','Power BI','Excel','Pandas','Tableau','Machine Learning','Data Visualization','Communication','Statistics','Git','HTML/CSS']

CITY_VARIANTS = {
    'Karachi':['karachi','KARACHI','Karachi ','khi'], 'Hyderabad':['hyderabad','HYDERABAD','Hyd'],
    'Lahore':['lahore','LAHORE','Lhr'], 'Islamabad':['islamabad','ISLAMABAD','Isb'],
    'Sukkur':['sukkur','SUKKUR'], 'Khairpur':['khairpur','KHAIRPUR'], 'Rawalpindi':['rawalpindi','Rawalpindi '],
}
EDU_VARIANTS = {
    'BS Information Technology':['BS IT','B.S Information Technology','bs information technology'],
    'BS Computer Science':['BSCS','B.S. Computer Science','bs computer science'],
    'BS Software Engineering':['BSSE','B.S Software Engineering','bs software engineering'],
    'BS Data Science':['BSDS','bs data science'],
}
DEPT_VARIANTS = {'Data Analytics':['data analytics','Data analyst','DATA ANALYTICS'],'Business Intelligence':['BI','business intelligence'],'Human Resources':['HR','human resources'],'Software Development':['Software dev','software development']}

def phone_norm(s):
    if pd.isna(s) or str(s).strip()=='' : return None
    digits = re.sub(r'\D','',str(s))
    if digits.startswith('92') and len(digits)>=12: digits = '0'+digits[2:]
    if len(digits)==10 and digits.startswith('3'): digits='0'+digits
    return digits if len(digits)==11 else digits

def email_norm(s):
    if pd.isna(s): return None
    return re.sub(r'\s+','',str(s)).lower().strip()

def name_norm(s):
    if pd.isna(s): return None
    return ' '.join(w.capitalize() for w in str(s).strip().split())

def city_norm(s):
    if pd.isna(s) or str(s).strip()=='' : return None
    t = str(s).strip().lower()
    aliases={'khi':'karachi','hyd':'hyderabad','lhr':'lahore','isb':'islamabad','nawab shah':'nawabshah'}
    t=aliases.get(t,t)
    return t.title()

def edu_norm(s):
    if pd.isna(s) or str(s).strip()=='' : return None
    t=str(s).strip().lower().replace('.','')
    mapping={'bs it':'BS Information Technology','bs information technology':'BS Information Technology','b s information technology':'BS Information Technology','b.s information technology':'BS Information Technology','bscs':'BS Computer Science','bs computer science':'BS Computer Science','b s computer science':'BS Computer Science','bsse':'BS Software Engineering','bs software engineering':'BS Software Engineering','b s software engineering':'BS Software Engineering','bsds':'BS Data Science','bs data science':'BS Data Science'}
    return mapping.get(t, next((e for e in EDU if e.lower()==t), str(s).strip()))

def dept_norm(s):
    if pd.isna(s): return None
    t=str(s).strip().lower()
    mapping={'data analyst':'Data Analytics','data analytics':'Data Analytics','bi':'Business Intelligence','business intelligence':'Business Intelligence','hr':'Human Resources','human resources':'Human Resources','software dev':'Software Development','software development':'Software Development'}
    return mapping.get(t, str(s).strip().title())

def skills_norm(s):
    if pd.isna(s) or str(s).strip()=='' : return None
    parts=re.split(r'[,;/|]+',str(s))
    aliases={'powerbi':'Power BI','power bi':'Power BI','ms excel':'Excel','excel':'Excel','python':'Python','sql':'SQL','pandas':'Pandas','tableau':'Tableau','machine learning':'Machine Learning','ml':'Machine Learning','data viz':'Data Visualization','data visualization':'Data Visualization','communication':'Communication','statistics':'Statistics','git':'Git','html/css':'HTML/CSS','html css':'HTML/CSS'}
    vals=[]
    for p in parts:
        q=p.strip().lower()
        if not q: continue
        v=aliases.get(q, p.strip().title())
        if v not in vals: vals.append(v)
    return ', '.join(vals)

def linkedin_norm(s):
    if pd.isna(s) or str(s).strip()=='' : return None
    t=str(s).strip().replace('http://','https://')
    if t.startswith('linkedin.com'): t='https://www.'+t
    if t.startswith('www.linkedin.com'): t='https://'+t
    return t.rstrip('/')

def choose_city():
    prov = random.choices(list(CITIES), weights=[42,32,10,5,11], k=1)[0]
    return prov, random.choice(CITIES[prov])

def build_base(n=860):
    rows=[]
    start=datetime(2025,3,1,8,0)
    for i in range(n):
        fn, ln=random.choice(FIRST), random.choice(LAST)
        name=f'{fn} {ln}'
        prov, city=choose_city()
        edu=random.choices(EDU,weights=[24,20,12,10,10,8,6],k=1)[0]
        dept=random.choices(DEPTS,weights=[28,16,18,10,10,8,10],k=1)[0]
        skill_count=random.randint(2,6)
        skills=random.sample(CANON_SKILLS,skill_count)
        if dept=='Data Analytics' and not any(x in skills for x in ['Python','SQL','Power BI','Excel']): skills[0]='Excel'
        age=int(np.clip(round(np.random.normal(24.8,3.2)),18,38))
        cgpa=round(float(np.clip(np.random.normal(3.05,0.42),2.0,4.0)),2)
        exp=max(0,int(np.random.gamma(2.0,5.5)))
        stipend=int(round(np.clip(np.random.normal(30000,11000),10000,65000)/1000)*1000)
        local=f'{fn}.{ln}{i+1}'.lower()
        email=f'{local}@{random.choice(["gmail.com","outlook.com","yahoo.com","icloud.com"])}'
        phone='03'+str(random.randint(0,4))+''.join(str(random.randint(0,9)) for _ in range(8))
        ts=start+timedelta(minutes=random.randint(0,60*24*60-1))
        rows.append({
            'application_id':f'INT-{10001+i}', 'applicant_name':name, 'email':email, 'phone':phone,
            'age':age,'gender':random.choices(GENDERS,[58,39,3],k=1)[0], 'city':city,'province':prov,
            'education_level':edu,'university':random.choice(UNIS),'cgpa':cgpa,'skills':', '.join(skills),
            'experience_months':exp,'preferred_department':dept,'application_source':random.choice(SOURCES),
            'expected_stipend_pkr':stipend,'submitted_at':ts.strftime('%Y-%m-%d %H:%M:%S'),
            'linkedin_url':f'https://www.linkedin.com/in/{local.replace(".","-")}'
        })
    return pd.DataFrame(rows)

raw=build_base()

# inject formatting inconsistencies
for idx in random.sample(list(raw.index), 55): raw.at[idx,'applicant_name']=random.choice([str(raw.at[idx,'applicant_name']).upper(),str(raw.at[idx,'applicant_name']).lower(),'  '+str(raw.at[idx,'applicant_name'])+' '])
for idx in random.sample(list(raw.index), 48): raw.at[idx,'email']=random.choice([str(raw.at[idx,'email']).upper(),' '+str(raw.at[idx,'email'])+' '])
for idx in random.sample(list(raw.index), 65):
    p=str(raw.at[idx,'phone']); raw.at[idx,'phone']=random.choice([f'{p[:4]}-{p[4:7]} {p[7:]}', '+92 '+p[1:4]+' '+p[4:7]+' '+p[7:], p[:4]+' '+p[4:]])
for city, vars_ in CITY_VARIANTS.items():
    pool=raw.index[raw.city==city].tolist()
    for idx in random.sample(pool, min(8,len(pool))): raw.at[idx,'city']=random.choice(vars_)
for canon, vars_ in EDU_VARIANTS.items():
    pool=raw.index[raw.education_level==canon].tolist()
    for idx in random.sample(pool,min(10,len(pool))): raw.at[idx,'education_level']=random.choice(vars_)
for canon, vars_ in DEPT_VARIANTS.items():
    pool=raw.index[raw.preferred_department==canon].tolist()
    for idx in random.sample(pool,min(8,len(pool))): raw.at[idx,'preferred_department']=random.choice(vars_)
for idx in random.sample(list(raw.index), 80):
    vals=[v.strip() for v in str(raw.at[idx,'skills']).split(',')]
    raw.at[idx,'skills']=random.choice(['; ',' / ',' | ']).join(random.choice([v.lower(),v.replace('Power BI','powerbi'),v]) for v in vals)

# missing values: deliberate cell-level issues
missing_plan={'phone':28,'city':18,'university':24,'cgpa':16,'skills':24,'linkedin_url':30,'gender':8}
used=defaultdict(set)
for col,count in missing_plan.items():
    for idx in random.sample(list(raw.index),count):
        raw.at[idx,col]=np.nan
        used[col].add(idx)

# outliers/invalid numeric values
outlier_rows=[]
for idx in random.sample(list(raw.index), 8): raw.at[idx,'age']=random.choice([15,16,52,58]); outlier_rows.append(idx)
for idx in random.sample([i for i in raw.index if i not in outlier_rows], 7): raw.at[idx,'cgpa']=random.choice([4.8,5.2,-0.5,9.1]); outlier_rows.append(idx)
for idx in random.sample([i for i in raw.index if i not in outlier_rows], 8): raw.at[idx,'experience_months']=random.choice([96,120,180,-6]); outlier_rows.append(idx)
for idx in random.sample([i for i in raw.index if i not in outlier_rows], 8): raw.at[idx,'expected_stipend_pkr']=random.choice([0,250000,500000,-10000]); outlier_rows.append(idx)

# duplicate records - copy 40 base applications and alter superficial formatting/date/id
base_dup_idx=random.sample(list(raw.index),40)
dups=[]
for j,idx in enumerate(base_dup_idx):
    r=raw.loc[idx].copy()
    r['application_id']=f'INT-{20001+j}'
    if pd.notna(r['email']): r['email']=str(r['email']).upper()
    if pd.notna(r['phone']): r['phone']=re.sub(r'\D','',str(r['phone']))
    if pd.notna(r['applicant_name']): r['applicant_name']=str(r['applicant_name']).lower()
    try:
        dt=pd.to_datetime(r['submitted_at'])+pd.Timedelta(minutes=random.randint(2,120))
        r['submitted_at']=dt.strftime('%Y-%m-%d %H:%M:%S')
    except: pass
    dups.append(r)
raw=pd.concat([raw,pd.DataFrame(dups)],ignore_index=True)
raw=raw.sample(frac=1,random_state=SEED).reset_index(drop=True)

# CLEANING
clean=raw.copy()
log=[]
def log_change(rowid, field, before, after, issue, action):
    b='' if pd.isna(before) else str(before)
    a='' if pd.isna(after) else str(after)
    if b!=a:
        log.append({'application_id':rowid,'field':field,'original_value':b,'cleaned_value':a,'issue_type':issue,'action':action})

def apply_norm(col, func, issue='Inconsistent format', action='Standardized'):
    for i,v in clean[col].items():
        if pd.isna(v): continue
        nv=func(v)
        log_change(clean.at[i,'application_id'],col,v,nv,issue,action)
        clean.at[i,col]=nv

apply_norm('applicant_name',name_norm,'Text formatting','Trimmed and title-cased')
apply_norm('email',email_norm,'Email formatting','Lowercased and trimmed')
apply_norm('phone',phone_norm,'Phone formatting','Normalized to 11 digits')
apply_norm('city',city_norm,'City formatting','Mapped to canonical city')
apply_norm('education_level',edu_norm,'Education formatting','Mapped to canonical degree')
apply_norm('preferred_department',dept_norm,'Department formatting','Mapped to canonical department')
apply_norm('skills',skills_norm,'Skills formatting','Standardized delimiters and labels')
apply_norm('linkedin_url',linkedin_norm,'URL formatting','Normalized URL')

# missing values using defensible rules
for i in clean.index:
    rid=clean.at[i,'application_id']
    if pd.isna(clean.at[i,'gender']):
        before=clean.at[i,'gender']; clean.at[i,'gender']='Prefer not to say'; log_change(rid,'gender',before,clean.at[i,'gender'],'Missing value','Filled with neutral category')
    if pd.isna(clean.at[i,'city']):
        before=clean.at[i,'city']; prov=clean.at[i,'province']; mode=clean.loc[clean.province==prov,'city'].dropna().mode(); val=mode.iloc[0] if len(mode) else 'Unknown'; clean.at[i,'city']=val; log_change(rid,'city',before,val,'Missing value','Imputed province mode')
    if pd.isna(clean.at[i,'university']):
        before=clean.at[i,'university']; clean.at[i,'university']='Not Provided'; log_change(rid,'university',before,'Not Provided','Missing value','Filled explicit category')
    if pd.isna(clean.at[i,'cgpa']):
        before=clean.at[i,'cgpa']; val=round(float(pd.to_numeric(clean['cgpa'],errors='coerce').where(lambda x:(x>=0)&(x<=4)).median()),2); clean.at[i,'cgpa']=val; log_change(rid,'cgpa',before,val,'Missing value','Imputed valid median')
    if pd.isna(clean.at[i,'skills']):
        before=clean.at[i,'skills']; clean.at[i,'skills']='Not Specified'; log_change(rid,'skills',before,'Not Specified','Missing value','Filled explicit category')
    if pd.isna(clean.at[i,'phone']):
        before=clean.at[i,'phone']; clean.at[i,'phone']='Not Provided'; log_change(rid,'phone',before,'Not Provided','Missing value','Filled explicit category')
    if pd.isna(clean.at[i,'linkedin_url']):
        before=clean.at[i,'linkedin_url']; clean.at[i,'linkedin_url']='Not Provided'; log_change(rid,'linkedin_url',before,'Not Provided','Missing value','Filled explicit category')

# outlier treatment
valid_age=clean['age'].where(clean['age'].between(18,45)); age_med=int(valid_age.median())
valid_cg=clean['cgpa'].where(clean['cgpa'].between(0,4)); cg_med=round(float(valid_cg.median()),2)
valid_exp=clean['experience_months'].where(clean['experience_months'].between(0,60)); exp_med=int(valid_exp.median())
valid_st=clean['expected_stipend_pkr'].where(clean['expected_stipend_pkr'].between(5000,100000)); st_med=int(valid_st.median())
for i in clean.index:
    rid=clean.at[i,'application_id']
    for col,lo,hi,med in [('age',18,45,age_med),('cgpa',0,4,cg_med),('experience_months',0,60,exp_med),('expected_stipend_pkr',5000,100000,st_med)]:
        v=float(clean.at[i,col])
        if v<lo or v>hi:
            before=clean.at[i,col]; clean.at[i,col]=med; log_change(rid,col,before,med,'Outlier/invalid numeric','Replaced with valid median')

# duplicate identification after normalization
key_email=clean['email'].fillna('').astype(str)
key_phone=clean['phone'].fillna('').astype(str)
key_name=clean['applicant_name'].fillna('').astype(str)
dup_mask=clean.duplicated(subset=['email','phone'],keep='first') & (key_email!='') & (key_phone!='Not Provided')
# fallback same name/email
fallback=clean.duplicated(subset=['applicant_name','email'],keep='first') & (key_email!='')
dup_mask=dup_mask|fallback
removed=clean.loc[dup_mask].copy()
for _,r in removed.iterrows():
    log.append({'application_id':r.application_id,'field':'record','original_value':'duplicate row','cleaned_value':'removed','issue_type':'Duplicate record','action':'Removed duplicate after normalized identity match'})
clean=clean.loc[~dup_mask].reset_index(drop=True)

# structure + derived fields
for df in (raw,clean):
    df['submitted_at']=pd.to_datetime(df['submitted_at'],errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
clean['skill_count']=clean['skills'].apply(lambda x: 0 if x=='Not Specified' else len([p for p in str(x).split(',') if p.strip()]))
clean['experience_years']=(pd.to_numeric(clean['experience_months'],errors='coerce').fillna(0)/12).round(1)

# metrics and issue statistics
missing_before=int(raw.isna().sum().sum())
standard_changes=sum(1 for x in log if x['issue_type'] not in ['Missing value','Duplicate record','Outlier/invalid numeric'])
outlier_changes=sum(1 for x in log if x['issue_type']=='Outlier/invalid numeric')
dup_removed=len(removed)
raw_records=len(raw); clean_records=len(clean)

# data quality scoring
required=['applicant_name','email','phone','age','city','education_level','university','cgpa','skills','preferred_department']
complete_before=1-raw[required].isna().sum().sum()/(len(raw)*len(required))
complete_after=1-clean[required].isna().sum().sum()/(len(clean)*len(required))
uniq_before=1-(dup_removed/max(raw_records,1))
valid_before=1-(outlier_changes/max(raw_records*4,1))
std_before=1-(standard_changes/max(raw_records*8,1))
quality_before=round(100*(.40*complete_before+.25*uniq_before+.20*valid_before+.15*std_before),1)
quality_after=round(100*(.40*complete_after+.25*1+.20*1+.15*1),1)

issue_counts={'Missing Values':missing_before,'Duplicate Records':dup_removed,'Outliers':outlier_changes,'Formatting / Standardization':standard_changes}
# per-field issue count from log
field_issues=Counter(x['field'] for x in log if x['field']!='record')
# before/after per field quality percentage
field_quality=[]
for c in ['applicant_name','email','phone','age','gender','city','education_level','university','cgpa','skills','experience_months','preferred_department','expected_stipend_pkr','linkedin_url']:
    before_missing=raw[c].isna().mean()*100
    before_issues=sum(1 for x in log if x['field']==c)
    before_issue_rate=min(100, max(before_missing, before_issues/raw_records*100))
    after_missing=clean[c].isna().mean()*100
    field_quality.append({'field':c,'before_quality':round(100-before_issue_rate,1),'after_quality':round(100-after_missing,1),'issues':int(field_issues.get(c,0))})

# issue density by date based on log joined to raw ids
id_to_date={r.application_id:str(r.submitted_at)[:10] for _,r in raw.iterrows()}
daily=Counter(id_to_date.get(x['application_id'],'2025-03-01') for x in log)
issue_by_date=[{'date':d,'issues':int(daily.get(d,0))} for d in pd.date_range('2025-03-01','2025-04-29').strftime('%Y-%m-%d')]

# boxplot stats helper
def box_stats(series):
    s=pd.to_numeric(series,errors='coerce').dropna()
    q1,q2,q3=np.percentile(s,[25,50,75]); iqr=q3-q1
    lo=max(float(s.min()),q1-1.5*iqr); hi=min(float(s.max()),q3+1.5*iqr)
    outs=s[(s<lo)|(s>hi)].tolist()
    return {'min':round(lo,2),'q1':round(float(q1),2),'median':round(float(q2),2),'q3':round(float(q3),2),'max':round(hi,2),'outliers':[round(float(x),2) for x in outs[:30]]}
box={'Age':box_stats(pd.to_numeric(raw.age,errors='coerce')),'CGPA':box_stats(pd.to_numeric(raw.cgpa,errors='coerce')),'Experience':box_stats(pd.to_numeric(raw.experience_months,errors='coerce'))}

# issue profile per row for dashboard filtering
raw_norm=raw.copy()
raw_norm['city_clean']=raw_norm['city'].apply(city_norm)
raw_norm['department_clean']=raw_norm['preferred_department'].apply(dept_norm)
raw_norm['education_clean']=raw_norm['education_level'].apply(edu_norm)
raw_norm['skills_clean']=raw_norm['skills'].apply(skills_norm)
issue_ids=defaultdict(list)
for x in log: issue_ids[x['application_id']].append(x['issue_type'])

summary={
 'raw_records':raw_records,'clean_records':clean_records,'duplicates_removed':dup_removed,'missing_values_fixed':missing_before,
 'outliers_treated':outlier_changes,'standardization_fixes':standard_changes,'quality_before':quality_before,'quality_after':quality_after,
 'issues_total':sum(issue_counts.values()),'issue_counts':issue_counts,'field_quality':field_quality,'issue_by_date':issue_by_date,
 'boxplots':box,'generated_at':'2026-09-10','cleaning_steps':['Profile raw data','Handle missing values','Remove duplicates','Treat outliers','Standardize values','Validate quality','Export clean dataset']
}

# dashboard rows to keep payload lean yet fully searchable
raw_dash=[]
for _,r in raw_norm.iterrows():
    raw_dash.append({
      'application_id':r.application_id,'applicant_name':'' if pd.isna(r.applicant_name) else str(r.applicant_name),
      'email':'' if pd.isna(r.email) else str(r.email),'phone':'' if pd.isna(r.phone) else str(r.phone),
      'age':None if pd.isna(r.age) else float(r.age),'gender':'' if pd.isna(r.gender) else str(r.gender),
      'city':'' if pd.isna(r.city) else str(r.city),'city_clean':'' if pd.isna(r.city_clean) else str(r.city_clean),
      'province':str(r.province),'education_level':'' if pd.isna(r.education_level) else str(r.education_level),
      'education_clean':'' if pd.isna(r.education_clean) else str(r.education_clean),'university':'' if pd.isna(r.university) else str(r.university),
      'cgpa':None if pd.isna(r.cgpa) else float(r.cgpa),'skills':'' if pd.isna(r.skills) else str(r.skills),
      'skills_clean':'' if pd.isna(r.skills_clean) else str(r.skills_clean),'experience_months':float(r.experience_months),
      'preferred_department':str(r.preferred_department),'department_clean':str(r.department_clean),'application_source':str(r.application_source),
      'expected_stipend_pkr':float(r.expected_stipend_pkr),'submitted_at':str(r.submitted_at),'issues':issue_ids.get(r.application_id,[])
    })
clean_dash=[]
for _,r in clean.iterrows():
    clean_dash.append({k:(None if pd.isna(v) else (float(v) if isinstance(v,(np.floating,)) else int(v) if isinstance(v,(np.integer,)) else str(v))) for k,v in r.items()})

# outputs
raw.to_csv(DATA/'task5_raw_internship_applications.csv',index=False)
clean.to_csv(DATA/'task5_cleaned_internship_applications.csv',index=False)
pd.DataFrame(log).to_csv(DATA/'cleaning_log.csv',index=False)
removed.to_csv(DATA/'duplicates_removed.csv',index=False)
with open(OUT/'cleaning_summary.json','w',encoding='utf-8') as f: json.dump(summary,f,indent=2)
with open(SRC/'data.js','w',encoding='utf-8') as f:
    f.write('window.TASK5_SUMMARY = '+json.dumps(summary,separators=(',',':'))+';\n')
    f.write('window.TASK5_RAW = '+json.dumps(raw_dash,separators=(',',':'))+';\n')
    f.write('window.TASK5_CLEAN = '+json.dumps(clean_dash,separators=(',',':'))+';\n')
    f.write('window.TASK5_LOG = '+json.dumps(log,separators=(',',':'))+';\n')

print(json.dumps(summary,indent=2))
