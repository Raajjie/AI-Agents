import re
import json
from typing import Dict, List, Any, Tuple
from collections import defaultdict

class UnitReadingAgent:
    def __init__(self):
        # Pattern to match unit readings like "Unit 19A reads 30 cubic meter" or "19B is 5 cubic meter"
        self.pattern = r'(?:Unit\s+)?(\d+[A-Z])\s+(?:reads|is|reading)\s+(\d+(?:\.\d+)?)\s+cubic\s+meter'
        self.reasoning_steps = []
    
    def _log_step(self, step_type: str, content: str):
        """Log reasoning steps for ReAct pattern"""
        step = f"{step_type}: {content}"
        self.reasoning_steps.append(step)
        print(step)
 
    def check_for_duplicates(self, matches: List[tuple]) -> bool:
        """
        Check for duplicate unit readings in the matches
        
        Args:
            matches (List[tuple]): List of tuples containing unit and reading pairs
            
        Returns:
            bool: True if duplicates found, False otherwise
        """
        seen_units = set()
        for unit, reading in matches:
            if unit in seen_units:
                return True
            seen_units.add(unit)
        return False

    def check_for_conflicting_values(self, matches: List[tuple]) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Check for units with conflicting reading values
        
        Args:
            matches (List[tuple]): List of tuples containing unit and reading pairs
            
        Returns:
            Tuple[bool, Dict]: (has_conflicts, conflicts_dict)
                - has_conflicts: True if conflicts found
                - conflicts_dict: Dictionary mapping unit to list of conflicting values
        """
        unit_readings = defaultdict(list)
        
        # Group readings by unit
        for unit, reading in matches:
            unit_readings[unit].append(reading)
        
        # Find units with multiple different readings
        conflicts = {}
        for unit, readings in unit_readings.items():
            unique_readings = list(set(readings))
            if len(unique_readings) > 1:
                conflicts[unit] = unique_readings
        
        return len(conflicts) > 0, conflicts

    def validate_matches(self, matches: List[tuple]) -> None:
        """
        Comprehensive validation of extracted matches
        
        Args:
            matches (List[tuple]): List of tuples containing unit and reading pairs
            
        Raises:
            ValueError: If validation fails
        """
        if not matches:
            raise ValueError("  👁️  Observation", f"Found error/s in regex matching")
        else:
            self._log_step("    👁️  Observation", f"Found no error/s in regex matching")
        
        # Check for exact duplicates
        self._log_step("    🔍 Action", "Checking for exact duplicate entries")
        if self.check_for_duplicates(matches):
            self._log_step("    👁️  Observation", "Found exact duplicate unit entries")
            # Remove exact duplicates
            matches = list(set(matches))
            self._log_step("    🔍 Action", f"Removed duplicates, now have {len(matches)} unique entries")
            self._log_step("    👁️  Observation", "No exact duplicate entries found")
        else:
            self._log_step("    👁️  Observation", "No exact duplicate entries found")

        # Check for conflicting values
        self._log_step("    🔍 Action", "Checking for units with conflicting reading values")
        has_conflicts, conflicts = self.check_for_conflicting_values(matches)
        
        if has_conflicts:
            self._log_step("    👁️  Observation", "Found units with conflicting reading values")
            conflict_details = []
            for unit, values in conflicts.items():
                conflict_detail = f"Unit {unit}: {', '.join(values)} cubic meters"
                conflict_details.append(conflict_detail)
                self._log_step("    💭 Thought", f"The conflicting values are {conflict_detail}" )
            
            error_msg = f"Conflicting readings found for the same unit(s): {'; '.join(conflict_details)}. Please provide consistent readings for each unit."
            raise ValueError(error_msg)
        else:
            self._log_step("    👁️  Observation", "No conflicting values found")

    def parse_input(self, input_text: str) -> List[Dict[str, Any]]:
        """
        Parse the input text and extract unit readings using ReAct pattern
        
        Args:
            input_text (str): Natural language input containing unit readings
            
        Returns:
            List: Simple list of unit readings
        """
        # Clear previous reasoning steps
        self.reasoning_steps = []
        
        # THOUGHT: Analyze what information is provided
        self._log_step("💭 Thought", f"What information is provided in: '{input_text}'")
        
        # ACTION: Extract unit and reading pairs
        self._log_step("🔍 Action", "Extract unit and reading pairs using regex pattern")
        matches = re.findall(self.pattern, input_text, re.IGNORECASE)
        
        # OBSERVATION: Report what was found
        self._log_step("👁️  Observation", f"Found {len(matches)} unit-reading pairs: {matches}")
        
        # THOUGHT: Plan validation strategy
        self._log_step("💭 Thought", "I need to validate extracted matches to ensure data consistency")
        
        # ACTION: Comprehensive validation
        try:
            self._log_step("    🔍 Action", "Checking for errors and inconsistency")
            self.validate_matches(matches)
        except ValueError as e:
            self._log_step("    🔍 Action", "Checking for errors and inconsistency")
            raise
        
        # THOUGHT: Plan how to structure the data
        self._log_step("💭 Thought", "I need to convert each match into the required JSON format")
        
        # ACTION: Process each match
        result = []
        # Remove duplicates while preserving order
        seen_units = set()
        unique_matches = []
        for unit, reading in matches:
            if unit not in seen_units:
                unique_matches.append((unit, reading))
                seen_units.add(unit)
        
        for i, (unit, reading) in enumerate(unique_matches):
            # OBSERVATION: Detail each unit processed
            self._log_step("    🔍 Action", f"Processing unit {unit} with reading {reading}")
            
            # ACTION: Create JSON object for this unit
            unit_data = {
                "unit": unit,
                "reading": int(float(reading))
            }
            result.append(unit_data)
            
            self._log_step("    👁️  Observation", f"The unit and reading pair is in JSON file {unit}: {unit_data}")
        

        return result
    
    def convert_to_json(self, input_text: str) -> str:
        """
        Convert input text to JSON string with ReAct reasoning
        
        Args:
            input_text (str): Natural language input
            
        Returns:
            str: JSON formatted string
        """
        print("\n" + "="*50)
        print("REASONING PROCESS (ReAct Pattern)")
        print("="*50)
        
        parsed_data = self.parse_input(input_text)
        
        print("\n" + "="*50)
        print("FINAL RESULT")
        print("="*50)
        
        json_string = json.dumps(parsed_data, indent=2)
    
        with open("output.json", "w") as f:
            f.write(json_string)
        
        return json_string
    
    def get_reasoning_steps(self) -> List[str]:
        """
        Get all reasoning steps from the last parsing operation
        
        Returns:
            List[str]: List of reasoning steps
        """
        return self.reasoning_steps
    
    def get_summary(self, input_text: str) -> Dict[str, Any]:
        """
        Get a summary of the parsed data
        
        Args:
            input_text (str): Natural language input
            
        Returns:
            Dict: Summary information
        """
        parsed_data = self.parse_input(input_text)
        
        total_reading = sum(item["reading"] for item in parsed_data)
        
        return {
            "total_units": len(parsed_data),
            "total_reading": total_reading,
            "average_reading": total_reading / len(parsed_data) if parsed_data else 0,
            "unit_list": [item["unit"] for item in parsed_data]
        }

# Example usage with interactive input
def main():
    agent = UnitReadingAgent()
    
    print("=" * 60)
    print("UNIT READING PARSER AGENT")
    print("=" * 60)
    print("Enter unit readings in natural language.")
    print("Examples:")
    print("- Unit 19A reads 30 cubic meter, 19B is 5 cubic meter")
    print("- 10A reads 25 cubic meter, Unit 10B is 15 cubic meter")
    print("- Unit 5C reads 100 cubic meter")
    print("=" * 60)
    
    while True:
        # Get user input
        user_input = input("\nEnter unit readings: ").strip()
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        # Skip empty inputs
        if not user_input:
            print("Please enter some unit readings.")
            continue
        
        try:
            # Process the input
            print(f"\nProcessing: {user_input}")
            json_output = agent.convert_to_json(user_input)
            print(json_output)
            

        except Exception as e:
            print(f"    👁️  Observation: Error processing input:")
            print(f"{e}")
            print("\nPlease check your input format and ensure consistent readings.")

if __name__ == "__main__":
    main()