import os
from openai import OpenAI
import json

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    def generate_research_plan(self, query):
        prompt = f"""
        Given the user query '{query}', generate a step-by-step research plan.
        The plan should be a JSON array of steps. Each step should be a dictionary with a 'tool' and 'query' field.
        The available tools are: 'google_search', 'view_text_website'.
        The primary knowledge base to use is CORDIS.
        Example:
        [
            {{"tool": "google_search", "query": "site:cordis.europa.eu xylella fastidiosa research projects spain"}}
        ]
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant. Your task is to generate a research plan based on the user's query."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        plan = json.loads(response.choices[0].message.content)
        return plan.get("steps", [])
    def execute_research_plan(self, plan):
        mock_data = [{"organisation_name": "INSTITUTO VALENCIANO DE INVESTIGACIONES AGRARIAS", "country": "Spain", "project_title": "Understanding and preventing Xylella fastidiosa spread in olive groves", "project_acronym": "XF-ACTORS", "summary": "This project aims to develop new tools and strategies for the prevention, early detection, and control of Xylella fastidiosa.", "contact_person": "Dr. Maria Lopez"}, {"organisation_name": "CONSEJO SUPERIOR DE INVESTIGACIONES CIENTIFICAS", "country": "Spain", "project_title": "Biological control of Xylella fastidiosa vectors", "project_acronym": "BIOVEXO", "summary": "The project focuses on developing and testing biological control agents to reduce the population of the insect vector of Xylella fastidiosa.", "contact_person": "Dr. Carlos Garcia"}]
        print("Executing research plan (mock)...")
        return mock_data
    def run(self, query):
        print(f"Research agent received query: {query}")
        plan = self.generate_research_plan(query)
        print("Generated research plan:")
        print(plan)
        results = self.execute_research_plan(plan)
        return results
