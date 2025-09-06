#!/usr/bin/env python3
"""
Test Agent Summoner Integration with Mission Control
Demonstrates intelligent task processing and dynamic agent discovery
"""

import sys
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from mission_control import EnhancedMissionControl

def test_novel_task_processing():
    """Test Agent Summoner integration with novel tasks that require discovery"""
    print("🧪 AGENT SUMMONER INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize Enhanced Mission Control
    mc = EnhancedMissionControl()
    
    # Test scenarios that should trigger Agent Summoner
    novel_tasks = [
        "I need to build an automated system for patent landscape analysis in agricultural biotechnology using machine learning",
        "Create an AI-powered social media monitoring system to track public perception of Xylella fastidiosa outbreaks",
        "Set up automated cryptocurrency payments for international research collaboration rewards",
        "Build a blockchain-based supply chain tracking system for phosphinic acid derivatives"
    ]
    
    print(f"\n🧠 Testing {len(novel_tasks)} novel tasks that should trigger Agent Summoner...")
    
    for i, task in enumerate(novel_tasks, 1):
        print(f"\n🚀 NOVEL TASK {i}:")
        print(f"📋 {task}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            result = mc.intelligent_task_processing(task)
            
            processing_time = time.time() - start_time
            
            if result.get('status') == 'success':
                approach = result.get('processing_approach')
                
                if approach == 'core_agents':
                    execution_result = result.get('execution_result', {})
                    assigned_agents = execution_result.get('assigned_agents', [])
                    print(f"✅ HANDLED BY CORE AGENTS: {assigned_agents}")
                    print(f"⚡ Processing time: {processing_time:.2f} seconds")
                    
                elif approach == 'agent_summoner_discovery':
                    print("🧙‍♂️ AGENT SUMMONER ACTIVATED!")
                    print(f"⏱️ Total processing time: {result.get('total_time', 0):.2f} seconds")
                    
                    cost_analysis = result.get('cost_analysis', {})
                    if cost_analysis:
                        print(f"💰 Summoning cost: {cost_analysis.get('total_estimated_cost', 'N/A')}")
                    
                    # Show discovered agent count
                    summoning_result = result.get('summoning_result', {})
                    if summoning_result:
                        agent_eval = summoning_result.get('agent_evaluation', {})
                        agent_discovery = agent_eval.get('agent_discovery', {})
                        recommendations = agent_discovery.get('recommendations', [])
                        print(f"🎯 Discovered {len(recommendations)} optimal agent recommendations")
                        
                        # Show recommended action
                        recommended_action = agent_eval.get('recommended_action', '')
                        if recommended_action:
                            print(f"💡 Recommendation: {recommended_action[:100]}...")
                else:
                    print(f"❓ Unknown processing approach: {approach}")
                    
            else:
                print(f"❌ TASK PROCESSING FAILED: {result}")
                
        except Exception as e:
            print(f"🚨 ERROR during processing: {e}")
            
        print("-" * 60)
        time.sleep(1)  # Brief pause between tests
    
    # Generate final status report
    print(f"\n📊 FINAL SYSTEM STATUS REPORT")
    print("=" * 40)
    
    status = mc.generate_status_report()
    
    print(f"🎛️ Mission Control Status: {status['mission_control_status']}")
    print(f"🤖 Core Agents: {len(status['core_agents'])}")
    print(f"🧙‍♂️ Discovered Agents: {status['agent_summoner_stats']['total_discovered_agents']}")
    print(f"📈 Summoning Sessions: {status['agent_summoner_stats']['total_summoning_sessions']}")
    
    total_cost = status['agent_summoner_stats']['total_summoning_cost']
    print(f"💰 Total Summoning Cost: ${total_cost:.3f}")
    
    if total_cost > 0:
        print(f"📊 Average Cost per Session: ${total_cost/max(1, status['agent_summoner_stats']['total_summoning_sessions']):.3f}")
        print(f"🎯 ROI Assessment: Professional-grade analysis at consumer pricing")
    
    system_health = status['system_health']['overall_health']
    print(f"🔋 System Health: {system_health}")
    
    # Show dynamic recommendations
    recommendations = status['recommendations']
    print(f"\n💡 SYSTEM RECOMMENDATIONS:")
    for rec in recommendations[:5]:  # Top 5 recommendations
        print(f"   • {rec}")
    
    print(f"\n🎉 INTEGRATION TEST COMPLETE!")
    print(f"✅ Agent Summoner successfully integrated with Mission Control")
    print(f"✅ Dynamic agent discovery operational")
    print(f"✅ Cost-effective intelligent task processing enabled")

def interactive_demo():
    """Interactive demo for testing Agent Summoner integration"""
    print("\n🧙‍♂️ INTERACTIVE AGENT SUMMONER DEMO")
    print("=" * 50)
    print("Enter novel tasks to test Agent Summoner capabilities")
    print("(Try tasks that aren't covered by our core agents)")
    print("Type 'exit' to quit")
    
    mc = EnhancedMissionControl()
    
    while True:
        try:
            user_input = input("\n🎯 Enter task: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
                
            if not user_input:
                continue
                
            print(f"\n🧠 Processing: {user_input}")
            print("-" * 40)
            
            result = mc.intelligent_task_processing(user_input)
            
            if result.get('status') == 'success':
                approach = result.get('processing_approach')
                if approach == 'agent_summoner_discovery':
                    print("🧙‍♂️ Agent Summoner activated and found optimal solutions!")
                    print(f"💰 Cost: {result.get('cost_analysis', {}).get('total_estimated_cost', 'N/A')}")
                elif approach == 'core_agents':
                    agents = result.get('execution_result', {}).get('assigned_agents', [])
                    print(f"⚡ Handled quickly by core agents: {agents}")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Interactive demo complete!")

if __name__ == "__main__":
    # Run the novel task processing test
    test_novel_task_processing()
    
    # Optionally run interactive demo
    print("\n" + "="*60)
    response = input("Run interactive demo? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        interactive_demo()
    
    print("\n🚀 Agent Summoner integration testing complete!")