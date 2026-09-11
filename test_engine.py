import engine
import json

def test_8_question_round_by_round_flow():
    print("=== Testing 8-Question Round-by-Round Flow (2 per round) ===")
    
    # 1. Setup
    session = engine.start_interview_session("Alex Sharma", "Software Development Engineer (SDE 1)", "Intermediate")
    assert session["current_round_idx"] == 0
    assert session["round_question_count"] == 1
    assert session["current_question"]
    print(f"[*] Started Session. Round 1 Q1: {session['current_question'][:70]}...")

    rounds_data = [
        ("Round 1: CS Fundamentals", [
            "Processes have independent memory spaces, while threads share the memory of their parent process. Context switching is managed by the OS kernel via PCBs.",
            "ACID stands for Atomicity, Consistency, Isolation, and Durability. B-Tree indexes speed up lookups from O(N) to O(log N)."
        ]),
        ("Round 2: DSA & Problem Solving", [
            "We can use a hash map to achieve O(N) time and O(N) space by storing the complement of each element as we iterate through the array.",
            "Floyd's Cycle Detection uses slow and fast pointers. If fast meets slow, a cycle exists. Time complexity is O(N) and space is O(1)."
        ]),
        ("Round 3: Project Defense & System Design", [
            "I built a real-time analytics engine using FastAPI, Kafka, and PostgreSQL. The primary bottleneck was database write contention, which we solved by micro-batching.",
            "We can use a Redis Cache-Aside pattern with TTL. For cache invalidation, we invalidate keys on database writes and use mutex locks for cache stampede prevention."
        ]),
        ("Round 4: HR & Behavioral", [
            "In a hackathon, a teammate insisted on an unfamiliar framework. Using STAR, I arranged a 15-minute spike to compare tradeoffs, and we aligned objectively.",
            "During a release, a regression occurred. I notified stakeholders immediately, rolled back to the stable build, wrote automated tests, and conducted a blameless post-mortem."
        ])
    ]

    total_q_count = 0
    for r_idx, (r_name, answers) in enumerate(rounds_data):
        print(f"\n--- Entering {r_name} (Round {r_idx + 1} of 4) ---")
        assert session["current_round_idx"] == r_idx
        
        # Question 1
        ans1 = answers[0]
        res1 = engine.process_candidate_answer(session, ans1)
        total_q_count += 1
        assert not res1["round_completed"], "Round should NOT be completed after 1st question"
        assert res1["feedback"], "Should receive brief feedback on Q1"
        assert res1["next_question"], "Should generate Q2 for the same round"
        print(f"[*] Answered Q1. Feedback: {res1['feedback'][:60]}...")
        print(f"[*] Round Q2: {res1['next_question'][:70]}...")

        # Question 2
        ans2 = answers[1]
        res2 = engine.process_candidate_answer(session, ans2)
        total_q_count += 1
        assert res2["round_completed"], "Round MUST be completed after 2nd question"
        assert res2["feedback"], "Should receive brief feedback on Q2"
        print(f"[*] Answered Q2. Feedback: {res2['feedback'][:60]}...")
        print(f"[+] {r_name} Completed! (2 of 2 questions answered)")

        if r_idx < 3:
            # Must explicitly call proceed_to_next_round to advance
            assert not res2["is_completed"], "Whole interview should not be completed yet"
            next_q = engine.proceed_to_next_round(session)
            assert session["current_round_idx"] == r_idx + 1
            assert session["round_question_count"] == 1
            assert not session["round_completed"]
            print(f"[+] Successfully progressed to Round {r_idx + 2}!")
        else:
            # Round 4 finished -> interview completed!
            assert res2["is_completed"], "Interview should be completed after Round 4 Q2"
            assert session["is_completed"]

    assert total_q_count == 8, "Must answer exactly 8 questions in total"
    assert len(session["history"]) == 8, "History must contain all 8 question exchanges"
    print("\n[+] Successfully completed all 8 questions across 4 rounds!")

    # Verify Report Generation
    report = session["final_report"]
    assert report, "Final report must be generated"
    assert "factor_scores" in report
    assert "round_scores" in report
    assert "skill_gaps" in report
    assert len(report["roadmap_7_day"]) == 7
    assert "final_recommendation" in report
    print("\n[+] Performance Report & 7-Day Roadmap Verified!")

def test_arena_evaluator_prompt():
    print("\n=== Testing Arena Evaluator Standard Contract (SDG 4) ===")
    prompt = "Teach me the basics of linear regression as if I am a beginner, then give me three practice questions."
    reply = engine.handle_arena_evaluator_message(prompt)
    assert len(reply) > 50
    print(f"[*] Response Length: {len(reply)} chars")
    print("[+] Arena Evaluator Contract Test PASSED!")

if __name__ == "__main__":
    test_8_question_round_by_round_flow()
    test_arena_evaluator_prompt()
    print("\nALL 8-QUESTION ROUND-BY-ROUND TESTS PASSED 100%!")
