---
name: gcloud-deployment-elite
description: Guidelines for resolving common deployment hurdles when using Google Cloud SDK, Cloud Run, and Firebase Hosting. Use when working with infrastructure, gcloud, firebase.
version: 1.0.0
category: core
triggers: [infrastructure, gcloud, firebase, cloud-run, django, deployment]
dependencies: [docker-elite]
inputs: [source files, project config]
outputs: [refactored code, review findings]
title: GCloud & Firebase Deployment Elite (2026)
date: 2026-03-08
task_ref: gcloud-deployment-resolutions
confidence_score: 1.0
tags: [infrastructure, gcloud, firebase, cloud-run, django, deployment]
links: ["[[skills/infrastructure/docker-elite]]"]
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