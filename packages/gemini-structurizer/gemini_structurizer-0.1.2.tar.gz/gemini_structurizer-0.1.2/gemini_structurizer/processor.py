import google.generativeai as genai
import os
import json
import argparse
import inspect # For more precise determination of caller path (optional)

# --- Global configuration variables (filename only) ---
DEFAULT_CONFIG_FILENAME = "gemini_structurizer_config.json"
INPUT_FILE_CONFIG_KEY = "input_file_to_process"

def get_caller_directory():
    """
    Tries to get the directory of the scriptmargins that called this library function.
    This is a heuristic method and usually works in simple scenarios.
    More complex stack inspection might be needed for more intricate library usage.
    """
    # Try to use inspect module to get the caller's file path
    # stack()[0] is current frame, stack()[1] is caller, stack()[2] is caller's caller, etc.
    # We need to find the first frame that is not this module's file
    try:
        for frame_info in inspect.stack():
            module_path = frame_info.filename
            if os.path.abspath(module_path) != os.path.abspath(__file__): # Ensure it's not this file
                caller_dir = os.path.dirname(os.path.abspath(module_path))
                if os.path.isdir(caller_dir): # Ensure it's a directory
                    return caller_dir
    except Exception:
        pass # Fallback if inspect fails

    # Fallback to current working directory, reasonable for most direct run scenarios
    return os.getcwd()


def get_config_path(config_filename=DEFAULT_CONFIG_FILENAME):
    """Gets the full path to the configuration file, based on the calling script's directory."""
    caller_dir = get_caller_directory()
    return os.path.join(caller_dir, config_filename)

def generate_default_config_content():
    """Generates default/template configuration file content."""
    return {
        "model_name": "gemini-2.5-flash-preview-04-17", # Or your preferred model
        "system_instruction": "# TODO: Fill in your system-level prompt here (e.g., You are a text analysis expert...)",
        "user_prompt_for_file_processing": "# TODO: Fill in your user prompt for file processing here.\n# You can use {filename} as a placeholder for the uploaded filename.\n# E.g., Please analyze the file named {filename} and extract...",
        "output_json_schema": {
            "type": "object",
            "properties": {
                "example_output_key": {
                    "type": "string",
                    "description": "# TODO: This is an example for your JSON Schema. Please replace it with your actual required Schema."
                }
            },
            "required": ["# TODO: example_output_key"]
        },
        INPUT_FILE_CONFIG_KEY: "# TODO: (Optional) Fill in the full path to the input file you want to process here, or pass it as a function argument."
    }

def load_or_create_config(custom_config_path=None):
    """
    Loads the configuration file. If it doesn't exist, creates it and prompts the user.
    The configuration file path is based on the calling script's directory.
    Args:
        custom_config_path (str, optional): The user can specify a custom configuration file path.
                                           If None, uses the default filename in the caller's directory to find/create.
    Returns:
        dict or None: The loaded configuration dictionary, or None if user action/error is required.
    """
    config_path_to_use = custom_config_path if custom_config_path else get_config_path()

    if not os.path.exists(config_path_to_use):
        print(f"Configuration file '{os.path.abspath(config_path_to_use)}' not found.")
        default_config = generate_default_config_content()
        try:
            os.makedirs(os.path.dirname(config_path_to_use), exist_ok=True) # Ensure directory exists
            with open(config_path_to_use, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print(f"Default configuration file created: '{os.path.abspath(config_path_to_use)}'")
            print("Please open this file, fill in the necessary configuration information, and then rerun.")
            return None
        except IOError as e:
            print(f"Error creating default configuration file '{os.path.abspath(config_path_to_use)}': {e}")
            return None
    
    try:
        with open(config_path_to_use, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_core_keys = ["model_name", "system_instruction", "user_prompt_for_file_processing", "output_json_schema"]
        missing_keys = [key for key in required_core_keys if key not in config or str(config[key]).startswith("# TODO:")]
        
        if missing_keys:
            print(f"Error: The following core configurations are missing or not filled (start with '# TODO:') in '{os.path.abspath(config_path_to_use)}':")
            for key in missing_keys:
                print(f"- {key}")
            print("Please check and fill in the configuration file, then rerun.")
            return None
            
        return config
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file '{os.path.abspath(config_path_to_use)}': {e}")
        return None
    except IOError as e:
        print(f"Error reading configuration file '{os.path.abspath(config_path_to_use)}': {e}")
        return None

def get_output_json_path(input_filepath):
    """Generates the output JSON file path based on the input file path."""
    if not input_filepath:
        return None
    # Output file in the same directory as the input file
    directory = os.path.dirname(os.path.abspath(input_filepath))
    filename = os.path.basename(input_filepath)
    name_part = filename.rsplit('.', 1)[0]
    return os.path.join(directory, name_part + ".json")

# --- Main processing function (now the core library functionality) ---
def structure_file_with_gemini(input_filepath, custom_config_path=None, overwrite_existing_output=False):
    """
    Processes the specified file using the Gemini API and generates structured JSON based on the configuration.

    Args:
        input_filepath (str): Path to the input file to be processed.
        custom_config_path (str, optional): Path to a custom configuration file.
                                           If None, uses the default name in the calling script's directory to find/create.
        overwrite_existing_output (bool, optional): If True, reprocesses even if the output JSON already exists. Defaults to False.

    Returns:
        str or None: Path to the generated JSON file on success, None on failure or skip (or path to existing file).
    """
    print("--- Gemini File Structurizer (Library Mode) ---")

    if not os.getenv('GOOGLE_API_KEY'):
        print("\nError: GOOGLE_API_KEY environment variable not set. Please configure before calling.")
        return None # Directly return error status in library function

    config_data = load_or_create_config(custom_config_path)

    if config_data is None:
        print("\nConfiguration loading or creation failed. Please ensure the configuration file is valid.")
        return None

    if not input_filepath:
        print("Error: No valid input_filepath provided.")
        return None
        
    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{os.path.abspath(input_filepath)}' not found.")
        return None

    output_json_filepath = get_output_json_path(input_filepath)
    if not output_json_filepath:
        print(f"Error: Could not generate output path for input '{input_filepath}'.")
        return None
        
    print(f"\nInput file: '{os.path.abspath(input_filepath)}'")
    print(f"Expected output: '{os.path.abspath(output_json_filepath)}'")

    if not overwrite_existing_output and os.path.exists(output_json_filepath):
        print(f"Info: Output file '{os.path.abspath(output_json_filepath)}' already exists and overwrite is not permitted. Returning path directly.")
        return output_json_filepath

    # --- Gemini API call logic ---
    uploaded_file = None
    try:
        print(f"Uploading file: {input_filepath}...")
        display_name = os.path.basename(input_filepath)
        uploaded_file = genai.upload_file(path=input_filepath, display_name=display_name)
        print(f"File '{display_name}' uploaded as: {uploaded_file.uri} (Resource name: {uploaded_file.name})")

        print(f"Using model: {config_data['model_name']}")
        model = genai.GenerativeModel(
            model_name=config_data["model_name"],
            system_instruction=config_data["system_instruction"],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=config_data["output_json_schema"] 
            )
        )

        user_prompt = config_data["user_prompt_for_file_processing"].format(filename=display_name)
        
        print(f"Processing file '{display_name}'...")
        response = model.generate_content([uploaded_file, user_prompt])

        if not response.parts:
            print("Error: No content parts in API response.")
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                 print(f"Prompt feedback: {response.prompt_feedback}")
            return None
        
        try:
            output_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse API response as JSON: {e}")
            print(f"Original response text: {response.text}")
            return None
        except AttributeError: 
            print("Error: API response object missing .text attribute.")
            return None
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_json_filepath), exist_ok=True)
        with open(output_json_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully extracted file structure to JSON: {os.path.abspath(output_json_filepath)}")
        return output_json_filepath

    except Exception as e:
        print(f"A critical error occurred during processing: {e}")
        # ... (more detailed error feedback can be added here) ...
        return None
    finally:
        if uploaded_file and hasattr(uploaded_file, 'name'):
            try:
                print(f"Deleting uploaded file: {uploaded_file.name} ({uploaded_file.uri})...")
                genai.delete_file(uploaded_file.name)
                print(f"Successfully deleted uploaded file: {uploaded_file.name}")
            except Exception as del_e:
                print(f"Error deleting uploaded file {uploaded_file.name}: {del_e}")

# --- Main execution block (primarily for testing the library or running as a standalone script) ---
def main_cli_entry():
    """Handles command-line execution logic."""
    # --- Debug input file path for easy VS Code direct run ---
    # DEBUG_INPUT_FILE = None
    DEBUG_INPUT_FILE = "test_input.txt" # Assumes test_input.txt is in the same directory as the script
    # Create a dummy test_input.txt for testing
    if DEBUG_INPUT_FILE and not os.path.exists(DEBUG_INPUT_FILE):
        try:
            # Ensure the script is run from a directory where it can create test_input.txt
            # For library use, this test file creation should ideally be in a separate test script.
            script_dir_for_test_file = get_caller_directory() if __name__ != '__main__' else os.getcwd()
            debug_file_path = os.path.join(script_dir_for_test_file, DEBUG_INPUT_FILE)

            if not os.path.exists(debug_file_path): # Check again after getting dir
                with open(debug_file_path, "w", encoding="utf-8") as f_test:
                    f_test.write("1: This is the first line\n2: This is the title of the second chapter\n3: Content ends\n")
                print(f"Created test file: {debug_file_path}")
        except IOError:
            print(f"Could not create test file {DEBUG_INPUT_FILE}. Please create it manually or modify the path.")
            DEBUG_INPUT_FILE = None # Avoid subsequent errors
    # -------------------------------------------

    parser = argparse.ArgumentParser(description="Gemini File Structurizer (Standalone Run Mode).")
    parser.add_argument(
        "-i", "--input",
        help="Path to the input file to process. Overrides DEBUG_INPUT_FILE and configuration file path."
    )
    parser.add_argument(
        "-c", "--config",
        help=f"Path to the configuration file. If not provided, looks for/creates {DEFAULT_CONFIG_FILENAME} in the current directory."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If specified, reprocesses and overwrites the output JSON file even if it already exists."
    )
    args = parser.parse_args()

    print("--- Gemini File Structurizer (Standalone Run Mode) ---")

    # Determine final input file path
    final_input_file = None
    if args.input:
        final_input_file = args.input
        print(f"Info: Using input file provided via command line: {final_input_file}")
    elif DEBUG_INPUT_FILE is not None and os.path.exists(os.path.join(get_caller_directory() if __name__ != '__main__' else os.getcwd(), DEBUG_INPUT_FILE)):
        final_input_file = os.path.join(get_caller_directory() if __name__ != '__main__' else os.getcwd(), DEBUG_INPUT_FILE)
        print(f"Info: Using input file specified by DEBUG_INPUT_FILE in script: {final_input_file}")
    else:
        # If run as standalone script without command line and DEBUG input, try to read from default config
        # Config path determination should be relative to where the script is run from if no -c is given
        config_path_for_input_lookup = args.config if args.config else get_config_path()
        temp_config = load_or_create_config(config_path_for_input_lookup)
        if temp_config:
            final_input_file_from_config = temp_config.get(INPUT_FILE_CONFIG_KEY)
            if final_input_file_from_config and not str(final_input_file_from_config).startswith("# TODO:"):
                final_input_file = final_input_file_from_config
                print(f"Info: Using input file specified in configuration file '{os.path.abspath(config_path_for_input_lookup)}': {final_input_file}")
            else:
                final_input_file = None
        else: # temp_config is None, likely because it was just created or failed to load
             print("Info: Configuration file might have just been created or failed to load correctly; cannot get input file path from it.")


    if not final_input_file:
        print(f"Error: No valid input file path specified via command line, DEBUG_INPUT_FILE, or configuration file.")
        print("--- Program End ---")
        exit()

    # Call the core library function
    # If -c is not given, custom_config_path will be None, and structure_file_with_gemini will use default logic
    result_path = structure_file_with_gemini(
        input_filepath=final_input_file,
        custom_config_path=args.config, # Allows user to specify a different config file
        overwrite_existing_output=args.overwrite
    )

    if result_path:
        print(f"\nProcessing complete!")
        if os.path.exists(result_path):
            try:
                with open(result_path, 'r', encoding='utf-8') as f_check:
                    print("\nJSON file content preview (first 500 characters):")
                    preview_content = f_check.read(500)
                    print(preview_content)
                    if len(preview_content) == 500:
                        print("...")
            except Exception as e:
                print(f"Could not read or preview the generated JSON file '{result_path}': {e}")
    else:
        print("\nFile processing failed or was skipped. Please check the messages above.")

    print("\n--- Program End ---")

if __name__ == '__main__':
    main_cli_entry()