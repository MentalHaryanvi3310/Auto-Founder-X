import React, { useState, useEffect } from 'react';
import { marketplaceAPI } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Alert, AlertDescription } from '../components/ui/alert';
import { 
  Search, 
  Heart, 
  Eye, 
  DollarSign, 
  TrendingUp, 
  Clock, 
  Filter,
  Loader2,
  AlertCircle,
  Star,
  Users,
  ExternalLink
} from 'lucide-react';

const Marketplace = () => {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [sortBy, setSortBy] = useState('recent');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchMarketplaceData();
    fetchCategories();
  }, [currentPage, selectedCategory, sortBy]);

  const fetchMarketplaceData = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        limit: 12,
        sort: sortBy
      };
      
      if (selectedCategory) {
        params.category = selectedCategory;
      }

      const response = await marketplaceAPI.getItems(params);
      
      if (response.data.success) {
        setItems(response.data.items);
        setTotalPages(response.data.pages);
      }
    } catch (error) {
      setError('Failed to load marketplace items');
      console.error('Marketplace error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await marketplaceAPI.getCategories();
      if (response.data.success) {
        setCategories(response.data.categories);
      }
    } catch (error) {
      console.error('Categories error:', error);
    }
  };

  const handleVote = async (itemId) => {
    try {
      const response = await marketplaceAPI.voteItem(itemId);
      if (response.data.success) {
        // Update the item's vote count locally
        setItems(prevItems =>
          prevItems.map(item =>
            item.id === itemId
              ? { ...item, votes: response.data.votes }
              : item
          )
        );
      }
    } catch (error) {
      console.error('Vote error:', error);
    }
  };

  const filteredItems = items.filter(item =>
    item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading && items.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading marketplace...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">MVP Marketplace</h1>
          <p className="text-gray-600 mt-2">
            Discover AI-built products, vote for your favorites, and find inspiration
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow-sm mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger>
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="recent">Most Recent</SelectItem>
                <SelectItem value="votes">Most Voted</SelectItem>
                <SelectItem value="views">Most Viewed</SelectItem>
              </SelectContent>
            </Select>
            
            <Button variant="outline" onClick={() => {
              setSearchTerm('');
              setSelectedCategory('');
              setSortBy('recent');
              setCurrentPage(1);
            }}>
              <Filter className="h-4 w-4 mr-2" />
              Clear Filters
            </Button>
          </div>
        </div>

        {/* Marketplace Grid */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <Star className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No products found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || selectedCategory 
                ? 'Try adjusting your search or filters'
                : 'Be the first to publish a product to the marketplace!'
              }
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {filteredItems.map((item) => (
                <Card key={item.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg line-clamp-2">{item.title}</CardTitle>
                        <CardDescription className="mt-2 line-clamp-3">
                          {item.description}
                        </CardDescription>
                      </div>
                      {item.category && (
                        <Badge variant="secondary" className="ml-2">
                          {item.category}
                        </Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {/* Creator Info */}
                      {item.creator && (
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <Users className="h-4 w-4" />
                          <span>
                            by {item.creator.first_name && item.creator.last_name 
                              ? `${item.creator.first_name} ${item.creator.last_name}`
                              : item.creator.username
                            }
                          </span>
                        </div>
                      )}

                      {/* Project Info */}
                      {item.project && (
                        <div className="text-sm text-gray-600">
                          <p className="font-medium">{item.project.name}</p>
                          <p className="line-clamp-2">{item.project.description}</p>
                        </div>
                      )}

                      {/* Stats */}
                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center space-x-1">
                            <Heart className="h-4 w-4" />
                            <span>{item.votes}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Eye className="h-4 w-4" />
                            <span>{item.views}</span>
                          </div>
                        </div>
                        
                        {item.price && item.is_for_sale && (
                          <div className="flex items-center space-x-1 text-green-600 font-medium">
                            <DollarSign className="h-4 w-4" />
                            <span>{item.price}</span>
                          </div>
                        )}
                      </div>

                      {/* Actions */}
                      <div className="flex items-center space-x-2 pt-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleVote(item.id)}
                          className="flex-1"
                        >
                          <Heart className="h-4 w-4 mr-1" />
                          Vote
                        </Button>
                        
                        <Button variant="outline" size="sm">
                          <ExternalLink className="h-4 w-4 mr-1" />
                          View
                        </Button>
                        
                        {item.is_for_sale && (
                          <Button size="sm" className="bg-green-600 hover:bg-green-700">
                            Buy
                          </Button>
                        )}
                      </div>

                      {/* Date */}
                      <div className="flex items-center space-x-1 text-xs text-gray-500 pt-2 border-t">
                        <Clock className="h-3 w-3" />
                        <span>
                          {new Date(item.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2">
                <Button
                  variant="outline"
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>
                
                <div className="flex items-center space-x-1">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const page = i + 1;
                    return (
                      <Button
                        key={page}
                        variant={currentPage === page ? "default" : "outline"}
                        size="sm"
                        onClick={() => setCurrentPage(page)}
                      >
                        {page}
                      </Button>
                    );
                  })}
                </div>
                
                <Button
                  variant="outline"
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}

        {/* Stats Section */}
        <div className="mt-12 bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Marketplace Stats</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{items.length}</div>
              <div className="text-sm text-gray-600">Total Products</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">
                {items.reduce((sum, item) => sum + item.votes, 0)}
              </div>
              <div className="text-sm text-gray-600">Total Votes</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">
                {items.reduce((sum, item) => sum + item.views, 0)}
              </div>
              <div className="text-sm text-gray-600">Total Views</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{categories.length}</div>
              <div className="text-sm text-gray-600">Categories</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Marketplace;

