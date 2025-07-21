import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { 
  Bot, 
  Lightbulb, 
  CheckCircle, 
  Hammer, 
  Palette, 
  Megaphone, 
  TrendingUp,
  Users,
  DollarSign,
  Rocket,
  Brain,
  Scale,
  Coins,
  Zap,
  ArrowRight,
  Star,
  Trophy,
  Store
} from 'lucide-react';

const Home = () => {
  const { isAuthenticated } = useAuth();

  const agents = [
    { name: 'Ideation Agent', icon: Lightbulb, description: 'Mines trends and estimates market potential', color: 'bg-yellow-100 text-yellow-800' },
    { name: 'Validation Agent', icon: CheckCircle, description: 'Creates surveys and validates market demand', color: 'bg-green-100 text-green-800' },
    { name: 'Product Agent', icon: Hammer, description: 'Builds MVPs with API integrations', color: 'bg-blue-100 text-blue-800' },
    { name: 'Design Agent', icon: Palette, description: 'Generates brand kits and UI components', color: 'bg-purple-100 text-purple-800' },
    { name: 'Marketing Agent', icon: Megaphone, description: 'Creates landing pages and content', color: 'bg-pink-100 text-pink-800' },
    { name: 'Sales Agent', icon: TrendingUp, description: 'Handles outreach and lead generation', color: 'bg-orange-100 text-orange-800' },
    { name: 'Analytics Agent', icon: TrendingUp, description: 'Tracks performance and generates insights', color: 'bg-indigo-100 text-indigo-800' },
    { name: 'CRM Agent', icon: Users, description: 'Manages leads and customer relationships', color: 'bg-cyan-100 text-cyan-800' },
    { name: 'VC Agent', icon: DollarSign, description: 'Creates pitch decks and finds investors', color: 'bg-emerald-100 text-emerald-800' },
    { name: 'Launch Agent', icon: Rocket, description: 'Coordinates product launches across platforms', color: 'bg-red-100 text-red-800' },
    { name: 'Learning Agent', icon: Brain, description: 'Analyzes performance and improves strategies', color: 'bg-violet-100 text-violet-800' },
    { name: 'Legal Agent', icon: Scale, description: 'Generates legal documents and policies', color: 'bg-gray-100 text-gray-800' },
    { name: 'Monetization Agent', icon: Coins, description: 'Optimizes revenue models and pricing', color: 'bg-amber-100 text-amber-800' },
    { name: 'AI Integration Agent', icon: Zap, description: 'Recommends and integrates AI services', color: 'bg-lime-100 text-lime-800' },
  ];

  const features = [
    {
      title: 'MVP Marketplace',
      description: 'Publish your AI-built products for others to discover, vote, and purchase.',
      icon: Store,
    },
    {
      title: 'Co-Founder Clone',
      description: 'AI replicates your persona from voice recordings to build in your style.',
      icon: Bot,
    },
    {
      title: 'Live Builder Mode',
      description: 'Watch agents work in real-time and intervene when needed.',
      icon: Rocket,
    },
    {
      title: 'StartUp Battle Arena',
      description: 'Compete weekly with other startups for funding and recognition.',
      icon: Trophy,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              The AI Co-Founder That{' '}
              <span className="text-primary">Never Sleeps</span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              You dream it, I build it. AutoFounder X coordinates 14 specialized AI agents to turn your startup ideas into reality.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              {isAuthenticated ? (
                <Link to="/dashboard">
                  <Button size="lg" className="px-8">
                    Go to Dashboard
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              ) : (
                <>
                  <Link to="/register">
                    <Button size="lg" className="px-8">
                      Get Started Free
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button variant="outline" size="lg">
                      Sign In
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              14 Specialized AI Agents
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Each agent is an expert in their domain, working together to build your startup from idea to launch.
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-6 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-2 xl:grid-cols-3">
            {agents.map((agent, index) => {
              const Icon = agent.icon;
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${agent.color}`}>
                        <Icon className="h-6 w-6" />
                      </div>
                      <CardTitle className="text-lg">{agent.name}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <CardDescription>{agent.description}</CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 sm:py-32 bg-gray-50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Bonus Features
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Beyond the core agents, AutoFounder X includes innovative features to enhance your startup journey.
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-2">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center space-x-3">
                      <div className="p-3 rounded-lg bg-primary/10">
                        <Icon className="h-8 w-8 text-primary" />
                      </div>
                      <CardTitle className="text-xl">{feature.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base">{feature.description}</CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              How It Works
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              From idea to launch in just a few simple steps.
            </p>
          </div>
          
          <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-3">
            <div className="text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="mt-6 text-xl font-semibold text-gray-900">Share Your Idea</h3>
              <p className="mt-2 text-gray-600">
                Describe your startup vision, target market, and goals through our intuitive project builder.
              </p>
            </div>
            
            <div className="text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="mt-6 text-xl font-semibold text-gray-900">AI Agents Work</h3>
              <p className="mt-2 text-gray-600">
                Watch as 14 specialized agents collaborate to validate, build, and launch your startup.
              </p>
            </div>
            
            <div className="text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="mt-6 text-xl font-semibold text-gray-900">Launch & Scale</h3>
              <p className="mt-2 text-gray-600">
                Get your MVP, marketing materials, and launch strategy ready for the market.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 sm:py-32 bg-primary">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to Build Your Startup?
            </h2>
            <p className="mt-6 text-lg leading-8 text-primary-foreground/80">
              Join thousands of entrepreneurs who are building the future with AI co-founders.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              {isAuthenticated ? (
                <Link to="/projects">
                  <Button size="lg" variant="secondary" className="px-8">
                    Start New Project
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              ) : (
                <Link to="/register">
                  <Button size="lg" variant="secondary" className="px-8">
                    Get Started Free
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;

