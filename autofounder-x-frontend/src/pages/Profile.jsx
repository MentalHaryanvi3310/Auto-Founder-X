import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Avatar, AvatarFallback } from '../components/ui/avatar';
import { 
  User, 
  Mail, 
  Calendar, 
  Settings, 
  Lock, 
  Mic,
  Save,
  AlertCircle,
  CheckCircle,
  Loader2,
  Crown,
  Trophy,
  Star
} from 'lucide-react';

const Profile = () => {
  const { user, updateProfile, changePassword } = useAuth();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [profileData, setProfileData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    username: user?.username || '',
    persona_data: user?.persona_data || ''
  });

  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  const getInitials = (user) => {
    if (user?.first_name && user?.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
    }
    return user?.username?.[0]?.toUpperCase() || 'U';
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const result = await updateProfile(profileData);
      
      if (result.success) {
        setMessage({ type: 'success', text: 'Profile updated successfully!' });
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to update profile' });
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    if (passwordData.new_password !== passwordData.confirm_password) {
      setMessage({ type: 'error', text: 'New passwords do not match' });
      setLoading(false);
      return;
    }

    try {
      const result = await changePassword({
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      });
      
      if (result.success) {
        setMessage({ type: 'success', text: 'Password changed successfully!' });
        setPasswordData({
          current_password: '',
          new_password: '',
          confirm_password: ''
        });
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to change password' });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePasswordInputChange = (field, value) => {
    setPasswordData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="text-xl">{getInitials(user)}</AvatarFallback>
            </Avatar>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {user?.first_name && user?.last_name 
                  ? `${user.first_name} ${user.last_name}`
                  : user?.username
                }
              </h1>
              <p className="text-gray-600">{user?.email}</p>
              <div className="flex items-center space-x-2 mt-2">
                <Crown className="h-4 w-4 text-yellow-500" />
                <span className="text-sm text-gray-600 capitalize">
                  {user?.subscription_tier} Member
                </span>
              </div>
            </div>
          </div>
        </div>

        {message.text && (
          <Alert variant={message.type === 'error' ? 'destructive' : 'default'} className="mb-6">
            {message.type === 'error' ? (
              <AlertCircle className="h-4 w-4" />
            ) : (
              <CheckCircle className="h-4 w-4" />
            )}
            <AlertDescription>{message.text}</AlertDescription>
          </Alert>
        )}

        {/* Profile Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Trophy className="h-8 w-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold">0</div>
                <p className="text-sm text-gray-600">Projects Created</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Star className="h-8 w-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">0</div>
                <p className="text-sm text-gray-600">Marketplace Votes</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center space-x-3 p-6">
              <Calendar className="h-8 w-8 text-green-500" />
              <div>
                <div className="text-2xl font-bold">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </div>
                <p className="text-sm text-gray-600">Member Since</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Profile Tabs */}
        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="profile">
              <User className="h-4 w-4 mr-2" />
              Profile
            </TabsTrigger>
            <TabsTrigger value="security">
              <Lock className="h-4 w-4 mr-2" />
              Security
            </TabsTrigger>
            <TabsTrigger value="persona">
              <Mic className="h-4 w-4 mr-2" />
              AI Persona
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile">
            <Card>
              <CardHeader>
                <CardTitle>Profile Information</CardTitle>
                <CardDescription>
                  Update your personal information and account details
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleProfileUpdate} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="first_name">First Name</Label>
                      <Input
                        id="first_name"
                        value={profileData.first_name}
                        onChange={(e) => handleInputChange('first_name', e.target.value)}
                        placeholder="Enter your first name"
                      />
                    </div>
                    <div>
                      <Label htmlFor="last_name">Last Name</Label>
                      <Input
                        id="last_name"
                        value={profileData.last_name}
                        onChange={(e) => handleInputChange('last_name', e.target.value)}
                        placeholder="Enter your last name"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="username">Username</Label>
                    <Input
                      id="username"
                      value={profileData.username}
                      onChange={(e) => handleInputChange('username', e.target.value)}
                      placeholder="Enter your username"
                    />
                  </div>

                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      value={user?.email || ''}
                      disabled
                      className="bg-gray-50"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Email cannot be changed. Contact support if needed.
                    </p>
                  </div>

                  <div className="flex justify-end">
                    <Button type="submit" disabled={loading}>
                      {loading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        <>
                          <Save className="h-4 w-4 mr-2" />
                          Save Changes
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="security">
            <Card>
              <CardHeader>
                <CardTitle>Change Password</CardTitle>
                <CardDescription>
                  Update your password to keep your account secure
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handlePasswordChange} className="space-y-4">
                  <div>
                    <Label htmlFor="current_password">Current Password</Label>
                    <Input
                      id="current_password"
                      type="password"
                      value={passwordData.current_password}
                      onChange={(e) => handlePasswordInputChange('current_password', e.target.value)}
                      placeholder="Enter your current password"
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="new_password">New Password</Label>
                    <Input
                      id="new_password"
                      type="password"
                      value={passwordData.new_password}
                      onChange={(e) => handlePasswordInputChange('new_password', e.target.value)}
                      placeholder="Enter your new password"
                      required
                    />
                  </div>

                  <div>
                    <Label htmlFor="confirm_password">Confirm New Password</Label>
                    <Input
                      id="confirm_password"
                      type="password"
                      value={passwordData.confirm_password}
                      onChange={(e) => handlePasswordInputChange('confirm_password', e.target.value)}
                      placeholder="Confirm your new password"
                      required
                    />
                  </div>

                  <div className="flex justify-end">
                    <Button type="submit" disabled={loading}>
                      {loading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Changing...
                        </>
                      ) : (
                        <>
                          <Lock className="h-4 w-4 mr-2" />
                          Change Password
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="persona">
            <Card>
              <CardHeader>
                <CardTitle>AI Co-Founder Persona</CardTitle>
                <CardDescription>
                  Customize how AI agents understand your style and preferences
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <Label htmlFor="persona_data">Persona Description</Label>
                    <Textarea
                      id="persona_data"
                      value={profileData.persona_data}
                      onChange={(e) => handleInputChange('persona_data', e.target.value)}
                      placeholder="Describe your communication style, business preferences, and how you want AI agents to represent you..."
                      rows={6}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      This helps AI agents build projects that match your style and vision.
                    </p>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Voice Profile (Coming Soon)</h4>
                    <p className="text-sm text-blue-700 mb-3">
                      Upload a voice recording to enable the Co-Founder Clone feature
                    </p>
                    <Button variant="outline" disabled>
                      <Mic className="h-4 w-4 mr-2" />
                      Record Voice Sample
                    </Button>
                  </div>

                  <div className="flex justify-end">
                    <Button onClick={handleProfileUpdate} disabled={loading}>
                      {loading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        <>
                          <Save className="h-4 w-4 mr-2" />
                          Save Persona
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Profile;

