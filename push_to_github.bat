@echo off
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

git add .
git commit -m "Hospital Management System with JWT Auth and WhatsApp Notifications"
git push -u origin main --force

echo.
echo ========================================
echo Done! Check: https://github.com/Kiso23/auth
echo ========================================
pause
