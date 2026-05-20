# 🚀 Django Scaffold CLI By Morshed Nayeem

A professional, interactive command-line tool to bootstrap production-ready Django projects instantly. 

Instead of spending hours wiring up databases and background workers, this scaffold generates a clean, scalable architecture with split environments (development/production) and Docker support right out of the box.

## Features
* **Django Production Setup:** Split settings (`base.py`, `development.py`, `production.py`) routed automatically via environment variables.
* **Docker & PostgreSQL:** Ready-to-use `docker-compose.yml` with persistent database volumes.
* **Asynchronous Tasks:** Optional automated setup for Celery, Redis, and Flower.
* **Environment Separation:** Auto-generates `.env.development` and `.env.production` files.
* **Clean Architecture:** Scalable folder structure perfect for APIs and web apps.

---

## Prerequisites

Ensure you have the following installed on your machine:
* Python 3.10+
* Git
* Docker (Optional, but required for running the production environment)

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/Morshed07/Python-Scaffold--Django.git](https://github.com/Morshed07/Python-Scaffold--Django.git)
cd Python-Scaffold--Django
2. Create a virtual environment
Keep the scaffolding tool's dependencies isolated from your global system:

Bash
python -m venv venv
3. Activate the virtual environment

Windows (PowerShell):

Bash
.\venv\Scripts\Activate.ps1
Windows (Command Prompt):

Bash
venv\Scripts\activate.bat

* **Mac / Linux:**
  ```bash
  source venv/bin/activate
  
4. Install CLI requirements
Install the libraries (typer, rich, etc.) required to run the interactive prompt:

Bash
pip install -r requirements.txt
Usage
Once your virtual environment is active, launch the scaffolder:

Bash
python scaffold.py