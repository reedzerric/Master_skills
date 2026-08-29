---
name: gcloud-deployment-elite
description: 'Deploying to Google Cloud and Firebase: fixing the gcloud CLI''s Python environment conflict, controlling build context with .gcloudignore, dependency handling for Cloud Build, and a deploy workflow that does not re-upload the world. Use when a gcloud deploy fails or uploads too much, when Cloud Build cannot resolve dependencies, or when the gcloud CLI breaks against the local Python. For containers generally, use docker-elite.'
version: 1.1.0
category: core
triggers: [gcloud deploy fails, cloud build dependency error, gcloudignore, gcloud cli python error, firebase deploy, cloud run deployment, build context too large]
dependencies: [docker-elite]
inputs: [an application and a GCP or Firebase target]
outputs: [a working deploy command, a .gcloudignore, build configuration]
tags: [infrastructure, gcloud, firebase, cloud-run, django, deployment]
links: ['[[docker-elite]]', '[[github-actions-elite]]']
confidence_score: 1.0
date: '2026-08-29'
task_ref: routing-repair-batch3
---

# GCloud & Firebase Deployment Elite (2026)

## 🎯 Purpose
Guidelines for resolving common deployment hurdles when using Google Cloud SDK, Cloud Run, and Firebase Hosting.

## 🛠️ The Process / Fact

### 1. GCloud Python Environment Fix
- **Issue:** GCloud SDK may fail if its bundled Python interpreter is corrupted or missing modules (e.g., ModuleNotFoundError: No module named 'enum').
- **Resolution:** Manually set CLOUDSDK_PYTHON to a known good Python executable (e.g., from your project's virtual environment).
- **PowerShell:** ` = 'C:\path\to\venv\Scripts\python.exe'`
- **Bash:** `export CLOUDSDK_PYTHON="/path/to/venv/bin/python"`

### 2. Build Context Control (.gcloudignore)
- **Standard:** By default, GCloud Build uses .gitignore. If you need to bundle a local database (e.g., db.sqlite3) or include source directories usually ignored in git (e.g., static/), you MUST create a .gcloudignore.
- **Practice:** Remove exclusions for db.sqlite3 and /static/ (source) in .gcloudignore to ensure they are uploaded to Cloud Build and bundled into the container image.

### 3. Dependency Management for Cloud Build
- **Requirement:** Ensure all runtime dependencies used in settings.py (like python-dotenv) are explicitly listed in 
equirements.txt.
- **Verification:** Always check that python-dotenv is pinned in 
equirements.txt before submitting a build that relies on .env loading.

### 4. Optimized Deployment Workflow
- **Frontend (Firebase):** Always run collectstatic locally before irebase deploy to ensure Hosting points to current assets.
- **Backend (Cloud Run):** Use gcloud builds submit followed by gcloud run deploy to ensure the new image is immediately active and serving traffic.

## ⚠️ Known Quirks or Edge Cases
- **SQLite Persistence:** SQLite in Cloud Run is ephemeral. Data is lost when the container sleeps (after 15 mins inactivity) unless bundled into the image. For permanent storage, migrate to Google Cloud SQL (PostgreSQL/MySQL).
- **Static Assets:** If using WhiteNoise, ensure STATICFILES_DIRS and STATIC_ROOT are correctly configured in Django to avoid 404s in the live container.

## 🔗 Related Memories
- [[skills/infrastructure/docker-elite]]