#!/usr/bin/env python3
"""
Phase 3: Smart Task Detection and Auto-delegation
Automatically detects complex tasks and delegates them to Codex
"""

import re
import json
from typing import Dict, List, Tuple
from codex_monitor import CodexMonitor

class SmartTaskDetector:
    def __init__(self):
        self.codex_monitor = CodexMonitor()
        
        # Complex task patterns that should be delegated
        self.complex_patterns = {
            "authentication": {
                "keywords": ["auth", "login", "user", "session", "jwt", "oauth"],
                "phrases": ["user authentication", "login system", "user management"],
                "complexity": "high"
            },
            "dashboard": {
                "keywords": ["dashboard", "analytics", "charts", "graphs", "visualization"],
                "phrases": ["create dashboard", "build dashboard", "analytics dashboard"],
                "complexity": "high"
            },
            "notification": {
                "keywords": ["notification", "alert", "reminder", "email", "sms"],
                "phrases": ["notification system", "alert system", "reminder system"],
                "complexity": "medium"
            },
            "api": {
                "keywords": ["api", "endpoint", "rest", "graphql", "webhook"],
                "phrases": ["api integration", "rest api", "create api"],
                "complexity": "medium"
            },
            "database": {
                "keywords": ["database", "db", "sql", "mongodb", "postgres", "mysql"],
                "phrases": ["database integration", "data model", "database schema"],
                "complexity": "high"
            },
            "full_system": {
                "keywords": ["complete", "full", "entire", "comprehensive", "system"],
                "phrases": ["complete system", "full implementation", "entire application"],
                "complexity": "very_high"
            }
        }
        
        # Action verbs that indicate implementation work
        self.action_verbs = [
            "create", "build", "implement", "develop", "design", 
            "add", "integrate", "setup", "configure", "deploy"
        ]
    
    def analyze_task_complexity(self, task_description: str) -> Dict:
        """Analyze task and determine if it should be delegated to Codex"""
        task_lower = task_description.lower()
        
        # Check for action verbs
        has_action = any(verb in task_lower for verb in self.action_verbs)
        
        # Analyze patterns
        matched_patterns = []
        total_complexity_score = 0
        
        for pattern_name, pattern_info in self.complex_patterns.items():
            keyword_matches = sum(1 for keyword in pattern_info["keywords"] if keyword in task_lower)
            phrase_matches = sum(1 for phrase in pattern_info["phrases"] if phrase in task_lower)
            
            if keyword_matches > 0 or phrase_matches > 0:
                matched_patterns.append({
                    "pattern": pattern_name,
                    "complexity": pattern_info["complexity"],
                    "keyword_matches": keyword_matches,
                    "phrase_matches": phrase_matches
                })
                
                # Add to complexity score
                complexity_scores = {
                    "low": 1,
                    "medium": 2,
                    "high": 3,
                    "very_high": 5
                }
                total_complexity_score += complexity_scores.get(pattern_info["complexity"], 1)
        
        # Check length and detail level
        word_count = len(task_description.split())
        detail_bonus = min(word_count // 10, 3)  # Bonus for detailed descriptions
        
        final_score = total_complexity_score + detail_bonus
        
        # Determine if should delegate
        should_delegate = (
            has_action and 
            final_score >= 2 and 
            len(matched_patterns) > 0
        )
        
        return {
            "should_delegate": should_delegate,
            "complexity_score": final_score,
            "matched_patterns": matched_patterns,
            "has_action_verb": has_action,
            "word_count": word_count,
            "recommendation": self._get_recommendation(final_score, should_delegate)
        }
    
    def _get_recommendation(self, score: int, should_delegate: bool) -> str:
        """Generate human-readable recommendation"""
        if not should_delegate:
            return "Handle directly - Simple task or informational request"
        
        if score >= 8:
            return "🔥 HIGHLY COMPLEX - Delegate to Codex immediately"
        elif score >= 5:
            return "🚀 COMPLEX - Strongly recommend Codex delegation"
        elif score >= 3:
            return "⚡ MODERATE - Consider Codex for efficiency"
        else:
            return "📝 SIMPLE - Can handle directly or delegate for learning"
    
    def auto_delegate_if_complex(self, task_description: str) -> Dict:
        """Automatically delegate task if it's complex enough"""
        analysis = self.analyze_task_complexity(task_description)
        
        if analysis["should_delegate"] and analysis["complexity_score"] >= 5:
            # Auto-delegate high complexity tasks
            result = self.codex_monitor.trigger_background_task(task_description)
            result["auto_delegated"] = True
            result["analysis"] = analysis
            return result
        else:
            return {
                "auto_delegated": False,
                "analysis": analysis,
                "message": f"Task analysis complete. {analysis['recommendation']}"
            }
    
    def suggest_delegation(self, task_description: str) -> str:
        """Generate a suggestion message for delegation"""
        analysis = self.analyze_task_complexity(task_description)
        
        if not analysis["should_delegate"]:
            return "This appears to be a simple task that can be handled directly."
        
        suggestion = f"""
🤖 **Task Complexity Analysis:**

**Recommendation:** {analysis['recommendation']}
**Complexity Score:** {analysis['complexity_score']}/10
**Matched Patterns:** {', '.join([p['pattern'] for p in analysis['matched_patterns']])}

**Suggested Action:**
- ✅ Delegate to Codex for efficient implementation
- ⏰ Estimated time savings: 20-60 minutes
- 🎯 Let Codex handle the heavy lifting while you focus on strategy

Would you like me to start Codex on this task?
"""
        return suggestion.strip()

def main():
    """CLI interface for testing smart detection"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 smart_task_detector.py 'task description'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    detector = SmartTaskDetector()
    
    # Analyze task
    analysis = detector.analyze_task_complexity(task)
    print("🔍 **Smart Task Analysis:**")
    print(f"Task: {task}")
    print(f"Should Delegate: {'✅ YES' if analysis['should_delegate'] else '❌ NO'}")
    print(f"Complexity Score: {analysis['complexity_score']}/10")
    print(f"Recommendation: {analysis['recommendation']}")
    
    if analysis["matched_patterns"]:
        print("\nMatched Patterns:")
        for pattern in analysis["matched_patterns"]:
            print(f"  - {pattern['pattern']}: {pattern['complexity']} complexity")
    
    # Show suggestion
    suggestion = detector.suggest_delegation(task)
    print("\n" + suggestion)
    
    # Auto-delegate if complex enough
    if analysis["complexity_score"] >= 7:
        print(f"\n🚀 **Auto-delegating to Codex...**")
        result = detector.auto_delegate_if_complex(task)
        if result.get("auto_delegated"):
            print("✅ Codex task started automatically!")

if __name__ == "__main__":
    main()