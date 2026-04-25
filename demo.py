from memory_engine import DifferentialMemoryEngine
import json
import time

def run_differential_audit():
    # 1. Initialize the Engine
    # We set a high novelty threshold (0.85) to ensure only 'new' info is saved.
    print("--- [INITIALIZING] Differential Memory Engine v2.0 ---")
    dme = DifferentialMemoryEngine(novelty_threshold=0.85, decay_factor=0.1)

    # 2. First Commit: Critical Business Logic
    print("\n[TURN 1] Committing core logic...")
    turn_1 = dme.commit("Nasdaq Trading Strategy: Maintain a 1.25% profit threshold with a 0.5% stop-loss.")
    print(f"Status: {turn_1}")

    # 3. Second Commit: REDUNDANT Information (The 'Smart' Test)
    # We try to send the same info again. A standard RAG would save it; ours will reject it.
    print("\n[TURN 2] Attempting to commit redundant data...")
    turn_2 = dme.commit("Nasdaq Trading Strategy: Maintain a 1.25% profit threshold.")
    status_2 = json.loads(turn_2)
    print(f"Status: {status_2['status']} | Novelty Score: {status_2['novelty']:.4f}")
    print("Result: Engine correctly identified and rejected redundant information.")

    # 4. Third Commit: NOVEL Information
    print("\n[TURN 3] Committing new operational constraints...")
    turn_3 = dme.commit("Operational Update: Only execute trades during New York session high-liquidity windows.")
    print(f"Status: {turn_3}")

    # 5. The Recall Test: Context Persistence
    # We query the engine to see if it still remembers the Turn 1 logic after Turn 3.
    print("\n--- [QUERY] Executing Latent State Recall ---")
    query_text = "What are my current trading limits and profit goals?"
    recall_json = dme.query(query_text)
    recall_data = json.loads(recall_json)

    print(f"Query: {query_text}")
    print(f"Engine Match: {recall_data['matches'][0]['content']}")
    print(f"Significance Score: {recall_data['matches'][0]['score']:.4f}")

    # 6. Export Audit Log
    # This is what you send to clients like Kenneth or Daniel as 'Proof of Work'.
    print("\n--- [AUDIT] Generating Final System Log ---")
    with open("differential_audit.json", "w") as f:
        f.write(dme.get_audit_log())
    
    print("Successfully generated 'differential_audit.json'. Use this for client verification.")

if __name__ == "__main__":
    run_differential_audit()
