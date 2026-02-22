# Streamlit Authentication with Keycloak - Sample

A sample project demonstrating **Streamlit** dashboard with **Keycloak** OIDC authentication.

# Local Installation

Tested with Python 3.12
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update 
sudo apt install python3.12 python3.12-venv python3.12-dev -y
```

# Run Locally (without Docker)

Remember to create virtual environment first and active it.

Second copy content of `.env.example` to `.env` and update values.

Finally run following commands:

```bash
pip install -r requirements.txt
streamlit run app.py
```