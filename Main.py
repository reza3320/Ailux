import genai
import logging
from prompt_toolkit import prompt
import subprocess

# Configure logging
logging.basicConfig(filename='ai_commands.log', level=logging.DEBUG)

# Configure your Gemini API key
genai.configure(api_key='YOUR_API_KEY')


def execute_and_capture_output(command):
  """Executes a command using subprocess and captures the output."""
  try:
    output = subprocess.run(command, capture_output=True, text=True).stdout
    return output
  except subprocess.CalledProcessError as e:
    logging.error(f"Command execution error: {e}")
    return f"Error: {e}"


def main():
  # Welcome message
  print("Welcome to the AI-assisted terminal!")

  while True:
    # Get user input
    user_input = prompt(">>> ")

    # Check for exit command
    if user_input.lower() == "exit":
        break

    # Process user input with Gemini
    response = genai.generate_text(prompt=user_input)
    print(response.text)

    # Check if response suggests a command
    if response.text.lower().startswith("run command: "):
      # Extract suggested command
      command = response.text[13:].strip()

      # Log the suggested command
      logging.info(f"AI suggested command: {command}")

      # Ask for user confirmation before execution (initial)
      confirmation = prompt("Confirm execution? (y/n): ")
      if confirmation.lower() == "y":
          # Execution loop
          while True:
              # Execute the command and capture output
              output = execute_and_capture_output(command)
              print(output)

              # Log the executed command and its output
              logging.info(f"Command executed: {command}")
              logging.info(f"Command output: {output}")

              # Check if successful or ask for user guidance on next steps
              if "success" in output.lower():  # Modify success condition as needed
                  print("Success!")
                  break  # Exit the execution loop
              else:
                  # AI analysis and suggestion
                  analysis = genai.generate_text(prompt=f"Analyze error: {output}")
                  print(analysis.text)

                  # User input for further guidance
                  user_action = prompt(
                      "What would you like to do next? (investigate, retry, modify command, cancel): "
                  )

                  # Update command based on user action
                  if user_action.lower() == "modify command":
                      new_command = prompt("Enter the modified command: ")
                      command = new_command
                  elif user_action.lower() == "cancel":
                      break  # Exit the execution loop
                  # Add logic for other user actions (investigate, retry with modifications)

      else:
          print("Command execution cancelled.")
          logging.info(f"Command execution denied: {command}")


if __name__ == "__main__":
  main()
