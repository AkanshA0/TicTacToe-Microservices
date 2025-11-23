# Tic-Tac-Toe Microservices Application (Kubernetes)

This project demonstrates how a simple Flask-based monolithic Tic-Tac-Toe web application was refactored into a microservices architecture and deployed on a local Kubernetes cluster using Kind (Kubernetes-in-Docker).

---

## 1. Overview

The application is split into two independent microservices:

| Service | Description | Kubernetes Service Type |
|----------|--------------|--------------------------|
| **Frontend Service** | Serves the web UI and proxies API calls to the backend | NodePort |
| **Backend Service** | Handles Tic-Tac-Toe game logic (move validation, winner detection, etc.) | ClusterIP |

Users access the frontend via a NodePort service on `localhost:30081`.  
The frontend communicates internally with the backend through Kubernetes networking.

---

## 2. Repository Structure

├── frontend/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── Dockerfile
├── backend/
│   ├── game_service.py
│   └── Dockerfile
├── frontend.yaml
├── game-api.yaml
├── kind-config.yaml
└── README.md

---

## 3. Architecture Comparison

### Before: Monolithic Architecture

In the original version (https://github.com/AkanshA0/Flask-TTT), the entire application was built as a single Flask service.  
This single app handled both the user interface (HTML rendering) and the game logic.
<pre>┌────────────────────────────────────────────┐
│ Flask App (Single Container) │
│ ├── UI Rendering (index.html) │
│ ├── Game Logic (Python functions) │
│ └── Routes (/ , /reset) │
│ │
│ Exposed directly to users via port 5000 │
└────────────────────────────────────────────┘</pre>
**Limitations**
- UI and game logic were tightly coupled.
- Difficult to scale individual components.
- Small changes required full redeployment.
- No clear separation between presentation and business logic.

---

### After: Microservices Architecture

The monolithic app was split into two independent services:
- A **Frontend Service** responsible for serving the user interface and proxying API requests.
- A **Backend Service** that exposes a REST API for game logic.

<pre>
User Browser (http://localhost:30081)
        │
        ▼
[Frontend Service - NodePort 30081]
Flask app serves UI and proxies requests
        │
(Internal HTTP request)
        │
        ▼
[Backend Service - ClusterIP 5000]
Flask REST API with game logic
</pre>

**Benefits**
- Independent scalability (frontend and backend can scale separately).
- Backend hidden from external users (ClusterIP).
- Clear separation of concerns.
- Simplified maintenance and CI/CD.

---

## 4. Application Components

### Frontend Service
- Flask web server exposing port `5001`.
- Serves `index.html` to users.
- Proxies `/move` and `/reset` routes internally to the backend (`http://tictactoe-backend:5000`).
- Deployed as a **NodePort Service** to expose port `30081` on the host.

### Backend Service
- Flask REST API exposing endpoints:
  - `POST /api/move`
  - `GET /api/reset`
- Contains the core Tic-Tac-Toe logic.
- Deployed as a **ClusterIP Service** (internal only).
