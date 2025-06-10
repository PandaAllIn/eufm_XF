EU Funds Manager (EU FM) - Implementation Blueprint & Prompts
This document provides a full, step-by-step implementation plan for the EU Funds Manager project. It is broken down into logical sprints, each containing granular prompts designed for a code-generation LLM. Each step builds directly on the previous one, ensuring an incremental and integrated development process.

Project Implementation Blueprint
The project will be built across several sprints, each delivering a self-contained, testable piece of functionality.

Sprint 0: Project Setup & Core Foundation: Initialize the frontend and backend projects, containerize them with Docker, and establish the database connection. The goal is a running local environment.

Sprint 1: User Authentication & Application Shell: Implement user registration and login. Create a protected dashboard area, ensuring a complete, secure authentication loop.

Sprint 2: Core Data Models & CRUD Operations: Build the functionality to create and view Clients and Projects. This establishes the core business logic of the application, without AI.

Sprint 3: Asynchronous Task Foundation & File Handling: Introduce the background task queue and enable secure file uploads for projects. This builds the architectural backbone for the AI agent.

Sprint 4: AI Research Agent - V1 Implementation: Implement the first version of the AI Research Agent. It will be triggered by a file upload, analyze the document using the Gemini API, and save the results.

Sprint 5: Proposal Writing Workspace & Draft Generation: Build the "NotebookLM-style" UI and implement the "Generate First Draft" feature, which will be the most complex AI interaction chain.

Sprint 6: Post-Award Management Features: Implement the financial, task, and milestone tracking features for active projects.

Sprint 7: External Collaboration & Final Polish: Implement the "Magic Link" feature for external partners and conduct final testing and refinement before deployment.

Iterative Implementation Plan & LLM Prompts
Below are the detailed, sequential prompts for a code-generation LLM.

Sprint 0: Project Setup & Core Foundation

The goal of this sprint is to have a live, running local development environment with a frontend, backend, and database all communicating.

Prompt 1: Backend Project Initialization (Python/FastAPI)

Create the initial file structure for a Python FastAPI backend application for the EU FM project.

1.  **Directory Structure:**
    - `eu_fm_backend/`
        - `app/`
            - `__init__.py`
            - `main.py`
            - `core/`
                - `__init__.py`
                - `config.py`
            - `api/`
                - `__init__.py`
        - `Dockerfile`
        - `requirements.txt`

2.  **`requirements.txt`:** Include `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`, `passlib[bcrypt]`, `psycopg2-binary`.

3.  **`app/core/config.py`:** Use Pydantic's `BaseSettings` to load environment variables for database connection details (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME).

4.  **`app/main.py`:** Initialize the FastAPI app. Create a single health-check endpoint at `/api/health` that returns `{"status": "ok"}`.

5.  **`Dockerfile`:** Create a multi-stage Dockerfile to build a production-ready container for the FastAPI application.

Prompt 2: Frontend Project Initialization (React)

Using Vite, initialize a new React application with TypeScript for the EU FM project frontend.

1.  **Initialization:** Use `npm create vite@latest eu-fm-frontend -- --template react-ts`.

2.  **Dependencies:** Add `axios` for API calls and `react-router-dom` for routing.

3.  **Directory Structure:** Create the following folders inside the `src` directory:
    - `components/`
    - `pages/`
    - `services/`
    - `hooks/`

4.  **`App.tsx`:** Set up a basic router with a single route `/` that renders a simple "Welcome to EU FM" message.

5.  **`Dockerfile`:** Create a multi-stage Dockerfile that builds the static assets using Node.js and serves them with Nginx.

Prompt 3: Docker Compose for Local Development

Create a `docker-compose.yml` file at the root of the project to orchestrate the backend, frontend, and database services.

1.  **Services:** Define three services: `backend`, `frontend`, and `db`.

2.  **`db` service:**
    - Use the official `postgres:15` image.
    - Mount a volume for data persistence (`./postgres_data:/var/lib/postgresql/data`).
    - Set environment variables for `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` using a `.env` file.

3.  **`backend` service:**
    - Build from the `./eu_fm_backend` directory.
    - Mount the source code as a volume for live reloading.
    - Set the command to `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
    - Make it depend on the `db` service.
    - Forward port `8000`.

4.  **`frontend` service:**
    - Build from the `./eu_fm_frontend` directory.
    - Mount the source code as a volume.
    - Forward port `5173`.

5.  Create a root-level `.env` file to store the shared database credentials.

Sprint 1: User Authentication & Application Shell

Goal: Implement a full registration and login flow, securing the application.

Prompt 4: Backend User Model and Registration

Based on the spec, implement the User model and a public registration endpoint.

1.  **Database Setup:** In the backend, create a database initialization module that connects to PostgreSQL and uses an ORM like SQLAlchemy or Tortoise ORM to define and create tables.

2.  **User Model:** Create the `User` model as defined in the spec (`id`, `email`, `password_hash`, `role`, `created_at`). The `password_hash` should not store plain text passwords; use `passlib.context.CryptContext` to hash passwords upon creation.

3.  **Registration Endpoint:** Create a new API route at `/api/auth/register`. It should accept an email and password, validate that the email is not already in use, hash the password, and create a new `User` record in the database.

Prompt 5: Backend JWT Login and Protected Route

Implement JWT-based authentication for logins.

1.  **JWT Utilities:** Add `python-jose[cryptography]` and `python-multipart` to `requirements.txt`. Create utility functions to `create_access_token` and `decode_access_token`. Use a `SECRET_KEY` and `ALGORITHM` from environment variables.

2.  **Login Endpoint:** Create a `/api/auth/token` endpoint. It should take a username (email) and password in a form body, verify the user's credentials against the database, and if successful, return a JWT `access_token`.

3.  **Protected Route:** Create a dependency function that verifies the JWT from the `Authorization: Bearer <token>` header. Use this dependency to protect a new endpoint, `/api/users/me`, which returns the details of the currently authenticated user.

Prompt 6: Frontend Login Page and Auth Service

Create the React components and services needed for user login.

1.  **Auth Service:** In `src/services/authService.ts`, create functions to handle API calls to the `/api/auth/register` and `/api/auth/token` endpoints using `axios`.

2.  **Login Page:** Create a new page component in `src/pages/LoginPage.tsx`. It should be a simple, unstyled form with email and password fields and a "Login" button.

3.  **State Management:** On successful login, store the returned JWT securely in the browser (e.g., in an `HttpOnly` cookie managed by the server or, for simplicity in this stage, `localStorage`). Create a simple auth context (`AuthContext`) to provide the user's authentication state to the entire application.

Prompt 7: Frontend Protected Routing and Dashboard Shell

Wire everything together to create a protected application shell.

1.  **`ProtectedRoute` Component:** Create a wrapper component that checks for the presence of a valid JWT using the `AuthContext`. If the user is authenticated, it renders its children. If not, it redirects to `/login`.

2.  **`DashboardPage` Component:** Create a simple placeholder page at `src/pages/DashboardPage.tsx`. It should display a welcome message and a "Logout" button. The logout button should clear the JWT and redirect to the login page.

3.  **Update `App.tsx`:** Modify the main router to use the `ProtectedRoute` component to wrap the `/dashboard` route. The `/login` and `/register` routes should remain public. The root `/` route should redirect to `/dashboard` if logged in, or `/login` if not.

