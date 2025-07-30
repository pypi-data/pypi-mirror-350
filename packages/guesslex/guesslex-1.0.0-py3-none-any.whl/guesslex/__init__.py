"""
Guesslex - A machine learning-based programming language detection library.

This package provides accurate detection of programming languages in code snippets
using an ensemble of machine learning models trained on diverse code samples.

Key Features:
- Supports 25+ programming languages
- High accuracy (96.9% on test set)
- Confidence scoring and detailed analysis
- Command-line interface and Python API
- Enhanced pattern matching and ensemble scoring
"""

from .core import (
    CodeFeatureExtractor,
    extract_languages_with_confidence,
    classify_with_confidence,
    aggregate_predictions,
    format_confidence_output,
    load_model,
    detect_languages,
    detect_language_simple
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Supported languages
SUPPORTED_LANGUAGES = [
    "python", "java", "javascript", "c", "cpp", "csharp", "go", "rust", "php", "ruby",
    "scala", "typescript", "swift", "kotlin", "haskell", "r", "lua", "perl", "sql", 
    "html", "css", "shell", "matlab", "dart", "elixir", "plain-text"
]

__all__ = [
    "CodeFeatureExtractor",
    "extract_languages_with_confidence", 
    "classify_with_confidence",
    "aggregate_predictions",
    "format_confidence_output",
    "load_model",
    "detect_languages",
    "detect_language_simple",
    "SUPPORTED_LANGUAGES",
    "__version__"
] 