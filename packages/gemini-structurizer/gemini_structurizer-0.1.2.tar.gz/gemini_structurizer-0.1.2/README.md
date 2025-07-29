# Gemini Structurizer

**Transform unstructured files into structured JSON using Google's Gemini API.**

Gemini Structurizer is a Python library and command-line tool that leverages the power of Google's Gemini models to parse various file types (like `.txt`, `.pdf`, etc.) and extract information into a user-defined JSON schema. It's designed to be flexible and configurable, allowing users to define the processing logic through prompts and schemas.

## Features

*   **AI-Powered Structure Extraction:** Utilizes Gemini's multimodal capabilities to understand file content.
*   **Configurable Processing:** Define extraction logic using a JSON configuration file:
    *   Specify the Gemini model to use.
    *   Provide system-level instructions.
    *   Craft user prompts tailored to your file .
    *   Define the desired output JSON schema.
*   **File Upload & Management:** Handles uploading files to the Gemini API and cleaning them up afterwards.
*   **Automatic Configuration File Generation:** If a configuration file is not found, a template is automatically generated to guide the user.
*   **Flexible Input:** Process files specified via a configuration file, command-line arguments, or directly within your Python scripts (when used as a library).
*   **Automatic Output Naming:** Output JSON files are conveniently named based on the input file.
*   **Skip Existing Output:** Avoids reprocessing if the target JSON output file already exists (can be overridden).
*   **Library & CLI:** Can be used шоколадный as a Python library in your projects or as a standalone command-line tool.

## Installation

### Prerequisites

*   Python 3.9.21+
*   A Google Cloud Project with the Gemini API enabled.
*   An API key for the Gemini API. Set this key to the `GOOGLE_API_KEY` environment variable.

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### From PyPI

```bash
pip install gemini-structurizer 
```
*(Replace `gemini-structurizer` with the actual name you publish on PyPI if different)*

<!-- ### From Source (for development or local use)

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/gemini-structurizer-package.git 
    cd gemini-structurizer-package
    ```
2.  Install in editable mode:
    ```bash
    pip install -e .
    ``` -->

## Usage

### As a Command-Line Tool

The primary way to use the tool is by providing a configuration file.

1.  **Configuration File (`gemini_structurizer_config.json`)**

    If the configuration file (default: `gemini_structurizer_config.json` in the current directory) doesn't exist, the tool will generate a template for you on its first run. You need to edit this file:

    ```json
    {
      "model_name": "gemini-2.5-flash-preview-04-17", // Or your preferred Gemini model
      "system_instruction": "You are an expert in extracting structured data from documents.",
      "user_prompt_for_file_processing": "Please analyze the content of the uploaded file '{filename}' and extract chapter information according to the provided schema. Each line in the input text file is prefixed with 'line_number:'.",
      "output_json_schema": {
        "type": "object",
        "properties": {
          "chapter_list": {
            "type": "array",
            "description": "List of chapters.",
            "items": {
              "type": "object",
              "properties": {
                "chapter_name": { "type": "string" },
                "start_line": { "type": "integer" },
                "end_line": { "type": "integer" },
                "short_name": { "type": "string" }
              },
              "required": ["chapter_name", "start_line", "end_line", "short_name"]
            }
          }
        },
        "required": ["chapter_list"]
      },
      "input_file_to_process": "path/to/your/input_file.txt" // Path to the file you want to process
    }
    ```

    **Key fields to configure:**
    *   `model_name`: The Gemini model to use (e.g., "gemini-1.5-pro", "gemini-1.5-flash-preview-04-17").
    *   `system_instruction`: High-level instructions for the AI model.
    *   `user_prompt_for_file_processing`: Specific instructions on how to process the uploaded file. You can use `{filename}` as a placeholder for the uploaded file's name.
    *   `output_json_schema`: The JSON schema defining the structure of the desired output.
    *   `input_file_to_process`: The path to the input file (e.g., `.txt`, `.pdf`). This can be overridden by the command-line `-i` argument.

2.  **Running the Tool:**

    *   **Using the default config file (`gemini_structurizer_config.json`) in the current directory:**
        ```bash
        gemini-structurize 
        ```
        *(This assumes you've set up the `entry_points` in `setup.py` and installed the package. If running the script directly: `python path/to/gemini_structurizer/processor.py`)*

    *   **Specifying an input file (overrides config):**
        ```bash
        gemini-structurize -i path/to/another_file.txt
        ```

    *   **Specifying a custom config file:**
        ```bash
        gemini-structurize -c path/to/custom_config.json -i path/to/input_file.txt
        ```

    *   **Overwriting existing output:**
        ```bash
        gemini-structurize -i path/to/input_file.txt --overwrite
        ```

    The output JSON file will be saved in the same directory as the input file, with the same base name but a `.json` extension.

### As a Python Library

```python
from gemini_structurizer import structure_file_with_gemini # Assuming __init__.py exposes this
import os

# Ensure GOOGLE_API_KEY is set in your environment
# os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY_HERE" # For testing, not recommended for production

input_document_path = "path/to/your/document.txt"
# Optional: path to a custom configuration file. 
# If None, it looks for 'gemini_structurizer_config.json' in the directory of the calling script.
custom_config = "path/to/my_specific_task_config.json" 

# Ensure the config file is set up correctly (model, prompts, schema)
# The 'input_file_to_process' in the config will be ignored if 'input_document_path' is provided here.

json_output_path = structure_file_with_gemini(
    input_filepath=input_document_path,
    custom_config_path=custom_config, # Can be None to use default config name in calling script's dir
    overwrite_existing_output=False # Set to True to re-process even if output exists
)

if json_output_path:
    print(f"Successfully processed file. Output at: {json_output_path}")
    with open(json_output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Now you can work with the structured 'data'
        print(data)
else:
    print("File processing failed.")

```

## How it Works

1.  The tool loads a JSON configuration file that defines the Gemini model, system instructions, user prompt (how to process the file), and the desired output JSON schema.
2.  The specified input file is uploaded to the Gemini API.
3.  The Gemini model processes the file content based on your prompts and attempts to generate a JSON output conforming to your schema.
4.  The resulting JSON is saved to a file.

## Configuration Details

The `gemini_structurizer_config.json` (or your custom config file) is crucial.

*   **`model_name`**: (String) The identifier for the Gemini model (e.g., "gemini-1.5-flash-preview-04-17").
*   **`system_instruction`**: (String) A general instruction for the AI model about its role or task.
*   **`user_prompt_for_file_processing`**: (String) This is where you tell the AI *how* to interpret the file and *what* to extract. You can use the placeholder `{filename}` which will be replaced by the name of the uploaded file. This prompt should guide the AI to produce data that fits your `output_json_schema`.
*   **`output_json_schema`**: (Object) A valid JSON Schema object that defines the structure of the JSON output you expect from the AI. The Gemini API will use this schema to format its response.
*   **`input_file_to_process`**: (String) Path to the default input file. This is overridden if an input file is provided via the `-i` command-line argument or as a direct argument when using the library function.

<!-- ## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or find bugs.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request. -->

## License

Distributed under the MIT License. See `LICENSE` file for more information.

## Contact

zionpi - zhanngpenng@gmail.com

<!-- Project Link: [https://github.com/ZionPi/gemini-structurizer-package](https://github.com/ZionPi/gemini-structurizer-package) -->

