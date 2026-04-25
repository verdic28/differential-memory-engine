import numpy as np
import json
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

class DifferentialMemoryEngine:
    """
    DME v2.0: High-fidelity Semantic Persistence Layer.
    Implements differential weight updates and novelty-based state tracking 
    to mitigate quadratic context growth in Agentic workflows.
    """
    def __init__(self, vector_dim=384, novelty_threshold=0.85, decay_factor=0.02):
        self.latent_space = {}  # The 'Latent State' of the session
        self.dim = vector_dim
        self.threshold = novelty_threshold
        self.decay = decay_factor
        self.audit_trail = []

    def _generate_embedding(self, text):
        """
        Internal Transformer Mock. 
        In production: return sentence_transformers_model.encode(text)
        """
        np.random.seed(hash(text) % (2**32))
        vector = np.random.normal(0, 1, self.dim)
        return vector / np.linalg.norm(vector)

    def compute_delta(self, new_vector):
        """
        Calculates the maximum similarity to existing state to determine novelty.
        """
        if not self.latent_space:
            return 1.0  # Absolute novelty for first entry
        
        existing_vectors = np.array([data["vector"] for data in self.latent_space.values()])
        similarities = cosine_similarity(new_vector.reshape(1, -1), existing_vectors)
        return 1.0 - np.max(similarities)

    def commit(self, content):
        """
        Differential Commit: Only persists information that exceeds the novelty threshold.
        """
        embedding = self._generate_embedding(content)
        delta = self.compute_delta(embedding)
        
        # Log the attempt for the audit trail
        entry_status = "REJECTED_REDUNDANT"
        
        if delta > (1.0 - self.threshold):
            entry_status = "COMMITTED_DIFFERENTIAL"
            entry_id = f"node_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            # Apply global state decay before adding new state
            for node in self.latent_space:
                self.latent_space[node]["importance"] *= (1.0 - self.decay)
            
            self.latent_space[entry_id] = {
                "vector": embedding,
                "importance": 1.0,
                "raw_data": content,
                "delta_score": float(delta)
            }

        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "status": entry_status,
            "novelty_score": float(delta),
            "content_fragment": content[:50] + "..."
        })
        
        return json.dumps({"status": entry_status, "novelty": float(delta)})

    def query(self, prompt, top_k=3):
        """
        Retrieves the most semantically relevant state updates, 
        weighted by their temporal 'Importance' score.
        """
        if not self.latent_space:
            return json.dumps({"error": "Latent space uninitialized."})

        query_vec = self._generate_embedding(prompt).reshape(1, -1)
        results = []

        for node_id, data in self.latent_space.items():
            sim = cosine_similarity(query_vec, data["vector"].reshape(1, -1))[0][0]
            # Significance = Semantic Similarity * Temporal Importance
            significance = sim * data["importance"]
            results.append({
                "content": data["raw_data"],
                "score": float(significance),
                "novelty": data["delta_score"]
            })

        # Sort by significance
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return json.dumps({
            "query": prompt,
            "matches": results[:top_k],
            "audit_ref": len(self.audit_trail)
        }, indent=2)

    def get_audit_log(self):
        return json.dumps(self.audit_trail, indent=4)
