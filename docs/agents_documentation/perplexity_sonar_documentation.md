# Perplexity Sonar API Integration Guide

This document provides a comprehensive overview of the Perplexity Sonar API and the strategy for integrating it into the EUFM assistant system.

## 1. Overview

Perplexity Sonar is a powerful AI model family designed for real-time, web-wide research and question-answering. Its key advantage is the ability to access live data from the internet and provide grounded results with citations, which is invaluable for our research-intensive project.

## 2. Key Models

We have access to several models, with two being of primary interest for our project:

*   **`sonar-reasoning`**: A fast, real-time model ideal for quick problem-solving and ad-hoc research queries.
*   **`sonar-deep-research`**: An expert-level model for conducting exhaustive searches and generating comprehensive, structured reports. This will be our primary tool for in-depth literature reviews and partner identification for Stage 2.

## 3. API Integration Strategy

The Perplexity API is **fully compatible with the OpenAI Chat Completions format**. This makes integration into our existing system straightforward.

### Implementation Steps:

1.  **Add a new method to `ai_services.py`:** A new method, `query_perplexity_sonar`, will be added to our `app/utils/ai_services.py` module.
2.  **Use OpenAI Client Libraries:** This new method will leverage the existing `openai` Python library. The only change required is to point the client to the Perplexity API endpoint.
3.  **API Key Management:** The Perplexity API key will be added to our `.env` file and managed through our existing settings configuration.

### Example Code for `ai_services.py`:

```python
# In app/utils/ai_services.py

from openai import OpenAI

class AIServices:
    # ... (existing methods)

    def query_perplexity_sonar(self, prompt, model="sonar-deep-research"):
        """
        Sends a query to the Perplexity Sonar API and returns the response.
        """
        print(f"--- Querying Perplexity Sonar ({model}) with prompt: {prompt[:50]}... ---")
        
        client = OpenAI(api_key=self.settings.get("perplexity_api_key"), base_url="https://api.perplexity.ai")
        
        messages = [
            {"role": "system", "content": "You are an expert research assistant for a Horizon Europe project."},
            {"role": "user", "content": prompt},
        ]
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"--- Error querying Perplexity Sonar: {str(e)} ---")
            return f"Error: Could not get a response from Perplexity Sonar. Details: {str(e)}"

```

## 4. Use Cases for the XYL-PHOS-CURE Project

Perplexity Sonar will be a critical tool for our Stage 2 preparation. Here are some examples of how we will use it:

*   **Literature Review:**
    *   "Find all peer-reviewed papers on the use of phosphinic acids in agriculture published since January 2024."
    *   "Summarize the latest findings on the economic impact of Xylella fastidiosa in the EU, with sources."
*   **Consortium Building:**
    *   "Identify research groups at the University of Malaga that have published on organophosphorus chemistry or plant pathology in the last three years."
    *   "List SMEs in the EU that specialize in the registration of new plant protection products."
*   **Policy & Regulation:**
    *   "What are the current EU regulations (post-2023) regarding the use of novel bactericides in olive groves?"
    *   "Provide a summary of the European Green Deal's specific objectives related to pesticide reduction."

This integration will significantly accelerate our research and ensure our Stage 2 proposal is built on the most current and comprehensive information available.
