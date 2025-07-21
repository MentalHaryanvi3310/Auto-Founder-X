# AutoFounder X - Complete Platform

**The AI Co-Founder That Never Sleeps**

AutoFounder X is a comprehensive platform that coordinates 14 specialized AI agents to turn your startup ideas into reality. From ideation to launch, our AI agents work together to build, validate, and scale your business.

## 🚀 Features

### Core Platform
- **User Authentication**: Secure registration, login, and profile management
- **Project Management**: Create, manage, and track startup projects
- **Real-time Dashboard**: Monitor AI agents and project progress
- **Responsive Design**: Works seamlessly on desktop and mobile

### 14 Specialized AI Agents
1. **Ideation Agent** - Mines trends and estimates market potential
2. **Validation Agent** - Creates surveys and validates market demand
3. **Product Agent** - Builds MVPs with API integrations
4. **Design Agent** - Generates brand kits and UI components
5. **Marketing Agent** - Creates landing pages and content
6. **Sales Agent** - Handles outreach and lead generation
7. **Analytics Agent** - Tracks performance and generates insights
8. **CRM Agent** - Manages leads and customer relationships
9. **VC Agent** - Creates pitch decks and finds investors
10. **Launch Agent** - Coordinates product launches across platforms
11. **Learning Agent** - Analyzes performance and improves strategies
12. **Legal Agent** - Generates legal documents and policies
13. **Monetization Agent** - Optimizes revenue models and pricing

### Bonus Features
- **MVP Marketplace** - Publish and discover AI-built products
- **Battle Arena** - Weekly startup competitions
- **Live Builder Mode** - Watch agents work in real-time
- **Co-Founder Clone** - AI replicates your persona

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT-based with Flask-JWT-Extended
- **API**: RESTful API with comprehensive endpoints
- **AI Agents**: Modular agent system with base classes

### Frontend (React)
- **Framework**: React 18 with Vite
- **Routing**: React Router for navigation
- **State Management**: Context API for authentication
- **HTTP Client**: Axios for API communication
- **UI**: Custom components with responsive design

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- pnpm (recommended) or npm

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd autofounder-x-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize database**
   ```bash
   python src/init_data.py
   ```

6. **Run the backend server**
   ```bash
   python src/main.py
   ```

   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd autofounder-x-frontend
   ```

2. **Install dependencies**
   ```bash
   pnpm install  # or npm install
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API base URL
   ```

4. **Run the development server**
   ```bash
   pnpm run dev  # or npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///autofounder.db
FLASK_ENV=development
PORT=5000
```

### Frontend Environment Variables (.env)
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

## 🚀 Production Deployment

### Backend Deployment
1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```
3. Configure a reverse proxy (nginx) for SSL and static files
4. Use PostgreSQL for production database

### Frontend Deployment
1. Build the production bundle:
   ```bash
   pnpm run build
   ```
2. Serve the `dist` folder using a web server (nginx, Apache, or CDN)
3. Update `VITE_API_BASE_URL` to point to your production API

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Project Endpoints
- `GET /api/projects` - Get user projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{id}` - Get specific project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Agent Endpoints
- `GET /api/agents` - Get all available agents
- `POST /api/agents/{agent_id}/start` - Start specific agent
- `POST /api/agents/start-all` - Start all agents
- `POST /api/agents/{agent_id}/stop` - Stop specific agent
- `GET /api/agents/{agent_id}/results` - Get agent results

### Marketplace Endpoints
- `GET /api/marketplace/items` - Get marketplace items
- `POST /api/marketplace/publish` - Publish to marketplace
- `POST /api/marketplace/vote` - Vote on item

### Battle Arena Endpoints
- `GET /api/battle-arena/competitions` - Get competitions
- `POST /api/battle-arena/enter` - Enter competition
- `GET /api/battle-arena/leaderboard/{id}` - Get leaderboard

## 🧪 Testing

### Backend Testing
```bash
cd autofounder-x-backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd autofounder-x-frontend
pnpm test  # or npm test
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in backend `.env` file
   - Kill existing processes: `lsof -ti:5000 | xargs kill -9`

2. **Database connection errors**
   - Ensure database file permissions are correct
   - Run `python src/init_data.py` to reinitialize

3. **CORS errors**
   - Verify frontend API base URL matches backend
   - Check CORS configuration in backend

4. **Agent execution errors**
   - Check agent logs in the backend console
   - Verify all required dependencies are installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built by Aniket and team
- Powered by AI agents and modern web technologies
- Inspired by the vision of democratizing startup creation

## 📞 Support

For support, email kadyananiket141@gmail.com or join our Discord community.

---

**AutoFounder X** - Where AI meets entrepreneurship. Build the future, one startup at a time.

