#!/bin/bash
if command -v docker-compose; then
  docker build -t assignment:latest .
  docker compose up
else
  echo "Please install Docker Compose and try again"
fi
