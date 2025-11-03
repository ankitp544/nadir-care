from typing import Dict, Any, List
from enum import Enum

class RecommendationType(str, Enum):
    ADMISSION = "ADMISSION"
    DOCTOR_VISIT = "DOCTOR_VISIT"
    HOME_MEDICATION = "HOME_MEDICATION"


def get_recommendation(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based recommendation engine.
    Analyzes parsed medical data and determines the appropriate recommendation.
    """
    severity = parsed_data.get("severity", "low").lower()
    conditions = parsed_data.get("conditions", [])
    symptoms = parsed_data.get("symptoms", [])
    test_results = parsed_data.get("test_results", [])
    
    # Critical keywords that indicate hospital admission
    critical_keywords = [
        "severe", "critical", "emergency", "urgent", "acute",
        "heart attack", "stroke", "pneumonia", "sepsis", "infection",
        "high fever", "chest pain", "difficulty breathing", "unconscious",
        "blood pressure", "bp", "heart rate", "pulse", "surgery"
    ]
    
    # Moderate keywords that indicate doctor visit
    moderate_keywords = [
        "moderate", "abnormal", "elevated", "increased", "decreased",
        "pain", "discomfort", "infection", "inflammation", "fever",
        "consult", "follow up", "examination", "test results"
    ]
    
    # Check severity level
    is_critical = severity in ["critical", "high"]
    is_moderate = severity == "moderate"
    
    # Check conditions and symptoms for critical indicators
    all_text = " ".join(conditions + symptoms + test_results).lower()
    
    critical_found = any(keyword in all_text for keyword in critical_keywords)
    moderate_found = any(keyword in all_text for keyword in moderate_keywords)
    
    # Decision logic
    if is_critical or critical_found:
        recommendation = RecommendationType.ADMISSION
        reasoning = "Based on the severity and critical indicators in your report, immediate hospital admission is recommended."
        suggested_actions = [
            "Seek immediate medical attention at the nearest hospital",
            "Call emergency services if symptoms worsen",
            "Do not delay treatment",
            "Inform family members about your condition"
        ]
        confidence = 0.85
    elif is_moderate or moderate_found:
        recommendation = RecommendationType.DOCTOR_VISIT
        reasoning = "Your medical report indicates moderate concerns that require professional medical consultation."
        suggested_actions = [
            "Schedule an appointment with your doctor as soon as possible",
            "Bring this report to your consultation",
            "Follow any prescribed medication or treatment plan",
            "Monitor your symptoms and report any changes"
        ]
        confidence = 0.75
    else:
        recommendation = RecommendationType.HOME_MEDICATION
        reasoning = "Based on your report, the condition appears manageable with appropriate home care and medication."
        suggested_actions = [
            "Follow the recommended medication schedule",
            "Rest and maintain good hydration",
            "Monitor your symptoms",
            "Contact a healthcare provider if symptoms persist or worsen"
        ]
        confidence = 0.65
    
    return {
        "recommendation": recommendation.value,
        "confidence": confidence,
        "reasoning": reasoning,
        "suggested_actions": suggested_actions
    }

