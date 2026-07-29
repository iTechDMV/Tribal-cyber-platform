def score_controls(answers):
    total = 0
    max_score = 0

    for family in answers:
        for control in family.get("controls", []):
            weight = control.get("weight", 1)
            max_score += weight
            if control.get("met"):
                total += weight

    return {
        "score": total,
        "max": max_score,
        "percent": round((total / max_score) * 100, 2)
    }
