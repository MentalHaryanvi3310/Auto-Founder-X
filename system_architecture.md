# AutoFounder X - Complete System Architecture

## Database Schema Design

The AutoFounder X platform requires a robust database schema to support user management, project tracking, agent operations, and all the advanced features outlined in the roadmap. The database will be designed using SQLAlchemy ORM with SQLite for the initial MVP, with the flexibility to migrate to PostgreSQL or Supabase for production scaling.

### Core Tables

#### Users Table
The users table forms the foundation of the authentication and user management system. Each user represents an entrepreneur or startup founder who will interact with the AI agents to build their ventures.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    subscription_tier VARCHAR(20) DEFAULT 'free',
    voice_profile_url VARCHAR(255),
    persona_data TEXT
);
```

The voice_profile_url field supports the "Co-Founder Clone" feature, storing the user's voice recording for AI persona replication. The persona_data field contains JSON-formatted information about the user's startup preferences, communication style, and other characteristics that agents can use to build in their voice.

#### Projects Table
Projects represent individual startup ventures that users create through the platform. Each project tracks the complete lifecycle from ideation to launch.

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    business_model VARCHAR(50),
    target_market TEXT,
    budget_range VARCHAR(50),
    timeline VARCHAR(50),
    status VARCHAR(20) DEFAULT 'planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    marketplace_votes INTEGER DEFAULT 0,
    battle_arena_score INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

The is_public field enables the MVP Marketplace feature, allowing users to publish their AI-built products for others to discover. The marketplace_votes and battle_arena_score fields support the gamification features outlined in the roadmap.

#### Agents Table
The agents table defines the 14 specialized AI agents and their current operational status across all projects.

```sql
CREATE TABLE agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    capabilities TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    version VARCHAR(20) DEFAULT '1.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Project_Agents Table
This junction table tracks which agents are assigned to specific projects and their current status within that project context.

```sql
CREATE TABLE project_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    agent_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'idle',
    current_task TEXT,
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    output_data TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (agent_id) REFERENCES agents (id)
);
```

The output_data field stores JSON-formatted results from each agent's work, enabling the Learning Agent to analyze past performance and improve future iterations.

### Agent-Specific Tables

#### Agent_Tasks Table
This table tracks individual tasks performed by agents, enabling detailed monitoring and the Live Builder Mode feature.

```sql
CREATE TABLE agent_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_agent_id INTEGER NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    task_description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result_data TEXT,
    error_message TEXT,
    FOREIGN KEY (project_agent_id) REFERENCES project_agents (id)
);
```

#### Marketplace_Items Table
Supporting the MVP Marketplace feature, this table stores products that users choose to publish publicly.

```sql
CREATE TABLE marketplace_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    is_for_sale BOOLEAN DEFAULT FALSE,
    votes INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

#### Battle_Arena_Competitions Table
This table manages the StartUp Battle Arena feature, tracking weekly competitions and leaderboards.

```sql
CREATE TABLE battle_arena_competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'upcoming',
    prize_credits INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Competition_Entries Table
Tracks which projects participate in battle arena competitions.

```sql
CREATE TABLE competition_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    votes INTEGER DEFAULT 0,
    ranking INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (competition_id) REFERENCES battle_arena_competitions (id),
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

## API Endpoints Design

The AutoFounder X platform will expose a comprehensive RESTful API that enables the frontend to interact with all backend services and agent functionalities. The API follows REST conventions with clear resource-based URLs and appropriate HTTP methods.

### Authentication Endpoints

#### POST /api/auth/register
Handles user registration with email verification and password strength validation.

Request Body:
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}
```

Response:
```json
{
    "success": true,
    "message": "User registered successfully",
    "user_id": 123,
    "token": "jwt_token_here"
}
```

#### POST /api/auth/login
Authenticates users and returns JWT tokens for session management.

Request Body:
```json
{
    "email": "string",
    "password": "string"
}
```

Response:
```json
{
    "success": true,
    "token": "jwt_token_here",
    "user": {
        "id": 123,
        "username": "string",
        "email": "string",
        "subscription_tier": "free"
    }
}
```

#### POST /api/auth/logout
Invalidates the current session token.

### User Management Endpoints

#### GET /api/users/profile
Retrieves the current user's profile information.

#### PUT /api/users/profile
Updates user profile information including voice profile for Co-Founder Clone feature.

#### POST /api/users/voice-profile
Uploads and processes voice recordings for persona replication.

### Project Management Endpoints

#### GET /api/projects
Retrieves all projects for the authenticated user with pagination support.

Query Parameters:
- page: integer (default: 1)
- limit: integer (default: 10)
- status: string (optional filter)

Response:
```json
{
    "projects": [
        {
            "id": 123,
            "name": "string",
            "description": "string",
            "status": "string",
            "created_at": "timestamp",
            "agents_status": {
                "ideation": "completed",
                "validation": "in_progress",
                "product": "pending"
            }
        }
    ],
    "total": 25,
    "page": 1,
    "pages": 3
}
```

#### POST /api/projects
Creates a new project and initializes the selected agents.

Request Body:
```json
{
    "name": "string",
    "description": "string",
    "business_model": "string",
    "target_market": "string",
    "budget_range": "string",
    "timeline": "string",
    "selected_agents": ["ideation", "validation", "product"]
}
```

#### GET /api/projects/{project_id}
Retrieves detailed information about a specific project including agent progress.

#### PUT /api/projects/{project_id}
Updates project information and settings.

#### DELETE /api/projects/{project_id}
Soft deletes a project (marks as inactive rather than permanent deletion).

### Agent Management Endpoints

#### GET /api/agents
Retrieves information about all available agents and their capabilities.

Response:
```json
{
    "agents": [
        {
            "id": 1,
            "name": "Ideation Agent",
            "type": "ideation",
            "description": "Mines Reddit, HN, Twitter, GitHub, ProductHunt for trends",
            "capabilities": ["trend_analysis", "market_research", "tam_estimation"],
            "is_active": true
        }
    ]
}
```

#### POST /api/agents/{agent_type}/start
Starts a specific agent for a project.

Request Body:
```json
{
    "project_id": 123,
    "parameters": {
        "target_market": "string",
        "keywords": ["string"]
    }
}
```

#### POST /api/agents/start-all
Starts all selected agents for a project in the correct sequence.

#### GET /api/agents/{agent_type}/status/{project_id}
Retrieves real-time status and progress for a specific agent on a project.

#### POST /api/agents/{agent_type}/stop
Stops a running agent gracefully.

### Specific Agent Endpoints

Each of the 14 agents will have specialized endpoints for their unique functionalities:

#### Ideation Agent Endpoints
- GET /api/agents/ideation/trends - Retrieves current market trends
- POST /api/agents/ideation/analyze - Analyzes a business idea for viability
- GET /api/agents/ideation/tam/{idea_id} - Calculates Total Addressable Market

#### Validation Agent Endpoints
- POST /api/agents/validation/create-survey - Creates validation surveys
- GET /api/agents/validation/results/{survey_id} - Retrieves survey results
- POST /api/agents/validation/waiting-list - Creates waiting list landing page

#### Product Agent Endpoints
- POST /api/agents/product/generate-mvp - Initiates MVP development
- GET /api/agents/product/integrations - Lists available API integrations
- POST /api/agents/product/deploy - Deploys the generated product

#### Design Agent Endpoints
- POST /api/agents/design/brand-kit - Generates complete brand identity
- POST /api/agents/design/ui-components - Creates React/Tailwind components
- GET /api/agents/design/assets/{project_id} - Retrieves design assets

#### Marketing Agent Endpoints
- POST /api/agents/marketing/landing-page - Generates landing page
- POST /api/agents/marketing/video - Creates explainer videos
- POST /api/agents/marketing/social-content - Generates social media content

#### Sales Agent Endpoints
- POST /api/agents/sales/outreach - Initiates cold outreach campaigns
- GET /api/agents/sales/leads - Retrieves lead information
- POST /api/agents/sales/funnel - Creates sales funnel

#### Analytics Agent Endpoints
- GET /api/agents/analytics/dashboard - Retrieves analytics dashboard data
- POST /api/agents/analytics/setup - Sets up tracking and analytics
- GET /api/agents/analytics/reports - Generates performance reports

#### CRM Agent Endpoints
- GET /api/agents/crm/contacts - Retrieves contact list
- POST /api/agents/crm/follow-up - Triggers automated follow-ups
- GET /api/agents/crm/pipeline - Retrieves sales pipeline data

#### VC Agent Endpoints
- POST /api/agents/vc/pitch-deck - Generates investor pitch deck
- GET /api/agents/vc/matches - Finds matching VCs using Crunchbase API
- POST /api/agents/vc/outreach - Initiates VC outreach

#### Launch Agent Endpoints
- POST /api/agents/launch/product-hunt - Submits to Product Hunt
- POST /api/agents/launch/social-media - Coordinates launch across platforms
- GET /api/agents/launch/tracking - Tracks launch performance

#### Learning Agent Endpoints
- GET /api/agents/learning/insights - Retrieves performance insights
- POST /api/agents/learning/feedback - Processes project feedback
- GET /api/agents/learning/recommendations - Provides improvement recommendations

#### Legal Agent Endpoints
- POST /api/agents/legal/documents - Generates legal documents
- GET /api/agents/legal/templates - Retrieves document templates
- POST /api/agents/legal/review - Reviews legal compliance

#### Monetization Agent Endpoints
- POST /api/agents/monetization/strategy - Develops monetization strategy
- POST /api/agents/monetization/pricing - Creates pricing page
- POST /api/agents/monetization/payment - Sets up payment processing

#### AI Integration Agent Endpoints
- GET /api/agents/ai-integration/recommendations - Recommends AI services
- POST /api/agents/ai-integration/setup - Sets up AI integrations
- GET /api/agents/ai-integration/tokens - Manages API tokens

### Marketplace Endpoints

#### GET /api/marketplace/items
Retrieves public marketplace items with filtering and sorting options.

Query Parameters:
- category: string
- sort: string (votes, views, recent)
- page: integer

#### POST /api/marketplace/publish
Publishes a project to the marketplace.

#### POST /api/marketplace/vote
Votes for a marketplace item.

#### GET /api/marketplace/item/{item_id}
Retrieves detailed information about a marketplace item.

### Battle Arena Endpoints

#### GET /api/battle-arena/competitions
Retrieves current and upcoming competitions.

#### POST /api/battle-arena/enter
Enters a project into a competition.

#### GET /api/battle-arena/leaderboard/{competition_id}
Retrieves competition leaderboard.

#### POST /api/battle-arena/vote
Votes for a competition entry.

### Real-time Endpoints

#### WebSocket /ws/project/{project_id}
Provides real-time updates for Live Builder Mode, streaming agent progress and outputs.

#### WebSocket /ws/notifications
Sends real-time notifications to users about agent completions, marketplace activity, and competition updates.

## Frontend Component Structure

The AutoFounder X frontend will be built using React with a modern component architecture that supports all the features outlined in the roadmap. The application will use React Router for navigation, Context API for state management, and Shadcn UI components for a consistent, professional interface.

### Application Structure

```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.jsx
│   │   ├── RegisterForm.jsx
│   │   └── ProtectedRoute.jsx
│   ├── dashboard/
│   │   ├── AgentDashboard.jsx
│   │   ├── ProjectList.jsx
│   │   ├── AgentCard.jsx
│   │   └── ProgressIndicator.jsx
│   ├── project/
│   │   ├── ProjectBuilder.jsx
│   │   ├── ProjectWizard.jsx
│   │   ├── AgentSelector.jsx
│   │   └── ProjectDetails.jsx
│   ├── marketplace/
│   │   ├── MarketplaceGrid.jsx
│   │   ├── ItemCard.jsx
│   │   ├── ItemDetails.jsx
│   │   └── PublishModal.jsx
│   ├── battle-arena/
│   │   ├── CompetitionList.jsx
│   │   ├── Leaderboard.jsx
│   │   ├── EntryCard.jsx
│   │   └── VotingInterface.jsx
│   ├── live-builder/
│   │   ├── LiveStream.jsx
│   │   ├── AgentOutput.jsx
│   │   ├── InterventionPanel.jsx
│   │   └── ProgressTimeline.jsx
│   ├── profile/
│   │   ├── UserProfile.jsx
│   │   ├── VoiceRecorder.jsx
│   │   └── SubscriptionManager.jsx
│   └── ui/
│       └── [Shadcn UI components]
├── contexts/
│   ├── AuthContext.jsx
│   ├── ProjectContext.jsx
│   └── WebSocketContext.jsx
├── hooks/
│   ├── useAuth.js
│   ├── useProjects.js
│   ├── useAgents.js
│   └── useWebSocket.js
├── services/
│   ├── api.js
│   ├── websocket.js
│   └── storage.js
├── utils/
│   ├── constants.js
│   ├── helpers.js
│   └── validators.js
└── pages/
    ├── Home.jsx
    ├── Dashboard.jsx
    ├── Projects.jsx
    ├── Marketplace.jsx
    ├── BattleArena.jsx
    ├── Profile.jsx
    └── NotFound.jsx
```

### Key Components

#### Authentication Components

The authentication system provides secure user registration and login with form validation and error handling.

**LoginForm.jsx** handles user authentication with email/password validation, remember me functionality, and integration with the AuthContext for session management.

**RegisterForm.jsx** manages user registration with real-time validation, password strength checking, and automatic login after successful registration.

**ProtectedRoute.jsx** wraps components that require authentication, redirecting unauthenticated users to the login page while preserving their intended destination.

#### Dashboard Components

The dashboard serves as the central hub where users monitor their projects and agent activities.

**AgentDashboard.jsx** displays the status of all 14 agents across user projects, with real-time updates via WebSocket connections. It includes the "Start All Agents" functionality that was missing in previous implementations.

**ProjectList.jsx** shows all user projects with filtering, sorting, and quick action buttons. It integrates with the ProjectContext to maintain consistent state across the application.

**AgentCard.jsx** represents individual agents with their current status, progress indicators, and control buttons. Each card displays the agent's capabilities and current task.

**ProgressIndicator.jsx** provides visual feedback for agent progress using animated progress bars and status indicators.

#### Project Builder Components

The project builder guides users through creating new startup projects with a step-by-step wizard interface.

**ProjectBuilder.jsx** serves as the main container for the project creation flow, managing state transitions between wizard steps and coordinating with the backend API.

**ProjectWizard.jsx** implements the 4-step wizard interface: Idea & Vision, Business Details, Agent Selection, and Review & Launch. Each step includes validation and the ability to navigate back and forth.

**AgentSelector.jsx** allows users to choose which of the 14 agents to include in their project, with detailed descriptions of each agent's capabilities and expected outputs.

**ProjectDetails.jsx** displays comprehensive information about existing projects, including agent progress, outputs, and the ability to modify project settings.

#### Marketplace Components

The marketplace enables users to discover, share, and purchase AI-built products.

**MarketplaceGrid.jsx** displays published projects in a responsive grid layout with filtering by category, sorting options, and search functionality.

**ItemCard.jsx** represents individual marketplace items with thumbnails, descriptions, vote counts, and quick action buttons.

**ItemDetails.jsx** provides detailed views of marketplace items including full descriptions, user reviews, and purchase options.

**PublishModal.jsx** allows users to publish their projects to the marketplace with category selection, pricing options, and visibility settings.

#### Battle Arena Components

The battle arena implements the gamification features with competitions and leaderboards.

**CompetitionList.jsx** displays current and upcoming competitions with entry requirements, prizes, and participation statistics.

**Leaderboard.jsx** shows competition rankings with real-time vote counts and participant information.

**EntryCard.jsx** represents competition entries with project information, vote buttons, and links to detailed views.

**VotingInterface.jsx** handles the voting mechanism with user authentication checks and vote tracking.

#### Live Builder Components

The live builder mode provides real-time streaming of the agent building process.

**LiveStream.jsx** displays the real-time output from agents as they work on projects, with the ability to pause, resume, and intervene in the process.

**AgentOutput.jsx** formats and displays the output from individual agents in a readable format with syntax highlighting for code and structured data.

**InterventionPanel.jsx** allows users to provide input or corrections to agents during the building process.

**ProgressTimeline.jsx** visualizes the overall project progress with completed milestones and upcoming tasks.

### State Management

The application uses React Context API for global state management, avoiding the complexity of Redux while maintaining clean data flow.

**AuthContext** manages user authentication state, login/logout functions, and user profile information. It provides authentication status to all components and handles token refresh.

**ProjectContext** maintains the current project state, project list, and project-related operations. It coordinates with the API service to keep project data synchronized.

**WebSocketContext** manages WebSocket connections for real-time updates, handling connection lifecycle, message routing, and reconnection logic.

### Custom Hooks

Custom hooks encapsulate common functionality and provide clean interfaces for components.

**useAuth** provides authentication-related functions and state, including login, logout, registration, and profile management.

**useProjects** handles project-related operations including creation, updating, deletion, and fetching project lists.

**useAgents** manages agent operations including starting, stopping, monitoring status, and retrieving agent outputs.

**useWebSocket** provides WebSocket functionality with automatic reconnection, message handling, and connection status.

### API Service Layer

The API service layer abstracts HTTP requests and provides a clean interface for components to interact with the backend.

**api.js** contains all HTTP request functions organized by feature area (auth, projects, agents, marketplace, etc.). It handles request/response formatting, error handling, and authentication token management.

**websocket.js** manages WebSocket connections with automatic reconnection, message queuing, and event handling.

**storage.js** provides local storage utilities for caching user preferences, temporary data, and offline functionality.

This comprehensive architecture ensures that all features from the roadmap can be implemented with clean separation of concerns, maintainable code, and excellent user experience. The component structure supports the complex interactions required for the AI agent coordination while maintaining simplicity for end users.

