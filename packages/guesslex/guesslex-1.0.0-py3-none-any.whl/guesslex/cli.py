#!/usr/bin/env python3
"""
Command-line interface for guesslex.
"""

import argparse
import json
import sys
from pathlib import Path

from .core import (
    extract_languages_with_confidence,
    format_confidence_output,
    load_model,
    CONFIDENCE_TH,
    PLAIN_TH
)

def main():
    """Main CLI entry point."""
    ap = argparse.ArgumentParser(description="Guesslex - Enhanced programming language detector with confidence scoring.")
    ap.add_argument("-m", "--model", help="Model file path (default: bundled model)")
    ap.add_argument("-i", "--input", help="Input file (default: stdin)")
    ap.add_argument("-o", "--out", help="Write JSON results to file")
    ap.add_argument("-v", "--verbose", action="store_true", help="Show detailed analysis")
    ap.add_argument("--json", action="store_true", help="Output clean JSON format with languages, confidences, and window counts")
    ap.add_argument("--confidence-threshold", type=float, default=CONFIDENCE_TH, help="Confidence threshold")
    ap.add_argument("--plain-threshold", type=float, default=PLAIN_TH, help="Plain text threshold")
    args = ap.parse_args()

    # Read input
    if args.input:
        txt = Path(args.input).read_text()
    else:
        txt = sys.stdin.read()
    
    # Load model and analyze
    pipe = load_model(args.model)
    result = extract_languages_with_confidence(txt, pipe)

    # Output results
    if args.json:
        # Clean JSON output format
        json_output = {
            "detected_languages": [],
            "analysis": {
                "total_windows": result['analysis']['windows_analyzed'],
                "total_lines": result['analysis']['total_lines'],
                "code_windows": result['analysis']['code_windows']
            }
        }
        
        # Add language details
        for lang in result['detected_languages']:
            if lang in result['confidence_summary']:
                summary = result['confidence_summary'][lang]
                json_output["detected_languages"].append({
                    "language": lang,
                    "confidence": round(summary['avg_confidence'], 3),
                    "window_count": summary['window_count'],
                    "confidence_range": {
                        "min": round(summary['min_confidence'], 3),
                        "max": round(summary['max_confidence'], 3)
                    }
                })
            else:
                # Handle case where language might not have detailed summary
                json_output["detected_languages"].append({
                    "language": lang,
                    "confidence": 1.0,
                    "window_count": 1,
                    "confidence_range": {"min": 1.0, "max": 1.0}
                })
        
        print(json.dumps(json_output, indent=2))
        
    elif args.out:
        # Save detailed JSON
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"Detailed results saved to {args.out}")
    
    else:
        # Print formatted output
        print(format_confidence_output(result, args.verbose))
        
        # Also print simple language list for compatibility
        print(f"\nSimple output: {json.dumps(result['all_languages'])}")

if __name__ == "__main__":
    main() 