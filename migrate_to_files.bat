@echo off
echo Migrating data from old formats to new file storage...
echo.
echo Step 1: Migrating domains from data.json
python migrate_json.py
echo.
echo Step 2: Migrating users from users.json
python migrate_json.py --users
echo.
echo Migration complete!
echo Press any key to exit...
pause >nul
