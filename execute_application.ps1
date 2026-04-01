# Powershell equivalent of execute_application.sh

# Keep up to date
git pull

# Install Dependencies
python -m venv .venv
.\.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Get variables from job_description.txt
# $COMPANY_NAME = python utils/get_company_name.py
# $JOB_TITLE = python utils/get_job_title.py

# Generate Resume and Cover Letter
# python src/main.py

# # Store and save resume and cover letter
# .\cleanup_scripts\store_resume_and_cl.ps1 $COMPANY_NAME $JOB_TITLE
# python cleanup_scripts\save_to_csv.py $COMPANY_NAME $JOB_TITLE

# Write-Host "Application successfully executed"

# Break down
deactivate
git add .
git commit -m "(Automated Commit) Job application updated"
git push