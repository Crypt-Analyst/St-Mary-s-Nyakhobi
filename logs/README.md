# Logs Directory

This directory contains application logs for the St. Mary's Nyakhobi website.

## Log Files

- **django.log**: General application logs (warnings, errors)
- **security.log**: Security-related events and alerts

## Configuration

Logs are configured in `st_marys_school/settings.py`:
- **Max Size**: 15MB per file
- **Backup Count**: 10 files
- **Level**: WARNING and above
- **Format**: `{levelname} {asctime} {module} {message}`

## Log Rotation

Logs automatically rotate when they reach 15MB. The system keeps up to 10 backup files.

## Monitoring

Review logs regularly for:
- Failed login attempts
- 404 errors (potential scanning)
- 500 errors (application issues)
- CSRF failures (attack attempts)
- Unusual traffic patterns

## Security

⚠️ **Important**: Log files may contain sensitive information. 
- Do not commit logs to version control
- Restrict access to authorized personnel only
- Logs are included in `.gitignore`

## Cleanup

Old log files can be safely deleted if needed, but keep at least the last 30 days for auditing purposes.
