import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (userData) => api.put('/auth/profile', userData),
  changePassword: (passwordData) => api.post('/auth/change-password', passwordData),
};

// Projects API
export const projectsAPI = {
  getProjects: (params = {}) => api.get('/projects', { params }),
  createProject: (projectData) => api.post('/projects', projectData),
  getProject: (projectId) => api.get(`/projects/${projectId}`),
  updateProject: (projectId, projectData) => api.put(`/projects/${projectId}`, projectData),
  deleteProject: (projectId) => api.delete(`/projects/${projectId}`),
  getProjectAgents: (projectId) => api.get(`/projects/${projectId}/agents`),
  addProjectAgent: (projectId, agentData) => api.post(`/projects/${projectId}/agents`, agentData),
};

// Agents API
export const agentsAPI = {
  getAgents: () => api.get('/agents'),
  startAgent: (agentType, data) => api.post(`/agents/${agentType}/start`, data),
  startAllAgents: (data) => api.post('/agents/start-all', data),
  stopAgent: (agentType, data) => api.post(`/agents/${agentType}/stop`, data),
  getAgentStatus: (agentType, projectId) => api.get(`/agents/${agentType}/status/${projectId}`),
  
  // Specific agent endpoints
  ideation: {
    getTrends: () => api.get('/agents/ideation/trends'),
    analyzeIdea: (idea) => api.post('/agents/ideation/analyze', { idea }),
  },
  validation: {
    createSurvey: (projectId) => api.post('/agents/validation/create-survey', { project_id: projectId }),
  },
  product: {
    generateMVP: (projectId) => api.post('/agents/product/generate-mvp', { project_id: projectId }),
  },
  marketing: {
    generateLandingPage: (projectId) => api.post('/agents/marketing/landing-page', { project_id: projectId }),
  },
};

// Marketplace API
export const marketplaceAPI = {
  getItems: (params = {}) => api.get('/marketplace/items', { params }),
  getItem: (itemId) => api.get(`/marketplace/items/${itemId}`),
  publishToMarketplace: (data) => api.post('/marketplace/publish', data),
  voteItem: (itemId) => api.post('/marketplace/vote', { item_id: itemId }),
  getCategories: () => api.get('/marketplace/categories'),
  getMyItems: () => api.get('/marketplace/my-items'),
};

// Battle Arena API
export const battleArenaAPI = {
  getCompetitions: (status = 'active') => api.get('/battle-arena/competitions', { params: { status } }),
  createCompetition: (data) => api.post('/battle-arena/competitions', data),
  enterCompetition: (data) => api.post('/battle-arena/enter', data),
  getLeaderboard: (competitionId) => api.get(`/battle-arena/leaderboard/${competitionId}`),
  voteEntry: (entryId) => api.post('/battle-arena/vote', { entry_id: entryId }),
  getMyEntries: () => api.get('/battle-arena/my-entries'),
};

// Users API
export const usersAPI = {
  getUsers: () => api.get('/users'),
  createUser: (userData) => api.post('/users', userData),
  getUser: (userId) => api.get(`/users/${userId}`),
  updateUser: (userId, userData) => api.put(`/users/${userId}`, userData),
  deleteUser: (userId) => api.delete(`/users/${userId}`),
};

// Health check
export const healthAPI = {
  check: () => api.get('/health'),
  info: () => api.get('/info'),
};

export default api;

