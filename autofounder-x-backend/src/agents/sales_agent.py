import random
from typing import Dict, Any, List
from .base_agent import BaseAgent

class SalesAgent(BaseAgent):
    """AI Agent for sales outreach and lead generation"""
    
    def __init__(self):
        super().__init__(
            agent_type="sales",
            name="Sales Agent",
            description="Handles outreach and lead generation"
        )
    
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sales strategy development"""
        self.log("Starting sales strategy development...")
        
        steps = [
            "Analyzing target customer segments",
            "Developing sales funnel",
            "Creating outreach sequences",
            "Building lead scoring system",
            "Setting up sales automation",
            "Creating sales materials",
            "Planning follow-up strategies"
        ]
        
        self.simulate_work(steps, 0.7)
        
        # Generate sales results
        sales_funnel = self.design_sales_funnel(project_data)
        outreach_strategy = self.create_outreach_strategy(project_data)
        lead_scoring = self.develop_lead_scoring(project_data)
        sales_materials = self.create_sales_materials(project_data)
        
        result = {
            "sales_funnel": sales_funnel,
            "outreach_strategy": outreach_strategy,
            "lead_scoring": lead_scoring,
            "sales_materials": sales_materials,
            "projected_conversion_rate": f"{random.uniform(15, 35):.1f}%",
            "estimated_sales_cycle": f"{random.randint(14, 90)} days"
        }
        
        self.results = result
        return self.generate_mock_result("sales_strategy", result)
    
    def design_sales_funnel(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive sales funnel"""
        business_model = project_data.get('business_model', 'saas')
        
        # Different funnels based on business model
        if business_model == 'saas':
            return {
                "funnel_stages": [
                    {
                        "stage": "Awareness",
                        "description": "Potential customers discover your solution",
                        "channels": ["Content marketing", "SEO", "Social media", "Paid ads"],
                        "metrics": ["Website traffic", "Brand searches", "Social mentions"],
                        "conversion_rate": "2-5%"
                    },
                    {
                        "stage": "Interest", 
                        "description": "Visitors engage with your content and value proposition",
                        "channels": ["Blog posts", "Webinars", "Free tools", "Email signup"],
                        "metrics": ["Email signups", "Content downloads", "Webinar attendance"],
                        "conversion_rate": "10-20%"
                    },
                    {
                        "stage": "Consideration",
                        "description": "Prospects evaluate your solution against alternatives",
                        "channels": ["Product demos", "Free trials", "Case studies", "Sales calls"],
                        "metrics": ["Demo requests", "Trial signups", "Sales qualified leads"],
                        "conversion_rate": "20-40%"
                    },
                    {
                        "stage": "Purchase",
                        "description": "Prospects become paying customers",
                        "channels": ["Sales team", "Self-service signup", "Proposal process"],
                        "metrics": ["Closed deals", "Revenue", "Customer acquisition cost"],
                        "conversion_rate": "15-30%"
                    },
                    {
                        "stage": "Retention",
                        "description": "Customers continue using and expanding their usage",
                        "channels": ["Customer success", "Upselling", "Referral programs"],
                        "metrics": ["Churn rate", "Expansion revenue", "NPS score"],
                        "conversion_rate": "80-95%"
                    }
                ],
                "funnel_optimization": {
                    "awareness_to_interest": "Improve content quality and targeting",
                    "interest_to_consideration": "Enhance lead nurturing sequences",
                    "consideration_to_purchase": "Streamline sales process and remove friction",
                    "purchase_to_retention": "Focus on onboarding and customer success"
                }
            }
        elif business_model == 'marketplace':
            return {
                "funnel_stages": [
                    {
                        "stage": "Discovery",
                        "description": "Users find your marketplace",
                        "channels": ["SEO", "Social media", "Partnerships", "Word of mouth"],
                        "metrics": ["Unique visitors", "Search rankings", "Referral traffic"],
                        "conversion_rate": "3-8%"
                    },
                    {
                        "stage": "Registration",
                        "description": "Visitors create accounts",
                        "channels": ["Homepage CTA", "Social login", "Email signup"],
                        "metrics": ["Registration rate", "Account completions"],
                        "conversion_rate": "15-25%"
                    },
                    {
                        "stage": "First Transaction",
                        "description": "Users make their first purchase or listing",
                        "channels": ["Onboarding flow", "Incentives", "Featured listings"],
                        "metrics": ["First transaction rate", "Time to first transaction"],
                        "conversion_rate": "25-45%"
                    },
                    {
                        "stage": "Repeat Usage",
                        "description": "Users become regular participants",
                        "channels": ["Email marketing", "Push notifications", "Loyalty programs"],
                        "metrics": ["Repeat transaction rate", "Monthly active users"],
                        "conversion_rate": "40-70%"
                    }
                ]
            }
        else:  # ecommerce
            return {
                "funnel_stages": [
                    {
                        "stage": "Traffic",
                        "description": "Visitors arrive at your store",
                        "channels": ["SEO", "Paid ads", "Social media", "Email marketing"],
                        "metrics": ["Sessions", "Unique visitors", "Traffic sources"],
                        "conversion_rate": "1-3%"
                    },
                    {
                        "stage": "Product View",
                        "description": "Visitors browse products",
                        "channels": ["Product pages", "Search", "Categories", "Recommendations"],
                        "metrics": ["Product page views", "Search usage", "Browse depth"],
                        "conversion_rate": "20-40%"
                    },
                    {
                        "stage": "Add to Cart",
                        "description": "Visitors add items to cart",
                        "channels": ["Product pages", "Quick add", "Bundles", "Promotions"],
                        "metrics": ["Add to cart rate", "Cart value", "Items per cart"],
                        "conversion_rate": "10-30%"
                    },
                    {
                        "stage": "Checkout",
                        "description": "Customers complete purchase",
                        "channels": ["Checkout flow", "Guest checkout", "Payment options"],
                        "metrics": ["Checkout completion", "Payment success", "Order value"],
                        "conversion_rate": "60-80%"
                    }
                ]
            }
    
    def create_outreach_strategy(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive outreach strategy"""
        target_market = project_data.get('target_market', '')
        business_model = project_data.get('business_model', 'saas')
        
        return {
            "target_segments": [
                {
                    "segment": "Early Adopters",
                    "characteristics": ["Tech-savvy", "Open to new solutions", "Willing to provide feedback"],
                    "size": "5-10% of total market",
                    "approach": "Direct outreach, beta programs, exclusive access",
                    "messaging": "Be among the first to experience the future of [industry]"
                },
                {
                    "segment": "Problem-Aware Prospects",
                    "characteristics": ["Actively seeking solutions", "Budget allocated", "Decision-making authority"],
                    "size": "15-25% of total market", 
                    "approach": "Solution-focused content, demos, consultative selling",
                    "messaging": "Solve your [specific problem] with our proven solution"
                },
                {
                    "segment": "Status Quo Challengers",
                    "characteristics": ["Dissatisfied with current solution", "Open to change", "ROI-focused"],
                    "size": "20-30% of total market",
                    "approach": "Comparison content, ROI calculators, migration support",
                    "messaging": "Why settle for less? Upgrade to a better solution"
                }
            ],
            "outreach_channels": [
                {
                    "channel": "Email Outreach",
                    "sequences": [
                        {
                            "name": "Cold Outreach Sequence",
                            "emails": 5,
                            "timeline": "2 weeks",
                            "open_rate": "25-35%",
                            "response_rate": "3-8%"
                        },
                        {
                            "name": "Warm Lead Nurturing",
                            "emails": 7,
                            "timeline": "4 weeks",
                            "open_rate": "40-55%",
                            "response_rate": "8-15%"
                        },
                        {
                            "name": "Re-engagement Campaign",
                            "emails": 3,
                            "timeline": "1 week",
                            "open_rate": "20-30%",
                            "response_rate": "2-5%"
                        }
                    ]
                },
                {
                    "channel": "LinkedIn Outreach",
                    "approach": [
                        "Connection requests with personalized messages",
                        "Engaging with prospects' content before outreach",
                        "Sharing valuable content to build credibility",
                        "Direct messages with value-first approach"
                    ],
                    "metrics": {
                        "connection_acceptance": "30-50%",
                        "message_response": "10-20%",
                        "meeting_booking": "5-15%"
                    }
                },
                {
                    "channel": "Content Marketing",
                    "tactics": [
                        "Industry-specific blog posts",
                        "Webinars and virtual events",
                        "Downloadable resources (ebooks, whitepapers)",
                        "Case studies and success stories"
                    ],
                    "lead_generation": "Gated content with lead magnets"
                },
                {
                    "channel": "Referral Program",
                    "structure": {
                        "customer_referrals": "20% commission or $500 credit",
                        "partner_referrals": "15% recurring commission",
                        "employee_referrals": "$1000 bonus per qualified lead"
                    }
                }
            ],
            "sales_automation": {
                "lead_qualification": "Automated scoring based on engagement and fit",
                "follow_up_sequences": "Triggered based on prospect behavior",
                "meeting_scheduling": "Calendar integration with automated booking",
                "proposal_generation": "Template-based proposals with dynamic pricing"
            }
        }
    
    def develop_lead_scoring(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop lead scoring system"""
        return {
            "scoring_criteria": {
                "demographic_fit": {
                    "company_size": {
                        "1-10 employees": 5,
                        "11-50 employees": 15,
                        "51-200 employees": 25,
                        "200+ employees": 20
                    },
                    "industry": {
                        "target_industry": 20,
                        "adjacent_industry": 10,
                        "other_industry": 0
                    },
                    "job_title": {
                        "decision_maker": 25,
                        "influencer": 15,
                        "end_user": 5
                    },
                    "budget_authority": {
                        "has_budget": 20,
                        "influences_budget": 10,
                        "no_budget_info": 0
                    }
                },
                "behavioral_engagement": {
                    "website_activity": {
                        "pricing_page_visit": 15,
                        "demo_request": 25,
                        "multiple_page_views": 10,
                        "return_visitor": 5
                    },
                    "content_engagement": {
                        "whitepaper_download": 10,
                        "webinar_attendance": 15,
                        "email_opens": 5,
                        "email_clicks": 10
                    },
                    "social_engagement": {
                        "linkedin_connection": 5,
                        "content_sharing": 10,
                        "comment_interaction": 8
                    }
                }
            },
            "score_ranges": {
                "hot_lead": "80-100 points",
                "warm_lead": "60-79 points", 
                "cold_lead": "40-59 points",
                "unqualified": "0-39 points"
            },
            "automated_actions": {
                "hot_lead": "Immediate sales team notification, priority follow-up",
                "warm_lead": "Add to nurturing sequence, schedule follow-up in 3 days",
                "cold_lead": "Add to long-term nurturing campaign",
                "unqualified": "Add to general newsletter, re-score monthly"
            }
        }
    
    def create_sales_materials(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create sales enablement materials"""
        project_name = project_data.get('name', 'Your Startup')
        
        return {
            "sales_deck": {
                "slides": [
                    {"slide": 1, "title": "Problem Statement", "content": "Current challenges in the market"},
                    {"slide": 2, "title": "Solution Overview", "content": f"How {project_name} solves these problems"},
                    {"slide": 3, "title": "Key Benefits", "content": "Primary value propositions"},
                    {"slide": 4, "title": "Product Demo", "content": "Live demonstration or screenshots"},
                    {"slide": 5, "title": "Customer Success", "content": "Case studies and testimonials"},
                    {"slide": 6, "title": "Pricing & Packages", "content": "Pricing options and ROI"},
                    {"slide": 7, "title": "Implementation", "content": "Onboarding and support process"},
                    {"slide": 8, "title": "Next Steps", "content": "Clear call to action"}
                ],
                "customization": "Slides can be customized per prospect/industry"
            },
            "one_pagers": [
                {
                    "type": "Product Overview",
                    "content": "High-level solution summary with key benefits",
                    "use_case": "Initial prospect meetings"
                },
                {
                    "type": "ROI Calculator",
                    "content": "Customizable ROI analysis tool",
                    "use_case": "Justifying investment to decision makers"
                },
                {
                    "type": "Competitive Comparison",
                    "content": "Feature and pricing comparison with competitors",
                    "use_case": "Addressing competitive concerns"
                },
                {
                    "type": "Implementation Timeline",
                    "content": "Step-by-step implementation process",
                    "use_case": "Addressing implementation concerns"
                }
            ],
            "email_templates": [
                {
                    "type": "Cold Outreach",
                    "subject_lines": [
                        "Quick question about [company's] [specific challenge]",
                        "Helping [company] save 10+ hours per week",
                        "[Mutual connection] suggested I reach out"
                    ],
                    "personalization_fields": ["Company name", "Industry", "Specific challenge", "Mutual connection"]
                },
                {
                    "type": "Follow-up After Demo",
                    "subject_lines": [
                        "Thanks for your time today - next steps",
                        "Following up on our conversation about [specific topic]",
                        "Proposal for [company name] - [solution name]"
                    ]
                },
                {
                    "type": "Proposal Delivery",
                    "subject_lines": [
                        "Your customized proposal for [solution name]",
                        "Next steps to get started with [company name]",
                        "Proposal: [specific ROI/benefit] for [company name]"
                    ]
                }
            ],
            "objection_handling": {
                "price_objection": {
                    "objection": "It's too expensive",
                    "response": "I understand budget is a concern. Let's look at the ROI - our customers typically see a 300% return within 6 months. Can we explore a phased implementation to spread the investment?"
                },
                "timing_objection": {
                    "objection": "Not the right time",
                    "response": "I appreciate you being upfront about timing. What would need to change for this to become a priority? In the meantime, would you like me to send you our ROI calculator to quantify the cost of waiting?"
                },
                "feature_objection": {
                    "objection": "Missing specific feature",
                    "response": "That's great feedback. This feature is actually on our roadmap for Q2. In the meantime, here's how our current solution addresses that need, and I can connect you with our product team to discuss timeline."
                },
                "authority_objection": {
                    "objection": "Need to check with my boss",
                    "response": "Absolutely, this is an important decision. What information would be helpful for your boss to make this decision? Would it be valuable for me to present to your team together?"
                }
            }
        }
    
    def generate_sales_sequence_api(self, project_id: int) -> Dict[str, Any]:
        """API endpoint to generate sales sequence"""
        return {
            "success": True,
            "sequence_id": random.randint(1000, 9999),
            "sequence_type": "Cold Outreach",
            "total_emails": 5,
            "timeline": "14 days",
            "emails": [
                {
                    "day": 1,
                    "subject": "Quick question about [company's] workflow efficiency",
                    "preview": "Personalized introduction with specific value proposition"
                },
                {
                    "day": 4,
                    "subject": "Following up - 15-minute efficiency audit?",
                    "preview": "Soft follow-up with low-commitment offer"
                },
                {
                    "day": 8,
                    "subject": "How [competitor] increased efficiency by 40%",
                    "preview": "Value-driven content with social proof"
                },
                {
                    "day": 11,
                    "subject": "Last attempt - worth a quick chat?",
                    "preview": "Final follow-up with clear next steps"
                },
                {
                    "day": 14,
                    "subject": "Keeping you in the loop",
                    "preview": "Soft close with future follow-up option"
                }
            ],
            "expected_metrics": {
                "open_rate": "28-35%",
                "response_rate": "5-12%",
                "meeting_booking": "2-5%"
            }
        }

