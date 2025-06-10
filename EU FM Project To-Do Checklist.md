EU FM Project To-Do Checklist
This checklist breaks down the entire EU FM project into actionable steps based on the defined sprints and prompts. Use it to track progress from initial setup to final deployment.

Sprint 0: Project Setup & Core Foundation
Goal: Initialize the frontend and backend projects, containerize them with Docker, and establish the database connection.

[ ] Prompt 1: Backend Project Initialization (Python/FastAPI)

[ ] Create the full directory structure for the backend.

[ ] Populate requirements.txt with initial dependencies.

[ ] Set up app/core/config.py for environment variables.

[ ] Implement the health-check endpoint in app/main.py.

[ ] Create the backend Dockerfile.

[ ] Prompt 2: Frontend Project Initialization (React)

[ ] Initialize the React project using Vite with TypeScript.

[ ] Add axios and react-router-dom dependencies.

[ ] Create the initial src directory structure.

[ ] Set up the basic router in App.tsx.

[ ] Create the frontend Dockerfile.

[ ] Prompt 3: Docker Compose for Local Development

[ ] Create the root docker-compose.yml file.

[ ] Define the db service using the postgres:15 image.

[ ] Define the backend service, building from its Dockerfile.

[ ] Define the frontend service, building from its Dockerfile.

[ ] Create and populate the root .env file with credentials.

[ ] Verify all services run and connect successfully with docker-compose up.

Sprint 1: User Authentication & Application Shell
Goal: Implement user registration and login. Create a protected dashboard area.

[ ] Prompt 4: Backend User Model and Registration

[ ] Set up the database connection and ORM in the backend.

[ ] Define the User model with secure password hashing.

[ ] Implement the /api/auth/register endpoint.

[ ] Prompt 5: Backend JWT Login and Protected Route

[ ] Add JWT dependencies to requirements.txt.

[ ] Create JWT utility functions (create_access_token, decode_access_token).

[ ] Implement the /api/auth/token (login) endpoint.

[ ] Implement the protected /api/users/me endpoint.

[ ] Prompt 6: Frontend Login Page and Auth Service

[ ] Create authService.ts with functions for register and login API calls.

[ ] Build the LoginPage.tsx component with a form.

[ ] Implement client-side JWT storage and create an AuthContext.

[ ] Prompt 7: Frontend Protected Routing and Dashboard Shell

[ ] Create the ProtectedRoute wrapper component.

[ ] Create the placeholder DashboardPage.tsx with a logout button.

[ ] Update App.tsx router to use the ProtectedRoute for the dashboard.

Sprint 2: Core Data Models & CRUD Operations
Goal: Build the functionality to create and view Clients and Projects.

[ ] Define Client and Project models in the backend ORM.

[ ] Create Pydantic schemas for Client and Project data transfer.

[ ] Implement API endpoint to create a new Client.

[ ] Implement API endpoint to create a new Project associated with a Client.

[ ] Implement API endpoint to list all Clients.

[ ] Implement API endpoint to list all Projects for a specific Client.

[ ] Create a "Clients" page on the frontend to display the list of clients.

[ ] On the "Clients" page, add a form to create a new client.

[ ] Create a "Project" view on the frontend that shows project details when a client is selected.

Sprint 3: Asynchronous Task Foundation & File Handling
Goal: Introduce the background task queue and enable secure file uploads for projects.

[ ] Add Celery and Redis to backend dependencies.

[ ] Configure Celery and Redis in the backend application.

[ ] Create a simple test background task (e.g., sending an email).

[ ] Define the Document model in the backend ORM.

[ ] Set up secure cloud storage (e.g., S3 bucket or equivalent).

[ ] Implement an API endpoint for securely uploading files, which stores the file in cloud storage and creates a Document record in the database.

[ ] Create a file upload component on the frontend's project detail page.

Sprint 4: AI Research Agent - V1 Implementation
Goal: Implement the first version of the AI Research Agent.

[ ] Add Google Gemini API client library to backend dependencies.

[ ] Create an "AI Service" module in the backend to manage all Gemini API calls.

[ ] Create a new background task: perform_initial_research.

[ ] Modify the file upload endpoint to trigger the perform_initial_research task.

[ ] In the background task, read the uploaded document's content.

[ ] Formulate a prompt for Gemini to analyze the text and extract key information (e.g., project themes, industry).

[ ] Call the Gemini API and parse the response.

[ ] Update the corresponding Project or Client record with the AI-extracted insights.

Sprint 5: Proposal Writing Workspace & Draft Generation
Goal: Build the "NotebookLM-style" UI and implement the "Generate First Draft" feature.

[ ] Design and build the two-panel "Workspace" UI in React.

[ ] Left panel: Display a list of AI-sourced documents and research findings.

[ ] Right panel: A text editor area for the proposal draft.

[ ] Implement a "Generate First Draft" button.

[ ] Create a new backend API endpoint: /api/projects/{project_id}/generate-draft.

[ ] This endpoint should trigger a complex background task for draft generation.

[ ] The task will perform the multi-step Gemini call chain: analyze application form structure, then write each section based on source documents.

[ ] Implement real-time updates (e.g., using WebSockets) to notify the user when the draft is ready.

[ ] Load the generated draft into the right-panel text editor.

Sprint 6: Post-Award Management Features
Goal: Implement the financial, task, and milestone tracking features.

[ ] Define Expense and Task models in the backend ORM.

[ ] Implement full CRUD API endpoints for both Expenses and project Tasks.

[ ] Create a "Financials" tab on the project detail page.

[ ] Build the UI for logging expenses and uploading receipts.

[ ] Implement the "Live Budget Dashboard" using Chart.js to visualize spending.

[ ] Create a "Work Plan" tab on the project detail page.

[ ] Build the UI to create and manage Work Packages and Tasks.

[- ] Optional V1: Implement the Gantt chart visualization.

Sprint 7: External Collaboration & Final Polish
Goal: Implement the "Magic Link" feature and conduct final testing.

[ ] Create a backend mechanism to generate and manage secure, single-use JWTs for external collaborators.

[ ] Create an API endpoint that, given a partner email and task, sends an email containing the "Magic Link".

[ ] Create a new public-facing, but secure, frontend page that validates the token from the URL.

[ ] Build the simple form on this page for the partner to submit their contribution.

[ ] Conduct thorough End-to-End (E2E) testing of all features.

[ ] Perform a final UI/UX review and polish all components for consistency and responsiveness.

[ ] Prepare for production deployment.
