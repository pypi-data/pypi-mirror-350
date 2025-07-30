import json

# TODO: Extend the method to get a schema to validate against.


def validate_json(json_str: str) -> dict:
    """Validate and clean JSON response from LLM"""
    try:
        # Remove any potential markdown formatting
        clean_response = json_str.strip("```").strip()
        if clean_response.startswith("json"):
            clean_response = clean_response[4:].strip()

        # Parse JSON
        result = json.loads(clean_response)
        return result

    except Exception as e:
        raise Exception(f"Invalid JSON response: {str(e)}")
