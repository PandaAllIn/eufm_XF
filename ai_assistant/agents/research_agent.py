import json
import openai

# This script defines the Research Agent.
# For development, it includes mock functions for the tools.
# In a real execution, the main controller would replace these mocks
# with the actual tool functions provided by the environment.

def google_search_mock(query: str) -> str:
    """A mock function for the google_search tool."""
    print(f"--- MOCK TOOL: Simulating Google search for: '{query}' ---")
    if "site:cordis.europa.eu" in query:
        return """[
            {"title": "CORDIS | XF-ACTORS Project", "url": "https://cordis.europa.eu/project/id/727987", "snippet": "Xylella Fastidiosa Active Containment Through a multidisciplinary-Oriented Research Strategy..."},
            {"title": "CORDIS | POnTE Project", "url": "https://cordis.europa.eu/project/id/635646", "snippet": "Pest Organisms Threatening Europe..."}
        ]"""
    if "university of valencia" in query.lower():
        return """[
            {"title": "University of Valencia - Plant Pathology", "url": "https://www.uv.es/plant-pathology", "snippet": "Research on Xylella fastidiosa and other plant pathogens..."}
        ]"""
    return "[]"

def view_text_website_mock(url: str) -> str:
    """A mock function for the view_text_website tool."""
    print(f"--- MOCK TOOL: Simulating viewing website: '{url}' ---")
    if "cordis.europa.eu" in url:
        return "The XF-ACTORS project, funded by Horizon 2020, brought together 29 partners, including the University of Bari and the National Research Council (CNR) of Italy, to research Xylella fastidiosa."
    if "uv.es" in url:
        return "The Plant Pathology department at the University of Valencia has several researchers, including Dr. Elena Garcia, working on Xylella fastidiosa."
    return "This is dummy content for the website."


class ResearchAgent:
    """
    The Research Agent is responsible for conducting online research.
    """

    KNOWLEDGE_BASE = {
        "partner_search_portals": [
            {"name": "CORDIS", "url": "https://cordis.europa.eu/", "description": "Primary database for EU-funded research projects. Excellent for finding partners from previous, related projects."},
            {"name": "Funding & Tenders Portal", "url": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/", "description": "Official EU portal for finding partners for specific funding calls."},
            {"name": "Enterprise Europe Network (EEN)", "url": "https://een.ec.europa.eu/", "description": "Network to find innovative SME partners."}
        ],
        "search_strategies": [
            "Identify consortia of past, successful Horizon 2020 or Horizon Europe projects on the same topic.",
            "Search for scientific publications from researchers in relevant countries.",
            "Look for agricultural cooperatives and industry associations in affected regions."
        ]
    }

    def __init__(self, settings, tools=None):
        self.settings = settings
        self.tools = tools or {
            "google_search": google_search_mock,
            "view_text_website": view_text_website_mock,
        }
        self.openai_client = None
        if self.settings.get("openai_api_key") and self.settings["openai_api_key"] != "YOUR_API_KEY_HERE":
            self.openai_client = openai.OpenAI(api_key=self.settings["openai_api_key"])
        print("Research Agent initialized with enhanced knowledge.")

    def _generate_research_plan(self, research_task: str) -> list[dict]:
        """Generates a structured research plan with search queries."""
        print("Agent is generating a detailed research plan with an LLM...")

        if not self.openai_client:
            print("WARNING: OpenAI client not initialized. Using mock research plan.")
            return [
                {"step": 1, "description": "Find past projects on CORDIS", "query": "site:cordis.europa.eu Xylella fastidiosa project"},
                {"step": 2, "description": "Find experts at University of Valencia", "query": "University of Valencia plant pathology Xylella"},
            ]

        prompt = f"""
        You are an expert research strategist for Horizon Europe proposals. Your goal is to find potential collaborators for a project about a cure for the Xylella fastidiosa bacterium.

        Your knowledge base includes these key strategies and portals:
        - Strategies: {json.dumps(self.KNOWLEDGE_BASE['search_strategies'])}
        - Key Portals: {json.dumps(self.KNOWLEDGE_BASE['partner_search_portals'])}

        Based on the following high-level research task, create a step-by-step research plan. Each step should be a specific action that involves a targeted Google search query.

        The task is: "{research_task}"

        Return your answer as a JSON-formatted list of objects. Each object should have 'step', 'description', and 'query'. For example:
        [
            {{"step": 1, "description": "Identify past EU-funded projects on the topic using CORDIS.", "query": "site:cordis.europa.eu Xylella fastidiosa"}},
            {{"step": 2, "description": "Find top-cited academic papers on the topic.", "query": "Xylella fastidiosa review paper collaborators"}}
        ]
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.settings.get("llm_model", "gpt-4o"),
                messages=[
                    {"role": "system", "content": "You are an expert research strategist that returns a JSON-formatted research plan."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            # The LLM might return a dict with a key, so we handle that.
            data = json.loads(response.choices[0].message.content)
            return data.get("plan", [])
        except Exception as e:
            print(f"An error occurred while calling OpenAI API: {e}")
            return []

    def _google_search(self, query: str) -> str:
        """Performs a Google search using the provided tool."""
        print(f"Agent is performing a search for: '{query}'")
        return self.tools["google_search"](query)

    def _view_text_website(self, url: str) -> str:
        """Views a website using the provided tool."""
        print(f"Agent is viewing URL: '{url}'")
        return self.tools["view_text_website"](url)

    def _extract_collaborator_info(self, url: str, content: str, research_task: str) -> dict:
        """Extracts collaborator information from website content."""
        print("Agent is extracting collaborator info with an LLM...")

        if not self.openai_client:
            print("WARNING: OpenAI client not initialized. Using mock extraction.")
            if "uv.es" in url or "cordis.europa.eu" in url:
                return { "collaborators": [{ "name": "Dr. Elena Garcia (from mock)", "role": "Lead Researcher", "affiliation": "University of Valencia", "email": "elena.garcia@uv.es", "summary_of_relevance": "Expert on Xylella fastidiosa epidemiology." }] }
            return {"collaborators": []}

        prompt = f"""
        You are a data extraction expert. Your task is to identify potential collaborators for a research project from the text of a webpage.
        The research project's goal is: "{research_task}"
        The webpage URL is: {url}
        The webpage content is:
        ---
        {content[:4000]}
        ---

        Please extract a list of potential collaborators. For each collaborator, provide their name, role/title, affiliation, email address (if available), and a brief summary of why they are relevant to the research task.

        Return your answer as a JSON object with a single key "collaborators", which is a list of objects. For example:
        {{
          "collaborators": [
            {{
              "name": "Dr. John Doe",
              "role": "Professor of Plant Science",
              "affiliation": "University of Example",
              "email": "john.doe@example.edu",
              "summary_of_relevance": "Published several papers on bacterial biofilms in plants."
            }}
          ]
        }}
        If no specific collaborators are found, return an empty list:
        {{ "collaborators": [] }}
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.settings.get("llm_model", "gpt-4o"),
                messages=[
                    {"role": "system", "content": "You are a data extraction expert that returns JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"An error occurred while calling OpenAI API for extraction: {e}")
            return {"collaborators": []}

    def _select_promising_urls(self, search_results: list[dict], research_task: str) -> list[str]:
        """Selects the most promising URLs from a list of search results."""
        print("Agent is selecting promising URLs with an LLM...")

        if not self.openai_client:
            print("WARNING: OpenAI client not initialized. Mocking URL selection.")
            return [result['url'] for result in search_results if result.get('url')][:2] # Limit to 2 for testing

        prompt = f"""
        You are a research analyst. Your goal is to find potential collaborators for a Horizon Europe project about a cure for the Xylella fastidiosa plant bacterium.
        The main research task is: "{research_task}"

        You have the following Google search results:
        ---
        {json.dumps(search_results, indent=2)}
        ---

        Based on the titles and snippets, please select the top 2-3 most promising and relevant URLs to investigate further.
        Return your answer as a JSON-formatted list of strings. For example:
        ["https://example.com/best-url", "https://example.com/another-good-one"]
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.settings.get("llm_model", "gpt-4o"),
                messages=[
                    {"role": "system", "content": "You are a research analyst that selects relevant URLs from search results and returns JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            # The LLM might return a dict with a key, so we need to handle that.
            data = json.loads(response.choices[0].message.content)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and 'urls' in data and isinstance(data['urls'], list):
                return data['urls']
            return [] # Fallback
        except Exception as e:
            print(f"An error occurred while calling OpenAI API for URL selection: {e}")
            return []

    def run(self, research_task: str) -> list[dict]:
        """
        Runs the research task and returns a list of potential collaborators.
        """
        print(f"\n--- Starting Research Agent Task ---")
        print(f"Task: {research_task}")

        # Step 1: Generate a research plan
        research_plan = self._generate_research_plan(research_task)
        if not research_plan:
            print("Could not generate a research plan. Aborting task.")
            return []
        print(f"Agent generated a {len(research_plan)}-step research plan.")

        potential_collaborators = []
        # Step 2: Execute the research plan
        for step in research_plan:
            print(f"\nExecuting Step {step['step']}: {step['description']}")

            # 2a: Perform search
            try:
                results_json = self._google_search(step['query'])
                search_results = json.loads(results_json)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Could not parse search results for query '{step['query']}': {e}")
                continue

            if not search_results:
                print("No search results for this step.")
                continue

            # 2b: Select promising URLs (can be skipped if results are very direct)
            promising_urls = self._select_promising_urls(search_results, research_task)
            print(f"Agent selected {len(promising_urls)} promising URLs to investigate.")

            # 2c: View websites and extract info
            for url in promising_urls:
                print(f"Investigating: {url}")
                content = self._view_text_website(url)
                if content:
                    extracted_data = self._extract_collaborator_info(url, content, research_task)
                    if extracted_data and extracted_data.get("collaborators"):
                        print(f"Extracted {len(extracted_data['collaborators'])} potential collaborator(s).")
                        potential_collaborators.extend(extracted_data["collaborators"])

        print(f"\n--- Research Agent Task Finished ---")
        print(f"Found a total of {len(potential_collaborators)} potential collaborators.")
        return potential_collaborators
