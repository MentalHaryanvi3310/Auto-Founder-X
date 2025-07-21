from src.models.user import db, Agent, BattleArenaCompetition
from datetime import date, timedelta

def init_agents():
    """Initialize the 14 AI agents as defined in the roadmap"""
    
    agents_data = [
        {
            'name': 'Ideation Agent',
            'type': 'ideation',
            'description': 'Mines Reddit, HN, Twitter, GitHub, ProductHunt, and indie tools for trends and opportunities',
            'capabilities': 'trend_analysis,market_research,tam_estimation,opportunity_identification'
        },
        {
            'name': 'Validation Agent',
            'type': 'validation',
            'description': 'Auto-posts to Reddit/HN/Quora, runs email tests, polls, creates waiting lists',
            'capabilities': 'survey_creation,market_validation,waiting_list_generation,feedback_collection'
        },
        {
            'name': 'Product Agent',
            'type': 'product',
            'description': 'Uses Replit + LangChain + Supabase to build MVP with third-party API integrations',
            'capabilities': 'mvp_development,api_integration,database_setup,deployment'
        },
        {
            'name': 'Design Agent',
            'type': 'design',
            'description': 'Generates brand kit, UI/UX using Figma plugins + Midjourney, converts to Tailwind/React',
            'capabilities': 'brand_design,ui_ux_design,component_generation,design_system_creation'
        },
        {
            'name': 'Marketing Agent',
            'type': 'marketing',
            'description': 'Builds landing page, SEO copy, newsletter, X thread, generates explainer videos',
            'capabilities': 'landing_page_creation,seo_optimization,content_marketing,video_generation'
        },
        {
            'name': 'Sales Agent',
            'type': 'sales',
            'description': 'Cold emails, LinkedIn outreach, B2B onboarding funnel, connects to Apollo/Instantly',
            'capabilities': 'cold_outreach,lead_generation,sales_funnel_creation,crm_integration'
        },
        {
            'name': 'Analytics Agent',
            'type': 'analytics',
            'description': 'Adds Google Analytics, PostHog, heatmaps, auto-generates reports & growth recommendations',
            'capabilities': 'analytics_setup,performance_tracking,report_generation,growth_analysis'
        },
        {
            'name': 'CRM Agent',
            'type': 'crm',
            'description': 'Tracks leads, manages users in Notion/HubSpot, triggers AI email follow-ups',
            'capabilities': 'lead_management,customer_tracking,automated_followups,pipeline_management'
        },
        {
            'name': 'VC Agent',
            'type': 'vc',
            'description': 'Writes pitch deck, records AI-generated founder pitch video, matches with VCs using Crunchbase',
            'capabilities': 'pitch_deck_creation,investor_matching,funding_strategy,presentation_generation'
        },
        {
            'name': 'Launch Agent',
            'type': 'launch',
            'description': 'Posts to ProductHunt, IndieHackers, X, etc., adds comment auto-replies, upvote tracking',
            'capabilities': 'product_launch,platform_posting,community_engagement,launch_tracking'
        },
        {
            'name': 'Learning Agent',
            'type': 'learning',
            'description': 'Tracks performance of every project & iterates MVP, uses past failures to train next version',
            'capabilities': 'performance_analysis,iteration_planning,failure_analysis,improvement_recommendations'
        },
        {
            'name': 'Legal Agent',
            'type': 'legal',
            'description': 'Auto-generates T&C, Privacy Policy, NDA, Freelancer Contracts using open source templates',
            'capabilities': 'legal_document_generation,compliance_checking,contract_creation,policy_writing'
        },
        {
            'name': 'Monetization Agent',
            'type': 'monetization',
            'description': 'Chooses best revenue model, implements pricing page + Stripe test plan',
            'capabilities': 'revenue_model_selection,pricing_strategy,payment_integration,monetization_optimization'
        },
        {
            'name': 'AI Integration Agent',
            'type': 'ai_integration',
            'description': 'Recommends best LLM per feature, auto-creates API bridges & tokens setup',
            'capabilities': 'ai_service_selection,api_integration,token_management,ai_optimization'
        }
    ]
    
    for agent_data in agents_data:
        # Check if agent already exists
        existing_agent = Agent.query.filter_by(type=agent_data['type']).first()
        if not existing_agent:
            agent = Agent(**agent_data)
            db.session.add(agent)
    
    db.session.commit()
    print("✅ Agents initialized successfully")

def init_sample_competitions():
    """Initialize sample battle arena competitions"""
    
    competitions_data = [
        {
            'name': 'AI Startup Showdown 2025',
            'description': 'Compete with your AI-powered startup ideas and win funding credits!',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
            'status': 'active',
            'prize_credits': 1000
        },
        {
            'name': 'SaaS Builder Challenge',
            'description': 'Build the next great SaaS tool and showcase it to the community',
            'start_date': date.today() + timedelta(days=7),
            'end_date': date.today() + timedelta(days=37),
            'status': 'upcoming',
            'prize_credits': 1500
        },
        {
            'name': 'Mobile App Innovation Contest',
            'description': 'Create innovative mobile applications that solve real-world problems',
            'start_date': date.today() + timedelta(days=14),
            'end_date': date.today() + timedelta(days=44),
            'status': 'upcoming',
            'prize_credits': 2000
        }
    ]
    
    for comp_data in competitions_data:
        # Check if competition already exists
        existing_comp = BattleArenaCompetition.query.filter_by(name=comp_data['name']).first()
        if not existing_comp:
            competition = BattleArenaCompetition(**comp_data)
            db.session.add(competition)
    
    db.session.commit()
    print("✅ Sample competitions initialized successfully")

def init_all_data():
    """Initialize all default data"""
    print("🚀 Initializing AutoFounder X data...")
    init_agents()
    init_sample_competitions()
    print("✅ All data initialized successfully!")

if __name__ == '__main__':
    init_all_data()

