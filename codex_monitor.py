#!/usr/bin/env python3
"""
Codex Background Task Monitor
Checks status of running Codex tasks and provides progress updates
"""

import os
import subprocess
import glob
from datetime import datetime
from pathlib import Path

class CodexMonitor:
    def __init__(self, project_root="/Users/panda/Desktop/Claude Code/eufm XF"):
        self.project_root = Path(project_root)
        self.log_dir = self.project_root / "logs"
        
    def check_status(self):
        """Check if Codex is currently running and return status"""
        status_file = self.log_dir / "codex_status"
        
        if not status_file.exists():
            return {
                "is_running": False,
                "status": "No tasks found",
                "message": "🤖 Codex is idle - ready for new tasks!"
            }
        
        status = status_file.read_text().strip()
        
        if status == "RUNNING":
            return self._get_running_status()
        elif status == "COMPLETED":
            return self._get_completed_status()
        elif status == "INTERRUPTED":
            return self._get_interrupted_status()
        else:
            return {
                "is_running": False,
                "status": "Unknown",
                "message": "🤔 Unknown Codex status"
            }
    
    def _get_running_status(self):
        """Get details about currently running task"""
        try:
            current_task = (self.log_dir / "current_task").read_text().strip()
            start_time = (self.log_dir / "task_start_time").read_text().strip()
            
            # Find latest log file
            latest_log = self._get_latest_log()
            
            return {
                "is_running": True,
                "status": "RUNNING",
                "current_task": current_task,
                "start_time": start_time,
                "log_file": latest_log,
                "message": f"🔄 **Codex is actively working!**\n\n"
                          f"**Task**: {current_task}\n"
                          f"**Started**: {start_time}\n"
                          f"**Log**: {latest_log}\n\n"
                          f"Codex is processing your request in the background..."
            }
        except Exception as e:
            return {
                "is_running": True,
                "status": "RUNNING",
                "message": f"🔄 Codex is running but status details unavailable: {e}"
            }
    
    def _get_completed_status(self):
        """Get details about last completed task"""
        try:
            latest_log = self._get_latest_log()
            return {
                "is_running": False,
                "status": "COMPLETED",
                "log_file": latest_log,
                "message": f"✅ **Latest Codex task completed!**\n\n"
                          f"**Results**: Check {latest_log}\n"
                          f"**Status**: Ready for new tasks\n\n"
                          f"🤖 Codex is now idle and ready for your next request."
            }
        except Exception as e:
            return {
                "is_running": False,
                "status": "COMPLETED",
                "message": f"✅ Task completed but details unavailable: {e}"
            }
    
    def _get_interrupted_status(self):
        """Get details about interrupted task"""
        return {
            "is_running": False,
            "status": "INTERRUPTED",
            "message": "⚠️ **Previous Codex task was interrupted**\n\n"
                      "The last task didn't complete normally. This could be due to:\n"
                      "- Manual cancellation\n"
                      "- System restart\n"
                      "- Unexpected error\n\n"
                      "🤖 Codex is ready for new tasks."
        }
    
    def _get_latest_log(self):
        """Find the most recent Codex log file"""
        log_files = glob.glob(str(self.log_dir / "codex_*.log"))
        if log_files:
            return max(log_files, key=os.path.getctime)
        return "No log files found"
    
    def get_log_tail(self, lines=20):
        """Get the last N lines from the latest log file"""
        latest_log = self._get_latest_log()
        
        if latest_log == "No log files found":
            return "No log files available"
        
        try:
            result = subprocess.run(
                ['tail', f'-{lines}', latest_log], 
                capture_output=True, 
                text=True
            )
            return result.stdout
        except Exception as e:
            return f"Error reading log: {e}"
    
    def trigger_background_task(self, task_description):
        """Start a Codex task in the background"""
        script_path = self.project_root / "scripts" / "codex-helper.sh"
        
        try:
            # Start the background process
            process = subprocess.Popen(
                ['bash', str(script_path), task_description],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            return {
                "success": True,
                "pid": process.pid,
                "message": f"🚀 **Codex task started successfully!**\n\n"
                          f"**Task**: {task_description}\n"
                          f"**PID**: {process.pid}\n"
                          f"**Status**: Background execution in progress\n\n"
                          f"You can:\n"
                          f"- Continue our conversation\n"
                          f"- Ask me to check progress anytime\n"
                          f"- View logs in the logs/ directory\n\n"
                          f"I'll notify you when it's complete! ✅"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Failed to start Codex task: {e}"
            }

def main():
    """CLI interface for monitoring Codex"""
    import sys
    
    monitor = CodexMonitor()
    
    if len(sys.argv) == 1:
        # Just check status
        status = monitor.check_status()
        print(status["message"])
    elif sys.argv[1] == "logs":
        # Show recent log output
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        tail_output = monitor.get_log_tail(lines)
        print(f"📋 **Latest {lines} lines from Codex logs:**\n")
        print(tail_output)
    elif sys.argv[1] == "start":
        # Start a new task
        if len(sys.argv) < 3:
            print("Usage: python3 codex_monitor.py start \"task description\"")
            sys.exit(1)
        task = " ".join(sys.argv[2:])
        result = monitor.trigger_background_task(task)
        print(result["message"])
    else:
        print("Usage:")
        print("  python3 codex_monitor.py              # Check status")
        print("  python3 codex_monitor.py logs [N]     # Show last N log lines")
        print("  python3 codex_monitor.py start \"task\" # Start new background task")

if __name__ == "__main__":
    main()