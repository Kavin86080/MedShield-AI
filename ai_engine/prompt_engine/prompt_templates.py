# Placeholder for prompt_templates.py
"""
MedShield-X Prompt Templates
Phase 2 - Prompt Engineering
"""


ZERO_SHOT_TEMPLATE = """
You are a healthcare AI assistant.

Question:
{question}

Answer:
"""


FEW_SHOT_TEMPLATE = """
You are a healthcare AI assistant.

Example 1

Question:
What is diabetes?

Answer:
Diabetes is a chronic condition affecting blood sugar regulation.

Example 2

Question:
What is hypertension?

Answer:
Hypertension is persistently elevated blood pressure.

Now answer:

Question:
{question}

Answer:
"""


CHAIN_OF_THOUGHT_TEMPLATE = """
You are a healthcare AI assistant.

Question:
{question}

Think step by step before answering.

Reasoning:

Answer:
"""


REACT_TEMPLATE = """
You are a healthcare AI assistant.

Question:
{question}

Thought:
Analyze the problem.

Action:
Retrieve relevant information.

Observation:
Review retrieved evidence.

Answer:
Provide the final response.
"""


MEDICAL_QA_TEMPLATE = """
You are MedShield-X.

Context:
{context}

Question:
{question}

Provide a medically relevant answer.
"""


RAG_TEMPLATE = """
You are MedShield-X.

Retrieved Context:
{context}

User Question:
{question}

Generate an answer using only the retrieved context.
"""