import re
from typing import Dict, List

# Try spaCy
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

PRIORITY_MAP = {
    "critical": "Critical",
    "urgent": "High",
    "high priority": "High",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "blocking": "Critical"
}

DEADLINE_PATTERNS = [
    r"\btomorrow\b(?: evening| morning| night)?",
    r"\bend of this week\b",
    r"\bfriday\b",
    r"\bnext monday\b",
    r"\bwednesday\b",
    r"\bnext week\b",
    r"\bby friday\b",
    r"\bthis week\b"
]

TASK_SKILLS = {
    "login": ["frontend", "react", "javascript", "ui"],
    "bug": ["frontend", "qa", "testing"],
    "database": ["database", "backend"],
    "performance": ["backend", "performance"],
    "api": ["backend", "apis", "documentation"],
    "documentation": ["documentation"],
    "design": ["ui", "ux", "design"],
    "onboarding": ["ui", "ux", "design"],
    "unit test": ["testing", "qa"],
    "payment": ["backend", "qa"]
}


def split_sentences(text):
    if nlp:
        return [s.text.strip() for s in nlp(text).sents]
    return [s.strip() for s in re.split(r'[.!?\n]+', text) if s.strip()]


def detect_deadline(s):
    s = s.lower()
    for p in DEADLINE_PATTERNS:
        m = re.search(p, s)
        if m:
            return m.group(0)
    return ""


def detect_priority(s):
    s = s.lower()
    for k, v in PRIORITY_MAP.items():
        if k in s:
            return v
    return "Medium"


def detect_assignee(s, team):
    s = s.lower()
    for member in team:
        if member["name"].lower() in s:
            return member["name"]

    if nlp:
        doc = nlp(s)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                for m in team:
                    if m["name"].lower() in ent.text.lower():
                        return m["name"]
    return None


def infer_skills(s):
    s = s.lower()
    skills = []
    for kw, sklist in TASK_SKILLS.items():
        if kw in s:
            skills.extend(sklist)
    return list(set(skills))


def assign_member_by_skills(skills, team):
    best = None
    best_score = 0
    for member in team:
        score = 0
        for ms in member["skills"]:
            for sk in skills:
                if sk in ms.lower():
                    score += 1
        if score > best_score:
            best_score = score
            best = member["name"]
    return best


def extract_tasks(text, team):
    sentences = split_sentences(text)
    trigger_words = ["need", "should", "fix", "write", "design", "update", "tackle"]
    candidates = [s for s in sentences if any(t in s.lower() for t in trigger_words)]

    tasks = []
    tid = 1
    for s in candidates:
        desc = s
        assignee = detect_assignee(s, team)
        deadline = detect_deadline(s)
        priority = detect_priority(s)
        skills = infer_skills(s)
        if not assignee and skills:
            assignee = assign_member_by_skills(skills, team)

        tasks.append({
            "id": tid,
            "description": desc,
            "assigned_to": assignee or "Unassigned",
            "deadline": deadline,
            "priority": priority,
            "dependencies": "",
            "inferred_skills": skills
        })
        tid += 1

    return tasks
