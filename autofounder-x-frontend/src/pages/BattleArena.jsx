import React, { useState, useEffect } from 'react';
import { battleArenaAPI } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Alert, AlertDescription } from '../components/ui/alert';
import { 
  Trophy, 
  Calendar, 
  Users, 
  Star, 
  Crown, 
  Medal, 
  Award,
  Clock,
  Target,
  TrendingUp,
  Loader2,
  AlertCircle,
  Vote,
  Gift
} from 'lucide-react';

const BattleArena = () => {
  const [activeCompetitions, setActiveCompetitions] = useState([]);
  const [upcomingCompetitions, setUpcomingCompetitions] = useState([]);
  const [completedCompetitions, setCompletedCompetitions] = useState([]);
  const [leaderboards, setLeaderboards] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('active');

  useEffect(() => {
    fetchCompetitions();
  }, []);

  const fetchCompetitions = async () => {
    try {
      setLoading(true);
      const [activeResponse, upcomingResponse, completedResponse] = await Promise.all([
        battleArenaAPI.getCompetitions('active'),
        battleArenaAPI.getCompetitions('upcoming'),
        battleArenaAPI.getCompetitions('completed')
      ]);

      if (activeResponse.data.success) {
        setActiveCompetitions(activeResponse.data.competitions);
        // Fetch leaderboards for active competitions
        for (const comp of activeResponse.data.competitions) {
          fetchLeaderboard(comp.id);
        }
      }

      if (upcomingResponse.data.success) {
        setUpcomingCompetitions(upcomingResponse.data.competitions);
      }

      if (completedResponse.data.success) {
        setCompletedCompetitions(completedResponse.data.competitions);
      }
    } catch (error) {
      setError('Failed to load competitions');
      console.error('Battle Arena error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLeaderboard = async (competitionId) => {
    try {
      const response = await battleArenaAPI.getLeaderboard(competitionId);
      if (response.data.success) {
        setLeaderboards(prev => ({
          ...prev,
          [competitionId]: response.data.leaderboard
        }));
      }
    } catch (error) {
      console.error('Leaderboard error:', error);
    }
  };

  const handleVote = async (entryId, competitionId) => {
    try {
      const response = await battleArenaAPI.voteEntry(entryId);
      if (response.data.success) {
        // Refresh leaderboard
        await fetchLeaderboard(competitionId);
      }
    } catch (error) {
      console.error('Vote error:', error);
    }
  };

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1:
        return <Crown className="h-5 w-5 text-yellow-500" />;
      case 2:
        return <Medal className="h-5 w-5 text-gray-400" />;
      case 3:
        return <Award className="h-5 w-5 text-amber-600" />;
      default:
        return <span className="text-sm font-medium">#{rank}</span>;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'upcoming':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const renderCompetitionCard = (competition, showLeaderboard = false) => (
    <Card key={competition.id} className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-xl">{competition.name}</CardTitle>
            <CardDescription className="mt-2">
              {competition.description}
            </CardDescription>
          </div>
          <Badge className={getStatusColor(competition.status)}>
            {competition.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Competition Info */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-500" />
              <span>
                {formatDate(competition.start_date)} - {formatDate(competition.end_date)}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-gray-500" />
              <span>{competition.entry_count || 0} entries</span>
            </div>
            <div className="flex items-center space-x-2">
              <Gift className="h-4 w-4 text-gray-500" />
              <span>{competition.prize_credits} credits</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-gray-500" />
              <span>
                {competition.status === 'active' 
                  ? `Ends ${formatDate(competition.end_date)}`
                  : competition.status === 'upcoming'
                  ? `Starts ${formatDate(competition.start_date)}`
                  : 'Completed'
                }
              </span>
            </div>
          </div>

          {/* Leaderboard Preview */}
          {showLeaderboard && leaderboards[competition.id] && (
            <div className="border-t pt-4">
              <h4 className="font-medium mb-3 flex items-center">
                <Trophy className="h-4 w-4 mr-2 text-yellow-500" />
                Top Entries
              </h4>
              <div className="space-y-2">
                {leaderboards[competition.id].slice(0, 3).map((entry) => (
                  <div key={entry.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                    <div className="flex items-center space-x-3">
                      {getRankIcon(entry.ranking)}
                      <div>
                        <p className="font-medium text-sm">{entry.project?.name}</p>
                        <p className="text-xs text-gray-600">
                          by {entry.creator?.first_name && entry.creator?.last_name 
                            ? `${entry.creator.first_name} ${entry.creator.last_name}`
                            : entry.creator?.username
                          }
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleVote(entry.id, competition.id)}
                      >
                        <Vote className="h-3 w-3 mr-1" />
                        {entry.votes}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
              
              {leaderboards[competition.id].length > 3 && (
                <Button variant="ghost" size="sm" className="w-full mt-2">
                  View Full Leaderboard
                </Button>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center space-x-2 pt-2">
            {competition.status === 'active' && (
              <>
                <Button variant="outline" className="flex-1">
                  Enter Competition
                </Button>
                <Button variant="outline">
                  View Details
                </Button>
              </>
            )}
            {competition.status === 'upcoming' && (
              <Button variant="outline" className="w-full">
                Set Reminder
              </Button>
            )}
            {competition.status === 'completed' && (
              <Button variant="outline" className="w-full">
                View Results
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading battle arena...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Trophy className="h-8 w-8 mr-3 text-yellow-500" />
            StartUp Battle Arena
          </h1>
          <p className="text-gray-600 mt-2">
            Compete with other entrepreneurs, showcase your AI-built startups, and win prizes
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Trophy className="h-8 w-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">{activeCompetitions.length}</div>
                <p className="text-sm text-gray-600">Active Competitions</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Calendar className="h-8 w-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{upcomingCompetitions.length}</div>
                <p className="text-sm text-gray-600">Upcoming Events</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Users className="h-8 w-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">
                  {activeCompetitions.reduce((sum, comp) => sum + (comp.entry_count || 0), 0)}
                </div>
                <p className="text-sm text-gray-600">Total Participants</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Gift className="h-8 w-8 text-purple-500" />
              <div>
                <div className="text-2xl font-bold">
                  {activeCompetitions.reduce((sum, comp) => sum + comp.prize_credits, 0)}
                </div>
                <p className="text-sm text-gray-600">Prize Credits</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Competition Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="active">
              Active ({activeCompetitions.length})
            </TabsTrigger>
            <TabsTrigger value="upcoming">
              Upcoming ({upcomingCompetitions.length})
            </TabsTrigger>
            <TabsTrigger value="completed">
              Completed ({completedCompetitions.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="active" className="mt-6">
            {activeCompetitions.length === 0 ? (
              <div className="text-center py-12">
                <Trophy className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No active competitions</h3>
                <p className="text-gray-600">Check back soon for new competitions!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {activeCompetitions.map((competition) => 
                  renderCompetitionCard(competition, true)
                )}
              </div>
            )}
          </TabsContent>

          <TabsContent value="upcoming" className="mt-6">
            {upcomingCompetitions.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No upcoming competitions</h3>
                <p className="text-gray-600">New competitions will be announced soon!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {upcomingCompetitions.map((competition) => 
                  renderCompetitionCard(competition, false)
                )}
              </div>
            )}
          </TabsContent>

          <TabsContent value="completed" className="mt-6">
            {completedCompetitions.length === 0 ? (
              <div className="text-center py-12">
                <Award className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No completed competitions</h3>
                <p className="text-gray-600">Past competition results will appear here.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {completedCompetitions.map((competition) => 
                  renderCompetitionCard(competition, false)
                )}
              </div>
            )}
          </TabsContent>
        </Tabs>

        {/* How It Works */}
        <div className="mt-12 bg-white p-8 rounded-lg shadow-sm">
          <h3 className="text-2xl font-bold mb-6 text-center">How Battle Arena Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Target className="h-8 w-8 text-blue-600" />
              </div>
              <h4 className="font-semibold mb-2">1. Enter Competition</h4>
              <p className="text-gray-600">
                Submit your AI-built startup project to active competitions
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Vote className="h-8 w-8 text-green-600" />
              </div>
              <h4 className="font-semibold mb-2">2. Get Votes</h4>
              <p className="text-gray-600">
                Community members vote for their favorite projects
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Crown className="h-8 w-8 text-yellow-600" />
              </div>
              <h4 className="font-semibold mb-2">3. Win Prizes</h4>
              <p className="text-gray-600">
                Top-ranked projects win credits and recognition
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BattleArena;

