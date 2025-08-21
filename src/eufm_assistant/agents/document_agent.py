import json
import openai

class DocumentAgent:
    def __init__(self, settings):
        self.settings = settings
        self.project_brief = ""
        self.openai_client = None
        if self.settings.get("openai_api_key") and self.settings["openai_api_key"] != "YOUR_API_KEY_HERE":
            self.openai_client = openai.OpenAI(api_key=self.settings["openai_api_key"])
        print("Document Agent initialized.")

    def load_project_brief(self, filepath):
        """Reads the project brief document."""
        try:
            with open(filepath, 'r') as f:
                self.project_brief = f.read()
            print("Project brief loaded successfully.")
            return True
        except FileNotFoundError:
            print(f"Error: Project brief not found at {filepath}")
            return False

    def draft_outreach_email(self, collaborator_profile: dict) -> dict:
        """
        Drafts a personalized outreach email to a potential collaborator.
        """
        print(f"Document Agent is drafting an email to: {collaborator_profile.get('name')}")

        if not self.openai_client:
            print("WARNING: OpenAI client not initialized. Using mock email draft.")
            return {
                "subject": "Collaboration Inquiry: Xylella Fastidiosa Research (Mock)",
                "body": f"Dear {collaborator_profile.get('name')},\n\nThis is a mock email body. We are interested in your work on {collaborator_profile.get('summary_of_relevance')}.\n\nSincerely,\nThe Project Team"
            }

        if not self.project_brief:
            print("ERROR: Project brief not loaded. Cannot draft email.")
            return {"subject": "Error", "body": "Could not draft email because project brief is missing."}

        prompt = f"""
        You are a professional business development manager for a high-tech R&D startup. Your goal is to draft a personalized outreach email to a potential collaborator for a Horizon Europe project.

        Your project's goal is to find a cure for the Xylella fastidiosa plant bacterium. The full project brief is below:
        --- PROJECT BRIEF ---
        {self.project_brief}
        --- END PROJECT BRIEF ---

        You are contacting the following person:
        --- COLLABORATOR PROFILE ---
        {json.dumps(collaborator_profile, indent=2)}
        --- END COLLABORATOR PROFILE ---

        Please draft a concise, professional, and compelling email. Be sure to:
        1.  Reference their specific work and explain why it is relevant to your project (use the 'summary_of_relevance' field).
        2.  Briefly introduce your project and its goal.
        3.  Clearly state your interest in a potential collaboration for your Horizon Europe proposal.
        4.  Suggest a brief call to discuss further.

        Return your answer as a single JSON object with two keys: "subject" and "body".
        """

        try:
            response = self.openai_client.chat.completions.create(
                model=self.settings.get("llm_model", "gpt-4o"),
                messages=[
                    {"role": "system", "content": "You are a professional business development manager who writes compelling, personalized outreach emails and returns them as JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"An error occurred while calling OpenAI API for email drafting: {e}")
            return {"subject": "Drafting Error", "body": f"Could not draft email due to an API error: {e}"}
