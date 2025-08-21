import json
import openai

class CoordinatorAgent:
    def __init__(self, settings):
        self.settings = settings
        self.context = {}
        self.openai_client = None
        if self.settings.get("openai_api_key") and self.settings["openai_api_key"] != "YOUR_API_KEY_HERE":
            self.openai_client = openai.OpenAI(api_key=self.settings["openai_api_key"])
        print("Coordinator Agent initialized.")

    def load_context_from_file(self, key, filepath):
        """Reads a file and adds its content to the agent's context."""
        try:
            with open(filepath, 'r') as f:
                self.context[key] = f.read()
            print(f"Coordinator context '{key}' loaded successfully from {filepath}.")
            return True
        except FileNotFoundError:
            print(f"Error: Context file not found at {filepath}")
            self.context[key] = None
            return False

    def generate_strategic_plan(self) -> list[str]:
        """
        Analyzes all loaded context and generates a high-level strategic plan.
        """
        print("Coordinator Agent is generating a strategic plan...")

        if not self.openai_client:
            print("WARNING: OpenAI client not initialized. Using mock strategic plan.")
            return [
                "Finalize the list of potential partners for the consortium.",
                "Draft the 10-page Stage 1 Proposal document.",
                "Create a detailed project timeline with dependencies for all Work Packages.",
            ]

        # Check for necessary context
        required_context = ['project_brief', 'architecture_design', 'wbs']
        if not all(key in self.context and self.context[key] for key in required_context):
            missing = [key for key in required_context if key not in self.context or not self.context[key]]
            print(f"ERROR: Missing necessary context to generate a plan: {missing}")
            return ["Error: Missing project context."]

        prompt = f"""
        You are a world-class Chief of Staff and project manager for a high-tech R&D project seeking EU funding. You are tasked with creating a high-level strategic plan.

        You have the following documents for context:

        1. The Project Brief (`project_brief`):
        ---
        {self.context.get('project_brief', 'Not available.')[:2000]}
        ---

        2. The System's Architectural Design (`architecture_design`):
        ---
        {self.context.get('architecture_design', 'Not available.')[:2000]}
        ---

        3. The Work Breakdown Structure (`wbs`):
        ---
        {self.context.get('wbs', 'Not available.')}
        ---

        Based on a holistic analysis of all this information, identify the top 3-5 most critical, immediate, high-level goals to move this project forward towards a successful Stage 1 proposal submission. The current state is that we have a plan and an AI assistant with a Research and Document agent.

        Return your answer as a JSON-formatted list of strings. Each string should be a clear, actionable goal.
        For example:
        ["Goal 1...", "Goal 2...", "Goal 3..."]
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.settings.get("llm_model", "gpt-4o"),
                messages=[
                    {"role": "system", "content": "You are a strategic project manager that provides high-level goals as a JSON list."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            data = json.loads(response.choices[0].message.content)
            # Handle if the LLM returns a dictionary with a key
            if isinstance(data, dict):
                plan = data.get("plan", data.get("goals", []))
                if isinstance(plan, list):
                    return plan
            elif isinstance(data, list):
                return data
            return ["Error: Could not parse plan from LLM response."]
        except Exception as e:
            print(f"An error occurred while calling OpenAI API for strategic planning: {e}")
            return [f"Error: Could not generate plan due to an API error: {e}"]
