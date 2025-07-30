"""
Defines data models for annotation requests and results.

Contains Pydantic models for structuring input, output, and explanations
in the annotation process. Ensures type safety and consistent data handling.
"""

from typing import List, Optional

from pydantic import BaseModel, field_validator

from .common import AnnotatorMetadata, EntityTypes, PatternRecognizer


class AnnotatorRequest(BaseModel):
    """
    Represents an annotation request.

    Contains text to annotate, language, and optional parameters
    to customize the annotation process.
    """

    text: str
    language: str
    correlation_id: Optional[str]
    score_threshold: Optional[float]
    entities: Optional[List[EntityTypes]]
    return_decision_process: Optional[bool]
    ad_hoc_recognizers: Optional[List[PatternRecognizer]]
    context: Optional[List[str]]


class AnnotationResult(BaseModel):
    """
    Represents the result of an annotation.

    Includes position, score, entity type, and optional metadata.
    """

    start: int
    end: int
    score: Optional[float]
    entity_type: str
    recognition_metadata: Optional[AnnotatorMetadata]

    @field_validator("entity_type")
    @classmethod
    def validate_entity_type(cls, v):
        if v not in EntityTypes.__members__:
            return "UNKNOWN"
        return v


class AnalysisExplanation(BaseModel):
    """
    Provides detailed explanation of an annotation analysis.

    Includes information about the recognizer, patterns, scores,
    and context improvements.
    """

    recognizer: str
    pattern_name: Optional[str]
    pattern: Optional[str]
    original_score: float
    score: float
    textual_explanation: Optional[str]
    score_context_improvement: float
    supportive_context_word: str
    validation_result: Optional[float]


class AnnotationResultWithAnaysisExplanation(AnnotationResult):
    """
    Extends AnnotationResult with detailed analysis explanation.
    """

    analysis_explanation: Optional[AnalysisExplanation]
