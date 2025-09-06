#!/usr/bin/env python3
"""
Test Agent Summoner with truly novel task outside core capabilities
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from mission_control import EnhancedMissionControl

def test_pure_novel_task():
    print("🧙‍♂️ TESTING PURE NOVEL TASK FOR AGENT SUMMONER")
    print("=" * 50)
    
    mc = EnhancedMissionControl()
    
    # Task that has NO keywords matching our core agents
    pure_novel_task = "I need specialized quantum computing optimization algorithms for molecular simulation workflows"
    
    print(f"📋 Pure novel task: {pure_novel_task}")
    print("-" * 50)
    
    # Show what core agents would be matched (should be none)
    matched = mc._match_core_agents(pure_novel_task)
    print(f"🔍 Matched core agents: {matched}")
    
    if not matched:
        print("✅ Perfect! No core agents matched - this should trigger Agent Summoner")
        print("🧙‍♂️ Starting Agent Summoner process...")
        
        # This will take ~70 seconds but will demonstrate the full pipeline
        result = mc.intelligent_task_processing(pure_novel_task)
        
        if result.get('status') == 'success':
            approach = result.get('processing_approach')
            print(f"🎯 Processing approach: {approach}")
            
            if approach == 'agent_summoner_discovery':
                print("🎉 SUCCESS! Agent Summoner was activated!")
                print(f"⏱️ Total time: {result.get('total_time', 0):.2f} seconds")
                print(f"💰 Cost: {result.get('cost_analysis', {}).get('total_estimated_cost', 'N/A')}")
                
                # Show discovered agents
                summoning_result = result.get('summoning_result', {})
                if summoning_result:
                    agent_eval = summoning_result.get('agent_evaluation', {})
                    integration_result = result.get('execution_result', {})
                    if hasattr(integration_result, 'get'):
                        discovered_agents = integration_result.get('assigned_discovered_agents', [])
                        print(f"🤖 Discovered agents: {len(discovered_agents)}")
        else:
            print(f"❌ Failed: {result}")
    else:
        print(f"⚠️ Task matched core agents: {matched} - trying different task")

if __name__ == "__main__":
    test_pure_novel_task()