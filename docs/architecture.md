# Architecture overview

TrustAI is structured around a small but clear evaluation lifecycle:

1. Validate a dataset.
2. Select a provider and prompt configuration.
3. Run the model on each case.
4. Apply deterministic metrics.
5. Summarize case-level and aggregate results.
6. Expose the results through a FastAPI layer.

The current implementation focuses on the foundation of that workflow and intentionally keeps the logic simple and inspectable.
