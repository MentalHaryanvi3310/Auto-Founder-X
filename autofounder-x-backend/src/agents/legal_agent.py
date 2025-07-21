import random
from typing import Dict, Any, List
from .base_agent import BaseAgent

class LegalAgent(BaseAgent):
    """AI Agent for legal compliance and documentation"""
    
    def __init__(self):
        super().__init__(
            agent_type="legal",
            name="Legal Agent",
            description="Handles legal compliance and documentation"
        )
    
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute legal compliance and documentation setup"""
        self.log("Starting legal compliance and documentation setup...")
        
        steps = [
            "Analyzing legal requirements",
            "Creating business entity structure",
            "Drafting terms of service and privacy policy",
            "Setting up intellectual property protection",
            "Ensuring regulatory compliance",
            "Creating employment and contractor agreements",
            "Establishing data protection measures"
        ]
        
        self.simulate_work(steps, 0.8)
        
        # Generate legal results
        business_structure = self.setup_business_structure(project_data)
        legal_documents = self.create_legal_documents(project_data)
        ip_protection = self.setup_ip_protection(project_data)
        compliance_framework = self.establish_compliance_framework(project_data)
        
        result = {
            "business_structure": business_structure,
            "legal_documents": legal_documents,
            "ip_protection": ip_protection,
            "compliance_framework": compliance_framework,
            "compliance_score": random.uniform(0.85, 0.97),
            "legal_risk_level": "Low to Medium"
        }
        
        self.results = result
        return self.generate_mock_result("legal_setup", result)
    
    def setup_business_structure(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Setup appropriate business structure"""
        business_model = project_data.get('business_model', 'saas')
        target_market = project_data.get('target_market', '')
        funding_plans = project_data.get('funding_plans', 'yes')
        
        # Recommend business structure based on needs
        if funding_plans == 'yes' or 'venture' in str(project_data.get('funding_type', '')).lower():
            recommended_structure = {
                "entity_type": "Delaware C-Corporation",
                "rationale": "Preferred by investors, allows multiple share classes, favorable tax treatment for stock options",
                "benefits": [
                    "Investor-friendly structure",
                    "Stock option plans for employees",
                    "Potential for tax-free reorganizations",
                    "Well-established legal precedents"
                ],
                "considerations": [
                    "Double taxation on profits",
                    "More complex reporting requirements",
                    "Higher setup and maintenance costs"
                ]
            }
        elif business_model in ['consulting', 'services']:
            recommended_structure = {
                "entity_type": "LLC (Limited Liability Company)",
                "rationale": "Flexible structure, pass-through taxation, simpler compliance",
                "benefits": [
                    "Pass-through taxation (no double taxation)",
                    "Flexible management structure",
                    "Limited personal liability",
                    "Simpler compliance requirements"
                ],
                "considerations": [
                    "Limited ability to raise venture capital",
                    "Self-employment taxes on profits",
                    "Varying state regulations"
                ]
            }
        else:
            recommended_structure = {
                "entity_type": "Delaware C-Corporation",
                "rationale": "Scalable structure for growth-oriented businesses",
                "benefits": [
                    "Professional credibility",
                    "Ability to raise capital",
                    "Employee stock option plans",
                    "Perpetual existence"
                ]
            }
        
        return {
            "recommended_structure": recommended_structure,
            "incorporation_process": {
                "steps": [
                    "Choose and reserve company name",
                    "File Certificate of Incorporation",
                    "Create corporate bylaws",
                    "Issue initial stock certificates",
                    "Obtain Federal EIN (Tax ID)",
                    "Open business bank account",
                    "File initial state reports"
                ],
                "timeline": "2-4 weeks",
                "estimated_cost": "$500-2000 (including legal fees)",
                "required_documents": [
                    "Certificate of Incorporation",
                    "Corporate Bylaws",
                    "Stock Purchase Agreements",
                    "Board Resolutions",
                    "Shareholder Agreements"
                ]
            },
            "ongoing_compliance": {
                "annual_requirements": [
                    "Annual franchise tax payment",
                    "Annual report filing",
                    "Board meeting minutes",
                    "Stock ledger maintenance"
                ],
                "estimated_annual_cost": "$300-800",
                "key_deadlines": [
                    "March 1: Annual franchise tax due",
                    "December 31: Annual report due",
                    "Quarterly: Board meetings recommended"
                ]
            },
            "equity_structure": {
                "authorized_shares": "10,000,000 shares",
                "initial_issuance": "8,000,000 shares to founders",
                "employee_option_pool": "1,500,000 shares (15%)",
                "reserved_for_investors": "500,000 shares (5%)",
                "vesting_schedule": "4-year vesting with 1-year cliff for founders and employees"
            }
        }
    
    def create_legal_documents(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create essential legal documents"""
        business_model = project_data.get('business_model', 'saas')
        
        return {
            "customer_facing_documents": {
                "terms_of_service": {
                    "purpose": "Define relationship between company and users",
                    "key_sections": [
                        "Service description and availability",
                        "User responsibilities and prohibited uses",
                        "Payment terms and refund policy",
                        "Intellectual property rights",
                        "Limitation of liability and disclaimers",
                        "Termination and suspension rights",
                        "Dispute resolution and governing law"
                    ],
                    "industry_specific_clauses": self.get_industry_specific_clauses(business_model),
                    "update_frequency": "Annually or when material changes occur"
                },
                "privacy_policy": {
                    "purpose": "Disclose data collection, use, and protection practices",
                    "key_sections": [
                        "Types of information collected",
                        "How information is used and shared",
                        "Data retention and deletion policies",
                        "User rights and choices",
                        "Security measures and breach notification",
                        "International data transfers",
                        "Contact information for privacy inquiries"
                    ],
                    "compliance_requirements": [
                        "GDPR (EU users)",
                        "CCPA (California users)",
                        "COPPA (if serving children under 13)",
                        "PIPEDA (Canadian users)"
                    ]
                },
                "cookie_policy": {
                    "purpose": "Disclose use of cookies and tracking technologies",
                    "requirements": "Required for GDPR compliance",
                    "key_elements": [
                        "Types of cookies used",
                        "Purpose of each cookie category",
                        "User consent mechanisms",
                        "How to disable cookies"
                    ]
                }
            },
            "business_agreements": {
                "customer_agreements": {
                    "saas_subscription_agreement": {
                        "purpose": "Govern paid subscription relationships",
                        "key_terms": [
                            "Service level agreements (SLAs)",
                            "Data ownership and portability",
                            "Subscription terms and auto-renewal",
                            "Support and maintenance obligations"
                        ]
                    },
                    "enterprise_service_agreement": {
                        "purpose": "Govern enterprise customer relationships",
                        "key_terms": [
                            "Custom pricing and payment terms",
                            "Enhanced security and compliance requirements",
                            "Professional services and implementation",
                            "Dedicated support and account management"
                        ]
                    }
                },
                "vendor_agreements": {
                    "software_license_agreements": {
                        "purpose": "License third-party software and tools",
                        "considerations": [
                            "Open source license compliance",
                            "Commercial software licensing terms",
                            "API usage agreements",
                            "Cloud service provider agreements"
                        ]
                    },
                    "professional_services_agreements": {
                        "purpose": "Engage consultants and service providers",
                        "key_terms": [
                            "Scope of work and deliverables",
                            "Payment terms and milestones",
                            "Intellectual property ownership",
                            "Confidentiality and non-disclosure"
                        ]
                    }
                }
            },
            "employment_documents": {
                "employee_handbook": {
                    "purpose": "Establish workplace policies and procedures",
                    "key_sections": [
                        "Company culture and values",
                        "Employment policies and procedures",
                        "Benefits and compensation information",
                        "Code of conduct and ethics",
                        "Anti-discrimination and harassment policies",
                        "Remote work and flexible arrangements"
                    ]
                },
                "employment_agreements": {
                    "offer_letters": "Standardized offer letter templates",
                    "employment_contracts": "At-will employment agreements with key terms",
                    "contractor_agreements": "Independent contractor agreements",
                    "non_disclosure_agreements": "Employee and contractor NDAs"
                },
                "equity_documents": {
                    "stock_option_plan": "Equity incentive plan for employees",
                    "option_agreements": "Individual stock option grants",
                    "restricted_stock_agreements": "Founder and early employee equity"
                }
            }
        }
    
    def get_industry_specific_clauses(self, business_model: str) -> List[str]:
        """Get industry-specific legal clauses"""
        clauses = {
            'saas': [
                "Service availability and uptime guarantees",
                "Data backup and disaster recovery",
                "API usage limits and restrictions",
                "Integration and third-party service disclaimers"
            ],
            'marketplace': [
                "User-generated content policies",
                "Transaction dispute resolution",
                "Seller verification and compliance",
                "Payment processing and escrow terms"
            ],
            'ecommerce': [
                "Product descriptions and warranty disclaimers",
                "Shipping and delivery terms",
                "Return and refund policies",
                "Product liability limitations"
            ],
            'fintech': [
                "Financial services regulations compliance",
                "Anti-money laundering (AML) requirements",
                "Know Your Customer (KYC) procedures",
                "Payment Card Industry (PCI) compliance"
            ]
        }
        
        return clauses.get(business_model, clauses['saas'])
    
    def setup_ip_protection(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Setup intellectual property protection"""
        return {
            "trademark_protection": {
                "company_name": {
                    "recommendation": "File federal trademark application",
                    "timeline": "6-12 months for approval",
                    "cost": "$275-400 per class (USPTO fees) + attorney fees",
                    "benefits": [
                        "Exclusive right to use name in commerce",
                        "Legal presumption of ownership",
                        "Ability to prevent confusingly similar marks",
                        "Enhanced damages for infringement"
                    ]
                },
                "logo_and_branding": {
                    "recommendation": "Consider trademark for distinctive logos",
                    "considerations": [
                        "Distinctiveness of design elements",
                        "Commercial use and recognition",
                        "Cost-benefit analysis for small businesses"
                    ]
                },
                "product_names": {
                    "recommendation": "Trademark key product and service names",
                    "strategy": "File applications as products gain market traction"
                }
            },
            "copyright_protection": {
                "software_code": {
                    "protection": "Automatic copyright protection upon creation",
                    "recommendations": [
                        "Include copyright notices in code",
                        "Maintain detailed development records",
                        "Consider formal registration for key components"
                    ]
                },
                "content_and_materials": {
                    "protection": "Website content, marketing materials, documentation",
                    "best_practices": [
                        "Copyright notices on all materials",
                        "Clear ownership policies for employee-created content",
                        "Proper licensing for third-party content"
                    ]
                }
            },
            "trade_secret_protection": {
                "confidential_information": {
                    "scope": [
                        "Proprietary algorithms and code",
                        "Customer lists and data",
                        "Business strategies and plans",
                        "Technical know-how and processes"
                    ],
                    "protection_measures": [
                        "Non-disclosure agreements with all personnel",
                        "Access controls and information security",
                        "Clear identification of confidential materials",
                        "Employee training on confidentiality obligations"
                    ]
                }
            },
            "patent_considerations": {
                "software_patents": {
                    "recommendation": "Evaluate patentability of core innovations",
                    "considerations": [
                        "High cost and complexity of patent prosecution",
                        "Limited enforceability of software patents",
                        "Alternative protection through trade secrets",
                        "Defensive patent strategies"
                    ],
                    "timeline": "18-36 months for approval",
                    "cost": "$10,000-25,000 per patent including attorney fees"
                }
            },
            "ip_management": {
                "invention_assignment": {
                    "requirement": "All employees and contractors must assign IP rights",
                    "documentation": "Invention assignment agreements in employment contracts"
                },
                "ip_audit": {
                    "frequency": "Annual review of IP portfolio",
                    "scope": [
                        "Identify new protectable IP",
                        "Review existing registrations and renewals",
                        "Assess competitive landscape",
                        "Evaluate licensing opportunities"
                    ]
                }
            }
        }
    
    def establish_compliance_framework(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Establish regulatory compliance framework"""
        business_model = project_data.get('business_model', 'saas')
        target_market = project_data.get('target_market', '')
        
        return {
            "data_protection_compliance": {
                "gdpr_compliance": {
                    "applicability": "Required if serving EU users",
                    "key_requirements": [
                        "Lawful basis for data processing",
                        "User consent mechanisms",
                        "Data subject rights (access, deletion, portability)",
                        "Data breach notification procedures",
                        "Privacy by design and default",
                        "Data Protection Officer (if required)"
                    ],
                    "implementation_steps": [
                        "Conduct data mapping and privacy impact assessment",
                        "Update privacy policy and consent mechanisms",
                        "Implement data subject request procedures",
                        "Establish breach notification processes",
                        "Train staff on GDPR requirements"
                    ],
                    "penalties": "Up to 4% of annual revenue or €20M"
                },
                "ccpa_compliance": {
                    "applicability": "Required if serving California residents",
                    "key_requirements": [
                        "Consumer right to know about data collection",
                        "Right to delete personal information",
                        "Right to opt-out of sale of personal information",
                        "Non-discrimination for exercising rights"
                    ],
                    "implementation_steps": [
                        "Update privacy policy with CCPA disclosures",
                        "Implement consumer request mechanisms",
                        "Establish 'Do Not Sell' processes",
                        "Train customer service on CCPA procedures"
                    ]
                }
            },
            "industry_specific_compliance": self.get_industry_compliance(business_model),
            "employment_compliance": {
                "federal_requirements": [
                    "Equal Employment Opportunity (EEO) compliance",
                    "Fair Labor Standards Act (FLSA) wage and hour rules",
                    "Family and Medical Leave Act (FMLA) if 50+ employees",
                    "Occupational Safety and Health Act (OSHA) workplace safety"
                ],
                "state_requirements": [
                    "State-specific employment laws",
                    "Workers' compensation insurance",
                    "Unemployment insurance",
                    "State disability insurance (where applicable)"
                ],
                "contractor_classification": {
                    "importance": "Proper classification to avoid penalties",
                    "factors": [
                        "Degree of control over work",
                        "Financial aspects of relationship",
                        "Type of relationship and permanency"
                    ],
                    "documentation": "Clear contractor agreements and work arrangements"
                }
            },
            "tax_compliance": {
                "federal_taxes": [
                    "Corporate income tax (if C-Corp)",
                    "Employment taxes (Social Security, Medicare, unemployment)",
                    "Quarterly estimated tax payments",
                    "Annual tax return filing"
                ],
                "state_taxes": [
                    "State income tax (varies by state)",
                    "State employment taxes",
                    "Sales tax (if applicable)",
                    "Annual state filings"
                ],
                "sales_tax_considerations": {
                    "nexus_rules": "Physical or economic presence triggers tax obligations",
                    "digital_services": "Varying state rules for SaaS and digital products",
                    "compliance_tools": "Consider automated sales tax solutions"
                }
            },
            "compliance_monitoring": {
                "regular_reviews": {
                    "quarterly": "Review new regulations and compliance updates",
                    "annually": "Comprehensive compliance audit and policy updates",
                    "ongoing": "Monitor regulatory changes and industry developments"
                },
                "compliance_calendar": {
                    "setup": "Track all compliance deadlines and requirements",
                    "automation": "Automated reminders for key deadlines",
                    "documentation": "Maintain compliance documentation and records"
                }
            }
        }
    
    def get_industry_compliance(self, business_model: str) -> Dict[str, Any]:
        """Get industry-specific compliance requirements"""
        compliance_frameworks = {
            'fintech': {
                "regulations": [
                    "Bank Secrecy Act (BSA) and Anti-Money Laundering (AML)",
                    "Know Your Customer (KYC) requirements",
                    "Payment Card Industry Data Security Standard (PCI DSS)",
                    "State money transmitter licenses (if applicable)"
                ],
                "oversight_bodies": ["FinCEN", "CFPB", "State banking regulators"],
                "key_requirements": [
                    "Customer identification and verification",
                    "Suspicious activity reporting",
                    "Data security and encryption",
                    "Regular compliance audits"
                ]
            },
            'healthcare': {
                "regulations": [
                    "Health Insurance Portability and Accountability Act (HIPAA)",
                    "Health Information Technology for Economic and Clinical Health (HITECH)",
                    "FDA regulations (if medical device software)"
                ],
                "key_requirements": [
                    "Protected Health Information (PHI) safeguards",
                    "Business Associate Agreements (BAAs)",
                    "Breach notification procedures",
                    "Access controls and audit logs"
                ]
            },
            'education': {
                "regulations": [
                    "Family Educational Rights and Privacy Act (FERPA)",
                    "Children's Online Privacy Protection Act (COPPA)",
                    "Student Data Privacy Consortium guidelines"
                ],
                "key_requirements": [
                    "Student record privacy protection",
                    "Parental consent for children under 13",
                    "Data minimization and purpose limitation",
                    "Secure data transmission and storage"
                ]
            }
        }
        
        return compliance_frameworks.get(business_model, {
            "regulations": ["General business regulations"],
            "key_requirements": ["Standard business compliance practices"]
        })
    
    def generate_legal_checklist_api(self, project_id: int) -> Dict[str, Any]:
        """API endpoint to generate legal compliance checklist"""
        return {
            "success": True,
            "checklist_id": random.randint(1000, 9999),
            "checklist_type": "Startup Legal Compliance",
            "priority_items": [
                {
                    "item": "Incorporate business entity",
                    "status": "pending",
                    "priority": "high",
                    "deadline": "Within 30 days",
                    "estimated_cost": "$500-2000"
                },
                {
                    "item": "Draft Terms of Service and Privacy Policy",
                    "status": "pending",
                    "priority": "high",
                    "deadline": "Before public launch",
                    "estimated_cost": "$1000-3000"
                },
                {
                    "item": "Trademark company name and logo",
                    "status": "pending",
                    "priority": "medium",
                    "deadline": "Within 90 days",
                    "estimated_cost": "$1000-2500"
                },
                {
                    "item": "Set up employment agreements and equity plans",
                    "status": "pending",
                    "priority": "medium",
                    "deadline": "Before hiring employees",
                    "estimated_cost": "$2000-5000"
                }
            ],
            "compliance_score": random.randint(65, 85),
            "estimated_total_cost": f"${random.randint(5000, 15000)}",
            "recommended_timeline": "3-6 months for full compliance",
            "next_steps": [
                "Schedule consultation with business attorney",
                "Begin incorporation process",
                "Start drafting customer-facing legal documents",
                "Research industry-specific compliance requirements"
            ]
        }

