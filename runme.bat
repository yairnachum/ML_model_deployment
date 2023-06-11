echo on
where /q docker-compose
if %errorlevel%==0 (
docker build -t assignment:latest .
docker compose up
) else (
echo Please install Docker Compose and try again.
pause
)
