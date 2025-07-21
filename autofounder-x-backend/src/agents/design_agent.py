import random
from typing import Dict, Any, List
from .base_agent import BaseAgent

class DesignAgent(BaseAgent):
    """AI Agent for design and brand kit generation"""
    
    def __init__(self):
        super().__init__(
            agent_type="design",
            name="Design Agent",
            description="Generates brand kits and UI components"
        )
    
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute design and branding work"""
        self.log("Starting design and branding work...")
        
        steps = [
            "Analyzing brand requirements",
            "Creating color palette",
            "Designing logo concepts",
            "Developing typography system",
            "Creating UI component library",
            "Designing marketing materials",
            "Generating brand guidelines"
        ]
        
        self.simulate_work(steps, 0.6)
        
        # Generate design results
        brand_kit = self.create_brand_kit(project_data)
        ui_components = self.design_ui_components(project_data)
        marketing_materials = self.create_marketing_materials(project_data)
        brand_guidelines = self.generate_brand_guidelines(project_data)
        
        result = {
            "brand_kit": brand_kit,
            "ui_components": ui_components,
            "marketing_materials": marketing_materials,
            "brand_guidelines": brand_guidelines,
            "design_system_completeness": random.uniform(0.85, 0.98)
        }
        
        self.results = result
        return self.generate_mock_result("design_system", result)
    
    def create_brand_kit(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive brand kit"""
        project_name = project_data.get('name', 'Your Startup')
        business_model = project_data.get('business_model', 'saas')
        
        # Color palettes based on business model
        color_palettes = {
            'saas': {
                "primary": "#2563eb",
                "secondary": "#64748b",
                "accent": "#10b981",
                "success": "#22c55e",
                "warning": "#f59e0b",
                "error": "#ef4444",
                "neutral": {
                    "50": "#f8fafc",
                    "100": "#f1f5f9",
                    "500": "#64748b",
                    "900": "#0f172a"
                }
            },
            'marketplace': {
                "primary": "#7c3aed",
                "secondary": "#6b7280",
                "accent": "#f59e0b",
                "success": "#10b981",
                "warning": "#f97316",
                "error": "#dc2626",
                "neutral": {
                    "50": "#fafafa",
                    "100": "#f4f4f5",
                    "500": "#71717a",
                    "900": "#18181b"
                }
            },
            'ecommerce': {
                "primary": "#dc2626",
                "secondary": "#374151",
                "accent": "#059669",
                "success": "#16a34a",
                "warning": "#ca8a04",
                "error": "#b91c1c",
                "neutral": {
                    "50": "#f9fafb",
                    "100": "#f3f4f6",
                    "500": "#6b7280",
                    "900": "#111827"
                }
            }
        }
        
        return {
            "logo": {
                "primary_logo": f"{project_name}_logo_primary.svg",
                "secondary_logo": f"{project_name}_logo_secondary.svg",
                "icon_only": f"{project_name}_icon.svg",
                "variations": [
                    "Full color on white",
                    "White on dark",
                    "Single color",
                    "Monochrome"
                ],
                "logo_concept": "Modern, clean design with geometric elements representing innovation and reliability"
            },
            "color_palette": color_palettes.get(business_model, color_palettes['saas']),
            "typography": {
                "primary_font": {
                    "name": "Inter",
                    "weights": ["400", "500", "600", "700"],
                    "usage": "Headings, UI elements, body text"
                },
                "secondary_font": {
                    "name": "JetBrains Mono",
                    "weights": ["400", "500"],
                    "usage": "Code, technical content"
                },
                "font_scale": {
                    "xs": "12px",
                    "sm": "14px",
                    "base": "16px",
                    "lg": "18px",
                    "xl": "20px",
                    "2xl": "24px",
                    "3xl": "30px",
                    "4xl": "36px",
                    "5xl": "48px"
                }
            },
            "iconography": {
                "style": "Outline icons with 2px stroke",
                "library": "Lucide React",
                "custom_icons": [
                    f"{project_name} logo icon",
                    "Feature-specific icons",
                    "Navigation icons"
                ]
            },
            "imagery": {
                "style": "Modern, clean photography with consistent lighting",
                "color_treatment": "Slight blue tint to match brand colors",
                "subjects": "Diverse professionals, modern workspaces, technology",
                "illustration_style": "Minimal line art with brand accent colors"
            }
        }
    
    def design_ui_components(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design UI component library"""
        return {
            "design_system": {
                "spacing_scale": {
                    "xs": "4px",
                    "sm": "8px", 
                    "md": "16px",
                    "lg": "24px",
                    "xl": "32px",
                    "2xl": "48px",
                    "3xl": "64px"
                },
                "border_radius": {
                    "sm": "4px",
                    "md": "8px",
                    "lg": "12px",
                    "xl": "16px",
                    "full": "9999px"
                },
                "shadows": {
                    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
                    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
                }
            },
            "components": [
                {
                    "name": "Button",
                    "variants": ["Primary", "Secondary", "Outline", "Ghost", "Link"],
                    "sizes": ["Small", "Medium", "Large"],
                    "states": ["Default", "Hover", "Active", "Disabled", "Loading"]
                },
                {
                    "name": "Input",
                    "variants": ["Text", "Email", "Password", "Search", "Textarea"],
                    "sizes": ["Small", "Medium", "Large"],
                    "states": ["Default", "Focus", "Error", "Disabled"]
                },
                {
                    "name": "Card",
                    "variants": ["Default", "Elevated", "Outlined"],
                    "components": ["Header", "Content", "Footer", "Actions"]
                },
                {
                    "name": "Navigation",
                    "variants": ["Top nav", "Side nav", "Breadcrumbs", "Tabs"],
                    "states": ["Active", "Inactive", "Hover"]
                },
                {
                    "name": "Modal",
                    "variants": ["Dialog", "Alert", "Confirmation", "Form"],
                    "sizes": ["Small", "Medium", "Large", "Full screen"]
                },
                {
                    "name": "Table",
                    "variants": ["Basic", "Striped", "Bordered", "Hoverable"],
                    "features": ["Sorting", "Filtering", "Pagination", "Selection"]
                },
                {
                    "name": "Form Elements",
                    "components": ["Checkbox", "Radio", "Select", "Switch", "Slider"],
                    "states": ["Default", "Checked", "Disabled", "Error"]
                },
                {
                    "name": "Feedback",
                    "components": ["Alert", "Toast", "Progress", "Loading", "Empty state"],
                    "variants": ["Success", "Warning", "Error", "Info"]
                }
            ],
            "layout_components": [
                {
                    "name": "Grid System",
                    "breakpoints": ["sm: 640px", "md: 768px", "lg: 1024px", "xl: 1280px"],
                    "columns": 12,
                    "gutters": ["16px", "24px", "32px"]
                },
                {
                    "name": "Container",
                    "max_widths": ["sm: 640px", "md: 768px", "lg: 1024px", "xl: 1280px"],
                    "padding": "16px on mobile, 24px on desktop"
                }
            ]
        }
    
    def create_marketing_materials(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create marketing material templates"""
        project_name = project_data.get('name', 'Your Startup')
        
        return {
            "digital_assets": [
                {
                    "type": "Social Media Templates",
                    "formats": [
                        "LinkedIn post (1200x627px)",
                        "Twitter header (1500x500px)",
                        "Instagram post (1080x1080px)",
                        "Facebook cover (820x312px)"
                    ],
                    "variations": ["Product announcement", "Feature highlight", "Company news", "Thought leadership"]
                },
                {
                    "type": "Web Graphics",
                    "formats": [
                        "Hero banner (1920x600px)",
                        "Feature icons (64x64px)",
                        "Product screenshots (mockups)",
                        "Testimonial graphics"
                    ]
                },
                {
                    "type": "Email Templates",
                    "formats": [
                        "Welcome email",
                        "Newsletter template",
                        "Product update",
                        "Promotional email"
                    ],
                    "specifications": "600px width, mobile responsive"
                },
                {
                    "type": "Presentation Templates",
                    "formats": [
                        "Pitch deck (16:9)",
                        "Product demo slides",
                        "Company overview",
                        "Sales presentation"
                    ],
                    "slide_count": "15-20 slides per template"
                }
            ],
            "print_materials": [
                {
                    "type": "Business Cards",
                    "size": "3.5 x 2 inches",
                    "variations": ["Standard", "Premium", "Digital card"]
                },
                {
                    "type": "Letterhead",
                    "size": "8.5 x 11 inches",
                    "elements": ["Logo", "Contact info", "Brand colors"]
                },
                {
                    "type": "Brochures",
                    "formats": ["Tri-fold", "Bi-fold", "Single page"],
                    "purpose": "Product overview, company profile"
                }
            ],
            "digital_brand_assets": {
                "favicon": "32x32px, 16x16px, ICO format",
                "app_icons": "iOS and Android app icons in all required sizes",
                "og_images": "1200x630px for social media sharing",
                "email_signatures": "HTML and image versions"
            }
        }
    
    def generate_brand_guidelines(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive brand guidelines"""
        project_name = project_data.get('name', 'Your Startup')
        
        return {
            "brand_overview": {
                "mission": f"To empower businesses with innovative solutions that drive growth and efficiency",
                "vision": f"To be the leading platform that transforms how businesses operate in the digital age",
                "values": ["Innovation", "Reliability", "User-centricity", "Transparency"],
                "brand_personality": ["Professional", "Approachable", "Innovative", "Trustworthy"]
            },
            "logo_usage": {
                "do": [
                    "Use the primary logo on white backgrounds",
                    "Maintain minimum clear space around logo",
                    "Use approved color variations only",
                    "Ensure logo is legible at all sizes"
                ],
                "dont": [
                    "Stretch or distort the logo",
                    "Use unapproved colors",
                    "Place logo on busy backgrounds",
                    "Use logo smaller than minimum size (24px)"
                ],
                "minimum_sizes": {
                    "digital": "24px height",
                    "print": "0.5 inch height"
                },
                "clear_space": "Equal to the height of the logo mark"
            },
            "color_usage": {
                "primary_applications": "Buttons, links, key UI elements",
                "secondary_applications": "Text, borders, backgrounds",
                "accessibility": "All color combinations meet WCAG AA standards",
                "color_ratios": {
                    "primary": "20% of design",
                    "secondary": "30% of design", 
                    "neutral": "50% of design"
                }
            },
            "typography_hierarchy": {
                "h1": "48px, Bold, Primary color",
                "h2": "36px, Bold, Primary color",
                "h3": "24px, Semibold, Secondary color",
                "h4": "20px, Semibold, Secondary color",
                "body": "16px, Regular, Neutral color",
                "caption": "14px, Regular, Muted color"
            },
            "voice_and_tone": {
                "voice_characteristics": ["Clear", "Confident", "Helpful", "Professional"],
                "tone_variations": {
                    "marketing": "Enthusiastic and inspiring",
                    "product": "Clear and instructional",
                    "support": "Empathetic and solution-focused",
                    "legal": "Formal and precise"
                },
                "writing_guidelines": [
                    "Use active voice",
                    "Keep sentences concise",
                    "Avoid jargon",
                    "Be inclusive and accessible"
                ]
            },
            "application_examples": {
                "website": "Homepage, product pages, blog",
                "mobile_app": "iOS and Android applications",
                "marketing": "Ads, social media, email campaigns",
                "print": "Business cards, brochures, signage",
                "merchandise": "T-shirts, stickers, promotional items"
            }
        }
    
    def generate_brand_kit_api(self, project_id: int) -> Dict[str, Any]:
        """API endpoint to generate brand kit"""
        return {
            "success": True,
            "brand_kit_id": random.randint(1000, 9999),
            "status": "generated",
            "deliverables": [
                "Logo files (SVG, PNG, JPG)",
                "Color palette with hex codes",
                "Typography specifications",
                "UI component library",
                "Brand guidelines PDF",
                "Marketing templates"
            ],
            "download_url": f"https://assets.autofounder-x.com/brand-kit/{random.randint(1000, 9999)}.zip",
            "preview_url": f"https://preview.autofounder-x.com/brand-kit/{random.randint(1000, 9999)}",
            "customization_options": [
                "Color palette adjustment",
                "Logo style variations",
                "Typography alternatives",
                "Additional templates"
            ]
        }

