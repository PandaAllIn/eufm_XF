#!/usr/bin/env python3
"""
Quick Agent Summoner Integration Test
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from mission_control import EnhancedMissionControl

def quick_test():
    print("🧙‍♂️ QUICK AGENT SUMMONER TEST")
    print("=" * 40)
    
    mc = EnhancedMissionControl()
    
    # Test a task that should trigger Agent Summoner (not covered by core agents)
    novel_task = "Build an automated cryptocurrency payment system for international research collaboration"
    
    print(f"📋 Testing novel task: {novel_task}")
    print("-" * 40)
    
    result = mc.intelligent_task_processing(novel_task)
    
    if result.get('status') == 'success':
        approach = result.get('processing_approach')
        print(f"✅ Processing approach: {approach}")
        
        if approach == 'agent_summoner_discovery':
            print("🧙‍♂️ SUCCESS! Agent Summoner was triggered!")
            print(f"⏱️ Processing time: {result.get('total_time', 0):.2f} seconds")
            print(f"💰 Cost: {result.get('cost_analysis', {}).get('total_estimated_cost', 'N/A')}")
        elif approach == 'core_agents':
            print("⚡ Handled by core agents (unexpected for this task)")
    else:
        print(f"❌ Processing failed: {result}")
    
    # Quick status check
    status = mc.generate_status_report()
    print(f"\n📊 Summoning sessions: {status['agent_summoner_stats']['total_summoning_sessions']}")
    print(f"🧙‍♂️ Total discovered agents: {status['agent_summoner_stats']['total_discovered_agents']}")

if __name__ == "__main__":
    quick_test()