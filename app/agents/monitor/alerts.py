"""
Deadline tracking and alerts system for EUFM project
"""
import yaml
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pathlib

class AlertsManager:
    """Manages deadline tracking and alert generation"""
    
    def __init__(self):
        self.project_root = pathlib.Path(__file__).resolve().parents[4]
        
    def load_wbs_data(self) -> Dict[str, Any]:
        """Load WBS data with deadlines"""
        try:
            with open(self.project_root / "wbs" / "wbs.yaml", "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {"wbs": {}}
    
    def get_critical_deadlines(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get deadlines within specified days"""
        wbs_data = self.load_wbs_data()
        critical_items = []
        now = datetime.now()
        cutoff = now + timedelta(days=days_ahead)
        
        for wp_id, items in wbs_data.get("wbs", {}).items():
            for item in items:
                if "due" in item and item["due"]:
                    try:
                        due_date = datetime.fromisoformat(str(item["due"]))
                        days_remaining = (due_date - now).days
                        
                        if due_date <= cutoff:
                            alert_level = self._get_alert_level(days_remaining, item.get("priority"))
                            critical_items.append({
                                "id": item["id"],
                                "title": item["title"],
                                "due_date": item["due"],
                                "days_remaining": days_remaining,
                                "owner": item.get("owner", "unassigned"),
                                "priority": item.get("priority", "normal"),
                                "alert_level": alert_level,
                                "wp": wp_id,
                                "type": item.get("type", "task")
                            })
                    except (ValueError, KeyError):
                        continue
        
        # Sort by days remaining (most urgent first)
        critical_items.sort(key=lambda x: x["days_remaining"])
        return critical_items
    
    def _get_alert_level(self, days_remaining: int, priority: str = None) -> str:
        """Determine alert level based on days remaining and priority"""
        if priority == "CRITICAL":
            if days_remaining <= 1:
                return "EMERGENCY"
            elif days_remaining <= 3:
                return "CRITICAL"
            else:
                return "WARNING"
        else:
            if days_remaining <= 0:
                return "OVERDUE"
            elif days_remaining <= 2:
                return "CRITICAL"
            elif days_remaining <= 5:
                return "WARNING"
            else:
                return "INFO"
    
    def get_overdue_items(self) -> List[Dict[str, Any]]:
        """Get items that are past due"""
        wbs_data = self.load_wbs_data()
        overdue_items = []
        now = datetime.now()
        
        for wp_id, items in wbs_data.get("wbs", {}).items():
            for item in items:
                if "due" in item and item["due"]:
                    try:
                        due_date = datetime.fromisoformat(str(item["due"]))
                        if due_date < now:
                            days_overdue = (now - due_date).days
                            overdue_items.append({
                                "id": item["id"],
                                "title": item["title"],
                                "due_date": item["due"],
                                "days_overdue": days_overdue,
                                "owner": item.get("owner", "unassigned"),
                                "priority": item.get("priority", "normal"),
                                "wp": wp_id,
                                "type": item.get("type", "task")
                            })
                    except (ValueError, KeyError):
                        continue
        
        # Sort by days overdue (most overdue first)
        overdue_items.sort(key=lambda x: x["days_overdue"], reverse=True)
        return overdue_items
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily status report"""
        critical_deadlines = self.get_critical_deadlines(7)
        overdue_items = self.get_overdue_items()
        
        # Special focus on September 4th deadline
        sept_4_items = [item for item in critical_deadlines 
                       if item["due_date"] == "2025-09-04"]
        
        report = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "critical_deadlines": critical_deadlines,
            "overdue_items": overdue_items,
            "september_4_deadline": sept_4_items,
            "summary": {
                "total_critical": len(critical_deadlines),
                "total_overdue": len(overdue_items),
                "emergency_level": len([i for i in critical_deadlines if i["alert_level"] == "EMERGENCY"]),
                "september_4_status": len(sept_4_items) > 0
            }
        }
        
        return report
    
    def get_alert_colors(self) -> Dict[str, str]:
        """Get Bootstrap color classes for alert levels"""
        return {
            "EMERGENCY": "danger",
            "CRITICAL": "warning", 
            "WARNING": "info",
            "INFO": "light",
            "OVERDUE": "dark"
        }

def generate_alerts_summary() -> str:
    """Generate a text summary for notifications"""
    manager = AlertsManager()
    report = manager.generate_daily_report()
    
    lines = [
        f"🔔 EUFM Daily Alert Summary - {report['date']}",
        f"",
        f"📅 CRITICAL: Stage 1 Proposal Due September 4, 2025",
        f"   Status: {'⚠️ URGENT ACTION REQUIRED' if report['summary']['september_4_status'] else '✅ On Track'}",
        f"",
        f"📊 Overview:",
        f"   • Critical deadlines (next 7 days): {report['summary']['total_critical']}",
        f"   • Overdue items: {report['summary']['total_overdue']}",
        f"   • Emergency level alerts: {report['summary']['emergency_level']}",
    ]
    
    if report['september_4_deadline']:
        lines.extend([
            f"",
            f"🚨 SEPTEMBER 4TH DEADLINE ITEMS:",
        ])
        for item in report['september_4_deadline']:
            lines.append(f"   • {item['title']} ({item['days_remaining']} days remaining)")
    
    if report['critical_deadlines']:
        lines.extend([
            f"",
            f"⏰ Upcoming Critical Deadlines:",
        ])
        for item in report['critical_deadlines'][:5]:  # Show top 5
            lines.append(f"   • {item['title']} - Due: {item['due_date']} ({item['days_remaining']} days)")
    
    return "\n".join(lines)