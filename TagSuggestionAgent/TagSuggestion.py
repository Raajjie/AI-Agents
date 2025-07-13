import re
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum

class ReasoningStep(Enum):
    THOUGHT = "💭 THOUGHT"
    ACTION = "🔍 ACTION"
    OBSERVATION = "👁️  OBSERVATION"
    CONCLUSION = "✅ CONCLUSION"

@dataclass
class TagRule:
    """Represents a rule for tag suggestion"""
    tag: str
    keywords: List[str]
    patterns: List[str]
    priority: int = 1
    description: str = ""

class TagSuggestionAgent:
    def __init__(self):
        self.tag_library = self._initialize_tag_library()
        self.reasoning_log = []
        
    def _initialize_tag_library(self) -> Dict[str, TagRule]:
        """Initialize the tag library with rules and patterns"""
        rules = [
            # Equipment Tags
            TagRule("Valve", ["valve", "gate", "ball valve", "check valve", "relief valve"], 
                   [r"\bvalve\b", r"\bgate\b", r"\bball\s+valve\b"], 1, "Valve-related equipment"),
            TagRule("Compressor", ["compressor", "pump", "blower"], 
                   [r"\bcompressor\b", r"\bpump\b", r"\bblower\b"], 1, "Compression equipment"),
            TagRule("Pipeline", ["pipe", "pipeline", "piping", "line"], 
                   [r"\bpipe\b", r"\bpipeline\b", r"\bpiping\b", r"\bline\b"], 1, "Pipeline infrastructure"),
            TagRule("Tank", ["tank", "vessel", "container", "storage"], 
                   [r"\btank\b", r"\bvessel\b", r"\bcontainer\b", r"\bstorage\b"], 1, "Storage equipment"),
            TagRule("Sensor", ["sensor", "gauge", "meter", "detector"], 
                   [r"\bsensor\b", r"\bgauge\b", r"\bmeter\b", r"\bdetector\b"], 1, "Monitoring equipment"),
            
            # Condition Tags
            TagRule("Corrosion", ["rust", "rusted", "corrosion", "corroded", "oxidation"], 
                   [r"\brust\w*\b", r"\bcorrod\w*\b", r"\boxid\w*\b"], 2, "Corrosion-related issues"),
            TagRule("Leak", ["leak", "leaking", "drip", "seepage", "spill"], 
                   [r"\bleak\w*\b", r"\bdrip\w*\b", r"\bseep\w*\b", r"\bspill\w*\b"], 2, "Leakage issues"),
            TagRule("Vibration", ["vibration", "vibrating", "shake", "shaking", "tremor"], 
                   [r"\bvibrat\w*\b", r"\bshak\w*\b", r"\btremor\b"], 2, "Vibration issues"),
            TagRule("Noise", ["noise", "loud", "grinding", "squealing", "rattling"], 
                   [r"\bnoise\b", r"\bloud\b", r"\bgrind\w*\b", r"\bsqueal\w*\b", r"\brattl\w*\b"], 2, "Noise issues"),
            TagRule("Temperature", ["hot", "cold", "overheating", "temperature", "thermal"], 
                   [r"\bhot\b", r"\bcold\b", r"\boverheat\w*\b", r"\btemperature\b", r"\bthermal\b"], 2, "Temperature issues"),
            TagRule("Pressure", ["pressure", "high pressure", "low pressure", "psi"], 
                   [r"\bpressure\b", r"\bpsi\b", r"\bbar\b"], 2, "Pressure-related issues"),
            TagRule("Damage", ["damage", "damaged", "broken", "cracked", "fractured"], 
                   [r"\bdamag\w*\b", r"\bbroken\b", r"\bcrack\w*\b", r"\bfractur\w*\b"], 2, "Physical damage"),
            
            # Location Tags
            TagRule("Compressor Zone", ["compressor 1", "compressor 2", "compressor area", "comp zone"], 
                   [r"\bcompressor\s+\d+\b", r"\bcomp\s+zone\b", r"\bcompressor\s+area\b"], 1, "Compressor area"),
            TagRule("Pump Station", ["pump station", "pump house", "pump room"], 
                   [r"\bpump\s+station\b", r"\bpump\s+house\b", r"\bpump\s+room\b"], 1, "Pump station area"),
            TagRule("Control Room", ["control room", "control panel", "operator station"], 
                   [r"\bcontrol\s+room\b", r"\bcontrol\s+panel\b", r"\boperator\s+station\b"], 1, "Control room area"),
            TagRule("Field", ["field", "outdoor", "outside", "external"], 
                   [r"\bfield\b", r"\boutdoor\b", r"\boutside\b", r"\bexternal\b"], 1, "Field location"),
            
            # Severity Tags
            TagRule("Critical", ["critical", "urgent", "immediate", "emergency", "severe"], 
                   [r"\bcritical\b", r"\burgent\b", r"\bimmediate\b", r"\bemergency\b", r"\bsevere\b"], 3, "Critical severity"),
            TagRule("High Priority", ["high", "priority", "important", "significant"], 
                   [r"\bhigh\s+priority\b", r"\bimportant\b", r"\bsignificant\b"], 3, "High priority"),
            TagRule("Routine", ["routine", "normal", "regular", "scheduled"], 
                   [r"\broutine\b", r"\bnormal\b", r"\bregular\b", r"\bscheduled\b"], 3, "Routine maintenance"),
        ]
        
        return {rule.tag: rule for rule in rules}
    
    def _log_reasoning(self, step: ReasoningStep, message: str):
        """Log a reasoning step"""
        self.reasoning_log.append(f"{step.value}: {message}")
        print(f"{step.value}: {message}")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from text"""
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _match_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """Match regex patterns against text"""
        matches = []
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(pattern)
        return matches
    
    def _calculate_confidence(self, keyword_matches: int, pattern_matches: int, total_keywords: int) -> float:
        """Calculate confidence score for a tag suggestion"""
        if total_keywords == 0:
            return 0.0
        
        keyword_score = keyword_matches / total_keywords
        pattern_bonus = min(pattern_matches * 0.2, 0.5)  # Max 50% bonus for patterns
        
        return min(keyword_score + pattern_bonus, 1.0)
    
    def suggest_tags(self, description: str) -> Dict[str, any]:
        """Main method to suggest tags for a given description"""
        self.reasoning_log = []
        
        self._log_reasoning(ReasoningStep.THOUGHT, 
                          f"Analyzing description: '{description}'")
        
        # Extract keywords
        keywords = self._extract_keywords(description)
        self._log_reasoning(ReasoningStep.ACTION, 
                          f"Extracted keywords: {keywords}")
        
        # Find matching tags
        suggested_tags = []
        tag_details = {}
        
        for tag_name, rule in self.tag_library.items():
            # Check keyword matches
            keyword_matches = sum(1 for kw in rule.keywords if kw in description.lower())
            pattern_matches = len(self._match_patterns(description, rule.patterns))
            
            if keyword_matches > 0 or pattern_matches > 0:
                confidence = self._calculate_confidence(keyword_matches, pattern_matches, len(rule.keywords))
                
                self._log_reasoning(ReasoningStep.OBSERVATION, 
                                  f"Tag '{tag_name}': {keyword_matches} keyword matches, "
                                  f"{pattern_matches} pattern matches, confidence: {confidence:.2f}")
                
                if confidence > 0.1:  # Minimum confidence threshold
                    suggested_tags.append({
                        'tag': tag_name,
                        'confidence': confidence,
                        'priority': rule.priority,
                        'matched_keywords': [kw for kw in rule.keywords if kw in description.lower()],
                        'matched_patterns': pattern_matches,
                        'description': rule.description
                    })
        
        # Sort by confidence and priority
        suggested_tags.sort(key=lambda x: (x['confidence'], x['priority']), reverse=True)
        
        # Select top tags
        final_tags = [tag['tag'] for tag in suggested_tags[:5]]  # Top 5 tags
        
        self._log_reasoning(ReasoningStep.CONCLUSION, 
                          f"Final suggested tags: {final_tags}")
        
        return {
            'tags': final_tags,
            'detailed_suggestions': suggested_tags,
            'reasoning_log': self.reasoning_log,
            'keywords_found': keywords
        }
    
    def explain_suggestion(self, tag_name: str, description: str) -> str:
        """Explain why a specific tag was suggested"""
        if tag_name not in self.tag_library:
            return f"Tag '{tag_name}' not found in library"
        
        rule = self.tag_library[tag_name]
        matched_keywords = [kw for kw in rule.keywords if kw in description.lower()]
        matched_patterns = self._match_patterns(description, rule.patterns)
        
        explanation = f"Tag '{tag_name}' was suggested because:\n"
        explanation += f"- Description: {rule.description}\n"
        if matched_keywords:
            explanation += f"- Matched keywords: {matched_keywords}\n"
        if matched_patterns:
            explanation += f"- Matched patterns: {len(matched_patterns)} pattern(s)\n"
        
        return explanation

# Example usage and testing
def main():
    agent = TagSuggestionAgent()


    print("=" * 60)
    print("TAG SUGGESTING AGENT")
    print("=" * 60)
    print("Enter natural language description.")
    print("Examples:")
    print("- Rusted valve found near compressor 2")
    print("- Loud grinding noise from pump station")
    print("- Scheduled maintenance on storage tank")
    print("\nType 'quit' to exit")
    print("=" * 60)

    while True:
        # Get user input
        description = input("Enter description (or 'quit' to exit): ")

        if description.lower() in ['quit', 'exit', 'q']:
            print("Exiting the agent. Goodbye!")
            break
        

        # Skip empty descriptions
        if not description.strip():
            print("No description provided. Please enter a valid description.")
            continue

        try:
            # Process the input description
            print(f"\nProcessing description: '{description}'")
            result = agent.suggest_tags(description)
            
            print(f"\nSUGGESTED TAGS: {result['tags']}")
            print(f"KEYWORDS FOUND: {result['keywords_found']}")
            
            print("\nDETAILED ANALYSIS:")
            for suggestion in result['detailed_suggestions']:
                print(f"  • {suggestion['tag']}: {suggestion['confidence']:.2f} confidence "
                      f"(Priority: {suggestion['priority']}, Keywords: {suggestion['matched_keywords']})")
            
            print("\nREASONING LOG:")
            for log in result['reasoning_log']:
                print(f"  - {log}")
        
        except Exception as e:
            print(f"Error processing description: {e}")
            continue


if __name__ == "__main__": 
    main()