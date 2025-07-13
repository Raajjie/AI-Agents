# 🏷️ TagSuggestion Agent — Context-Aware Tagging with ReAct Reasoning

**TagSuggestionAgent** is a Python-based intelligent tagging system that uses a rule-based engine combined with a **ReAct-style reasoning process** to suggest meaningful tags for technical issue descriptions. It works particularly well for industrial environments where reports describe issues like "rusted valve near compressor 2."

---

## ReAct Framework
This code follows the follow the Thought --> Action --> Observation --> Final Output paradigm of ReAct. Specificallly, the step-by-step process of the code is as follows:  

STEP 1: 💭 Thought: I need to analyze the input description to understand what tags may apply.  
STEP 2: 🔍 Action: Extract all words (keywords) from the natural language input.  
STEP 3: 👁️ Observation: Keywords successfully extracted.  
STEP 4: 💭 Thought: I should now compare the input against known tag rules.  
STEP 5: 🔍 Action: Iterate through each tag rule and count keyword matches and regex pattern matches.  
STEP 6: 👁️ Observation: For each tag, report number of matches and compute a confidence score.  
STEP 7: 💭 Thought: I will filter out tags with low confidence.  
STEP 8: 🔍 Action: Keep only tags above the confidence threshold.  
STEP 9: 👁️ Observation: Valid tags with sufficient confidence collected.  
STEP 10: 💭 Thought: I should now prioritize the best suggestions.  
STEP 11: 🔍 Action: Sort valid tags by confidence and priority.  
STEP 12: 👁️ Observation: Top tags selected.  
STEP 13: ✅ Final Output: I now return the final tags and reasoning.  

---

## Example Input 

### Sample Input 1:
Rusted valve found near compressor 2

### Sample Input 2:
Loud grinding noise from pump station

---

## Expected Output

### Output 1:

SUGGESTED TAGS: ['Corrosion', 'Compressor', 'Compressor Zone', 'Valve']  
KEYWORDS FOUND: ['rusted', 'valve', 'found', 'near', 'compressor', '2']

### Output 2:

SUGGESTED TAGS: ['Noise', 'Compressor', 'Pump Station']  
KEYWORDS FOUND: ['loud', 'grinding', 'noise', 'from', 'pump', 'station']  
