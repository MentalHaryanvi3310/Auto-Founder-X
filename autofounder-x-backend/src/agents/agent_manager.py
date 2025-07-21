import asyncio
import threading
import time
from typing import Dict, Any, List, Optional
from enum import Enum

# Import all agent classes
from .ideation_agent import IdeationAgent
from .validation_agent import ValidationAgent
from .product_agent import ProductAgent
from .marketing_agent import MarketingAgent
from .design_agent import DesignAgent
from .sales_agent import SalesAgent
from .analytics_agent import AnalyticsAgent
from .crm_agent import CRMAgent
from .vc_agent import VCAgent
from .launch_agent import LaunchAgent
from .learning_agent import LearningAgent
from .legal_agent import LegalAgent
from .monetization_agent import MonetizationAgent

class AgentStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    BUILDING = "building"
    COMPLETED = "completed"
    ERROR = "error"

class AgentManager:
    """Manages all AI agents and their execution"""
    
    def __init__(self):
        self.agents = self._initialize_agents()
        self.agent_status = {agent_type: AgentStatus.IDLE for agent_type in self.agents.keys()}
        self.agent_results = {}
        self.agent_threads = {}
        self.project_data = {}
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all available agents"""
        return {
            "ideation": IdeationAgent(),
            "validation": ValidationAgent(),
            "product": ProductAgent(),
            "marketing": MarketingAgent(),
            "design": DesignAgent(),
            "sales": SalesAgent(),
            "analytics": AnalyticsAgent(),
            "crm": CRMAgent(),
            "vc": VCAgent(),
            "launch": LaunchAgent(),
            "learning": LearningAgent(),
            "legal": LegalAgent(),
            "monetization": MonetizationAgent()
        }
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get information about all available agents"""
        agents_info = []
        for agent_type, agent in self.agents.items():
            agents_info.append({
                "id": agent_type,
                "name": agent.name,
                "description": agent.description,
                "status": self.agent_status[agent_type].value,
                "last_activity": getattr(agent, 'last_activity', None),
                "current_task": getattr(agent, 'current_task', None),
                "progress": getattr(agent, 'progress', 0),
                "results_available": agent_type in self.agent_results
            })
        return agents_info
    
    def get_agent_status(self, agent_type: str) -> Dict[str, Any]:
        """Get detailed status of a specific agent"""
        if agent_type not in self.agents:
            return {"error": "Agent not found"}
        
        agent = self.agents[agent_type]
        return {
            "id": agent_type,
            "name": agent.name,
            "description": agent.description,
            "status": self.agent_status[agent_type].value,
            "last_activity": getattr(agent, 'last_activity', None),
            "current_task": getattr(agent, 'current_task', None),
            "progress": getattr(agent, 'progress', 0),
            "logs": getattr(agent, 'logs', []),
            "results_available": agent_type in self.agent_results,
            "execution_time": getattr(agent, 'execution_time', None)
        }
    
    def start_agent(self, agent_type: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start a specific agent"""
        if agent_type not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        if self.agent_status[agent_type] == AgentStatus.ACTIVE:
            return {"success": False, "error": "Agent is already running"}
        
        # Store project data for the agent
        self.project_data[agent_type] = project_data
        
        # Start agent in a separate thread
        thread = threading.Thread(
            target=self._execute_agent,
            args=(agent_type, project_data),
            daemon=True
        )
        thread.start()
        self.agent_threads[agent_type] = thread
        
        self.agent_status[agent_type] = AgentStatus.ACTIVE
        
        return {
            "success": True,
            "message": f"{self.agents[agent_type].name} started successfully",
            "agent_id": agent_type,
            "status": AgentStatus.ACTIVE.value
        }
    
    def stop_agent(self, agent_type: str) -> Dict[str, Any]:
        """Stop a specific agent"""
        if agent_type not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        if self.agent_status[agent_type] != AgentStatus.ACTIVE:
            return {"success": False, "error": "Agent is not running"}
        
        # Set agent status to idle (the thread will check this)
        self.agent_status[agent_type] = AgentStatus.IDLE
        agent = self.agents[agent_type]
        agent.stop()
        
        return {
            "success": True,
            "message": f"{agent.name} stopped successfully",
            "agent_id": agent_type,
            "status": AgentStatus.IDLE.value
        }
    
    def start_all_agents(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start all agents for a project"""
        started_agents = []
        failed_agents = []
        
        for agent_type in self.agents.keys():
            if self.agent_status[agent_type] == AgentStatus.IDLE:
                result = self.start_agent(agent_type, project_data)
                if result["success"]:
                    started_agents.append(agent_type)
                else:
                    failed_agents.append({"agent": agent_type, "error": result["error"]})
        
        return {
            "success": len(failed_agents) == 0,
            "started_agents": started_agents,
            "failed_agents": failed_agents,
            "total_started": len(started_agents),
            "message": f"Started {len(started_agents)} agents successfully"
        }
    
    def stop_all_agents(self) -> Dict[str, Any]:
        """Stop all running agents"""
        stopped_agents = []
        
        for agent_type in self.agents.keys():
            if self.agent_status[agent_type] == AgentStatus.ACTIVE:
                result = self.stop_agent(agent_type)
                if result["success"]:
                    stopped_agents.append(agent_type)
        
        return {
            "success": True,
            "stopped_agents": stopped_agents,
            "total_stopped": len(stopped_agents),
            "message": f"Stopped {len(stopped_agents)} agents successfully"
        }
    
    def get_agent_results(self, agent_type: str) -> Dict[str, Any]:
        """Get results from a specific agent"""
        if agent_type not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        if agent_type not in self.agent_results:
            return {"success": False, "error": "No results available"}
        
        return {
            "success": True,
            "agent_id": agent_type,
            "agent_name": self.agents[agent_type].name,
            "results": self.agent_results[agent_type],
            "status": self.agent_status[agent_type].value
        }
    
    def get_all_results(self) -> Dict[str, Any]:
        """Get results from all agents that have completed"""
        all_results = {}
        
        for agent_type, results in self.agent_results.items():
            all_results[agent_type] = {
                "agent_name": self.agents[agent_type].name,
                "status": self.agent_status[agent_type].value,
                "results": results
            }
        
        return {
            "success": True,
            "total_agents": len(self.agents),
            "completed_agents": len(all_results),
            "results": all_results
        }
    
    def _execute_agent(self, agent_type: str, project_data: Dict[str, Any]):
        """Execute an agent in a separate thread"""
        try:
            agent = self.agents[agent_type]
            self.agent_status[agent_type] = AgentStatus.BUILDING
            
            # Execute the agent
            start_time = time.time()
            results = agent.execute(project_data)
            execution_time = time.time() - start_time
            
            # Store results
            self.agent_results[agent_type] = results
            agent.execution_time = execution_time
            
            # Update status
            if self.agent_status[agent_type] != AgentStatus.IDLE:  # Check if not manually stopped
                self.agent_status[agent_type] = AgentStatus.COMPLETED
                
        except Exception as e:
            self.agent_status[agent_type] = AgentStatus.ERROR
            self.agent_results[agent_type] = {
                "error": str(e),
                "agent_type": agent_type,
                "timestamp": time.time()
            }
    
    def configure_agent(self, agent_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Configure a specific agent"""
        if agent_type not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        agent = self.agents[agent_type]
        
        # Apply configuration
        for key, value in config.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        return {
            "success": True,
            "message": f"{agent.name} configured successfully",
            "agent_id": agent_type,
            "config": config
        }
    
    def get_agent_logs(self, agent_type: str) -> Dict[str, Any]:
        """Get logs from a specific agent"""
        if agent_type not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        agent = self.agents[agent_type]
        logs = getattr(agent, 'logs', [])
        
        return {
            "success": True,
            "agent_id": agent_type,
            "agent_name": agent.name,
            "logs": logs,
            "log_count": len(logs)
        }
    
    def clear_agent_results(self, agent_type: str = None) -> Dict[str, Any]:
        """Clear results for a specific agent or all agents"""
        if agent_type:
            if agent_type not in self.agents:
                return {"success": False, "error": "Agent not found"}
            
            if agent_type in self.agent_results:
                del self.agent_results[agent_type]
            
            # Reset agent state
            agent = self.agents[agent_type]
            agent.reset()
            self.agent_status[agent_type] = AgentStatus.IDLE
            
            return {
                "success": True,
                "message": f"Results cleared for {agent.name}",
                "agent_id": agent_type
            }
        else:
            # Clear all results
            self.agent_results.clear()
            
            # Reset all agents
            for agent_type, agent in self.agents.items():
                agent.reset()
                self.agent_status[agent_type] = AgentStatus.IDLE
            
            return {
                "success": True,
                "message": "All agent results cleared",
                "cleared_count": len(self.agents)
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        status_counts = {}
        for status in AgentStatus:
            status_counts[status.value] = sum(1 for s in self.agent_status.values() if s == status)
        
        return {
            "total_agents": len(self.agents),
            "status_breakdown": status_counts,
            "active_agents": [agent_type for agent_type, status in self.agent_status.items() if status == AgentStatus.ACTIVE],
            "completed_agents": [agent_type for agent_type, status in self.agent_status.items() if status == AgentStatus.COMPLETED],
            "available_results": len(self.agent_results),
            "system_health": "healthy" if status_counts.get("error", 0) == 0 else "degraded"
        }

# Global agent manager instance
agent_manager = AgentManager()

