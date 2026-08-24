# Design Rationale

The LLM is deliberately not the source of truth. It is used for intent understanding and natural-language phrasing.

Products, inventory, prices, order state, delivery dates and purchase completion are controlled by deterministic backend functions.

This reduces hallucination risk, creates an audit boundary, makes transactions testable, and keeps the model replaceable.
