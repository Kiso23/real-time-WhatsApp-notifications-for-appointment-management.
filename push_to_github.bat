@echo off
echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

git init
git add .
git commit -m "Initial commit: Hospital Management System with JWT Auth and WhatsApp Notifications"
git remote add origin https://github.com/Kiso23/auth.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Done! Check: https://github.com/Kiso23/auth
echo ========================================
pause
