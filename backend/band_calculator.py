import re
from typing import Dict, Any, Tuple

READING_BAND_MAP = [
    (39, 40, 9.0),
    (37, 38, 8.5),
    (35, 36, 8.0),
    (33, 34, 7.5),
    (30, 32, 7.0),
    (27, 29, 6.5),
    (23, 26, 6.0),
    (19, 22, 5.5),
    (15, 18, 5.0),
    (13, 14, 4.5),
    (10, 12, 4.0),
    (8, 9, 3.5),
    (6, 7, 3.0),
    (4, 5, 2.5),
    (1, 3, 2.0),
    (0, 0, 1.0)
]

def normalize_answer(text: str) -> str:
    """Cleans up text for flexible IELTS comparison"""
    if not text:
        return ""
    # Strip spaces and convert to lower
    t = str(text).strip().lower()
    # Remove leading A), B) etc if multiple choice letter is passed
    match = re.match(r"^([a-d])[\)\.]\s*(.*)", t)
    if match:
        return match.group(1).lower()
    # Remove unnecessary articles and punctuation
    t = re.sub(r"[^\w\s]", "", t)
    return " ".join(t.split())

def calculate_band(raw_score: int, total_questions: int, section_type: str = "reading") -> float:
    """
    Calculates IELTS Band score (1.0 to 9.0) based on raw score.
    Scales dynamically if test has fewer or more than 40 questions.
    """
    if total_questions <= 0:
        return 1.0
        
    # Scale to 40 questions benchmark
    scaled_score = round((raw_score / total_questions) * 40)
    scaled_score = max(0, min(40, scaled_score))

    for min_s, max_s, band in READING_BAND_MAP:
        if min_s <= scaled_score <= max_s:
            return band
            
    return 1.0

def evaluate_test_submission(questions: list, user_answers: dict) -> Tuple[int, int, float, list]:
    """
    Compares user answers with correct answers.
    Returns (correct_count, total_count, band_score, itemized_results)
    """
    correct_count = 0
    total_count = len(questions)
    itemized = []

    for q in questions:
        q_id = str(q["id"])
        q_num = q["question_number"]
        correct = str(q["correct_answer"]).strip()
        user_ans = str(user_answers.get(q_id, user_answers.get(str(q_num), ""))).strip()

        norm_user = normalize_answer(user_ans)
        norm_correct = normalize_answer(correct)

        # Check match: exact or multiple choice letter match
        is_correct = False
        if norm_user and norm_correct:
            if norm_user == norm_correct:
                is_correct = True
            elif norm_user.startswith(norm_correct) or norm_correct.startswith(norm_user):
                is_correct = True

        if is_correct:
            correct_count += 1

        itemized.append({
            "question_id": q["id"],
            "question_number": q_num,
            "prompt": q["prompt"],
            "user_answer": user_ans,
            "correct_answer": correct,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    band_score = calculate_band(correct_count, total_count)
    return correct_count, total_count, band_score, itemized
