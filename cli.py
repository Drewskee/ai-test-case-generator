#!/usr/bin/env python3
"""
Command Line Interface for AI Test Case Generator

This file makes it easy to use the test case generator from your terminal.
You can run commands like: python cli.py generate "your user story"
"""

import click
import os
from dotenv import load_dotenv
from test_case_generator import AITestCaseGenerator
from colorama import Fore, Style, init
import json

# Initialize colorama for colored terminal output
init(autoreset=True)


def print_success(message):
    """Print a success message in green"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message):
    """Print an error message in red"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message):
    """Print an info message in blue"""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")


def print_test_case(tc, index):
    """Pretty print a single test case to the terminal"""
    print(f"\n{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Test Case {index}: {tc.title}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Type:{Style.RESET_ALL} {tc.test_type}")
    print(f"{Fore.CYAN}Priority:{Style.RESET_ALL} {tc.priority}")
    print(f"\n{Fore.CYAN}Description:{Style.RESET_ALL}")
    print(f"  {tc.description}")

    if tc.preconditions:
        print(f"\n{Fore.CYAN}Preconditions:{Style.RESET_ALL}")
        for precond in tc.preconditions:
            print(f"  • {precond}")

    print(f"\n{Fore.CYAN}Steps:{Style.RESET_ALL}")
    for i, step in enumerate(tc.steps, 1):
        print(f"  {i}. {step}")

    print(f"\n{Fore.CYAN}Expected Result:{Style.RESET_ALL}")
    print(f"  {tc.expected_result}")


@click.group()
def cli():
    """
    AI-Powered Test Case Generator

    Generate comprehensive test cases from user stories using AI.
    Perfect for QA engineers, developers, and product managers!
    """
    # Load environment variables from .env file
    load_dotenv()


@cli.command()
@click.argument('user_story')
@click.option('--count', '-c', default=5, help='Number of test cases to generate (default: 5)')
@click.option('--model', '-m', default='gpt-3.5-turbo', help='OpenAI model to use')
@click.option('--output', '-o', help='Save to file (e.g., test_cases.json or test_cases.md)')
@click.option('--focus', '-f', multiple=True, help='Focus areas (e.g., -f security -f performance)')
def generate(user_story, count, model, output, focus):
    """
    Generate test cases from a user story.

    Example:
    python cli.py generate "As a user, I want to login with email and password"

    With options:
    python cli.py generate "User story here" --count 10 --output tests.md --focus security
    """
    print_info(f"Generating {count} test cases...")

    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print_error("OPENAI_API_KEY not found!")
        print_info("Please create a .env file with your API key:")
        print("  OPENAI_API_KEY=your-key-here")
        print_info("Get your API key from: https://platform.openai.com/api-keys")
        return

    try:
        # Create generator
        generator = AITestCaseGenerator(api_key, model=model)

        # Generate test cases
        focus_list = list(focus) if focus else None
        test_cases = generator.generate_test_cases(
            user_story=user_story,
            num_cases=count,
            focus_areas=focus_list
        )

        # Display test cases in terminal
        print_success(f"Generated {len(test_cases)} test cases!\n")

        for i, tc in enumerate(test_cases, 1):
            print_test_case(tc, i)

        # Save to file if requested
        if output:
            if output.endswith('.json'):
                generator.export_to_json(test_cases, output)
                print_success(f"\nSaved test cases to {output}")
            elif output.endswith('.md'):
                generator.export_to_markdown(test_cases, output)
                print_success(f"\nSaved test cases to {output}")
            else:
                print_error("Output file must end with .json or .md")

    except Exception as e:
        print_error(f"Failed to generate test cases: {e}")
        return


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--count', '-c', default=5, help='Number of test cases per story')
@click.option('--output-dir', '-o', default='output', help='Output directory for generated tests')
def batch(file_path, count, output_dir):
    """
    Generate test cases for multiple user stories from a file.

    The file should contain one user story per line.

    Example:
    python cli.py batch stories.txt --output-dir test_output
    """
    print_info(f"Reading user stories from {file_path}...")

    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print_error("OPENAI_API_KEY not found in .env file")
        return

    # Read user stories
    with open(file_path, 'r', encoding='utf-8') as f:
        stories = [line.strip() for line in f if line.strip()]

    print_info(f"Found {len(stories)} user stories")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate test cases for each story
    generator = AITestCaseGenerator(api_key)

    for i, story in enumerate(stories, 1):
        print_info(f"\nProcessing story {i}/{len(stories)}...")
        print(f"  {story[:80]}...")

        try:
            test_cases = generator.generate_test_cases(story, num_cases=count)

            # Save to files
            base_name = f"story_{i:03d}"
            json_path = os.path.join(output_dir, f"{base_name}.json")
            md_path = os.path.join(output_dir, f"{base_name}.md")

            generator.export_to_json(test_cases, json_path)
            generator.export_to_markdown(test_cases, md_path)

            print_success(f"  Generated {len(test_cases)} test cases")

        except Exception as e:
            print_error(f"  Failed: {e}")
            continue

    print_success(f"\nCompleted! Check {output_dir}/ for results")


@cli.command()
def setup():
    """
    Interactive setup to configure your API key.

    Walks you through creating a .env file with your OpenAI API key.
    """
    print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}AI Test Case Generator - Setup{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}\n")

    print_info("This tool requires an OpenAI API key to function.")
    print_info("Get your key from: https://platform.openai.com/api-keys\n")

    # Check if .env already exists
    if os.path.exists('.env'):
        print_info(".env file already exists")
        overwrite = click.confirm("Do you want to update it?", default=False)
        if not overwrite:
            print_info("Setup cancelled")
            return

    # Get API key from user
    api_key = click.prompt("Enter your OpenAI API key", hide_input=True)

    # Write to .env file
    with open('.env', 'w') as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
        f.write(f"# Add other configuration here\n")

    print_success("Configuration saved to .env file!")
    print_info("\nYou can now generate test cases:")
    print('  python cli.py generate "As a user, I want to login..."')


@cli.command()
def examples():
    """
    Show example user stories and commands.

    Helpful for learning how to write good user stories
    and use the tool effectively.
    """
    print(f"\n{Fore.YELLOW}Example User Stories:{Style.RESET_ALL}\n")

    examples = [
        {
            "title": "Login Feature",
            "story": "As a user, I want to login with email and password so that I can access my personalized dashboard"
        },
        {
            "title": "Shopping Cart",
            "story": "As a customer, I want to add items to my cart and checkout so that I can purchase products"
        },
        {
            "title": "Password Reset",
            "story": "As a user, I want to reset my password via email so that I can regain access if I forget it"
        },
        {
            "title": "File Upload",
            "story": "As a user, I want to upload profile pictures up to 5MB so that I can personalize my account"
        },
        {
            "title": "Search Feature",
            "story": "As a user, I want to search products by name, category, or price range so that I can find items quickly"
        }
    ]

    for i, ex in enumerate(examples, 1):
        print(f"{Fore.CYAN}{i}. {ex['title']}{Style.RESET_ALL}")
        print(f"   {ex['story']}\n")

    print(f"\n{Fore.YELLOW}Example Commands:{Style.RESET_ALL}\n")

    commands = [
        ("Basic usage", 'python cli.py generate "Your user story here"'),
        ("Generate more tests", 'python cli.py generate "Your story" --count 10'),
        ("Focus on security", 'python cli.py generate "Your story" --focus security'),
        ("Save to file", 'python cli.py generate "Your story" --output tests.md'),
        ("Batch processing", 'python cli.py batch user_stories.txt'),
    ]

    for desc, cmd in commands:
        print(f"{Fore.CYAN}{desc}:{Style.RESET_ALL}")
        print(f"  {cmd}\n")


if __name__ == '__main__':
    cli()
