# 🧹 Data Cleaning & Preprocessing Dashboard
### Task 5 - Data Analyst Internship at Internee.pk

**Author:** Sajid Ali  
**Role:** Data Analyst Intern - Internee.pk  
**Education:** BS Information Technology, Shah Abdul Latif University, Khairpur  
**Location:** Sindh, Pakistan  
**Portfolio:** https://sajidexpertise.vercel.app/  
**LinkedIn:** https://www.linkedin.com/in/sajidexpertise  
**GitHub:** https://github.com/sajidexpertise

---

## Project Objective

The objective of Task 5 is to improve data accuracy by cleaning and transforming raw internship application data into a consistent, structured, and analysis-ready dataset. The project focuses on applicant demographics, education, skills, contact information, experience, department preferences, and application metadata.

The cleaning workflow follows the Task 5 requirements:

- identify and handle **missing values**;
- identify and remove **duplicate records**;
- detect and treat **outliers / invalid numeric values**;
- standardize inconsistent text, categories, contact fields, skills, and URLs;
- restructure the data for reliable downstream analysis;
- automate the workflow using **Python and Pandas**.

## Why Python (Pandas)?

The Task 5 guideline allows **Python (Pandas) or SQL** for automation. This project uses Pandas because it provides a reproducible pipeline for profiling, null handling, duplicate detection, outlier treatment, text normalization, feature creation, quality validation, and CSV export. The dashboard itself uses HTML, CSS, and JavaScript so it can be reviewed directly in a browser without requiring Power BI or a Python runtime.

## Dataset

This repository includes a **realistic portfolio dataset** created for internship training and demonstration. It does not contain confidential applicant information.

| Dataset | Records | Purpose |
|---|---:|---|
| Raw internship applications | 900 | Deliberately contains realistic quality issues |
| Cleaned applications | 860 | Final analysis-ready dataset |
| Removed duplicate records | 40 | Audit evidence for duplicate removal |
| Cleaning log | 946 actions | Field-level before/after audit trail |

### Cleaning results

- **152 missing values handled**
- **40 duplicate records removed**
- **32 invalid/outlier numeric values treated**
- **722 formatting / standardization actions**
- **860 final cleaned records**

> The quality score shown in the browser dashboard is rule-based and recalculates for the currently filtered subset. The workbook summary also contains the complete-dataset quality metrics used during validation.

## Data Dictionary

| Field | Description | Cleaning / validation |
|---|---|---|
| `application_id` | Unique application identifier | Preserved as audit key |
| `applicant_name` | Applicant name | Trimmed and converted to Title Case |
| `email` | Email address | Lowercased and whitespace removed |
| `phone` | Pakistan mobile number | Normalized to local 11-digit form; missing explicitly labeled |
| `age` | Applicant age | Valid range 18-45; invalid values replaced with valid median |
| `gender` | Applicant gender | Missing values mapped to a neutral category |
| `city` | Applicant city | Case/abbreviation mapping; missing city imputed from province mode |
| `province` | Province / territory | Structured category |
| `education_level` | Degree / qualification | Common abbreviations mapped to canonical degree names |
| `university` | University / institute | Missing values labeled `Not Provided` |
| `cgpa` | CGPA | Valid range 0-4; missing/invalid values use valid median |
| `skills` | Applicant skills | Delimiters, casing, and common aliases standardized |
| `experience_months` | Experience in months | Valid range 0-60; invalid values use valid median |
| `preferred_department` | Internship department | Aliases mapped to canonical department labels |
| `application_source` | Application source | Structured category |
| `expected_stipend_pkr` | Expected stipend | Valid range PKR 5,000-100,000 |
| `submitted_at` | Submission timestamp | Parsed and standardized |
| `linkedin_url` | LinkedIn profile | Normalized HTTPS URL or explicit missing category |
| `skill_count` | Number of standardized skills | Derived field |
| `experience_years` | Experience in years | Derived from months |

The Excel workbook contains a dedicated **Data Dictionary** sheet with these definitions.

## Cleaning Methodology

### 1. Data profiling
The pipeline profiles row count, schema, missingness, field consistency, duplicate identity patterns, and numeric validity.

### 2. Missing values
The project intentionally avoids one generic rule for all missing values:

- CGPA -> valid median;
- city -> most common city within the applicant's province;
- gender -> `Prefer not to say`;
- university -> `Not Provided`;
- skills -> `Not Specified`;
- phone / LinkedIn -> `Not Provided`.

### 3. Duplicate detection
Identity fields are normalized first. Duplicates are then detected using:

1. normalized `email + phone`;
2. fallback normalized `applicant_name + email`.

The first valid occurrence is retained and the repeated record is written to the duplicate audit file.

### 4. Outlier / invalid value treatment
The pipeline validates:

- age: **18-45**;
- CGPA: **0-4**;
- experience: **0-60 months**;
- expected stipend: **PKR 5,000-100,000**.

Values outside a valid range are replaced using the median of valid observations for that field. This is deterministic and documented in the cleaning log.

### 5. Standardization
The automation standardizes names, emails, phone formats, city aliases, education labels, department labels, skill delimiters / aliases, URLs, and timestamps.

### 6. Validation
`scripts/validate_project.py` checks row reconciliation, required fields, duplicate identities, numeric ranges, email standardization, and required project files.

## Interactive Dashboard

The dashboard is intentionally different from a standard bar-chart / donut-chart layout. The selected visual concept is implemented with:

- **cleaning pipeline visualization**;
- **data-flow / Sankey-style process view**;
- **calendar issue-density heatmap**;
- **box plots for outlier inspection**;
- **treemap-style issue composition**;
- **before-vs-after field quality heatmap**;
- **KPI progress bars**;
- **before/after correction audit table**;
- dedicated views for Profiling, Missing Values, Duplicates, Outliers, Standardization, Quality Rules, Clean Dataset, and Reports.

### Working controls

- date range;
- department;
- city;
- education level;
- skill keyword;
- global search;
- Apply Filters;
- Reset Filters;
- responsive KPI recalculation;
- clean dataset search / filtering;
- sorting and pagination;
- record details modal;
- Download Cleaned CSV;
- Print / Export Report;
- **dark / light theme switch** (dark is the default);
- responsive sidebar and mobile layout.

All visible dashboard controls are functional.

## Tools and Technologies

- Python
- Pandas
- NumPy
- HTML5
- CSS3
- JavaScript (Vanilla, no external chart dependency)
- CSV
- Microsoft Excel
- Git / GitHub
- GitHub Pages

## Folder Structure

```text
Task_5_Data_Cleaning_Preprocessing_InterneePk/
├── index.html
├── README.md
├── SUBMISSION_GUIDE.md
├── PROJECT_CHECKLIST.md
├── OPEN_DASHBOARD.bat
├── requirements.txt
├── linkedin_post.txt
├── video_demo_script.md
├── data/
│   ├── task5_raw_internship_applications.csv
│   ├── task5_cleaned_internship_applications.csv
│   ├── task5_data_cleaning_workbook.xlsx
│   ├── cleaning_log.csv
│   └── duplicates_removed.csv
├── src/
│   ├── styles.css
│   ├── app.js
│   └── data.js
├── scripts/
│   ├── generate_and_clean_data.py
│   └── validate_project.py
├── assets/
│   └── dashboard-preview.png
└── outputs/
    ├── dashboard-screenshot.png
    ├── analysis-summary.pdf
    ├── cleaning_summary.json
    ├── generation_log.txt
    └── validation_report.txt
```

## Run the Dashboard on Windows

### Fastest method - no Python required

1. Extract the ZIP file.
2. Open `Task_5_Data_Cleaning_Preprocessing_InterneePk`.
3. Double-click `index.html`.
4. Chrome, Edge, or your default browser will open the dashboard.

You may also double-click `OPEN_DASHBOARD.bat`. The default launcher opens `index.html` directly.

### Optional local server mode

If your browser/security software blocks local-file scripts, run:

```bat
OPEN_DASHBOARD.bat server
```

The launcher checks Python in this order:

1. `C:\Python314\python.exe`
2. `python`
3. `py -3`

It then opens `http://127.0.0.1:8000/`.

## Re-run the Cleaning Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the complete generation / cleaning workflow:

```bash
python scripts/generate_and_clean_data.py
```

Validate the output:

```bash
python scripts/validate_project.py
```

> Re-running the generator recreates the project datasets using the documented portfolio-data generation rules and fixed seed.

## Open on Mobile

### Easiest method
After GitHub Pages deployment, open the live dashboard URL in Chrome on Android/iOS. The layout automatically switches to the mobile navigation and single-column panels.

### Local ZIP method
Extract the ZIP using a file manager and tap `index.html`. Browser behavior for local JavaScript differs by phone, so GitHub Pages is recommended for the most consistent mobile experience.

## GitHub Upload

1. Create a new GitHub repository.
2. Use the repository name recommended in `SUBMISSION_GUIDE.md`.
3. Extract this ZIP.
4. Upload the **contents of this project folder** so `index.html` is in the repository root.
5. Commit the files to `main`.

## GitHub Pages Deployment

1. Open the repository on GitHub.
2. Go to **Settings -> Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select branch **main**.
5. Select folder **/(root)**.
6. Click **Save**.
7. Wait for GitHub Pages to publish the site.

Expected URL format:

```text
https://sajidexpertise.github.io/<repository-name>/
```

Do not use this as a final submission URL until GitHub confirms that the deployment exists.

## Main Findings

The raw internship application dataset contains four main data-quality problem groups: missing values, repeated applicant identities, invalid numeric values, and inconsistent formatting/categories. Skills required the most standardization because applicants commonly enter different delimiters and naming styles. Identity normalization is also important because apparent differences in phone/email formatting can hide true duplicates.

## Recommendations

- enforce input validation at the application-form level;
- use dropdown lists for city, education and department fields;
- validate CGPA, age, experience and stipend ranges before submission;
- normalize identity fields before performing duplicate checks;
- run the Pandas cleaning pipeline before every dashboard/report refresh;
- keep an auditable cleaning log for reproducibility.

## Known Limitations

- The dataset is a realistic portfolio dataset rather than confidential production applicant data.
- Missing phone/LinkedIn information is not fabricated; it is explicitly labeled.
- Median replacement is appropriate for this training dataset but production imputation rules should be confirmed with business owners.
- Duplicate logic is rule-based and would need identity-resolution review for a production recruitment system.

## Ethical / Data Note

No real applicant identities or confidential Internee.pk records are used. The data is designed for learning, portfolio demonstration, and reproducible analysis. Cleaning rules are documented to avoid silently changing data without an audit trail.

## Author

**Sajid Ali**  
Data Analyst Intern - Internee.pk  
Sindh, Pakistan

---

**Task 5: Data Cleaning & Preprocessing - Internee.pk Data Analyst Internship**
