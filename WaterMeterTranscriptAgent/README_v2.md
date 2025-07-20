# 💧 WaterMeterTranscripter - Water Meter Reading Extractor (with ReAct Reasoning)

**WaterMeterTranscripter** is a Python tool that extracts and validates water meter readings from natural language inputs using regex and a simplified **ReAct reasoning framework with LangGraph Tools**. It identifies unit-reading pairs, checks for duplicates or conflicting values, and outputs clean, structured JSON data.

---

## Tools Initialized
LangChain provides support for tools powered by Pydantic models, allowing developers to define structured input schemas for tools that agents can use. This helps agents understand what kind of input is required and ensures type safety and clarity during execution. The following tools are initialized in the code:

      1. RegexExtractionTool
      2. ValidationTool
      3. RemoveDuplicatesTool
      4. CreateJSONTool


## ReAct Framework with LangGraph
This code follows the follow the Thought --> Action --> Observation --> Final Output paradigm of ReAct. Specificallly, the process of the code is done by using two LangGraph nodes:

        [User Input] 
            ↓
        [Reasoner Node (THOUGHT)] 💭 --(decides to call tool)--> [Tool Node (ACTION)] 🔧
            ↑                                               ↓
            └-------------------<--- returns result (OBSERVATION) --------┘

Parts of the LangGraph Workflow:
    1. Reasoner Node 
      - Decides what tools to call, does the THOUGHT process
    2. Tool Node
      - Contains all the tools in one node to be accessed by reasoner node when needed, does the ACTION and returns OBSERVATION


---

## Sample Test Cases 

### Sample Input 1:
```
Unit 12A reads 321 cubic meter and Unit 2B reads 67.89 m3  
```

### Output 1:
```
[
  {
    "unit": "12A",
    "reading": 321
  },
  {
    "unit": "2B",
    "reading": 67
  }
]
```

### Sample Input 2:
```
Unit 2B reads 67.89 cubic meter and Unit 2B reads 67.89 cubic meter
```
---

### Output 2:
```
[  {  
    "unit": "2B",  
    "reading": 67.89  
  },  
]  
```


