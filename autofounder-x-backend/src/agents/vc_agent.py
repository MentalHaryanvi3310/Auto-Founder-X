import random
from typing import Dict, Any, List
from .base_agent import BaseAgent

class VCAgent(BaseAgent):
    """AI Agent for VC outreach and fundraising support"""
    
    def __init__(self):
        super().__init__(
            agent_type="vc",
            name="VC Agent",
            description="Handles VC outreach and fundraising"
        )
    
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute VC outreach and fundraising strategy"""
        self.log("Starting VC outreach and fundraising strategy...")
        
        steps = [
            "Analyzing funding requirements",
            "Researching relevant VCs and investors",
            "Creating investor target list",
            "Developing pitch materials",
            "Preparing financial projections",
            "Creating outreach strategy",
            "Setting up investor tracking system"
        ]
        
        self.simulate_work(steps, 0.8)
        
        # Generate VC results
        funding_strategy = self.develop_funding_strategy(project_data)
        investor_research = self.research_investors(project_data)
        pitch_materials = self.create_pitch_materials(project_data)
        outreach_plan = self.create_outreach_plan(project_data)
        
        result = {
            "funding_strategy": funding_strategy,
            "investor_research": investor_research,
            "pitch_materials": pitch_materials,
            "outreach_plan": outreach_plan,
            "funding_probability": random.uniform(0.65, 0.85),
            "estimated_timeline": f"{random.randint(3, 9)} months"
        }
        
        self.results = result
        return self.generate_mock_result("vc_strategy", result)
    
    def develop_funding_strategy(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive funding strategy"""
        business_model = project_data.get('business_model', 'saas')
        current_stage = project_data.get('current_stage', 'idea')
        
        # Determine funding stage and requirements
        if current_stage in ['idea', 'prototype']:
            funding_stage = "Pre-Seed"
            typical_range = "$100K - $500K"
            use_of_funds = ["Product development", "Initial team hiring", "Market validation"]
        elif current_stage in ['mvp', 'beta']:
            funding_stage = "Seed"
            typical_range = "$500K - $2M"
            use_of_funds = ["Product refinement", "Team expansion", "Customer acquisition"]
        elif current_stage in ['launched', 'growing']:
            funding_stage = "Series A"
            typical_range = "$2M - $10M"
            use_of_funds = ["Scale operations", "Market expansion", "Product development"]
        else:
            funding_stage = "Series B+"
            typical_range = "$10M+"
            use_of_funds = ["International expansion", "New product lines", "Strategic acquisitions"]
        
        return {
            "funding_stage": funding_stage,
            "funding_requirements": {
                "target_amount": typical_range,
                "minimum_viable": f"${int(typical_range.split(' - ')[0].replace('$', '').replace('K', '000').replace('M', '000000')) * 0.7:,.0f}",
                "maximum_desired": typical_range.split(' - ')[1] if ' - ' in typical_range else typical_range,
                "runway_target": "18-24 months"
            },
            "use_of_funds": {
                "product_development": "35%",
                "team_expansion": "40%", 
                "marketing_sales": "15%",
                "operations": "10%"
            },
            "valuation_strategy": {
                "pre_money_valuation": self.estimate_valuation(project_data, funding_stage),
                "valuation_methodology": [
                    "Revenue multiple (if applicable)",
                    "Comparable company analysis",
                    "DCF analysis for mature companies",
                    "Market size and penetration potential"
                ],
                "key_value_drivers": [
                    "Market size and growth rate",
                    "Competitive differentiation",
                    "Team experience and track record",
                    "Traction and growth metrics",
                    "Technology and IP advantages"
                ]
            },
            "funding_timeline": {
                "preparation": "4-6 weeks",
                "active_fundraising": "3-6 months",
                "due_diligence": "4-8 weeks",
                "closing": "2-4 weeks",
                "total_timeline": "6-9 months"
            },
            "alternative_funding": {
                "revenue_based_financing": "For companies with recurring revenue",
                "venture_debt": "Complement to equity funding",
                "grants_competitions": "Non-dilutive funding options",
                "strategic_partnerships": "Corporate venture arms"
            }
        }
    
    def estimate_valuation(self, project_data: Dict[str, Any], funding_stage: str) -> Dict[str, Any]:
        """Estimate company valuation"""
        business_model = project_data.get('business_model', 'saas')
        
        # Valuation ranges by stage and business model
        valuation_ranges = {
            "Pre-Seed": {
                "saas": "$1M - $4M",
                "marketplace": "$1M - $3M", 
                "ecommerce": "$500K - $2M"
            },
            "Seed": {
                "saas": "$4M - $15M",
                "marketplace": "$3M - $12M",
                "ecommerce": "$2M - $8M"
            },
            "Series A": {
                "saas": "$15M - $50M",
                "marketplace": "$12M - $40M",
                "ecommerce": "$8M - $25M"
            }
        }
        
        base_range = valuation_ranges.get(funding_stage, {}).get(business_model, "$1M - $5M")
        
        return {
            "estimated_range": base_range,
            "factors_affecting_valuation": [
                "Market size and growth potential",
                "Revenue growth rate and predictability",
                "Competitive landscape and differentiation",
                "Team experience and execution capability",
                "Technology and intellectual property",
                "Customer acquisition and retention metrics"
            ],
            "valuation_benchmarks": {
                "revenue_multiple": "8-15x ARR for SaaS companies",
                "growth_rate": "Companies growing >100% YoY command premium",
                "market_size": "TAM >$1B increases valuation multiple",
                "retention_rate": ">90% net revenue retention adds premium"
            }
        }
    
    def research_investors(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research and categorize potential investors"""
        business_model = project_data.get('business_model', 'saas')
        funding_stage = project_data.get('funding_stage', 'seed')
        
        return {
            "tier_1_investors": [
                {
                    "name": "Sequoia Capital",
                    "focus": "Early to growth stage technology companies",
                    "check_size": "$1M - $25M",
                    "portfolio_fit": "Strong SaaS portfolio, looks for market leaders",
                    "contact": "Partner: [Name], Associate: [Name]",
                    "warm_intro_path": "Portfolio company CEO, mutual connection",
                    "recent_investments": ["Stripe", "Zoom", "Dropbox"]
                },
                {
                    "name": "Andreessen Horowitz (a16z)",
                    "focus": "Software, marketplaces, crypto",
                    "check_size": "$500K - $50M",
                    "portfolio_fit": "Strong marketplace and SaaS focus",
                    "contact": "General Partner: [Name]",
                    "warm_intro_path": "Portfolio company founder, a16z network",
                    "recent_investments": ["Airbnb", "Facebook", "Slack"]
                },
                {
                    "name": "Bessemer Venture Partners",
                    "focus": "Cloud computing, SaaS, marketplaces",
                    "check_size": "$1M - $20M",
                    "portfolio_fit": "Strong SaaS expertise and track record",
                    "contact": "Partner: [Name]",
                    "warm_intro_path": "Bessemer portfolio company",
                    "recent_investments": ["Shopify", "Twilio", "LinkedIn"]
                }
            ],
            "tier_2_investors": [
                {
                    "name": "First Round Capital",
                    "focus": "Pre-seed and seed stage technology",
                    "check_size": "$500K - $3M",
                    "portfolio_fit": "Early stage SaaS and marketplace companies",
                    "contact": "Partner: [Name]",
                    "warm_intro_path": "First Round Dorm Room Fund, portfolio companies"
                },
                {
                    "name": "Initialized Capital",
                    "focus": "Seed stage B2B and consumer companies",
                    "check_size": "$250K - $2M",
                    "portfolio_fit": "Strong seed stage track record",
                    "contact": "General Partner: [Name]"
                },
                {
                    "name": "Homebrew",
                    "focus": "Seed stage companies changing daily life",
                    "check_size": "$500K - $1.5M",
                    "portfolio_fit": "Consumer and SMB-focused companies",
                    "contact": "Partner: [Name]"
                }
            ],
            "angel_investors": [
                {
                    "name": "Industry Expert Angels",
                    "description": "Former executives from relevant companies",
                    "value_add": "Industry expertise, customer introductions",
                    "check_size": "$25K - $100K",
                    "examples": ["Former Salesforce VP", "Ex-HubSpot CMO"]
                },
                {
                    "name": "Successful Entrepreneur Angels",
                    "description": "Founders who have built and exited companies",
                    "value_add": "Operational expertise, fundraising guidance",
                    "check_size": "$50K - $250K",
                    "examples": ["SaaS company founders", "Marketplace builders"]
                }
            ],
            "strategic_investors": [
                {
                    "name": "Corporate VCs",
                    "description": "Investment arms of large corporations",
                    "value_add": "Partnership opportunities, customer access",
                    "examples": ["Salesforce Ventures", "Microsoft Ventures", "Google Ventures"],
                    "considerations": "May have strategic agenda beyond financial returns"
                }
            ],
            "research_methodology": {
                "data_sources": [
                    "Crunchbase for investment history",
                    "PitchBook for detailed fund information",
                    "AngelList for angel investors",
                    "LinkedIn for warm introduction paths"
                ],
                "evaluation_criteria": [
                    "Investment stage and check size fit",
                    "Portfolio company relevance",
                    "Geographic focus alignment",
                    "Value-add beyond capital",
                    "Warm introduction availability"
                ]
            }
        }
    
    def create_pitch_materials(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive pitch materials"""
        project_name = project_data.get('name', 'Your Startup')
        
        return {
            "pitch_deck": {
                "slide_structure": [
                    {
                        "slide": 1,
                        "title": "Company Overview",
                        "content": "Company name, tagline, and one-liner description",
                        "key_elements": ["Logo", "Compelling tagline", "Clear value proposition"]
                    },
                    {
                        "slide": 2,
                        "title": "Problem",
                        "content": "The pain point you're solving",
                        "key_elements": ["Market size", "Current solutions' shortcomings", "Cost of problem"]
                    },
                    {
                        "slide": 3,
                        "title": "Solution",
                        "content": "Your unique approach to solving the problem",
                        "key_elements": ["Product demo", "Key features", "Differentiation"]
                    },
                    {
                        "slide": 4,
                        "title": "Market Opportunity",
                        "content": "TAM, SAM, SOM analysis",
                        "key_elements": ["Market size", "Growth rate", "Market trends"]
                    },
                    {
                        "slide": 5,
                        "title": "Product",
                        "content": "Product demonstration and roadmap",
                        "key_elements": ["Screenshots", "User flow", "Future features"]
                    },
                    {
                        "slide": 6,
                        "title": "Traction",
                        "content": "Proof of product-market fit",
                        "key_elements": ["User growth", "Revenue", "Key partnerships"]
                    },
                    {
                        "slide": 7,
                        "title": "Business Model",
                        "content": "How you make money",
                        "key_elements": ["Revenue streams", "Pricing strategy", "Unit economics"]
                    },
                    {
                        "slide": 8,
                        "title": "Competition",
                        "content": "Competitive landscape analysis",
                        "key_elements": ["Direct competitors", "Indirect competitors", "Competitive advantages"]
                    },
                    {
                        "slide": 9,
                        "title": "Team",
                        "content": "Why you're the right team to execute",
                        "key_elements": ["Founder backgrounds", "Key hires", "Advisory board"]
                    },
                    {
                        "slide": 10,
                        "title": "Financial Projections",
                        "content": "3-5 year financial forecast",
                        "key_elements": ["Revenue projections", "Key metrics", "Path to profitability"]
                    },
                    {
                        "slide": 11,
                        "title": "Funding Ask",
                        "content": "How much you're raising and why",
                        "key_elements": ["Funding amount", "Use of funds", "Milestones"]
                    },
                    {
                        "slide": 12,
                        "title": "Thank You",
                        "content": "Contact information and next steps",
                        "key_elements": ["Contact details", "Call to action", "Appendix reference"]
                    }
                ],
                "design_guidelines": {
                    "visual_style": "Clean, professional, consistent branding",
                    "content_density": "Minimal text, focus on visuals and key points",
                    "storytelling": "Logical flow that builds compelling narrative",
                    "timing": "10-12 minutes for presentation, 15-20 for Q&A"
                }
            },
            "executive_summary": {
                "length": "1-2 pages",
                "sections": [
                    "Company overview and mission",
                    "Problem and solution summary",
                    "Market opportunity highlights",
                    "Traction and key metrics",
                    "Team credentials",
                    "Funding requirements and use"
                ],
                "purpose": "Email attachment for initial investor outreach"
            },
            "financial_model": {
                "components": [
                    "Revenue projections (5 years)",
                    "Cost structure and unit economics",
                    "Cash flow projections",
                    "Key assumptions and drivers",
                    "Scenario analysis (base, optimistic, pessimistic)",
                    "Funding requirements and runway"
                ],
                "key_metrics": {
                    "saas": ["ARR", "MRR", "CAC", "LTV", "Churn rate", "NRR"],
                    "marketplace": ["GMV", "Take rate", "Active users", "Transaction volume"],
                    "ecommerce": ["Revenue", "Gross margin", "AOV", "Customer acquisition"]
                }
            },
            "supporting_materials": {
                "product_demo": "Video demonstration or live demo script",
                "customer_references": "Case studies and testimonials",
                "market_research": "Third-party validation of market size and trends",
                "technical_documentation": "Architecture overview and IP portfolio",
                "team_bios": "Detailed backgrounds of key team members",
                "press_coverage": "Media mentions and industry recognition"
            }
        }
    
    def create_outreach_plan(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create investor outreach plan"""
        return {
            "outreach_strategy": {
                "warm_introductions": {
                    "priority": "Highest",
                    "success_rate": "40-60%",
                    "approach": [
                        "Identify mutual connections through LinkedIn",
                        "Reach out to portfolio company founders",
                        "Leverage accelerator and university networks",
                        "Ask existing investors for introductions"
                    ],
                    "email_template": "Hi [Mutual Connection], I hope you're doing well. I'm reaching out because I'm raising a [Stage] round for [Company], and I believe [Investor] would be a great fit given their focus on [Relevant Focus]. Would you be comfortable making an introduction? Happy to send over our deck and executive summary. Best, [Your Name]"
                },
                "cold_outreach": {
                    "priority": "Medium",
                    "success_rate": "5-15%",
                    "approach": [
                        "Research investor's recent investments and interests",
                        "Personalize email with specific relevance",
                        "Keep initial email short and compelling",
                        "Include executive summary as attachment"
                    ],
                    "email_template": "Hi [Investor Name], I'm [Your Name], founder of [Company]. We're building [One-line description] and have achieved [Key traction metric]. Given your investment in [Portfolio Company] and focus on [Relevant Sector], I believe there could be strong alignment. Would you be interested in learning more? I've attached our executive summary. Best regards, [Your Name]"
                },
                "networking_events": {
                    "priority": "Medium",
                    "success_rate": "20-30%",
                    "events": [
                        "Industry conferences and summits",
                        "Investor meetups and demo days",
                        "Accelerator events and pitch competitions",
                        "University alumni events"
                    ],
                    "preparation": [
                        "Research attendee list in advance",
                        "Prepare 30-second elevator pitch",
                        "Bring business cards and one-pagers",
                        "Follow up within 24 hours"
                    ]
                }
            },
            "outreach_sequence": {
                "initial_contact": {
                    "timing": "Day 0",
                    "content": "Personalized introduction email with executive summary",
                    "goal": "Generate interest and secure initial meeting"
                },
                "follow_up_1": {
                    "timing": "Day 7",
                    "content": "Soft follow-up with additional context or recent milestone",
                    "goal": "Stay top of mind without being pushy"
                },
                "follow_up_2": {
                    "timing": "Day 21",
                    "content": "Share relevant industry news or company update",
                    "goal": "Provide value while maintaining contact"
                },
                "final_follow_up": {
                    "timing": "Day 45",
                    "content": "Final attempt with clear next steps",
                    "goal": "Get definitive yes/no response"
                }
            },
            "tracking_system": {
                "crm_setup": "Track all investor interactions in CRM",
                "key_fields": [
                    "Investor name and firm",
                    "Contact information",
                    "Introduction source",
                    "Meeting dates and outcomes",
                    "Follow-up requirements",
                    "Investment decision timeline"
                ],
                "pipeline_stages": [
                    "Research/Target",
                    "Initial Outreach",
                    "First Meeting",
                    "Due Diligence",
                    "Term Sheet",
                    "Closed/Passed"
                ]
            },
            "success_metrics": {
                "response_rate": "Target 20-30% for warm intros, 5-10% for cold",
                "meeting_conversion": "Target 50% of responses convert to meetings",
                "investment_conversion": "Target 10-20% of meetings result in investment",
                "timeline_targets": [
                    "50 investor targets identified - Week 1",
                    "Initial outreach completed - Week 4",
                    "10 first meetings scheduled - Week 8",
                    "Term sheet received - Week 16",
                    "Round closed - Week 24"
                ]
            }
        }
    
    def generate_investor_list_api(self, project_id: int) -> Dict[str, Any]:
        """API endpoint to generate investor target list"""
        return {
            "success": True,
            "list_id": random.randint(1000, 9999),
            "total_investors": random.randint(75, 150),
            "breakdown": {
                "tier_1_vcs": random.randint(15, 25),
                "tier_2_vcs": random.randint(20, 35),
                "angel_investors": random.randint(25, 50),
                "strategic_investors": random.randint(10, 20)
            },
            "warm_intro_opportunities": random.randint(20, 40),
            "estimated_outreach_timeline": "6-8 weeks",
            "success_probability": f"{random.uniform(65, 85):.0f}%",
            "recommended_approach": [
                "Start with warm introductions to tier 1 VCs",
                "Parallel outreach to angel investors",
                "Follow up with tier 2 VCs and strategic investors",
                "Maintain consistent communication cadence"
            ]
        }

