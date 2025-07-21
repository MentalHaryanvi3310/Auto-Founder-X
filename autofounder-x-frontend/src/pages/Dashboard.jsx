import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { projectsAPI, agentsAPI } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { Alert, AlertDescription } from '../components/ui/alert';
import { 
  Plus, 
  Play, 
  Pause, 
  RotateCcw,
  TrendingUp,
  Users,
  Hammer,
  CheckCircle,
  Clock,
  AlertCircle,
  Loader2
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [startingAgents, setStartingAgents] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [projectsResponse, agentsResponse] = await Promise.all([
        projectsAPI.getProjects({ limit: 5 }),
        agentsAPI.getAgents()
      ]);

      if (projectsResponse.data.success) {
        setProjects(projectsResponse.data.projects);
      }

      if (agentsResponse.data.success) {
        setAgents(agentsResponse.data.agents);
      }
    } catch (error) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartAllAgents = async () => {
    if (projects.length === 0) {
      setError('No projects available. Create a project first.');
      return;
    }

    try {
      setStartingAgents(true);
      setError('');
      
      // Start agents for the most recent project
      const latestProject = projects[0];
      const response = await agentsAPI.startAllAgents({ project_id: latestProject.id });
      
      if (response.data.success) {
        // Refresh dashboard data to show updated agent status
        await fetchDashboardData();
      } else {
        setError(response.data.message || 'Failed to start agents');
      }
    } catch (error) {
      setError('Failed to start agents. Please try again.');
      console.error('Start agents error:', error);
    } finally {
      setStartingAgents(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'idle':
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <Play className="h-4 w-4" />;
      case 'completed':
        return <CheckCircle className="h-4 w-4" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4" />;
      case 'idle':
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name || user?.username}!
          </h1>
          <p className="text-gray-600 mt-2">
            Monitor your AI agents and track your startup projects.
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Projects</CardTitle>
              <Hammer className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{projects.length}</div>
              <p className="text-xs text-muted-foreground">
                Active startup projects
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{agents.filter(a => a.is_active).length}</div>
              <p className="text-xs text-muted-foreground">
                AI agents available
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">94%</div>
              <p className="text-xs text-muted-foreground">
                Project completion rate
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Projects */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Recent Projects</CardTitle>
                  <CardDescription>Your latest startup projects</CardDescription>
                </div>
                <Link to="/projects">
                  <Button variant="outline" size="sm">
                    <Plus className="h-4 w-4 mr-2" />
                    New Project
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {projects.length === 0 ? (
                <div className="text-center py-8">
                  <Hammer className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">No projects yet</p>
                  <Link to="/projects">
                    <Button>Create Your First Project</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {projects.map((project) => (
                    <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <h3 className="font-medium">{project.name}</h3>
                        <p className="text-sm text-gray-600">{project.description}</p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge variant="outline">{project.status}</Badge>
                          <span className="text-xs text-gray-500">
                            {new Date(project.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      <Link to={`/projects/${project.id}`}>
                        <Button variant="ghost" size="sm">View</Button>
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Agent Control Panel */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Agent Control Panel</CardTitle>
                  <CardDescription>Monitor and control your AI agents</CardDescription>
                </div>
                <Button 
                  onClick={handleStartAllAgents}
                  disabled={startingAgents || projects.length === 0}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {startingAgents ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Starting...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Start All Agents
                    </>
                  )}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {agents.slice(0, 6).map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${getStatusColor('idle')}`}>
                        {getStatusIcon('idle')}
                      </div>
                      <div>
                        <h4 className="font-medium text-sm">{agent.name}</h4>
                        <p className="text-xs text-gray-600">{agent.description}</p>
                      </div>
                    </div>
                    <Badge className={getStatusColor('idle')}>
                      Idle
                    </Badge>
                  </div>
                ))}
                
                {agents.length > 6 && (
                  <div className="text-center pt-2">
                    <Link to="/agents">
                      <Button variant="ghost" size="sm">
                        View All {agents.length} Agents
                      </Button>
                    </Link>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <Link to="/projects">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="flex items-center space-x-3 p-6">
                <Hammer className="h-8 w-8 text-primary" />
                <div>
                  <h3 className="font-medium">Projects</h3>
                  <p className="text-sm text-gray-600">Manage your startups</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/marketplace">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="flex items-center space-x-3 p-6">
                <TrendingUp className="h-8 w-8 text-primary" />
                <div>
                  <h3 className="font-medium">Marketplace</h3>
                  <p className="text-sm text-gray-600">Discover AI-built products</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/battle-arena">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="flex items-center space-x-3 p-6">
                <Users className="h-8 w-8 text-primary" />
                <div>
                  <h3 className="font-medium">Battle Arena</h3>
                  <p className="text-sm text-gray-600">Compete with others</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/profile">
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="flex items-center space-x-3 p-6">
                <RotateCcw className="h-8 w-8 text-primary" />
                <div>
                  <h3 className="font-medium">Profile</h3>
                  <p className="text-sm text-gray-600">Manage your account</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

