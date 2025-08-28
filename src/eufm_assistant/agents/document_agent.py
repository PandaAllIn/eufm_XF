import os
from openai import OpenAI


class DocumentAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.knowledge_base_path = "src/eufm_assistant/docs/Horizon_Xilella.md"

    def get_project_context(self):
        try:
            with open(self.knowledge_base_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Project context not found. Please ensure Horizon_Xilella.md is in the correct path."

    def draft_outreach_emails(self, partner_data):
        project_context = self.get_project_context()
        emails = []
        for partner in partner_data:
            prompt = f"""
            You are a professional project manager for a Horizon Europe project focused on curing Xylella fastidiosa.
            Your task is to draft a personalized outreach email to a potential collaborator.
            **Project Context:**
            {project_context[:4000]}...
            **Collaborator Information:**
            - Organisation: {partner.get("organisation_name", "N/A")}
            - Country: {partner.get("country", "N/A")}
            - Relevant Project: {partner.get("project_title", "N/A")} ({partner.get("project_acronym", "N/A")})
            - Summary: {partner.get("summary", "N/A")}
            - Contact Person: {partner.get("contact_person", "N/A")}
            **Instructions:**
            - The email should be formal, professional, and concise.
            - It should introduce our project and express interest in their work.
            - It should highlight the synergy between our project and their previous work on {partner.get("project_acronym", "their relevant project")}.
            - The goal is to initiate a conversation about potential collaboration.
            - Address the email to the contact person if available, otherwise use a generic greeting.
            """
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project manager drafting outreach emails.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            email_content = response.choices[0].message.content
            emails.append(email_content)
        return emails
