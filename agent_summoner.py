#!/usr/bin/env python3
"""
Agent Summoner - Intelligent Agent Discovery & Orchestration System
Uses real-time research to discover, evaluate, and create optimal agents for any task
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

from agents.perplexity_sonar_agent import PerplexitySonarAgent

class AgentSummoner:
    def __init__(self, project_root="/Users/panda/Desktop/Claude Code/eufm XF"):
        self.project_root = Path(project_root)
        self.summoner_data = self.project_root / "research_data" / "agent_summoner"
        self.summoner_data.mkdir(parents=True, exist_ok=True)
        
        # Initialize research capabilities
        self.researcher = PerplexitySonarAgent()
        self.researcher.configure_apis(sonar_key='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')
        
        # Agent discovery database
        self.discovered_agents = {}
        self.agent_performance = {}
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup Agent Summoner logging"""
        log_file = self.project_root / "logs" / f"agent_summoner_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - AGENT_SUMMONER - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧙‍♂️ Agent Summoner initialized")
        
    def analyze_task(self, user_request: str) -> Dict:
        """Analyze task requirements and complexity"""
        self.logger.info(f"📋 Analyzing task: {user_request[:100]}...")
        
        analysis_query = f'''
        Analyze this task request and provide structured information:
        
        TASK: "{user_request}"
        
        Please provide:
        1. DOMAIN: What field/industry does this belong to?
        2. TASK_TYPE: What category of work is this? (research, analysis, development, monitoring, etc.)
        3. COMPLEXITY: Rate complexity 1-10 and explain why
        4. REQUIRED_CAPABILITIES: What specific capabilities are needed?
        5. ESTIMATED_RESOURCES: Time, computational, and expertise requirements
        6. CONSTRAINTS: Any specific limitations or requirements
        7. SUCCESS_CRITERIA: How to measure successful completion
        
        Format as structured analysis with clear categories.
        '''
        
        result = self.researcher.perplexity_research(analysis_query, model='sonar-reasoning')
        
        if result['status'] == 'success':
            analysis_content = result['response']['choices'][0]['message']['content']
            
            # Parse the analysis (simplified parsing for prototype)
            task_analysis = {
                'original_request': user_request,
                'analysis_content': analysis_content,
                'domain': self._extract_field(analysis_content, 'DOMAIN'),
                'task_type': self._extract_field(analysis_content, 'TASK_TYPE'),
                'complexity': self._extract_field(analysis_content, 'COMPLEXITY'),
                'capabilities': self._extract_field(analysis_content, 'REQUIRED_CAPABILITIES'),
                'resources': self._extract_field(analysis_content, 'ESTIMATED_RESOURCES'),
                'constraints': self._extract_field(analysis_content, 'CONSTRAINTS'),
                'success_criteria': self._extract_field(analysis_content, 'SUCCESS_CRITERIA'),
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("✅ Task analysis completed")
            return task_analysis
        else:
            self.logger.error("❌ Task analysis failed")
            return {'error': 'Task analysis failed'}
            
    def _extract_field(self, content: str, field_name: str) -> str:
        """Simple field extraction from analysis content"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if field_name in line.upper():
                # Try to get the content after the field name
                if ':' in line:
                    return line.split(':', 1)[1].strip()
                elif i + 1 < len(lines):
                    return lines[i + 1].strip()
        return "Not specified"
        
    def discover_agents(self, task_analysis: Dict) -> Dict:
        """Research and discover optimal agents for the task"""
        self.logger.info("🔍 Researching optimal agents for task...")
        
        discovery_query = f'''
        I need to find the best AI agents, APIs, platforms, and tools for this task:
        
        DOMAIN: {task_analysis.get('domain', 'General')}
        TASK TYPE: {task_analysis.get('task_type', 'Unknown')}
        COMPLEXITY: {task_analysis.get('complexity', 'Unknown')}
        REQUIREMENTS: {task_analysis.get('capabilities', 'Not specified')}
        
        ORIGINAL REQUEST: "{task_analysis.get('original_request', '')}"
        
        Please research and provide:
        
        1. EXISTING AI AGENTS: Specific named agents/platforms that can handle this task
        2. API SERVICES: Commercial APIs and services available
        3. OPEN SOURCE TOOLS: Free alternatives and frameworks
        4. INTEGRATION METHODS: How to implement/integrate these solutions
        5. COST ESTIMATES: Pricing models and cost considerations
        6. PERFORMANCE BENCHMARKS: Speed, accuracy, reliability data if available
        7. RECOMMENDATIONS: Top 3 recommended approaches with pros/cons
        
        Focus on 2024 current solutions with specific names, URLs, and implementation details.
        '''
        
        result = self.researcher.perplexity_research(discovery_query, model='sonar-reasoning')
        
        if result['status'] == 'success':
            discovery_content = result['response']['choices'][0]['message']['content']
            
            agent_discovery = {
                'task_analysis': task_analysis,
                'discovery_content': discovery_content,
                'discovered_at': datetime.now().isoformat(),
                'research_cost': 0.009,  # Approximate cost
                'recommendations': self._parse_recommendations(discovery_content)
            }
            
            # Save discovery results
            discovery_file = self.summoner_data / f"agent_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(discovery_file, 'w') as f:
                json.dump(agent_discovery, f, indent=2)
                
            self.logger.info(f"✅ Agent discovery completed - saved to {discovery_file}")
            return agent_discovery
        else:
            self.logger.error("❌ Agent discovery failed")
            return {'error': 'Agent discovery failed'}
            
    def _parse_recommendations(self, content: str) -> List[Dict]:
        """Parse recommendations from discovery content"""
        # Simplified parsing for prototype
        recommendations = []
        
        if "RECOMMENDATIONS" in content.upper():
            lines = content.split('\n')
            in_recommendations = False
            current_rec = ""
            
            for line in lines:
                if "RECOMMENDATIONS" in line.upper():
                    in_recommendations = True
                    continue
                    
                if in_recommendations:
                    if line.strip().startswith(('1.', '2.', '3.', '-', '*')):
                        if current_rec:
                            recommendations.append({
                                'description': current_rec.strip(),
                                'confidence': 'medium'
                            })
                        current_rec = line
                    else:
                        current_rec += " " + line
                        
            # Add the last recommendation
            if current_rec:
                recommendations.append({
                    'description': current_rec.strip(),
                    'confidence': 'medium'
                })
                
        return recommendations[:3]  # Top 3 recommendations
        
    def evaluate_agents(self, agent_discovery: Dict) -> Dict:
        """Evaluate discovered agents and recommend optimal configuration"""
        self.logger.info("⚖️ Evaluating agents and optimizing selection...")
        
        evaluation_query = f'''
        Based on this agent discovery research, provide a strategic evaluation:
        
        DISCOVERED AGENTS:
        {agent_discovery.get('discovery_content', '')[:2000]}
        
        TASK REQUIREMENTS:
        - Domain: {agent_discovery['task_analysis'].get('domain')}
        - Complexity: {agent_discovery['task_analysis'].get('complexity')}
        - Resources: {agent_discovery['task_analysis'].get('resources')}
        
        Please provide:
        
        1. OPTIMAL CONFIGURATION: Best single solution or combination of agents
        2. IMPLEMENTATION PLAN: Step-by-step setup and integration approach
        3. COST-BENEFIT ANALYSIS: Expected costs vs. value delivered
        4. RISK ASSESSMENT: Potential challenges and mitigation strategies
        5. SUCCESS METRICS: How to measure and monitor performance
        6. ALTERNATIVE OPTIONS: Backup approaches if primary fails
        
        Focus on practical, implementable recommendations for immediate deployment.
        '''
        
        result = self.researcher.perplexity_research(evaluation_query, model='sonar-reasoning')
        
        if result['status'] == 'success':
            evaluation_content = result['response']['choices'][0]['message']['content']
            
            agent_evaluation = {
                'agent_discovery': agent_discovery,
                'evaluation_content': evaluation_content,
                'evaluated_at': datetime.now().isoformat(),
                'total_research_cost': 0.018,  # Discovery + evaluation
                'recommended_action': self._extract_recommended_action(evaluation_content)
            }
            
            # Save evaluation results
            evaluation_file = self.summoner_data / f"agent_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(evaluation_file, 'w') as f:
                json.dump(agent_evaluation, f, indent=2)
                
            self.logger.info(f"✅ Agent evaluation completed - saved to {evaluation_file}")
            return agent_evaluation
        else:
            self.logger.error("❌ Agent evaluation failed")
            return {'error': 'Agent evaluation failed'}
            
    def _extract_recommended_action(self, content: str) -> str:
        """Extract the main recommended action from evaluation"""
        if "OPTIMAL CONFIGURATION" in content.upper():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "OPTIMAL CONFIGURATION" in line.upper():
                    # Get next few lines
                    next_lines = lines[i+1:i+5]
                    return " ".join([l.strip() for l in next_lines if l.strip()])
        return "Review full evaluation for recommendations"
        
    def summon_agent(self, user_request: str) -> Dict:
        """Complete agent summoning process: analyze → discover → evaluate → recommend"""
        self.logger.info(f"🧙‍♂️ SUMMONING OPTIMAL AGENT FOR: {user_request}")
        
        start_time = time.time()
        
        # Step 1: Analyze the task
        self.logger.info("📋 STEP 1: Analyzing task requirements...")
        task_analysis = self.analyze_task(user_request)
        
        if 'error' in task_analysis:
            return task_analysis
            
        # Step 2: Discover available agents
        self.logger.info("🔍 STEP 2: Discovering optimal agents...")
        agent_discovery = self.discover_agents(task_analysis)
        
        if 'error' in agent_discovery:
            return agent_discovery
            
        # Step 3: Evaluate and recommend
        self.logger.info("⚖️ STEP 3: Evaluating and optimizing selection...")
        agent_evaluation = self.evaluate_agents(agent_discovery)
        
        if 'error' in agent_evaluation:
            return agent_evaluation
            
        # Generate final summoning result
        total_time = time.time() - start_time
        
        summoning_result = {
            'user_request': user_request,
            'task_analysis': task_analysis,
            'agent_discovery': agent_discovery,
            'agent_evaluation': agent_evaluation,
            'summoning_stats': {
                'total_time_seconds': round(total_time, 2),
                'research_queries': 3,
                'total_cost': 0.027,  # ~$0.03 for complete agent summoning
                'cost_per_query': 0.009
            },
            'summoned_at': datetime.now().isoformat()
        }
        
        # Save complete summoning result
        summoning_file = self.summoner_data / f"agent_summoning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summoning_file, 'w') as f:
            json.dump(summoning_result, f, indent=2)
            
        self.logger.info(f"🎉 AGENT SUMMONING COMPLETED!")
        self.logger.info(f"⏱️ Total time: {total_time:.2f} seconds")
        self.logger.info(f"💰 Total cost: $0.027")
        self.logger.info(f"📁 Results saved to: {summoning_file}")
        
        return summoning_result
        
    def get_summoning_summary(self, summoning_result: Dict) -> str:
        """Generate human-readable summary of summoning results"""
        if 'error' in summoning_result:
            return f"❌ Summoning failed: {summoning_result['error']}"
            
        analysis = summoning_result['task_analysis']
        evaluation = summoning_result['agent_evaluation']
        stats = summoning_result['summoning_stats']
        
        summary = f"""
🧙‍♂️ AGENT SUMMONING COMPLETE!

📋 TASK ANALYZED:
• Domain: {analysis.get('domain', 'Unknown')}
• Complexity: {analysis.get('complexity', 'Unknown')}
• Type: {analysis.get('task_type', 'Unknown')}

🔍 AGENTS DISCOVERED & EVALUATED:
• Research completed in {stats['total_time_seconds']} seconds
• Cost: ${stats['total_cost']} for comprehensive analysis
• {stats['research_queries']} research queries executed

💡 RECOMMENDED ACTION:
{evaluation.get('recommended_action', 'Review detailed evaluation')}

📊 NEXT STEPS:
1. Review detailed analysis in saved files
2. Implement recommended agent configuration
3. Monitor performance and optimize as needed

💰 COST EFFICIENCY:
${stats['total_cost']} for professional-grade agent research & recommendation
(Equivalent to $500+/hour consultant analysis)
"""
        return summary

def main():
    """Demo the Agent Summoner capabilities"""
    summoner = AgentSummoner()
    
    # Example summoning scenarios
    demo_tasks = [
        "I need to monitor competitor patent filings in agricultural biotechnology",
        "Create a system to track EU regulatory changes for plant protection products",
        "Build an agent that can analyze scientific papers for Xylella fastidiosa research trends"
    ]
    
    print("🧙‍♂️ AGENT SUMMONER DEMO")
    print("=" * 60)
    
    for i, task in enumerate(demo_tasks, 1):
        print(f"\n📋 DEMO {i}: {task}")
        print("-" * 40)
        
        result = summoner.summon_agent(task)
        summary = summoner.get_summoning_summary(result)
        print(summary)
        
        print("-" * 40)
        time.sleep(2)  # Rate limiting between demos

if __name__ == "__main__":
    main()