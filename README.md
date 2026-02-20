# Streamlit Authentication with Keycloak - Sample

A sample project demonstrating **Streamlit** dashboard with **Keycloak** OIDC authentication.

## Features

- 🔐 Keycloak OIDC authentication via `streamlit-keycloak`
- 📊 Sample dashboard with 6 chart types (area, bar, line, pie, donut, data table)
- 📈 Randomly generated sample data (revenue, sales, visitors, demographics, orders)
- 🐳 Docker Compose setup for Keycloak + PostgreSQL + Streamlit

## Quick Start

### 1. Start all services

```bash
docker compose -f docker-compose/keycloak.yml up -d --build
```

### 2. Configure Keycloak

1. Open Keycloak Admin Console: http://localhost:8080
2. Login with `admin` / `admin@123`
3. Create a new Realm called `myrealm`
4. Create a new Client:
   - **Client ID**: `streamlit-app`
   - **Client type**: OpenID Connect
   - **Valid redirect URIs**: `http://localhost:8501/*`
   - **Web origins**: `http://localhost:8501`
5. Create a test user in the realm and set a password

### 3. Access the Dashboard

Open http://localhost:8501 — you'll be redirected to Keycloak for login.

## Run Locally (without Docker)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Set environment variables before running:

```bash
export KEYCLOAK_URL=http://localhost:8080
export KEYCLOAK_REALM=myrealm
export KEYCLOAK_CLIENT_ID=streamlit-app
```

## Project Structure

```
.
├── app.py                        # Main Streamlit application
├── Dockerfile                    # Docker image for Streamlit app
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
└── docker-compose/
    └── keycloak.yml              # Docker Compose (Keycloak + Postgres + Streamlit)
```

## Sample Dashboard Contents

| Chart | Description |
|-------|-------------|
| 📈 Monthly Revenue Trend | Area chart — 12 months of revenue data |
| 🏷️ Sales by Category | Horizontal bar chart — 7 product categories |
| 🌐 Daily Website Visitors | Line chart — 30 days of traffic data |
| 🗺️ Users by Region | Donut chart — 5 geographic regions |
| 📋 Order Status | Pie chart — 5 order statuses |
| 🏆 Top 10 Products | Data table with units sold & revenue |
