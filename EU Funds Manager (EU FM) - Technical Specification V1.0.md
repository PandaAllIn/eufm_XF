EU Funds Manager (EU FM) - Technical Specification V1.0
Document Version: 1.0

Date: June 9, 2025

Status: Ready for Development

1. Project Vision & Goals
The European Union Funds Manager (EU FM) is an advanced, AI-powered software platform designed to serve as the core operational tool for a consulting business that helps clients secure and manage non-refundable EU funds.

Goal 1 (Efficiency): Radically reduce the time and effort required to identify funding opportunities and draft high-quality proposals.

Goal 2 (Effectiveness): Increase the success rate of grant applications by leveraging AI for deep research and data-driven insights.

Goal 3 (Control): Provide a centralized, all-in-one platform for managing the entire grant lifecycle, from discovery to final reporting, ensuring compliance and control.

Goal 4 (Adaptability): Build a flexible core platform that can be extended and integrated with other business systems in the future.

2. System Architecture
A modern, scalable web application architecture is recommended. Given the initial single-user scope, a monolithic backend approach is appropriate, but with a strict separation of concerns to allow for future evolution into microservices if needed.

Frontend: A single-page application (SPA) built with a modern JavaScript framework like React or Vue.js. This will provide a responsive, dynamic user experience. Component libraries like Material-UI or Tailwind CSS should be used for a polished and consistent UI.

Backend: A RESTful or GraphQL API built with a robust framework like Python (Django/FastAPI) or Node.js (Express.js). Python is recommended due to its strong ecosystem of data science and AI libraries.

Database: A relational database like PostgreSQL is required to enforce data integrity and manage relationships between entities.

AI Service Layer: A dedicated module within the backend responsible for all interactions with the Google Gemini API. This layer will handle prompt engineering, API requests, response parsing, and error handling for all AI-powered features.

Task Queue & Worker: For long-running processes like the AI Research Agent's web scraping and document analysis, a task queue (e.g., Celery with Redis or RabbitMQ) is essential. This prevents the main API from timing out and allows for asynchronous background processing.

3. Data Models & Handling
Data security is paramount. All sensitive client data and uploaded documents must be encrypted at rest using industry-standard AES-256 encryption.

Core Data Entities:

User

id: UUID (Primary Key)

email: String (Encrypted)

password_hash: String

role: String (Enum: ADMINISTRATOR)

created_at: DateTime

Client

id: UUID (Primary Key)

name: String (Encrypted)

structured_data: JSONB (Encrypted, for AI-parsed info like industry, size, etc.)

created_at: DateTime

Project

id: UUID (Primary Key)

client_id: UUID (Foreign Key to Client)

name: String

status: String (Enum: DISCOVERY, PROPOSAL, ACTIVE, COMPLETED, ARCHIVED)

created_at: DateTime

Document

id: UUID (Primary Key)

project_id: UUID (Foreign Key to Project)

file_name: String

storage_path: String (Path to encrypted file in cloud storage)

source_type: String (Enum: CLIENT_UPLOAD, AI_RESEARCH, APPLICATION_FORM)

content_hash: String (SHA-256 hash to detect duplicates)

uploaded_at: DateTime

FundingOpportunity

id: UUID (Primary Key)

project_id: UUID (Foreign Key to Project)

call_name: String

call_url: String

deadline: DateTime

total_success_score: Float

raw_data: JSONB (All scraped details of the fund)

status: String (Enum: SUGGESTED, IN_PROPOSAL, WON, LOST)

Expense

id: UUID (Primary Key)

project_id: UUID (Foreign Key to Project)

description: String

amount: Decimal

currency: String (e.g., 'EUR', 'RON')

expense_date: Date

budget_category: String

receipt_document_id: UUID (Foreign Key to Document)

Task (for Work Plans)

id: UUID (Primary Key)

project_id: UUID (Foreign Key to Project)

title: String

description: Text

work_package: String

due_date: DateTime

status: String (Enum: TODO, IN_PROGRESS, DONE)

assigned_to: String (Partner name/email)

4. Detailed Feature Breakdown & Logic
This section expands upon the functional specification with implementation details.

Module 1: AI Research & Discovery

AI Research Agent (Background Task):

When a project is created, a background job must be dispatched to the task queue.

The worker will execute the research logic:

Formulate search queries based on the client's profile.

Use web scraping libraries (e.g., Python's BeautifulSoup, Scrapy) and potentially browser automation tools (e.g., Playwright) to gather data.

Call the Gemini API for summarization and analysis of scraped content.

Populate the FundingOpportunity and Document tables.

Update the project status to DISCOVERY_COMPLETED and notify the user.

Ranking Logic: The Total Success Score should be a weighted calculation. For V1: (AlignmentFit * 0.7) + (BudgetAdequacy * 0.3). These sub-scores will be determined by Gemini based on specific prompts.

Module 2: Proposal Writing Workspace

Draft Generation: This will be a multi-step Gemini API call chain.

First, Gemini must analyze the structure of the uploaded application form to create an outline (JSON).

For each section in the outline, a new prompt must be engineered that instructs Gemini to answer that specific section's question using the provided source documents.

The results are then stitched together into a single document.

AI Co-Pilot: The frontend will capture the user's highlighted text and the natural language command. This context will be sent to the backend, which will create a specific, targeted prompt for the Gemini API to perform the requested text manipulation.

Module 3: Post-Award Project Management

Magic Link for Reporting:

Generate a cryptographically secure, single-use token (JWT is a good option) associated with a specific reporting task and partner email.

Store the token hash in the database.

The link in the email will include this token.

When the partner accesses the link, the backend validates the token, displays the submission form, and invalidates the token upon successful submission.

5. Error Handling & Logging Strategy
Backend API:

All API responses should follow a consistent format.

Success (2xx): { "data": { ... } }

Error (4xx/5xx): { "error": { "code": "AUTH_ERROR", "message": "Invalid credentials provided." } }

All errors, exceptions, and API calls to third-party services (especially Gemini) must be logged with a structured logging library (e.g., Loguru for Python). Logs should include a request ID to trace a single request through the system.

Frontend UI:

Never use browser alert() or confirm() dialogs.

Use a centralized notification system (e.g., "toast" messages) to display non-blocking success or error messages to the user (e.g., "Project created successfully," "Failed to upload document.").

For critical errors, use a modal dialog to provide more information and suggested actions.

6. Testing Plan
A multi-layered testing strategy is required to ensure quality and reliability.

Unit Tests:

Focus: Individual functions, especially business logic in the backend.

Examples: Test the Total Success Score calculation, data validation rules on models, specific API endpoint logic.

Tools: pytest (Python), Jest (JavaScript).

Integration Tests:

Focus: The interaction between different components.

Examples: Test that a frontend form submission correctly calls the backend API and stores data in the database. Test the full flow of a background job from API dispatch to task completion.

Tools: pytest with database fixtures, Jest with mock API servers.

End-to-End (E2E) Tests:

Focus: Simulating a real user's journey through the application in a browser.

Examples: A single test that logs in, creates a client, starts a project, validates the research results, and logs out.

Tools: Cypress or Playwright.

User Acceptance Testing (UAT):

Focus: Manual testing by the end-user (you) on a staging environment to confirm the software meets all business requirements specified in this document. This is the final step before deployment.

7. Deployment & Infrastructure
Cloud Provider: A major cloud provider like Google Cloud Platform (GCP), AWS, or Azure is recommended. GCP is a natural choice given the reliance on the Gemini API.

Containerization: The frontend and backend applications should be containerized using Docker. This ensures consistency between development, testing, and production environments. Docker Compose should be used to manage the local development environment.

Environments: A minimum of two environments should be maintained:

Staging: A clone of the production environment for UAT.

Production: The live environment for the end-user.
