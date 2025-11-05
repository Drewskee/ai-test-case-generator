"""
AI-Powered Test Case Generator

This module generates test cases from user stories using OpenAI's API.
A user story describes what a user wants to do (e.g., "As a user, I want to login...")
and this tool creates structured test cases to verify that feature works.
"""

import openai
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

# Set up logging to track what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """
    Data structure for a single test case.

    A dataclass is a convenient way to store related data together.
    Think of it like a form with fields that must be filled out.
    """
    title: str              # Brief name for the test
    description: str        # What this test verifies
    steps: List[str]        # Numbered steps to execute
    expected_result: str    # What should happen if feature works
    test_type: str          # Type: unit, integration, or e2e (end-to-end)
    priority: str           # Priority: high, medium, or low
    preconditions: List[str]  # What must be set up before testing


class AITestCaseGenerator:
    """
    Main class that handles test case generation.

    This class is like a specialized worker that knows how to:
    1. Take a user story as input
    2. Send it to OpenAI's AI
    3. Get back structured test cases
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the generator with API credentials.

        Args:
            api_key: Your OpenAI API key (keep this secret!)
            model: Which AI model to use (default is gpt-3.5-turbo)
        """
        if not api_key:
            raise ValueError("API key is required. Get one from https://platform.openai.com/api-keys")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Initialized AI Test Case Generator with model: {model}")

    def generate_test_cases(
        self,
        user_story: str,
        num_cases: int = 5,
        focus_areas: Optional[List[str]] = None
    ) -> List[TestCase]:
        """
        Generate test cases from a user story.

        This is the main method that does the work:
        1. Takes your user story description
        2. Creates a detailed prompt for the AI
        3. Sends it to OpenAI
        4. Parses the response into structured test cases

        Args:
            user_story: Description of what the user wants to do
            num_cases: How many test cases to generate (default: 5)
            focus_areas: Specific areas to focus on (e.g., ["security", "performance"])

        Returns:
            List of TestCase objects with all test details
        """
        logger.info(f"Generating {num_cases} test cases for user story...")

        # Build the prompt (instructions) for the AI
        prompt = self._build_prompt(user_story, num_cases, focus_areas)

        try:
            # Call OpenAI's API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert QA engineer and test case designer. "
                                   "Generate comprehensive, practical test cases that cover "
                                   "positive scenarios, negative scenarios, edge cases, and security."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},  # Ensure JSON response
                temperature=0.7  # Controls creativity (0-1, higher = more creative)
            )

            # Extract and parse the response
            content = response.choices[0].message.content
            logger.info("Successfully received response from OpenAI")

            # Convert JSON string to Python objects
            test_data = json.loads(content)

            # Convert dictionary data to TestCase objects
            test_cases = self._parse_test_cases(test_data)

            logger.info(f"Generated {len(test_cases)} test cases successfully")
            return test_cases

        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"Failed to generate test cases: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise Exception(f"Invalid response format from AI: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def _build_prompt(
        self,
        user_story: str,
        num_cases: int,
        focus_areas: Optional[List[str]]
    ) -> str:
        """
        Build the prompt (instructions) to send to the AI.

        A good prompt is like giving clear instructions to a helper.
        The clearer and more detailed, the better the results.
        """
        focus_text = ""
        if focus_areas:
            focus_text = f"\nPay special attention to: {', '.join(focus_areas)}"

        prompt = f"""
Given this user story:
"{user_story}"

Generate exactly {num_cases} comprehensive test cases in JSON format.{focus_text}

Include:
- Positive test cases (happy path - when everything goes right)
- Negative test cases (error scenarios - what if user does something wrong?)
- Edge cases (boundary conditions - extreme or unusual situations)
- Security considerations (what could go wrong security-wise?)

Return ONLY valid JSON in this exact format:
{{
  "test_cases": [
    {{
      "title": "Brief descriptive title",
      "description": "What this test verifies",
      "steps": ["Step 1", "Step 2", "Step 3"],
      "expected_result": "What should happen",
      "test_type": "unit|integration|e2e",
      "priority": "high|medium|low",
      "preconditions": ["What must be set up first"]
    }}
  ]
}}

Ensure test cases are:
- Specific and actionable
- Include actual test data examples
- Cover different scenarios
- Practical to implement
"""
        return prompt

    def _parse_test_cases(self, test_data: Dict) -> List[TestCase]:
        """
        Convert raw dictionary data into TestCase objects.

        This transforms the JSON response into Python objects
        that are easier to work with in code.
        """
        test_cases = []

        # Handle different possible JSON structures
        cases_list = test_data.get('test_cases', test_data.get('tests', []))

        for case_data in cases_list:
            try:
                test_case = TestCase(
                    title=case_data.get('title', 'Untitled Test'),
                    description=case_data.get('description', ''),
                    steps=case_data.get('steps', []),
                    expected_result=case_data.get('expected_result', ''),
                    test_type=case_data.get('test_type', 'integration'),
                    priority=case_data.get('priority', 'medium'),
                    preconditions=case_data.get('preconditions', [])
                )
                test_cases.append(test_case)
            except Exception as e:
                logger.warning(f"Skipping invalid test case: {e}")
                continue

        return test_cases

    def export_to_json(self, test_cases: List[TestCase], filename: str):
        """
        Save test cases to a JSON file.

        JSON is a standard format that can be read by other tools,
        imported into test management systems, or shared with team members.
        """
        output = {
            "test_cases": [
                {
                    "title": tc.title,
                    "description": tc.description,
                    "steps": tc.steps,
                    "expected_result": tc.expected_result,
                    "test_type": tc.test_type,
                    "priority": tc.priority,
                    "preconditions": tc.preconditions
                }
                for tc in test_cases
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(test_cases)} test cases to {filename}")

    def export_to_markdown(self, test_cases: List[TestCase], filename: str):
        """
        Save test cases to a human-readable Markdown file.

        Markdown is easy to read and can be viewed in GitHub, Notion, etc.
        Great for documentation and sharing with non-technical team members.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Test Cases\n\n")

            for i, tc in enumerate(test_cases, 1):
                f.write(f"## Test Case {i}: {tc.title}\n\n")
                f.write(f"**Type:** {tc.test_type}  \n")
                f.write(f"**Priority:** {tc.priority}  \n\n")
                f.write(f"**Description:** {tc.description}\n\n")

                if tc.preconditions:
                    f.write("**Preconditions:**\n")
                    for precond in tc.preconditions:
                        f.write(f"- {precond}\n")
                    f.write("\n")

                f.write("**Steps:**\n")
                for j, step in enumerate(tc.steps, 1):
                    f.write(f"{j}. {step}\n")
                f.write("\n")

                f.write(f"**Expected Result:** {tc.expected_result}\n\n")
                f.write("---\n\n")

        logger.info(f"Exported {len(test_cases)} test cases to {filename}")


# Example usage (this runs if you execute this file directly)
if __name__ == "__main__":
    # This is just a simple example for testing
    # In practice, you'd use the CLI we'll create next

    import os
    from dotenv import load_dotenv

    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        exit(1)

    # Create generator
    generator = AITestCaseGenerator(api_key)

    # Example user story
    user_story = """
    As a user, I want to login with my email and password
    so that I can access my personalized dashboard
    """

    # Generate test cases
    test_cases = generator.generate_test_cases(user_story, num_cases=5)

    # Print results
    for i, tc in enumerate(test_cases, 1):
        print(f"\n{i}. {tc.title}")
        print(f"   Type: {tc.test_type} | Priority: {tc.priority}")
        print(f"   {tc.description}")
