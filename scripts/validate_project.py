from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
raw=pd.read_csv(ROOT/'data/task5_raw_internship_applications.csv')
clean=pd.read_csv(ROOT/'data/task5_cleaned_internship_applications.csv')
log=pd.read_csv(ROOT/'data/cleaning_log.csv')
with open(ROOT/'outputs/cleaning_summary.json',encoding='utf-8') as f: s=json.load(f)
checks=[]
def check(name,ok,detail=''):
    checks.append((name,bool(ok),detail))

check('Raw row count',len(raw)==s['raw_records'],f'{len(raw)} rows')
check('Clean row count',len(clean)==s['clean_records'],f'{len(clean)} rows')
check('Duplicates removed',len(raw)-len(clean)==s['duplicates_removed'],f'{len(raw)-len(clean)} removed')
check('Required fields complete',not clean[['applicant_name','email','phone','city','education_level','cgpa','skills']].isna().any().any())
check('Duplicate identities removed',not clean.duplicated(['email','phone']).any())
check('Age range',clean.age.between(18,45).all())
check('CGPA range',clean.cgpa.between(0,4).all())
check('Experience range',clean.experience_months.between(0,60).all())
check('Stipend range',clean.expected_stipend_pkr.between(5000,100000).all())
check('Emails standardized',(clean.email==clean.email.str.lower().str.strip()).all())
check('Dashboard file exists',(ROOT/'index.html').exists())
check('Dashboard data exists',(ROOT/'src/data.js').exists())
check('README exists',(ROOT/'README.md').exists())
check('Excel workbook exists',(ROOT/'data/task5_data_cleaning_workbook.xlsx').exists())

for name,ok,detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f' - {detail}' if detail else ''))
print(f'\nResult: {sum(x[1] for x in checks)}/{len(checks)} checks passed')
raise SystemExit(0 if all(x[1] for x in checks) else 1)
