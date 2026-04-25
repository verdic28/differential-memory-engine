# Differential Memory Engine (DME) v1.0

A specialized Python framework designed to solve **Context Drag** in GenAI agents. Instead of relying on $O(n^2)$ token-bloated KV caches or lossy RAG, DME uses a **Differential Semantic State** to persist session logic.

## The Problem: Context Drag
Standard LLM sessions suffer from "Log Replay" overhead. As the session grows, the costs per turn increase superlinearly, and core reasoning is "pushed out" of the active window.

## The Solution: Differential Persistence
DME implements a **Differential Weight Update** logic:
- **State Tracking:** Maintains a persistent vector-space representation of the session's "Global Logic."
- **Delta Extraction:** Identifies what is *new* vs. what is *redundant* in the current turn.
- **Semantic Anchor:** Ensures core variables (Profit thresholds, architectural constraints) never leave the "Latent Memory" even if they leave the token window.

## Quick Start
```python
from memory_engine import DifferentialMemory

mem = DifferentialMemory(decay_rate=0.05)
mem.update("The target Nasdaq profit threshold is 1.25%")
# ... 50 turns later ...
recall = mem.recall("What is our risk limit?")
