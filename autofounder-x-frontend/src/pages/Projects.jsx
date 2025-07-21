import React, { useState, useEffect } from 'react';
import { projectsAPI, agentsAPI } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Checkbox } from '../components/ui/checkbox';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { 
  Plus, 
  Hammer, 
  Calendar,
  DollarSign,
  Target,
  Lightbulb,
  CheckCircle,
  Palette,
  Megaphone,
  TrendingUp,
  Users,
  Rocket,
  Brain,
  Scale,
  Coins,
  Zap,
  Loader2,
  AlertCircle,
  Play
} from 'lucide-react';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState('');
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    business_model: '',
    target_market: '',
    budget_range: '',
    timeline: '',
    selected_agents: []
  });

  const agentIcons = {
    ideation: Lightbulb,
    validation: CheckCircle,
    product: Hammer,
    design: Palette,
    marketing: Megaphone,
    sales: TrendingUp,
    analytics: TrendingUp,
    crm: Users,
    vc: DollarSign,
    launch: Rocket,
    learning: Brain,
    legal: Scale,
    monetization: Coins,
    ai_integration: Zap,
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [projectsResponse, agentsResponse] = await Promise.all([
        projectsAPI.getProjects(),
        agentsAPI.getAgents()
      ]);

      if (projectsResponse.data.success) {
        setProjects(projectsResponse.data.projects);
      }

      if (agentsResponse.data.success) {
        setAgents(agentsResponse.data.agents);
      }
    } catch (error) {
      setError('Failed to load data');
      console.error('Fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAgentToggle = (agentType) => {
    setFormData(prev => ({
      ...prev,
      selected_agents: prev.selected_agents.includes(agentType)
        ? prev.selected_agents.filter(a => a !== agentType)
        : [...prev.selected_agents, agentType]
    }));
  };

  const handleCreateProject = async () => {
    try {
      setCreating(true);
      setError('');

      const response = await projectsAPI.createProject(formData);
      
      if (response.data.success) {
        setShowCreateDialog(false);
        setCurrentStep(1);
        setFormData({
          name: '',
          description: '',
          business_model: '',
          target_market: '',
          budget_range: '',
          timeline: '',
          selected_agents: []
        });
        await fetchData();
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      setError('Failed to create project');
      console.error('Create project error:', error);
    } finally {
      setCreating(false);
    }
  };

  const nextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return formData.name && formData.description;
      case 2:
        return formData.business_model && formData.budget_range && formData.timeline;
      case 3:
        return formData.selected_agents.length > 0;
      case 4:
        return true;
      default:
        return false;
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Project Name *</Label>
              <Input
                id="name"
                placeholder="Enter your startup name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                placeholder="Describe your startup idea and vision"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={4}
              />
            </div>
            <div>
              <Label htmlFor="target_market">Target Market</Label>
              <Textarea
                id="target_market"
                placeholder="Who are your target customers?"
                value={formData.target_market}
                onChange={(e) => handleInputChange('target_market', e.target.value)}
                rows={3}
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="business_model">Business Model *</Label>
              <Select onValueChange={(value) => handleInputChange('business_model', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select business model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="saas">SaaS (Software as a Service)</SelectItem>
                  <SelectItem value="marketplace">Marketplace</SelectItem>
                  <SelectItem value="ecommerce">E-commerce</SelectItem>
                  <SelectItem value="freemium">Freemium</SelectItem>
                  <SelectItem value="subscription">Subscription</SelectItem>
                  <SelectItem value="advertising">Advertising</SelectItem>
                  <SelectItem value="consulting">Consulting</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="budget_range">Budget Range *</Label>
              <Select onValueChange={(value) => handleInputChange('budget_range', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select budget range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0-1k">$0 - $1,000</SelectItem>
                  <SelectItem value="1k-5k">$1,000 - $5,000</SelectItem>
                  <SelectItem value="5k-10k">$5,000 - $10,000</SelectItem>
                  <SelectItem value="10k-25k">$10,000 - $25,000</SelectItem>
                  <SelectItem value="25k-50k">$25,000 - $50,000</SelectItem>
                  <SelectItem value="50k+">$50,000+</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="timeline">Timeline *</Label>
              <Select onValueChange={(value) => handleInputChange('timeline', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select timeline" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1-month">1 Month</SelectItem>
                  <SelectItem value="3-months">3 Months</SelectItem>
                  <SelectItem value="6-months">6 Months</SelectItem>
                  <SelectItem value="1-year">1 Year</SelectItem>
                  <SelectItem value="flexible">Flexible</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <div>
              <Label>Select AI Agents *</Label>
              <p className="text-sm text-gray-600 mb-4">
                Choose which AI agents you want to work on your project
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {agents.map((agent) => {
                const Icon = agentIcons[agent.type] || Hammer;
                const isSelected = formData.selected_agents.includes(agent.type);
                
                return (
                  <div
                    key={agent.id}
                    className={`flex items-center space-x-3 p-3 border rounded-lg cursor-pointer transition-colors ${
                      isSelected ? 'border-primary bg-primary/5' : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => handleAgentToggle(agent.type)}
                  >
                    <Checkbox
                      checked={isSelected}
                      onChange={() => handleAgentToggle(agent.type)}
                    />
                    <Icon className="h-5 w-5 text-primary" />
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{agent.name}</h4>
                      <p className="text-xs text-gray-600">{agent.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Review & Launch</h3>
            <div className="space-y-3">
              <div>
                <Label>Project Name</Label>
                <p className="text-sm">{formData.name}</p>
              </div>
              <div>
                <Label>Description</Label>
                <p className="text-sm">{formData.description}</p>
              </div>
              <div>
                <Label>Business Model</Label>
                <p className="text-sm">{formData.business_model}</p>
              </div>
              <div>
                <Label>Budget Range</Label>
                <p className="text-sm">{formData.budget_range}</p>
              </div>
              <div>
                <Label>Timeline</Label>
                <p className="text-sm">{formData.timeline}</p>
              </div>
              <div>
                <Label>Selected Agents ({formData.selected_agents.length})</Label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {formData.selected_agents.map((agentType) => {
                    const agent = agents.find(a => a.type === agentType);
                    return (
                      <Badge key={agentType} variant="outline">
                        {agent?.name || agentType}
                      </Badge>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading projects...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
            <p className="text-gray-600 mt-2">
              Manage your startup projects and AI agents
            </p>
          </div>
          
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                New Project
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Create New Project</DialogTitle>
                <DialogDescription>
                  Step {currentStep} of 4: Build your startup with AI agents
                </DialogDescription>
              </DialogHeader>
              
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="py-4">
                {renderStep()}
              </div>

              <div className="flex items-center justify-between">
                <Button
                  variant="outline"
                  onClick={prevStep}
                  disabled={currentStep === 1}
                >
                  Previous
                </Button>
                
                <div className="flex space-x-2">
                  {[1, 2, 3, 4].map((step) => (
                    <div
                      key={step}
                      className={`w-3 h-3 rounded-full ${
                        step === currentStep
                          ? 'bg-primary'
                          : step < currentStep
                          ? 'bg-primary/50'
                          : 'bg-gray-200'
                      }`}
                    />
                  ))}
                </div>

                {currentStep < 4 ? (
                  <Button
                    onClick={nextStep}
                    disabled={!canProceed()}
                  >
                    Next
                  </Button>
                ) : (
                  <Button
                    onClick={handleCreateProject}
                    disabled={creating || !canProceed()}
                  >
                    {creating ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Creating...
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4 mr-2" />
                        Start Building
                      </>
                    )}
                  </Button>
                )}
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Projects Grid */}
        {projects.length === 0 ? (
          <div className="text-center py-12">
            <Hammer className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No projects yet</h3>
            <p className="text-gray-600 mb-6">
              Create your first project and let AI agents build your startup
            </p>
            <Button onClick={() => setShowCreateDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Project
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Card key={project.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{project.name}</CardTitle>
                    <Badge variant="outline">{project.status}</Badge>
                  </div>
                  <CardDescription>{project.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Target className="h-4 w-4" />
                      <span>{project.business_model}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <DollarSign className="h-4 w-4" />
                      <span>{project.budget_range}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Calendar className="h-4 w-4" />
                      <span>{project.timeline}</span>
                    </div>
                    
                    {/* Agent Status */}
                    {project.agents_status && Object.keys(project.agents_status).length > 0 && (
                      <div className="pt-3 border-t">
                        <p className="text-sm font-medium mb-2">Agent Status</p>
                        <div className="flex flex-wrap gap-1">
                          {Object.entries(project.agents_status).slice(0, 3).map(([agentType, status]) => (
                            <Badge key={agentType} variant="secondary" className="text-xs">
                              {agentType}: {status}
                            </Badge>
                          ))}
                          {Object.keys(project.agents_status).length > 3 && (
                            <Badge variant="secondary" className="text-xs">
                              +{Object.keys(project.agents_status).length - 3} more
                            </Badge>
                          )}
                        </div>
                      </div>
                    )}
                    
                    <div className="pt-3">
                      <Button variant="outline" className="w-full">
                        View Details
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Projects;

