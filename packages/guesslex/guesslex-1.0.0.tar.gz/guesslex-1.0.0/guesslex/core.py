"""
Core functionality for the guesslex library.
""" 
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import joblib
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# ─────────  Custom Feature Extractor (needed for model loading)
class CodeFeatureExtractor(BaseEstimator, TransformerMixin):
    """Custom feature extractor for code-specific patterns"""
    
    def __init__(self):
        self.feature_names = [
            'avg_line_length', 'punct_density', 'indent_consistency',
            'bracket_ratio', 'keyword_density', 'camel_case_ratio',
            'snake_case_ratio', 'comment_ratio', 'string_ratio'
        ]
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            features.append(self._extract_features(text))
        return np.array(features)
    
    def _extract_features(self, text):
        lines = [l for l in text.splitlines() if l.strip()]
        if not lines:
            return [0] * len(self.feature_names)
        
        # Average line length
        avg_line_len = np.mean([len(l) for l in lines])
        
        # Punctuation density
        punct_chars = len(re.findall(r'[;{}()<>#\[\]=+\-*/%]', text))
        punct_density = punct_chars / max(1, len(text))
        
        # Indentation consistency
        indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
        indent_consistency = 1.0 - (np.std(indents) / max(1, np.mean(indents))) if indents else 0
        
        # Bracket ratio
        brackets = len(re.findall(r'[{}()\[\]]', text))
        bracket_ratio = brackets / max(1, len(text))
        
        # Keyword density (common programming keywords)
        keywords = len(re.findall(r'\b(if|else|for|while|function|class|def|return|import|include)\b', text, re.I))
        keyword_density = keywords / max(1, len(text.split()))
        
        # Camel case ratio
        camel_case = len(re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b', text))
        camel_case_ratio = camel_case / max(1, len(text.split()))
        
        # Snake case ratio
        snake_case = len(re.findall(r'\b[a-z]+_[a-z_]+\b', text))
        snake_case_ratio = snake_case / max(1, len(text.split()))
        
        # Comment ratio
        comment_lines = sum(1 for l in lines if re.match(r'^\s*[#///*]', l))
        comment_ratio = comment_lines / max(1, len(lines))
        
        # String ratio
        strings = len(re.findall(r'["\'][^"\']*["\']', text))
        string_ratio = strings / max(1, len(text.split()))
        
        return [
            avg_line_len, punct_density, indent_consistency,
            bracket_ratio, keyword_density, camel_case_ratio,
            snake_case_ratio, comment_ratio, string_ratio
        ]

# Pickle compatibility fix: Make CodeFeatureExtractor available in __main__ namespace
# This handles the case where the model was trained in a __main__ context
import __main__
__main__.CodeFeatureExtractor = CodeFeatureExtractor

# Get the path to the bundled model
def get_model_path() -> str:
    """Get the path to the bundled model file."""
    return str(Path(__file__).parent / "model.joblib")

# Load the model lazily
_model_cache = None

def load_model(model_path: Optional[str] = None):
    """Load the trained model with pickle compatibility fixes."""
    global _model_cache
    if _model_cache is None:
        path = model_path or get_model_path()
        try:
            _model_cache = joblib.load(path)
        except AttributeError as e:
            if "CodeFeatureExtractor" in str(e) and "__main__" in str(e):
                # This is the pickle compatibility issue - try to fix it
                print("Detected pickle compatibility issue, attempting to fix...")
                
                # Add our module to sys.modules as __main__ temporarily
                original_main = sys.modules.get('__main__')
                try:
                    # Create a mock __main__ module with our CodeFeatureExtractor
                    import types
                    mock_main = types.ModuleType('__main__')
                    mock_main.CodeFeatureExtractor = CodeFeatureExtractor
                    sys.modules['__main__'] = mock_main
                    
                    # Try loading again
                    _model_cache = joblib.load(path)
                    print("Successfully loaded model with compatibility fix!")
                    
                finally:
                    # Restore original __main__
                    if original_main is not None:
                        sys.modules['__main__'] = original_main
                    else:
                        sys.modules.pop('__main__', None)
            else:
                raise e
    return _model_cache

# High-level API functions
def detect_language_simple(text: str, model_path: Optional[str] = None) -> str:
    """
    Simple API to detect the primary language of a code snippet.
    
    Args:
        text: The code text to analyze
        model_path: Optional path to a custom model file
        
    Returns:
        The detected language as a string
    """
    result = detect_languages(text, model_path)
    if result['all_languages']:
        return result['all_languages'][0]
    return 'plain-text'

def detect_languages(text: str, model_path: Optional[str] = None) -> Dict:
    """
    Detect programming languages in a code snippet with confidence scores.
    
    Args:
        text: The code text to analyze
        model_path: Optional path to a custom model file
        
    Returns:
        Dictionary containing detected languages and confidence information
    """
    pipe = load_model(model_path)
    return extract_languages_with_confidence(text, pipe)

# ─────────  Tunables
MODEL_PATH   = get_model_path()  # Use bundled model
WIN          = 12
STRIDE       = 3
PLAIN_TH     = 0.50  # Lowered threshold for better sensitivity
CONFIDENCE_TH = 0.70  # Lowered threshold for high confidence predictions
PUNCT_RE     = re.compile(r"[;{}()<>#\[\]=+\-*/%]|::|=>|->|<>")
FENCE_RE     = re.compile(
    r"```(\w+)?\s*\n(.*?)```"                # fenced markdown
    r"|<script[^>]*>(.*?)</script>"          # HTML script/style
    r"|<style[^>]*>(.*?)</style>",
    re.S | re.I
)

# Enhanced language-specific patterns with weights for better classification
LANG_PATTERNS = {
    'python': [
        (r'\bdef\s+\w+\s*\(', 3.0),  # Strong indicator
        (r'\bimport\s+\w+', 2.5),
        (r'\bfrom\s+\w+\s+import', 2.5),
        (r'if\s+__name__\s*==\s*["\']__main__["\']', 3.0),  # Very strong
        (r'f["\'][^"\']*{[^}]*}[^"\']*["\']', 2.8),  # f-strings
        (r'@\w+\s*\n\s*def', 2.5),  # decorators
        (r'\bself\.', 2.0),
        (r':\s*$', 1.5),  # colon at end of line
        (r'\.join\s*\(', 1.8),
        (r'\belif\b', 2.0),
        (r'__\w+__', 2.2),  # dunder methods
        (r'print\s*\(', 1.5),
        (r'\.decode\(', 1.8),
        (r'\.encode\(', 1.8),
        (r'secrets\.', 2.0),
        (r'base64\.', 1.8),
        (r'\.urlsafe_b64encode\(', 3.0),  # Very specific to Python
        (r'token_bytes\(', 2.8),  # Python secrets module
    ],
    'javascript': [
        (r'\bfunction\s+\w+\s*\(', 3.0),
        (r'\bconst\s+\w+', 2.5),
        (r'\blet\s+\w+', 2.5),
        (r'\bvar\s+\w+', 2.0),
        (r'console\.log\s*\(', 2.8),
        (r'=>', 2.5),  # arrow functions
        (r'\.then\s*\(', 2.5),
        (r'\.catch\s*\(', 2.5),
        (r'require\s*\(', 2.3),
        (r'document\.', 2.8),
        (r'window\.', 2.8),
        (r'\.prototype\.', 2.5),
        (r'\basync\s+function', 2.8),
        (r'\bawait\s+', 2.5),
        (r'\.json\s*\(\s*\)', 2.0),
        (r'new\s+\w+\s*\(', 1.8),
        # Patterns that distinguish JS from TS (lack of type annotations)
        (r'\bfunction\s+\w+\s*\([^)]*\)\s*{', 2.0),  # No return type
        (r'\bconst\s+\w+\s*=', 1.8),  # No type annotation
    ],
    'typescript': [
        (r'\binterface\s+\w+', 3.5),  # Very strong TS indicator
        (r':\s*\w+\s*[=;]', 3.0),  # type annotations
        (r'Promise<\w+>', 3.0),
        (r'\btype\s+\w+\s*=', 3.2),
        (r'<T>', 2.8),  # generics
        (r'\bexport\s+interface', 3.5),
        (r'\bexport\s+type', 3.2),
        (r':\s*string\b', 2.5),
        (r':\s*number\b', 2.5),
        (r':\s*boolean\b', 2.5),
        (r'\?\s*:', 2.3),  # optional chaining
        (r'as\s+\w+', 2.0),  # type assertions
        (r'async\s+\w+\s*\([^)]*\):\s*Promise', 3.0),
        (r':\s*Promise<', 3.2),  # Strong TS indicator
        (r'crypto\.subtle\.', 3.0),  # Web Crypto API often in TS
        (r'crypto\.getRandomValues\(', 2.8),
        (r'Uint8Array\(', 2.5),
        (r'TextEncoder\(\)', 2.5),
        (r'\.padStart\(', 2.0),
    ],
    'java': [
        (r'\bpublic\s+class\s+\w+', 3.5),
        (r'System\.out\.println', 3.2),
        (r'\bpublic\s+static\s+void\s+main', 3.5),
        (r'\bpackage\s+\w+', 3.0),
        (r'\bimport\s+\w+\.', 2.5),
        (r'@Override', 2.8),
        (r'\bString\[\]', 2.5),
        (r'\bArrayList\b', 2.3),
        (r'\bHashMap\b', 2.3),
        (r'\bpublic\s+\w+\s+\w+\s*\(', 2.0),
        (r'\bprivate\s+\w+\s+\w+', 2.0),
        (r'\bnew\s+\w+\s*\(', 1.5),
        (r'\.length\b', 1.5),
    ],
    'c': [
        (r'#include\s*<\w+\.h>', 3.5),
        (r'\bprintf\s*\(', 3.0),
        (r'\bmain\s*\(\s*\)', 3.2),
        (r'\bchar\s*\*', 2.8),
        (r'\btypedef\s+struct', 3.0),
        (r'\bstruct\s+\w+', 2.5),
        (r'\bmalloc\s*\(', 2.8),
        (r'\bfree\s*\(', 2.8),
        (r'\bsize_t\b', 2.5),
        (r'\bFILE\s*\*', 2.8),
        (r'\bstdio\.h\b', 3.0),
        (r'\bstdlib\.h\b', 3.0),
        (r'\bsrand\s*\(', 2.0),
        (r'\brand\s*\(', 2.0),
        (r'\btime\(NULL\)', 2.5),  # Common C pattern
        (r'\bunsigned\)', 2.0),  # C-style cast
    ],
    'cpp': [
        (r'#include\s*<iostream>', 3.8),
        (r'#include\s*<string>', 3.5),
        (r'std::\w+', 3.2),
        (r'\bstd::cout\b', 3.5),
        (r'\bstd::string\b', 3.2),
        (r'\bstd::endl\b', 3.2),
        (r'using\s+namespace', 3.0),
        (r'::\w+', 2.5),  # scope resolution
        (r'\btemplate\s*<', 3.0),
        (r'\bvirtual\s+', 2.8),
        (r'class\s+\w+\s*{', 2.5),
        (r'public:', 2.0),
        (r'private:', 2.0),
        (r'namespace\s+\w+', 2.5),
        (r'std::default_random_engine', 3.5),  # C++ specific
        (r'std::uniform_int_distribution', 3.5),
        (r'std::random_device', 3.5),
    ],
    'go': [
        (r'\bpackage\s+main', 3.8),
        (r'\bfunc\s+\w+\s*\(', 3.0),
        (r'\bimport\s*\(', 3.2),
        (r'\bfmt\.Println', 3.5),
        (r':\s*=', 3.0),  # Go's short variable declaration
        (r'\bmake\s*\(', 2.8),
        (r'\bgo\s+func', 3.0),
        (r'\bdefer\s+', 2.8),
        (r'\brange\s+', 2.5),
        (r'\bvar\s+\w+\s+\w+', 2.3),
        (r'\bfunc\s+main\s*\(\s*\)', 3.5),
        (r'\berr\s*:=', 2.5),
        (r'\bif\s+err\s*!=\s*nil', 3.0),
    ],
    'rust': [
        (r'\bfn\s+\w+\s*\(', 3.0),
        (r'\blet\s+mut\s+', 3.2),
        (r'\blet\s+\w+\s*=', 2.5),
        (r'\bmatch\s+\w+', 2.8),
        (r'\bprintln!\s*\(', 3.5),
        (r'\buse\s+\w+::', 2.8),
        (r'\bimpl\s+\w+', 2.5),
        (r'\bstruct\s+\w+\s*{', 2.3),
        (r'\benum\s+\w+', 2.5),
        (r'\bpub\s+fn', 2.8),
        (r'\bResult<', 2.8),
        (r'\bOption<', 2.8),
        (r'\bVec<', 2.5),
        (r'&str\b', 2.5),
        (r'&mut\s+', 2.3),
    ],
    'ruby': [
        (r'\bdef\s+\w+', 2.8),
        (r'\bend\b', 2.5),
        (r'\bclass\s+\w+', 2.5),
        (r'\brequire\s+["\']', 2.8),
        (r'\bputs\s+', 2.5),
        (r'\battr_accessor\b', 3.0),
        (r'\battr_reader\b', 3.0),
        (r'@\w+', 2.0),  # instance variables
        (r'@@\w+', 2.5),  # class variables
        (r'\|\w+\|', 2.3),  # block parameters
        (r'\.each\s+do', 2.8),
        (r'\.times\s+do', 2.8),
        (r'SecureRandom\.', 3.0),  # Ruby-specific
        (r'Digest::', 2.8),
        (r'Base64\.', 2.5),
        (r'\.hexdigest\(', 2.5),
        (r'require\s+["\']securerandom["\']', 3.2),
        (r'require\s+["\']digest["\']', 3.0),
        (r'require\s+["\']base64["\']', 3.0),
    ],
    'php': [
        (r'<\?php', 3.8),
        (r'\$\w+', 3.0),
        (r'\becho\s+', 2.5),
        (r'\bprint\s+', 2.5),
        (r'\bfunction\s+\w+\s*\(', 2.0),
        (r'\bclass\s+\w+', 2.0),
        (r'\bpublic\s+function', 2.8),
        (r'\bprivate\s+function', 2.8),
        (r'\bprotected\s+function', 2.8),
        (r'\$this->', 2.8),
        (r'array\s*\(', 2.5),
        (r'\[\]', 2.0),
        (r'\.php\b', 2.5),
        (r'\bforeach\s*\(', 2.5),
        (r'\bas\s+\$', 2.3),
    ],
}

# ─────────  Helpers
def load(text: str):
    fenced_langs = set()
    residual = text
    offset = 0
    for m in FENCE_RE.finditer(text):
        hint = (m.group(1) or "unknown").lower()
        code = m.group(2) or m.group(3) or m.group(4) or ""
        if code.strip():
            fenced_langs.add(hint)
        blk = m.group(0)
        residual = residual[:m.start()-offset] + ("\n" * blk.count("\n")) + residual[m.end()-offset:]
        offset += m.end() - m.start()
    return list(fenced_langs), residual

def windows(lines: List[str]) -> List[Tuple[int,int,str]]:
    wins=[]
    # Standard sliding windows
    for i in range(0, len(lines)-WIN+1, STRIDE):
        wins.append((i+1, i+WIN, "\n".join(lines[i:i+WIN])))
    
    # Add a final window to ensure we cover the end of the file
    if len(lines) >= WIN:
        last_start = len(lines) - WIN
        # Only add if it's not already covered by the last regular window
        if not wins or wins[-1][0] - 1 < last_start:
            wins.append((last_start+1, len(lines), "\n".join(lines[last_start:])))
    
    return wins

def punct_density(text: str) -> float:
    return len(PUNCT_RE.findall(text)) / max(1, len(text))

def pattern_score(text: str, lang: str) -> float:
    """Calculate a score based on language-specific patterns"""
    if lang not in LANG_PATTERNS:
        return 0.0
    
    patterns = LANG_PATTERNS[lang]
    matches = 0
    total_weight = 0
    
    for pattern, weight in patterns:
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            matches += weight
        total_weight += weight
    
    return matches / max(1, total_weight)

def get_top_pattern_matches(text: str, top_k: int = 3) -> List[Tuple[str, float]]:
    """Get top K languages by pattern matching score"""
    scores = []
    for lang in LANG_PATTERNS:
        score = pattern_score(text, lang)
        if score > 0:
            scores.append((lang, score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

def get_language_disambiguation_score(predicted_lang: str, pattern_matches: List[Tuple[str, float]], 
                                    confidence: float, text: str) -> Tuple[str, float, str]:
    """
    Apply advanced language disambiguation with ensemble scoring.
    Returns (final_language, final_confidence, reason)
    """
    # Language confusion pairs - languages that are commonly misclassified
    confusion_pairs = {
        'javascript': ['typescript', 'kotlin', 'java'],
        'typescript': ['javascript', 'kotlin', 'java'],
        'kotlin': ['java', 'javascript', 'typescript', 'swift'],
        'java': ['kotlin', 'csharp', 'typescript'],
        'csharp': ['java', 'kotlin', 'typescript'],
        'swift': ['kotlin', 'csharp'],
        'c': ['cpp'],
        'cpp': ['c'],
        'python': ['ruby'],
        'ruby': ['python'],
        'go': ['c', 'rust'],
        'rust': ['go', 'cpp'],
    }
    
    # Get structural analysis boost
    structural_boost = get_contextual_confidence_boost(text, predicted_lang, confidence)
    
    # If no pattern matches, use ensemble scoring with structural analysis
    if not pattern_matches:
        pattern_score = 0.0
        ensemble_conf, conf_level = get_ensemble_confidence(confidence, pattern_score, structural_boost, predicted_lang)
        return predicted_lang, ensemble_conf, f"ensemble_no_patterns_{conf_level}"
    
    best_pattern_lang, best_pattern_score = pattern_matches[0]
    
    # Very strong pattern evidence - but verify with ensemble
    if best_pattern_score > 0.6:
        # Check if structural analysis supports this
        struct_boost_for_pattern = get_contextual_confidence_boost(text, best_pattern_lang, confidence)
        pattern_ensemble_conf, conf_level = get_ensemble_confidence(
            confidence, best_pattern_score, struct_boost_for_pattern, best_pattern_lang
        )
        
        # If ensemble confidence is high, trust the pattern
        if pattern_ensemble_conf > 0.75:
            return best_pattern_lang, pattern_ensemble_conf, f"strong_pattern_ensemble_{conf_level}"
        else:
            # Pattern is strong but ensemble disagrees - be cautious
            final_ensemble_conf, conf_level = get_ensemble_confidence(
                confidence, best_pattern_score * 0.7, structural_boost, predicted_lang
            )
            return predicted_lang, final_ensemble_conf, f"pattern_ensemble_conflict_{conf_level}"
    
    # Check for language confusion with ensemble scoring
    if predicted_lang in confusion_pairs:
        confused_with = confusion_pairs[predicted_lang]
        
        # If pattern strongly suggests a different language from confusion set
        if best_pattern_lang in confused_with and best_pattern_score > 0.3:
            # Get ensemble score for the pattern-suggested language
            pattern_struct_boost = get_contextual_confidence_boost(text, best_pattern_lang, confidence)
            pattern_ensemble_conf, pattern_conf_level = get_ensemble_confidence(
                confidence, best_pattern_score, pattern_struct_boost, best_pattern_lang
            )
            
            # Get ensemble score for the original prediction
            orig_ensemble_conf, orig_conf_level = get_ensemble_confidence(
                confidence, 0.0, structural_boost, predicted_lang
            )
            
            # Choose the language with higher ensemble confidence
            if pattern_ensemble_conf > orig_ensemble_conf + 0.1:  # Small bias toward pattern
                return best_pattern_lang, pattern_ensemble_conf, f"disambiguation_ensemble_{pattern_conf_level}"
            else:
                return predicted_lang, orig_ensemble_conf, f"model_over_pattern_{orig_conf_level}"
        
        # If pattern confirms the predicted language
        elif best_pattern_lang == predicted_lang and best_pattern_score > 0.2:
            ensemble_conf, conf_level = get_ensemble_confidence(
                confidence, best_pattern_score, structural_boost, predicted_lang
            )
            return predicted_lang, ensemble_conf, f"pattern_confirmation_ensemble_{conf_level}"
        
        # Weak evidence for confused language - apply ensemble with penalty
        elif confidence < 0.7 and best_pattern_lang in confused_with:
            penalized_conf = confidence * 0.8
            ensemble_conf, conf_level = get_ensemble_confidence(
                penalized_conf, best_pattern_score * 0.5, structural_boost, predicted_lang
            )
            return predicted_lang, ensemble_conf, f"weak_confused_ensemble_{conf_level}"
    
    # Pattern confirms prediction - use full ensemble
    if best_pattern_lang == predicted_lang:
        ensemble_conf, conf_level = get_ensemble_confidence(
            confidence, best_pattern_score, structural_boost, predicted_lang
        )
        return predicted_lang, ensemble_conf, f"pattern_confirmation_ensemble_{conf_level}"
    
    # Pattern suggests different language with decent confidence
    elif best_pattern_score > 0.25 and confidence < 0.6:
        # Compare ensemble scores for both languages
        pattern_struct_boost = get_contextual_confidence_boost(text, best_pattern_lang, confidence)
        pattern_ensemble_conf, pattern_conf_level = get_ensemble_confidence(
            confidence, best_pattern_score, pattern_struct_boost, best_pattern_lang
        )
        
        orig_ensemble_conf, orig_conf_level = get_ensemble_confidence(
            confidence, 0.0, structural_boost, predicted_lang
        )
        
        if pattern_ensemble_conf > orig_ensemble_conf:
            return best_pattern_lang, pattern_ensemble_conf, f"pattern_override_ensemble_{pattern_conf_level}"
        else:
            return predicted_lang, orig_ensemble_conf, f"model_over_weak_pattern_{orig_conf_level}"
    
    # Default: use ensemble scoring for model prediction
    ensemble_conf, conf_level = get_ensemble_confidence(
        confidence, best_pattern_score if best_pattern_lang == predicted_lang else 0.0, 
        structural_boost, predicted_lang
    )
    return predicted_lang, ensemble_conf, f"model_ensemble_{conf_level}"

def classify_with_confidence(pipe, wins):
    """Enhanced classification with detailed confidence scoring"""
    X = [w[2] for w in wins]
    probs = pipe.predict_proba(X)
    
    results = []
    
    for k, prob_dist in enumerate(probs):
        txt = wins[k][2]
        
        # Get top predictions with probabilities
        top_indices = np.argsort(prob_dist)[::-1][:3]
        top_predictions = [(pipe.classes_[i], prob_dist[i]) for i in top_indices]
        
        # Calculate additional features
        punct_dens = punct_density(txt)
        pattern_matches = get_top_pattern_matches(txt)
        
        # Primary prediction
        predicted_class = top_predictions[0][0]
        confidence = top_predictions[0][1]
        
        # Enhanced decision logic
        final_label, final_confidence, decision_reason = get_language_disambiguation_score(predicted_class, pattern_matches, confidence, txt)
        
        # Improved plain text detection (after disambiguation)
        is_likely_code = False
        
        # Check for strong code indicators that should override plain text detection
        if pattern_matches and pattern_matches[0][1] > 0.15:  # Lowered from 0.2
            is_likely_code = True
        
        # Check for specific code patterns that indicate it's not plain text
        code_indicators = [
            r'\bdef\s+\w+\s*\(',  # Python functions
            r'\bimport\s+\w+',    # Import statements
            r'\bfrom\s+\w+\s+import',  # Python imports
            r'#include\s*<',      # C/C++ includes
            r'\bstd::\w+',        # C++ std namespace
            r'\bfunction\s+\w+',  # JavaScript functions
            r'\binterface\s+\w+', # TypeScript interfaces
            r'\bclass\s+\w+',     # Class definitions
            r'{\s*$',             # Opening braces
            r'}\s*$',             # Closing braces
            r';\s*$',             # Semicolons at end of line
            r'secrets\.',         # Python secrets module
            r'base64\.',          # Base64 operations
            r'SecureRandom\.',    # Ruby SecureRandom
            r'crypto\.',          # Crypto operations
        ]
        
        for pattern in code_indicators:
            if re.search(pattern, txt, re.MULTILINE):
                is_likely_code = True
                break
        
        # Apply plain text detection with improved logic
        if not is_likely_code and (final_confidence < PLAIN_TH or punct_dens < 0.02):  # Lowered punct threshold
            final_label = "plain-text"
            final_confidence = max(0.6, 1.0 - final_confidence)
            decision_reason = "plain_text_detection"
        
        # Ensure confidence is reasonable
        final_confidence = max(0.1, min(0.99, final_confidence))
        
        result = {
            'window': k,
            'text_preview': txt[:100] + "..." if len(txt) > 100 else txt,
            'predicted_language': final_label,
            'confidence': final_confidence,
            'decision_reason': decision_reason,
            'model_predictions': top_predictions,
            'pattern_matches': pattern_matches,
            'punct_density': punct_dens,
            'lines': (wins[k][0], wins[k][1])
        }
        
        results.append(result)
    
    return results

def aggregate_predictions(results: List[Dict]) -> Dict:
    """Aggregate window predictions with improved multi-language context analysis"""
    if not results:
        return {'languages': [], 'confidence_summary': {}}
    
    # Filter out plain-text predictions for aggregation
    code_results = [r for r in results if r['predicted_language'] != 'plain-text']
    
    if not code_results:
        return {
            'languages': ['plain-text'],
            'confidence_summary': {
                'plain-text': {
                    'avg_confidence': np.mean([r['confidence'] for r in results]),
                    'window_count': len(results),
                    'decision_reasons': [r['decision_reason'] for r in results]
                }
            },
            'detailed_results': results
        }
    
    # Count languages and calculate confidence statistics
    lang_stats = {}
    for result in code_results:
        lang = result['predicted_language']
        if lang not in lang_stats:
            lang_stats[lang] = {
                'confidences': [],
                'window_count': 0,
                'decision_reasons': [],
                'high_confidence_windows': 0,
                'ensemble_windows': 0,
                'pattern_confirmations': 0
            }
        
        lang_stats[lang]['confidences'].append(result['confidence'])
        lang_stats[lang]['window_count'] += 1
        lang_stats[lang]['decision_reasons'].append(result['decision_reason'])
        
        # Track quality indicators
        if result['confidence'] > 0.6:  # Lowered from 0.7 for shorter docs
            lang_stats[lang]['high_confidence_windows'] += 1
        
        if 'ensemble' in result['decision_reason']:
            lang_stats[lang]['ensemble_windows'] += 1
            
        if 'pattern_confirmation' in result['decision_reason']:
            lang_stats[lang]['pattern_confirmations'] += 1
    
    # Calculate enhanced statistics with quality metrics
    confidence_summary = {}
    for lang, stats in lang_stats.items():
        confidence_summary[lang] = {
            'avg_confidence': np.mean(stats['confidences']),
            'max_confidence': np.max(stats['confidences']),
            'min_confidence': np.min(stats['confidences']),
            'window_count': stats['window_count'],
            'decision_reasons': stats['decision_reasons'],
            'high_confidence_ratio': stats['high_confidence_windows'] / stats['window_count'],
            'ensemble_ratio': stats['ensemble_windows'] / stats['window_count'],
            'pattern_confirmation_ratio': stats['pattern_confirmations'] / stats['window_count'],
            'quality_score': (
                stats['high_confidence_windows'] * 0.4 +
                stats['ensemble_windows'] * 0.3 +
                stats['pattern_confirmations'] * 0.3
            ) / stats['window_count']
        }
    
    # Sort languages by enhanced scoring that considers quality
    lang_scores = []
    total_windows = len(code_results)
    
    for lang, summary in confidence_summary.items():
        frequency_score = summary['window_count'] / total_windows
        confidence_score = summary['avg_confidence']
        quality_score = summary['quality_score']
        
        # Enhanced combined score with quality weighting
        combined_score = (
            frequency_score * 0.4 +
            confidence_score * 0.4 +
            quality_score * 0.2
        )
        
        lang_scores.append((lang, combined_score, summary))
    
    lang_scores.sort(key=lambda x: x[1], reverse=True)
    
    # MUCH MORE LENIENT DETECTION FOR SHORT DOCUMENTS
    significant_languages = []
    
    if lang_scores:
        # Language relationship analysis
        related_languages = {
            'javascript': ['typescript'],
            'typescript': ['javascript'],
            'c': ['cpp'],
            'cpp': ['c'],
            'java': ['kotlin'],
            'kotlin': ['java'],
            'python': ['ruby'],
            'ruby': ['python'],
        }
        
        # Commonly confused languages that need higher quality thresholds
        commonly_confused = ['kotlin', 'swift', 'scala']
        
        # Web languages that tend to have lower confidence but are important
        web_languages = ['css', 'html', 'javascript', 'typescript']
        
        # VERY lenient multi-language detection for short documents
        for lang, score, summary in lang_scores:
            frequency = summary['window_count'] / total_windows
            
            # Much more lenient base thresholds for short documents
            min_windows = 1  # Always allow at least 1 window
            min_confidence = 0.25  # Raised further to prevent false positives
            min_frequency = 0.01   # Even lower frequency threshold (1%)
            
            # Special handling for web languages
            if lang in web_languages:
                min_confidence = 0.20  # More lenient for web languages
                min_frequency = 0.01
            
            # Adjust thresholds based on language characteristics
            if lang in commonly_confused:
                min_confidence = 0.30  # Raised for confused languages
                min_frequency = 0.02
            
            # Special handling for related languages
            if significant_languages:
                top_lang = significant_languages[0]
                if (top_lang in related_languages and 
                    lang in related_languages.get(top_lang, [])):
                    # Very lenient for related languages
                    min_confidence = 0.22  # Raised from 0.18
                    min_frequency = 0.01
            
            # Quality-based adjustments
            if summary['quality_score'] > 0.2:  # Lowered quality threshold
                min_confidence -= 0.03  # Reward good quality
            
            # Special handling for single-window detections (common in short docs)
            if summary['window_count'] == 1:
                min_frequency = 0.01  # Very low threshold for single windows
                min_confidence = 0.25  # Raised to match base threshold
                # Special case for web languages
                if lang in web_languages:
                    min_confidence = 0.20
                # If there are pattern matches, be even more lenient
                if any('pattern' in reason for reason in summary['decision_reasons']):
                    min_confidence = 0.22  # Raised from 0.20
            
            # Check if language meets criteria
            meets_frequency = frequency >= min_frequency
            meets_confidence = summary['avg_confidence'] >= min_confidence
            meets_windows = summary['window_count'] >= min_windows
            
            # Much more lenient criteria for small presence
            if frequency < 0.25:  # Small presence (increased from 0.20)
                # Require either minimal confidence OR any quality OR decent max confidence
                base_confidence_threshold = 0.20 if lang in web_languages else 0.25
                meets_small_criteria = (
                    summary['avg_confidence'] >= base_confidence_threshold or  # Lower for web languages
                    summary['quality_score'] >= 0.15 or   # Raised from 0.10
                    summary['max_confidence'] >= 0.40 or  # Raised from 0.35
                    any('pattern' in reason for reason in summary['decision_reasons'])  # Pattern support
                )
            else:
                meets_small_criteria = True
            
            if meets_frequency and meets_confidence and meets_windows and meets_small_criteria:
                significant_languages.append(lang)
        
        # Ensure we have at least one language if any code was detected
        if not significant_languages and lang_scores:
            # Add the top language with very minimal quality check
            top_lang, top_score, top_summary = lang_scores[0]
            if top_summary['avg_confidence'] > 0.15:  # Very minimal threshold
                significant_languages = [top_lang]
    
    # More lenient post-processing: Handle JavaScript/TypeScript confusion
    if 'javascript' in significant_languages and 'typescript' in significant_languages:
        js_summary = confidence_summary['javascript']
        ts_summary = confidence_summary['typescript']
        
        # Prefer TypeScript if it has significantly more windows (stronger presence)
        if ts_summary['window_count'] > js_summary['window_count'] * 2:
            significant_languages.remove('javascript')
        # Prefer JavaScript if it has significantly more windows and higher confidence
        elif (js_summary['window_count'] > ts_summary['window_count'] * 2 and
              js_summary['avg_confidence'] > ts_summary['avg_confidence'] + 0.10):
            significant_languages.remove('typescript')
        # If TypeScript has better confidence and similar or more windows, prefer TypeScript
        elif (ts_summary['avg_confidence'] >= js_summary['avg_confidence'] and
              ts_summary['window_count'] >= js_summary['window_count']):
            significant_languages.remove('javascript')
        # Only remove if there's a very significant difference in all metrics
        elif (js_summary['avg_confidence'] > ts_summary['avg_confidence'] + 0.20 and
              js_summary['window_count'] > ts_summary['window_count'] and
              js_summary['quality_score'] > ts_summary['quality_score'] + 0.3):
            significant_languages.remove('typescript')
    
    # Post-processing: Handle C/C++ confusion (more lenient)
    if 'c' in significant_languages and 'cpp' in significant_languages:
        c_summary = confidence_summary['c']
        cpp_summary = confidence_summary['cpp']
        
        # Only remove if there's a very significant difference
        if (cpp_summary['avg_confidence'] > c_summary['avg_confidence'] + 0.20 and
            cpp_summary['quality_score'] > c_summary['quality_score'] + 0.3 and
            cpp_summary['window_count'] > c_summary['window_count'] * 2):
            significant_languages.remove('c')
        elif (c_summary['avg_confidence'] > cpp_summary['avg_confidence'] + 0.20 and
              c_summary['quality_score'] > cpp_summary['quality_score'] + 0.3 and
              c_summary['window_count'] > cpp_summary['window_count'] * 2):
            significant_languages.remove('cpp')
    
    return {
        'languages': significant_languages,
        'confidence_summary': confidence_summary,
        'detailed_results': results,
        'total_windows': len(results),
        'code_windows': len(code_results)
    }

# ─────────  Enhanced Extraction
def extract_languages_with_confidence(text: str, pipe) -> Dict:
    """Extract languages with detailed confidence information"""
    fenced_langs, residual = load(text)
    lines = residual.splitlines()
    wins = windows(lines)

    if not wins:
        return {
            'fenced_languages': fenced_langs,
            'detected_languages': [],
            'all_languages': sorted(fenced_langs) if fenced_langs else [],
            'confidence_summary': {},
            'detailed_results': [],
            'analysis': {
                'total_lines': len(lines),
                'windows_analyzed': 0,
                'code_windows': 0,
                'fenced_blocks': len(fenced_langs),
                'message': 'No content windows to analyze'
            }
        }
    
    # Classify windows with confidence
    classification_results = classify_with_confidence(pipe, wins)
    
    # Aggregate results
    aggregated = aggregate_predictions(classification_results)
    
    # Combine with fenced languages
    all_languages = list(set(fenced_langs + aggregated['languages']))
    
    return {
        'fenced_languages': fenced_langs,
        'detected_languages': aggregated['languages'],
        'all_languages': sorted(all_languages),
        'confidence_summary': aggregated['confidence_summary'],
        'detailed_results': aggregated.get('detailed_results', []),
        'analysis': {
            'total_lines': len(lines),
            'windows_analyzed': len(wins),
            'code_windows': aggregated.get('code_windows', 0),
            'fenced_blocks': len(fenced_langs)
        }
    }

def format_confidence_output(result: Dict, verbose: bool = False) -> str:
    """Format the confidence output for display"""
    output = []
    
    # Summary
    output.append("=== LANGUAGE DETECTION RESULTS ===")
    output.append(f"Detected Languages: {', '.join(result['all_languages']) if result['all_languages'] else 'None'}")
    output.append(f"Analysis: {result['analysis']['windows_analyzed']} windows from {result['analysis']['total_lines']} lines")
    
    if result['fenced_languages']:
        output.append(f"Fenced Code Blocks: {', '.join(result['fenced_languages'])}")
    
    # Confidence details
    if result['confidence_summary']:
        output.append("\n=== CONFIDENCE DETAILS ===")
        for lang, summary in sorted(result['confidence_summary'].items(), 
                                   key=lambda x: x[1]['avg_confidence'], reverse=True):
            output.append(f"{lang}:")
            output.append(f"  Average Confidence: {summary['avg_confidence']:.3f}")
            output.append(f"  Windows Detected: {summary['window_count']}")
            if 'max_confidence' in summary:
                output.append(f"  Confidence Range: {summary['min_confidence']:.3f} - {summary['max_confidence']:.3f}")
    
    # Verbose details
    if verbose and result['detailed_results']:
        output.append("\n=== DETAILED WINDOW ANALYSIS ===")
        for i, detail in enumerate(result['detailed_results'][:10]):  # Limit to first 10
            output.append(f"Window {i+1} (lines {detail['lines'][0]}-{detail['lines'][1]}):")
            output.append(f"  Language: {detail['predicted_language']} (confidence: {detail['confidence']:.3f})")
            output.append(f"  Reason: {detail['decision_reason']}")
            if detail['pattern_matches']:
                patterns = ', '.join([f"{lang}({score:.2f})" for lang, score in detail['pattern_matches'][:3]])
                output.append(f"  Pattern Matches: {patterns}")
            output.append(f"  Preview: {detail['text_preview']}")
            output.append("")
    
    return '\n'.join(output)

def analyze_code_structure(text: str) -> Dict[str, float]:
    """Analyze structural characteristics of code for language identification"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return {}
    
    structure_scores = {}
    
    # Indentation analysis
    indents = [len(l) - len(l.lstrip()) for l in text.splitlines() if l.strip()]
    if indents:
        # Python/Ruby tend to have consistent 4-space indentation
        if np.std(indents) < 2 and np.mean(indents) > 0:
            structure_scores['python_indent'] = 0.8
            structure_scores['ruby_indent'] = 0.6
        
        # C-style languages often use 2-space or mixed indentation
        elif np.std(indents) > 2:
            structure_scores['c_style_indent'] = 0.7
    
    # Bracket analysis
    open_braces = text.count('{')
    close_braces = text.count('}')
    if open_braces > 0 and abs(open_braces - close_braces) <= 1:
        structure_scores['c_style_braces'] = min(1.0, open_braces / max(1, len(lines)) * 3)
    
    # Semicolon density (C-style languages)
    semicolons = text.count(';')
    if semicolons > 0:
        structure_scores['c_style_semicolons'] = min(1.0, semicolons / max(1, len(lines)) * 2)
    
    # Colon analysis (Python, Ruby)
    colons_at_eol = len(re.findall(r':\s*$', text, re.MULTILINE))
    if colons_at_eol > 0:
        structure_scores['python_colons'] = min(1.0, colons_at_eol / max(1, len(lines)) * 4)
    
    # Function definition patterns
    def_count = len(re.findall(r'\bdef\s+\w+', text))
    func_count = len(re.findall(r'\bfunction\s+\w+', text))
    fn_count = len(re.findall(r'\bfn\s+\w+', text))
    
    if def_count > 0:
        structure_scores['python_def'] = min(1.0, def_count / max(1, len(lines)) * 8)
        structure_scores['ruby_def'] = min(0.8, def_count / max(1, len(lines)) * 6)
    
    if func_count > 0:
        structure_scores['js_function'] = min(1.0, func_count / max(1, len(lines)) * 8)
    
    if fn_count > 0:
        structure_scores['rust_fn'] = min(1.0, fn_count / max(1, len(lines)) * 8)
        structure_scores['go_fn'] = min(0.8, fn_count / max(1, len(lines)) * 6)
    
    return structure_scores

def get_contextual_confidence_boost(text: str, predicted_lang: str, base_confidence: float) -> float:
    """Apply contextual analysis to boost confidence for correct predictions"""
    structure = analyze_code_structure(text)
    boost = 0.0
    
    # Language-specific structural confirmations
    if predicted_lang == 'python':
        boost += structure.get('python_indent', 0) * 0.15
        boost += structure.get('python_colons', 0) * 0.2
        boost += structure.get('python_def', 0) * 0.15
        # Penalize if C-style features are strong
        boost -= structure.get('c_style_braces', 0) * 0.1
        boost -= structure.get('c_style_semicolons', 0) * 0.1
    
    elif predicted_lang in ['javascript', 'typescript', 'java', 'c', 'cpp', 'csharp']:
        boost += structure.get('c_style_braces', 0) * 0.15
        boost += structure.get('c_style_semicolons', 0) * 0.1
        boost += structure.get('c_style_indent', 0) * 0.05
        # Penalize if Python-style features are strong
        boost -= structure.get('python_colons', 0) * 0.15
        
        if predicted_lang == 'javascript':
            boost += structure.get('js_function', 0) * 0.2
    
    elif predicted_lang == 'rust':
        boost += structure.get('rust_fn', 0) * 0.2
        boost += structure.get('c_style_braces', 0) * 0.1
        # Rust has less semicolons than other C-style languages
        boost -= structure.get('c_style_semicolons', 0) * 0.05
    
    elif predicted_lang == 'go':
        boost += structure.get('go_fn', 0) * 0.15
        boost += structure.get('c_style_braces', 0) * 0.1
    
    elif predicted_lang == 'ruby':
        boost += structure.get('ruby_indent', 0) * 0.1
        boost += structure.get('ruby_def', 0) * 0.15
        # Ruby has fewer braces than C-style languages
        boost -= structure.get('c_style_braces', 0) * 0.1
    
    return min(0.3, max(-0.2, boost))  # Cap boost/penalty

def get_ensemble_confidence(model_confidence: float, pattern_score: float, 
                          structural_boost: float, predicted_lang: str) -> Tuple[float, str]:
    """Combine multiple confidence sources for final score"""
    
    # Base weights for different confidence sources
    model_weight = 0.6
    pattern_weight = 0.3
    structure_weight = 0.1
    
    # Adjust weights based on confidence levels
    if model_confidence > 0.8:
        model_weight = 0.7  # Trust high-confidence model more
        pattern_weight = 0.2
        structure_weight = 0.1
    elif model_confidence < 0.4:
        model_weight = 0.4  # Trust low-confidence model less
        pattern_weight = 0.4
        structure_weight = 0.2
    
    # Calculate ensemble score
    ensemble_score = (
        model_confidence * model_weight +
        pattern_score * pattern_weight +
        (0.5 + structural_boost) * structure_weight
    )
    
    # Determine confidence level
    if ensemble_score > 0.85:
        confidence_level = "very_high"
    elif ensemble_score > 0.7:
        confidence_level = "high"
    elif ensemble_score > 0.5:
        confidence_level = "medium"
    elif ensemble_score > 0.3:
        confidence_level = "low"
    else:
        confidence_level = "very_low"
    
    return min(0.99, max(0.1, ensemble_score)), confidence_level