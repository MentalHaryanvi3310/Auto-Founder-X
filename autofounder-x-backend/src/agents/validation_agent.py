import random
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ValidationAgent(BaseAgent):
    """AI Agent for market validation and survey creation"""
    
    def __init__(self):
        super().__init__(
            agent_type="validation",
            name="Validation Agent", 
            description="Creates surveys and validates market demand"
        )
    
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation process"""
        self.log("Starting market validation...")
        
        steps = [
            "Creating target customer personas",
            "Designing validation surveys",
            "Setting up feedback collection",
            "Analyzing validation metrics",
            "Generating validation report"
        ]
        
        self.simulate_work(steps, 0.6)
        
        # Generate validation results
        personas = self.create_customer_personas(project_data)
        survey = self.create_survey(project_data)
        metrics = self.generate_validation_metrics(project_data)
        recommendations = self.generate_validation_recommendations(project_data)
        
        result = {
            "customer_personas": personas,
            "survey": survey,
            "validation_metrics": metrics,
            "recommendations": recommendations,
            "validation_score": random.uniform(0.65, 0.92)
        }
        
        self.results = result
        return self.generate_mock_result("validation_analysis", result)
    
    def create_customer_personas(self, project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create target customer personas"""
        business_model = project_data.get('business_model', 'saas')
        target_market = project_data.get('target_market', '')
        
        # Base personas that can be customized
        persona_templates = [
            {
                "name": "Tech-Savvy Professional",
                "age_range": "25-40",
                "occupation": "Software Developer/Product Manager",
                "pain_points": [
                    "Inefficient workflows",
                    "Too many disconnected tools",
                    "Lack of automation"
                ],
                "goals": [
                    "Increase productivity",
                    "Streamline processes",
                    "Focus on high-value work"
                ],
                "preferred_channels": ["LinkedIn", "Twitter", "Tech blogs"],
                "budget": "$50-500/month",
                "decision_factors": ["Ease of use", "Integration capabilities", "ROI"]
            },
            {
                "name": "Small Business Owner",
                "age_range": "30-55", 
                "occupation": "Entrepreneur/Business Owner",
                "pain_points": [
                    "Limited budget",
                    "Wearing multiple hats",
                    "Need for growth"
                ],
                "goals": [
                    "Scale business efficiently",
                    "Reduce operational costs",
                    "Improve customer satisfaction"
                ],
                "preferred_channels": ["Facebook", "Google", "Industry forums"],
                "budget": "$20-200/month",
                "decision_factors": ["Cost-effectiveness", "Simplicity", "Support quality"]
            },
            {
                "name": "Enterprise Decision Maker",
                "age_range": "35-60",
                "occupation": "Director/VP/C-Level",
                "pain_points": [
                    "Complex procurement processes",
                    "Security and compliance requirements",
                    "Need for scalability"
                ],
                "goals": [
                    "Drive digital transformation",
                    "Improve team efficiency",
                    "Ensure data security"
                ],
                "preferred_channels": ["Industry events", "LinkedIn", "Analyst reports"],
                "budget": "$1000+/month",
                "decision_factors": ["Security", "Scalability", "Vendor reputation"]
            }
        ]
        
        # Return 2-3 relevant personas
        return random.sample(persona_templates, random.randint(2, 3))
    
    def create_survey(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create validation survey"""
        project_name = project_data.get('name', 'Your Startup')
        description = project_data.get('description', '')
        
        survey_questions = [
            {
                "id": 1,
                "type": "multiple_choice",
                "question": f"How interested would you be in using {project_name}?",
                "options": [
                    "Very interested",
                    "Somewhat interested", 
                    "Neutral",
                    "Not very interested",
                    "Not interested at all"
                ],
                "required": True
            },
            {
                "id": 2,
                "type": "text",
                "question": "What is your biggest challenge in this area?",
                "required": True
            },
            {
                "id": 3,
                "type": "multiple_choice",
                "question": "How do you currently solve this problem?",
                "options": [
                    "Manual processes",
                    "Existing software tools",
                    "Outsourcing",
                    "Don't have a solution",
                    "Other"
                ],
                "required": True
            },
            {
                "id": 4,
                "type": "scale",
                "question": "How much would you be willing to pay monthly for this solution?",
                "scale": {
                    "min": 0,
                    "max": 500,
                    "step": 25,
                    "currency": "USD"
                },
                "required": True
            },
            {
                "id": 5,
                "type": "text",
                "question": "What features would be most important to you?",
                "required": False
            },
            {
                "id": 6,
                "type": "multiple_choice",
                "question": "How did you hear about us?",
                "options": [
                    "Social media",
                    "Search engine",
                    "Friend/colleague referral",
                    "Industry publication",
                    "Other"
                ],
                "required": False
            }
        ]
        
        return {
            "title": f"{project_name} Market Validation Survey",
            "description": f"Help us understand your needs for {description}",
            "questions": survey_questions,
            "estimated_time": "3-5 minutes",
            "target_responses": 100,
            "distribution_channels": [
                "Email to existing contacts",
                "Social media posts",
                "Industry forums",
                "LinkedIn outreach",
                "Google Ads survey"
            ]
        }
    
    def generate_validation_metrics(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock validation metrics"""
        # Simulate survey responses
        total_responses = random.randint(85, 150)
        interested_responses = int(total_responses * random.uniform(0.6, 0.85))
        
        return {
            "survey_responses": total_responses,
            "completion_rate": f"{random.randint(65, 85)}%",
            "interest_level": {
                "very_interested": f"{random.randint(25, 40)}%",
                "somewhat_interested": f"{random.randint(20, 35)}%",
                "neutral": f"{random.randint(15, 25)}%",
                "not_interested": f"{random.randint(5, 15)}%"
            },
            "willingness_to_pay": {
                "average": f"${random.randint(45, 120)}/month",
                "median": f"${random.randint(35, 95)}/month",
                "range": "$0-500/month"
            },
            "top_pain_points": [
                "Time-consuming manual processes",
                "Lack of integration between tools",
                "Difficulty tracking progress",
                "High costs of current solutions"
            ],
            "feature_priorities": [
                "Easy integration with existing tools",
                "Real-time analytics and reporting",
                "Mobile accessibility",
                "Automated workflows",
                "Customizable dashboards"
            ],
            "market_size_validation": {
                "target_market_size": f"{random.randint(500, 2000)}K potential users",
                "addressable_market": f"${random.randint(50, 200)}M annually",
                "early_adopter_segment": f"{random.randint(15, 35)}K users"
            }
        }
    
    def generate_validation_recommendations(self, project_data: Dict[str, Any]) -> List[str]:
        """Generate validation-based recommendations"""
        recommendations = [
            "Strong market interest validates the core concept - proceed with MVP development",
            "Focus on integration capabilities as this was the top requested feature",
            "Consider tiered pricing starting at $49/month based on willingness to pay data",
            "Target early adopters in the tech industry for initial user base",
            "Prioritize mobile app development as 68% of respondents prefer mobile access",
            "Build strong onboarding process as ease of use is a key decision factor",
            "Develop case studies and ROI calculators to address cost concerns",
            "Consider freemium model to lower barrier to entry for small businesses"
        ]
        
        return random.sample(recommendations, random.randint(4, 6))
    
    def create_survey_api(self, project_id: int) -> Dict[str, Any]:
        """API endpoint to create survey for a project"""
        # Mock survey creation
        survey_id = random.randint(1000, 9999)
        
        return {
            "success": True,
            "survey_id": survey_id,
            "survey_url": f"https://surveys.autofounder-x.com/{survey_id}",
            "message": "Survey created successfully",
            "estimated_responses": random.randint(50, 200),
            "distribution_plan": {
                "email_blast": "Send to 500 contacts",
                "social_media": "Post on LinkedIn, Twitter, Facebook",
                "paid_ads": "$100 Google Ads budget",
                "community_outreach": "Share in 5 relevant forums"
            }
        }

