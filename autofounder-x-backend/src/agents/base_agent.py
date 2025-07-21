import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all AI agents in AutoFounder X"""
    
    def __init__(self, agent_type: str, name: str, description: str):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.status = "idle"  # idle, running, completed, failed
        self.progress = 0
        self.current_task = ""
        self.results = {}
        self.logs = []
        self.start_time = None
        self.end_time = None
        
    def log(self, message: str, level: str = "info"):
        """Add a log entry"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "agent": self.name
        }
        self.logs.append(log_entry)
        print(f"[{self.name}] {level.upper()}: {message}")
    
    def update_status(self, status: str, progress: int = None, task: str = None):
        """Update agent status"""
        self.status = status
        if progress is not None:
            self.progress = progress
        if task is not None:
            self.current_task = task
        
        self.log(f"Status updated: {status} ({progress}%) - {task}")
    
    def start_work(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start working on a project"""
        self.start_time = datetime.now()
        self.status = "running"
        self.progress = 0
        self.current_task = f"Starting {self.name}"
        self.results = {}
        
        self.log(f"Starting work on project: {project_data.get('name', 'Unknown')}")
        
        try:
            result = self.execute(project_data)
            self.status = "completed"
            self.progress = 100
            self.end_time = datetime.now()
            self.log("Work completed successfully")
            return result
        except Exception as e:
            self.status = "failed"
            self.log(f"Work failed: {str(e)}", "error")
            raise e
    
    @abstractmethod
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_type": self.agent_type,
            "name": self.name,
            "status": self.status,
            "progress": self.progress,
            "current_task": self.current_task,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "results": self.results,
            "logs": self.logs[-10:]  # Last 10 logs
        }
    
    def simulate_work(self, steps: List[str], duration_per_step: float = 1.0):
        """Simulate work progress for demo purposes"""
        total_steps = len(steps)
        for i, step in enumerate(steps):
            progress = int((i + 1) / total_steps * 100)
            self.update_status("running", progress, step)
            time.sleep(duration_per_step)
    
    def generate_mock_result(self, result_type: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate mock results for demo purposes"""
        base_result = {
            "agent": self.name,
            "type": result_type,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        if data:
            base_result.update(data)
            
        return base_result

