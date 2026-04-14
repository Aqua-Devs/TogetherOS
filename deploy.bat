@echo off
echo ================================================
echo TOGETHEROS - AUTO DEPLOY TO GITHUB
echo ================================================
echo.

echo [1/4] Checking git status...
git status
echo.

echo [2/4] Adding changes...
git add .
echo.

echo [3/4] Committing changes...
git commit -m "Fix database path for Render deployment"
echo.

echo [4/4] Pushing to GitHub...
git push origin main
echo.

echo ================================================
echo DONE! Render will auto-deploy in 2-3 minutes.
echo ================================================
echo.
echo Check status at: https://dashboard.render.com
echo.
pause
