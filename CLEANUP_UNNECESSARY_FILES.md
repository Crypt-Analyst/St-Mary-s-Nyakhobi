# Unnecessary Files to Delete - Cleanup List

## Files to DELETE (Obsolete/Redundant/Unused)

### 1. Duplicate/Old Setup Scripts
- ❌ `setup.bat` - Old Windows batch script (replaced by PowerShell)
- ❌ `setup.ps1` - Generic setup (not used)
- ❌ `setup_nyakhobi.ps1` - Old school-specific setup
- ❌ `status.bat` - Old status checker

### 2. Redundant Documentation (Keep only essential)
- ❌ `ADMIN_FEATURE_AUDIT.md` - Audit document (task completed)
- ❌ `ADMIN_PORTAL_INTEGRATION.md` - Integration doc (integrated now)
- ❌ `ADMIN_VISUAL_GUIDE.md` - Redundant with ADMIN_USAGE_GUIDE
- ❌ `ADMIN_WORKFLOW_GUIDE.md` - Redundant with ADMIN_USAGE_GUIDE
- ❌ `DEPLOYMENT_EMERGENCY_FIX.md` - Old emergency fix doc
- ❌ `RENDER_DEPLOYMENT_FIX.md` - Old deployment fix
- ❌ `SECURITY_CHECKLIST_STATUS.md` - Checklist completed
- ❌ `SECURITY_IMPLEMENTATION_COMPLETE.md` - Implementation done
- ❌ `SECURITY_SUMMARY.md` - Redundant with SECURITY.md
- ❌ `NYAKHOBI_SETUP_GUIDE.md` - Old setup guide

### 3. Obsolete Data/Population Scripts
- ❌ `populate_database.py` - Old population script (data already in DB)
- ❌ `populate_news.py` - Old news populator
- ❌ `populate_portal.py` - Old portal populator
- ❌ `simple_portal_data.py` - Old data script
- ❌ `cleanup_events.py` - One-time cleanup script
- ❌ `update_principal.py` - One-time update script
- ❌ `update_school_info.py` - One-time update script
- ❌ `create_superuser.py` - Use Django command instead

### 4. Old Data Files (JSON fixtures - data in database now)
- ❌ `basic_data.json` - Old fixture
- ❌ `comprehensive_data.json` - Old fixture
- ❌ `sample_data.json` - Old fixture
- ❌ `school_data_fixture.json` - Old fixture

### 5. Old Images in Root (should be in media/)
- ❌ `CamScanner 30-09-2025 15.34.pdf` - Move to media or delete
- ❌ `CamScanner 30-09-2025 15.35.pdf` - Move to media or delete
- ❌ `CamScanner 30-09-2025 15.37.pdf` - Move to media or delete
- ❌ `IMG-20250930-WA0007.jpg` - Move to media or delete
- ❌ `WhatsApp Image 2025-09-30 at 15.45.22.jpeg` - Move to media or delete
- ❌ `WhatsApp Image 2025-09-30 at 15.45.23.jpeg` - Move to media or delete

### 6. Old Text Files
- ❌ `START_HERE.txt` - Obsolete starter file

---

## Files to KEEP (Essential)

### Documentation (Keep)
- ✅ `README.md` - Main project documentation
- ✅ `SETUP.md` - Setup instructions
- ✅ `DEPLOYMENT.md` - Deployment guide
- ✅ `DEPLOY_NOW.md` - Quick deploy reference
- ✅ `ADMIN_USAGE_GUIDE.md` - Admin portal usage (comprehensive)
- ✅ `ADMIN_COMPLETE_FEATURES.md` - Feature list
- ✅ `ADMIN_PORTAL_GUIDE.md` - Portal guide
- ✅ `NEWS_DISPLAY_FIX.md` - Recent fix documentation
- ✅ `CBC_SENIOR_SECONDARY_UPDATE.md` - Latest update doc
- ✅ `CBC_SUBJECTS_LIST.md` - New subjects list
- ✅ `CLOUDINARY_SETUP.md` - Media storage guide
- ✅ `SUPABASE_DATABASE_INFO.md` - Database info
- ✅ `RENDER_BUILD_COMMANDS.md` - Build commands
- ✅ `SECURITY.md` - Security documentation
- ✅ `QUICKSTART_SECURITY.md` - Security quick start

### Configuration Files (Keep)
- ✅ `.env` - Environment variables (local)
- ✅ `.env.example` - Example env file
- ✅ `.gitignore` - Git ignore rules
- ✅ `build.sh` - Render build script
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `manage.py` - Django management

### Database & Media (Keep)
- ✅ `db.sqlite3` - Local database (gitignored)
- ✅ `media/` - Uploaded media files
- ✅ `static/` - Static files
- ✅ `staticfiles/` - Collected static files
- ✅ `logs/` - Log files

### Django Apps (Keep All)
- ✅ `academics/` - Academics app
- ✅ `admin_portal/` - Admin portal app
- ✅ `admissions/` - Admissions app
- ✅ `contact/` - Contact app
- ✅ `events/` - Events app
- ✅ `faculty/` - Faculty app
- ✅ `home/` - Home app
- ✅ `news/` - News app (legacy, might merge with events)
- ✅ `portal/` - Student portal app
- ✅ `st_marys_school/` - Main project folder
- ✅ `templates/` - All templates

---

## Recommended Actions

### Phase 1: Safe Deletion (Do Now)
Delete these files - they're definitely not needed:

```powershell
# Documentation cleanup
Remove-Item "ADMIN_FEATURE_AUDIT.md"
Remove-Item "ADMIN_PORTAL_INTEGRATION.md"
Remove-Item "ADMIN_VISUAL_GUIDE.md"
Remove-Item "ADMIN_WORKFLOW_GUIDE.md"
Remove-Item "DEPLOYMENT_EMERGENCY_FIX.md"
Remove-Item "RENDER_DEPLOYMENT_FIX.md"
Remove-Item "SECURITY_CHECKLIST_STATUS.md"
Remove-Item "SECURITY_IMPLEMENTATION_COMPLETE.md"
Remove-Item "SECURITY_SUMMARY.md"
Remove-Item "NYAKHOBI_SETUP_GUIDE.md"

# Old scripts
Remove-Item "setup.bat"
Remove-Item "setup.ps1"
Remove-Item "setup_nyakhobi.ps1"
Remove-Item "status.bat"
Remove-Item "populate_database.py"
Remove-Item "populate_news.py"
Remove-Item "populate_portal.py"
Remove-Item "simple_portal_data.py"
Remove-Item "cleanup_events.py"
Remove-Item "update_principal.py"
Remove-Item "update_school_info.py"
Remove-Item "create_superuser.py"

# Old data files
Remove-Item "basic_data.json"
Remove-Item "comprehensive_data.json"
Remove-Item "sample_data.json"
Remove-Item "school_data_fixture.json"

# Old text file
Remove-Item "START_HERE.txt"
```

### Phase 2: Move Media Files (Do Now)
Move images/PDFs to proper media folder or delete if not needed:

```powershell
# Move to media folder or delete
Remove-Item "CamScanner 30-09-2025 15.34.pdf"
Remove-Item "CamScanner 30-09-2025 15.35.pdf"
Remove-Item "CamScanner 30-09-2025 15.37.pdf"
Remove-Item "IMG-20250930-WA0007.jpg"
Remove-Item "WhatsApp Image 2025-09-30 at 15.45.22.jpeg"
Remove-Item "WhatsApp Image 2025-09-30 at 15.45.23.jpeg"
```

### Phase 3: Optional Cleanup (Consider Later)

**Merge/Consolidate Apps?**
- Consider merging `news/` app into `events/` app (both handle announcements)
- Or merge into `admin_portal/` since NewsAnnouncement model is there

---

## Summary

### Total Files to Delete: ~35 files

**Categories**:
- Documentation: 10 files
- Scripts: 12 files
- Data files: 4 files
- Media files: 6 files
- Text files: 1 file

**Disk Space Saved**: ~5-10 MB (mainly from PDFs and images)

**Benefits**:
- Cleaner project structure
- Easier to navigate
- Less confusion about which files to use
- Faster git operations

---

## Execute Cleanup

Run this PowerShell script to clean up everything at once:

```powershell
# Navigate to project directory
cd "C:\Users\Afronic\Desktop\St Mary's WEB"

# Documentation cleanup
Remove-Item "ADMIN_FEATURE_AUDIT.md" -ErrorAction SilentlyContinue
Remove-Item "ADMIN_PORTAL_INTEGRATION.md" -ErrorAction SilentlyContinue
Remove-Item "ADMIN_VISUAL_GUIDE.md" -ErrorAction SilentlyContinue
Remove-Item "ADMIN_WORKFLOW_GUIDE.md" -ErrorAction SilentlyContinue
Remove-Item "DEPLOYMENT_EMERGENCY_FIX.md" -ErrorAction SilentlyContinue
Remove-Item "RENDER_DEPLOYMENT_FIX.md" -ErrorAction SilentlyContinue
Remove-Item "SECURITY_CHECKLIST_STATUS.md" -ErrorAction SilentlyContinue
Remove-Item "SECURITY_IMPLEMENTATION_COMPLETE.md" -ErrorAction SilentlyContinue
Remove-Item "SECURITY_SUMMARY.md" -ErrorAction SilentlyContinue
Remove-Item "NYAKHOBI_SETUP_GUIDE.md" -ErrorAction SilentlyContinue

# Old scripts
Remove-Item "setup.bat" -ErrorAction SilentlyContinue
Remove-Item "setup.ps1" -ErrorAction SilentlyContinue
Remove-Item "setup_nyakhobi.ps1" -ErrorAction SilentlyContinue
Remove-Item "status.bat" -ErrorAction SilentlyContinue
Remove-Item "populate_database.py" -ErrorAction SilentlyContinue
Remove-Item "populate_news.py" -ErrorAction SilentlyContinue
Remove-Item "populate_portal.py" -ErrorAction SilentlyContinue
Remove-Item "simple_portal_data.py" -ErrorAction SilentlyContinue
Remove-Item "cleanup_events.py" -ErrorAction SilentlyContinue
Remove-Item "update_principal.py" -ErrorAction SilentlyContinue
Remove-Item "update_school_info.py" -ErrorAction SilentlyContinue
Remove-Item "create_superuser.py" -ErrorAction SilentlyContinue

# Old data files
Remove-Item "basic_data.json" -ErrorAction SilentlyContinue
Remove-Item "comprehensive_data.json" -ErrorAction SilentlyContinue
Remove-Item "sample_data.json" -ErrorAction SilentlyContinue
Remove-Item "school_data_fixture.json" -ErrorAction SilentlyContinue

# Media files in root
Remove-Item "CamScanner 30-09-2025 15.34.pdf" -ErrorAction SilentlyContinue
Remove-Item "CamScanner 30-09-2025 15.35.pdf" -ErrorAction SilentlyContinue
Remove-Item "CamScanner 30-09-2025 15.37.pdf" -ErrorAction SilentlyContinue
Remove-Item "IMG-20250930-WA0007.jpg" -ErrorAction SilentlyContinue
Remove-Item "WhatsApp Image 2025-09-30 at 15.45.22.jpeg" -ErrorAction SilentlyContinue
Remove-Item "WhatsApp Image 2025-09-30 at 15.45.23.jpeg" -ErrorAction SilentlyContinue

# Old text file
Remove-Item "START_HERE.txt" -ErrorAction SilentlyContinue

Write-Host "Cleanup complete! Removed ~35 obsolete files." -ForegroundColor Green
```

---

**Last Updated**: October 5, 2025  
**Status**: Ready for execution
