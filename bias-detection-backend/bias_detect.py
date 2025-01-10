# bias_detector.py
import re
from typing import Dict, List

class BiasDetector:
    def __init__(self):
        self.bias_patterns = {
            r"\b(?:chairman|chairwoman)\b": "chair/chairperson",
            r"\b(?:businessman|businesswoman)\b": "business person/professional",
            r"\bmanpower\b": "workforce/staff",
            r"\b(?:policeman|policewoman)\b": "police officer",
            r"\b(?:mailman|mailwoman)\b": "mail carrier",
            r"\b(?:fireman|firewoman)\b": "firefighter",
            r"\bmanmade\b": "artificial/manufactured",
            r"\bguys\b": "everyone/team",
            r"\b(?:he|she) or (?:he|she)\b": "they",
            r"\bhis/her\b": "their",
            r"\bmanning\b": "staffing/operating",
        }

        self.problematic_phrases = {
            "normal person": "person",
            "crazy": "challenging/difficult",
            "handicapped": "person with a disability",
            "elderly": "older person/senior",
            "youngster": "young person",
            "third-world": "developing nation",
            "whitelist": "allowlist",
            "blacklist": "blocklist",
            "master": "primary/main",
            "struggling": "facing challenges",
            "I expected more": "I believe there's potential for more",
            "surprised by how much you're struggling": "noticed some challenges you're facing",
            "you need to focus on": "you could benefit from focusing on",
            "I would hope you don’t": "please let me know how I can support you",
            "man up": "show resilience",
            "you guys": "everyone/team",
            "pull yourself together": "stay composed",
            "get over it": "work through it",
            "you're so lazy": "you seem overwhelmed, let’s discuss how to manage this",
            "let's circle back": "let's revisit this topic later",
            "that's so stupid": "that's not an effective approach",
            "this is not ideal": "this is not the most efficient solution",
            "kill two birds with one stone": "accomplish two tasks with one solution",
            "go back to the drawing board": "reassess the approach",
            "you're just too sensitive": "let’s address the concern respectfully",
            "you should just relax": "let's find ways to reduce stress together",
            "don't make a scene": "let’s resolve this privately",
            "that's the way it's always been done": "let’s consider exploring new approaches",
            "no pain, no gain": "growth comes from consistent effort, not from discomfort",
            "that's just the way it is": "let’s focus on finding solutions",
            "let's stay on track": "let's focus on the task at hand",
            "I'm swamped": "I have a lot on my plate, but I’ll prioritize effectively",
            "she's so emotional": "she's passionate and engaged",
            "he's too quiet": "he’s focused and observant",
        }


    def analyze_text(self, text: str) -> Dict:
        findings = []
        suggestions = []
        
        for pattern, replacement in self.bias_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                findings.append({
                    "type": "gender-specific language",
                    "text": match.group(),
                    "position": match.span()
                })
                suggestions.append(f"Consider using '{replacement}' instead of '{match.group()}'")
        
        for phrase, alternative in self.problematic_phrases.items():
            if phrase.lower() in text.lower():
                findings.append({
                    "type": "potentially non-inclusive language",
                    "text": phrase,
                    "position": (text.lower().find(phrase.lower()), 
                               text.lower().find(phrase.lower()) + len(phrase))
                })
                suggestions.append(f"Consider using '{alternative}' instead of '{phrase}'")
        
        improved_text = text
        for pattern, replacement in self.bias_patterns.items():
            improved_text = re.sub(pattern, replacement, improved_text, flags=re.IGNORECASE)
        
        for phrase, alternative in self.problematic_phrases.items():
            improved_text = improved_text.replace(phrase, alternative)
        
        return {
            "original_text": text,
            "findings": findings,
            "suggestions": suggestions,
            "improved_text": improved_text
        }