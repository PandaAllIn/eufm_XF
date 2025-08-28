import os
from openai import OpenAI
import json

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    def generate_research_plan(self, query):
        prompt = f"""
        You are a research assistant tasked with finding potential collaborators for a Horizon Europe project on Xylella fastidiosa.
        Your goal is to generate a step-by-step research plan to find people and institutions based on a user's query.

        **User Query:** "{query}"

        **Instructions:**
        1. Create a research plan as a JSON object containing a "steps" key, which holds an array of step objects.
        2. Each step must be a dictionary with a "tool" and a "query" field.
        3. The only available tools are: `google_search` and `view_text_website`.
        4. Your primary search target should be the CORDIS website (cordis.europa.eu), as it is the main repository for EU-funded research projects.
        5. Construct a `google_search` query that is likely to find relevant projects or researchers on CORDIS. Use the `site:cordis.europa.eu` operator. Combine this with keywords from the user's query.

        **Example Output:**
        {{
          "steps": [
            {{
              "tool": "google_search",
              "query": "site:cordis.europa.eu xylella fastidiosa University of Malaga"
            }}
          ]
        }}

        Generate the JSON research plan for the user query above.
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant generating a JSON research plan."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        plan = json.loads(response.choices[0].message.content)
        return plan.get("steps", [])
    def synthesize_results(self, query, collected_data):
        """
        Synthesizes collected raw data into a structured format using an LLM.
        """
        print("Synthesizing collected data...")

        prompt = f"""
        Given the following raw data collected from web searches based on the query "{query}",
        extract the details for potential collaborators.
        The output should be a JSON object with a "partners" key, containing a list of dictionaries.
        Each dictionary should represent a potential partner and have the following keys:
        "organisation_name", "country", "project_title", "project_acronym", "summary", "contact_person".
        If a value is not found, use "N/A".

        **Collected Data:**
        ---
        {collected_data}
        ---

        Generate the structured JSON output.
        """

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Your task is to process raw text and extract structured information about research partners."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        structured_data = json.loads(response.choices[0].message.content)
        return structured_data.get("partners", [])

    def run(self, query):
        """
        This is a placeholder for the full orchestration.
        In a real run, an orchestrator would:
        1. Call generate_research_plan(query)
        2. Execute the plan using external tools.
        3. Call synthesize_results(query, collected_data)
        For this implementation, we will simulate this by returning the mock data
        so the rest of the application can function.
        """
        print(f"Research agent received query: {query}")
        print("Executing research plan (mock)...")
        # The mock data is what we expect synthesize_results to produce.
        mock_data = [{"organisation_name": "INSTITUTO VALENCIANO DE INVESTIGACIONES AGRARIAS", "country": "Spain", "project_title": "Understanding and preventing Xylella fastidiosa spread in olive groves", "project_acronym": "XF-ACTORS", "summary": "This project aims to develop new tools and strategies for the prevention, early detection, and control of Xylella fastidiosa.", "contact_person": "Dr. Maria Lopez"}, {"organisation_name": "CONSEJO SUPERIOR DE INVESTIGACIONES CIENTIFICAS", "country": "Spain", "project_title": "Biological control of Xylella fastidiosa vectors", "project_acronym": "BIOVEXO", "summary": "The project focuses on developing and testing biological control agents to reduce the population of the insect vector of Xylella fastidiosa.", "contact_person": "Dr. Carlos Garcia"}]
        return mock_data
