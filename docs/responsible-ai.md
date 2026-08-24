# Responsible AI and Governance

- **Explainability:** UI marks tool-backed responses as verified backend data.
- **Accuracy:** transactional facts originate from database tools.
- **Hallucination control:** missing tool data is reported as unavailable.
- **Prompt injection:** common schema, SQL, credential and system-prompt extraction attempts are blocked.
- **Transaction safety:** purchases require explicit confirmation and inventory validation.
- **Auditability:** tool calls are logged with session ID, tool name and success state.
- **Privacy:** frontend does not receive SQL, credentials or internal schemas.
- **Limitations:** no production authentication, payment processing, advanced abuse detection or formal model evaluation in this POC.
