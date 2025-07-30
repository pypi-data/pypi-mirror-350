# Creating Custom Prompts for FlowAI

G'day! This guide will help you create your own custom prompts for FlowAI. Custom prompts are a ripper way to automate your workflow and get the most out of your LLM.

## Prompt File Location

All prompt files should be placed in the `~/flowai-prompts` directory. This directory is created automatically when you run `flowai --init`. The files should have a `.txt` extension.

## Prompt File Structure

A prompt file has two main components:

1. **System Instructions**
   The first part of the file contains instructions for the LLM about its role and how to process the input. This section should:
   - Define the LLM's role and task
   - Explain what input it will receive
   - Specify the expected output format
   - List any special requirements or constraints

2. **Context and Template Markers**
   The file can include special markers that get replaced with actual content:
   - `{{CONTEXT}}` - Gets replaced with the input content (e.g., git diff, file contents)
   - `[placeholder]` - Square brackets indicate where the LLM should insert specific content
   
## Example Prompt File

Here's a basic example for creating pull request descriptions:

```
You are tasked with creating a comprehensive pull request description based on git commit messages.
Your description should be clear, concise, and follow best practices.

Here are the commit messages to analyze:

{{CONTEXT}}

Create a pull request description with the following structure:

# [A clear and concise title summarizing the changes]

## Summary
[Brief overview of the changes and their purpose]

## Changes Made
[List of main changes, referencing specific commits]

## Testing
[Description of how the changes were tested]

## Additional Notes
[Any important information not covered above]
```

## Template Guidelines

1. **Context Placement**
   - Use `{{CONTEXT}}` where you want the input content to appear
   - Usually placed after explaining what the content represents
   - Can include formatting around it (e.g., in code blocks or quotes)

2. **Dynamic Content**
   - Use `[placeholder]` for content the LLM should generate
   - Make placeholders descriptive (e.g., `[list of changes made]`)
   - Can include formatting hints in the placeholder

3. **Structure**
   - Start with clear instructions about the LLM's role
   - Explain what the context represents
   - Provide a clear output structure
   - Use markdown formatting for better readability

## Common Use Cases

Here are some ideas for custom prompts:

1. **Bug Report Template**
   - Analyze error logs
   - Generate structured bug reports
   - Suggest potential fixes

2. **Documentation Generator**
   - Generate function/class documentation
   - Create API endpoint documentation
   - Write usage examples

3. **Code Refactoring Plan**
   - Analyze code complexity
   - Suggest refactoring steps
   - Identify technical debt

4. **Release Notes Generator**
   - Summarize git commits
   - Categorize changes
   - Generate user-friendly notes

5. **Test Case Generator**
   - Analyze function signatures
   - Generate test scenarios
   - Create test templates

## Tips and Tricks

1. **Context is King**
   - Always specify what context the prompt expects (git diff, logs, etc.)
   - Explain how the context should be interpreted
   - Include example commands in the description

2. **Structured Output**
   - Use markdown headings for clear sections
   - Include placeholder sections with square brackets
   - Add formatting examples where needed

3. **Error Handling**
   - Include instructions for handling missing or invalid input
   - Provide fallback options
   - Specify what to do with empty context

4. **Reusability**
   - Make prompts generic enough to be reused
   - Use clear placeholder names
   - Add comments explaining each section

## Example Commands

Here are some common ways to use prompt files:

```bash
# Code Review
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/code-review.txt

# Generate Documentation
cat myfile.py | flowai --prompt-file ~/flowai-prompts/generate-docs.txt

# Create Release Notes
git log --oneline main..HEAD | flowai --prompt-file ~/flowai-prompts/release-notes.txt

# Analyze Error Logs
tail -n 100 error.log | flowai --prompt-file ~/flowai-prompts/error-analysis.txt
``` 