This repo contains a logical model of the global AI ecosystem. The model is defined by a schema using LinkML written in YAML, with a model instance also written in YAML.

The model instance includes values for variables (such as canonical orders of magnitude of elements in the global economy) and is used to generate mermaid diagrams embedded in a Markdown document representing different perspectives from the model (e.g. Governance, Economic, Technical, and whole of model). 

The build process generated web pages using Docusaurus.

### Purpose

The model was created to make sense of how the global AI ecosystem works so that better understanding is developed of how things work, why they work that way, and the consequences of decisions and individual, organisation, and government levels.

The schema is defined in the `ai_ecosystem_schema.yaml` file.

The model instance is defined in the `ai_ecosystem.yaml` file.

The sense-making / insight deriving purpose of this model is its core value proposition. 

### Use

We want to be able to ask powerful questions of the model and have the explanation be derived from the model - ASSUMING THAT THE MODEL CAN CORRECTLY AND ADEQUATELY answer the question. It is entirely possible that questions may surface gaps or errors in the model. In which case the model will need to be corrected.

An example of the kind of question we want the model to help answer and understand is:

"The current global interests in AI include the to-be-expected discussions on existential threats and employment threats from AI. Other than these,  a significant volume of discussion is on the utility and economic impact of "AI Agents". **Where can a viewer see AI Agents in our model?**"

### Contributing Inquiries & Sense-Making Pages

To explore a new question or generate an inquiry page:
1. Open your LLM environment of choice (e.g., Google AI Studio, Claude, ChatGPT).
2. Load the system instructions from [`prompts/inquiry_protocol.md`](./prompts/inquiry_protocol.md).
3. Provide the canonical model [`model/ai_ecosystem.yaml`](./model/ai_ecosystem.yaml) as context
4. Explore your question conversationally, "how does the model ... ?"
5. Once the analysis (response) is sound, prompt the AI: *"Draft the inquiry artifact."*
6. Save the output to `docs/inquiries/<inquiry-id>.md` and submit a Pull Request.

**WARNING:** Be careful with step 3, some A prompt dialogues struggle with attached YAML files and get caught in a loop. If in doubt, use place the content of the file(s) in the prompt within fences. Fence start is "\`\`\`yaml" and end fence is "\`\`\`".