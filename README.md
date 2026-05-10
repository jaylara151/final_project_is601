# IS601 Final Project Calculator History App

## Project Overview

This project is my final project for IS601. It is a FastAPI web application that allows users to create calculations, save calculation history, update notes, delete saved calculations, and view a simple report summary.

The goal of this project was to build a full web application that uses FastAPI for the backend, SQLAlchemy for database management, HTML/CSS for the front end, Docker for deployment, and GitHub Actions for CI/CD.

## Docker Hub Image

The Docker image for this project is available here:

https://hub.docker.com/r/jaylara/final_project_is601

You can pull the image with:

```bash
docker pull jaylara/final_project_is601:latest

## Main Feature

The main feature I added is a **Calculation History and Reports** feature.

Users can:

- Create a new calculation
- Save the calculation to the database
- View all saved calculations
- View details for one calculation
- Update a note on a saved calculation
- Delete a calculation
- View a report summary

This feature demonstrates BREAD operations:

- **Browse**: View all saved calculations
- **Read**: View one calculation
- **Edit**: Update a calculation note
- **Add**: Create a new calculation
- **Delete**: Delete a saved calculation

## Project Structure

```text
final_project_is601/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── calculation.py
│   ├── routes/
│   │   └── calculations.py
│   ├── schemas/
│   │   └── calculation.py
│   └── services/
│       └── calculation_service.py
├── templates/
│   ├── index.html
│   ├── history.html
│   ├── detail.html
│   └── report.html
├── static/
│   └── style.css
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .github/workflows/
│   └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md