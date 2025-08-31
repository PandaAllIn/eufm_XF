# Multi-Agent Collaboration Research

## Overview
This document summarizes patterns and techniques for combining multiple large language model (LLM) agents. Sources include Reddit discussions (e.g., r/AI_Agents, r/Anthropic, r/ClaudeCode, r/GeminiCLI) and engineering blogs.

## Collaboration Patterns
- **Hierarchical Planner–Executor:** A supervising agent decomposes work and delegates to specialist agents. Discussions highlight its use for research pipelines and code generation.
- **Peer Review Loops:** Agents independently tackle the same task and critique each other's output before returning a final answer.
- **Shared Memory / Blackboard:** Agents write to a shared knowledge base so others can pick up context without direct messaging.

## Orchestration Frameworks
- [AutoGen](https://github.com/microsoft/autogen) enables conversational multi-agent teams with role-based agents and a controller for dialogue management.
- [LangGraph](https://github.com/langchain-ai/langgraph) and LangChain's agent ecosystem provide planning, memory, and routing primitives.
- [CrewAI](https://github.com/joaomdmoura/crewai) offers YAML-configured crews where each agent is mapped to a task, with support for multiple LLM providers.

## Router / Task Dispatcher Patterns
- A **Router Agent** receives a user request and selects a specialized agent or model. Selection strategies include keyword rules, embedding similarity, or an LLM-based judge.
- Open-source examples include LangChain's `MultiPromptChain`, AutoGen's `GroupChat` with a `RouterAgent`, and frameworks that integrate OpenAI, Claude, and Gemini via provider-specific tools.

## Cross‑Model Workflows
- Projects often combine models by capability: e.g., Claude for long-context reasoning, Gemini for multimodal understanding, and GPT-4o for coding.
- Task dispatchers evaluate cost, latency, and accuracy before routing to the most suitable model. Fallback chains handle failures.

## Selected Discussions & Resources
- r/AI_Agents threads on multi-agent project management and AutoGen experiments.
- r/Anthropic and r/ClaudeCode posts on coordinating Claude agents for code reviews.
- r/GeminiCLI discussions on using Gemini as a planning hub for tool-using agents.
- LangChain blog: [Agent Router Pattern](https://blog.langchain.dev/agent-router/)
- Microsoft Research blog: [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://microsoft.github.io/autogen/)

## Key Takeaways
1. **Central Dispatcher** improves reliability by matching tasks to agents with the right tools or models.
2. **Shared context** (memory or documents) reduces redundant calls and supports iterative refinement.
3. **Cross-LLM routing** leverages strengths of diverse models while keeping costs manageable.
4. **Open-source frameworks** like AutoGen, LangGraph, and CrewAI provide reusable components for building these systems.
