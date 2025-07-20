# 💧 WaterMeterTranscripter - Water Meter Reading Extractor (with ReAct Reasoning)

**WaterMeterTranscripter** is a Python tool that extracts and validates water meter readings from natural language inputs using regex and a simplified **ReAct reasoning framework**. It identifies unit-reading pairs, checks for duplicates or conflicting values, and outputs clean, structured JSON data.

---

## ReAct Framework
This code follows the follow the Thought --> Action --> Observation --> Final Output paradigm of ReAct. Specificallly, the step-by-step process of the code is as follows:  

STEP 1: 💭 Thought: What is inside natural language input?  
STEP 2: 🔍 Action: Extract readings using regex  
STEP 3: 👁️ Observation: Report found unit and reading matches  
STEP 4: 💭 Thought: I need to validate of extracted data  
STEP 5: 🔍 Action: Check for duplicates  
STEP 6: 👁️ Observation: Report if any duplicates are found  
STEP 7: 🔍 Action: Check for conflicting readings (same unit, different values)  
STEP 8: 👁️ Observation: Report any conflicts or confirm all is good  
STEP 8: 💭 Thought: I need to prepare final JSON structure  
STEP 9: 🔍 Action: Transform matches into dictionary entries  
STEP 9: 👁️ Observation: Report and confirm final structure  
STEP 10: 💭 Thought: I got the Final Output  


---

## Example Input 

### Sample Input 1:
```
Unit 19A reads 30 cubic meter, 19B is 5 cubic meter  
```
### Sample Input 2:
```
10A reads 25 cubic meter, Unit 10B is 15 cubic meter
```
---

## Expected Output

### Output 1:
```
[  {  
    "unit": "19A",  
    "reading": 30  
  },  
  {  
    "unit": "19B",  
    "reading": 5  
  } ] 
```

### Output 2:
```
[  {  
    "unit": "10A",  
    "reading": 25  
  },  
  {  
    "unit": "10B",  
    "reading": 15  
  } ]  
```

