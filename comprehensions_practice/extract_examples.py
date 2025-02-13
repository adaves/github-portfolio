import json
import nbformat
import ast

def convert_to_json_serializable(obj):
    """Convert Python objects to JSON serializable types"""
    if isinstance(obj, set):
        return list(obj)
    return obj

def safe_eval(output_str):
    """Safely evaluate output string and convert to JSON serializable type"""
    try:
        if output_str:
            result = ast.literal_eval(output_str)
            return convert_to_json_serializable(result)
    except:
        return None
    return None

def extract_examples_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    exercises = []
    exercise_id = 1
    
    for cell in nb.cells:
        if cell.cell_type == 'code':
            # Look for comprehension examples
            source = cell.source.strip()
            if source and '=' in source and '[' in source and 'for' in source:
                # This looks like a comprehension example
                output = None
                if cell.outputs and hasattr(cell.outputs[0], 'data'):
                    output = cell.outputs[0].data.get('text/plain')
                
                # Convert output to JSON serializable format
                expected_output = safe_eval(output)
                
                exercise = {
                    "id": f"comp_{exercise_id}",
                    "prompt": f"Create a list comprehension that achieves the following: {source.split('=')[0].strip()}",
                    "sample_solution": source.split('=')[1].strip(),
                    "test_cases": [{"input": None, "expected_output": expected_output}],
                    "context": "List comprehension example",
                    "difficulty": "medium",
                    "tags": ["list", "comprehension"]
                }
                exercises.append(exercise)
                exercise_id += 1
    
    return exercises

def create_practice_json():
    notebooks = ['comprehensions_.ipynb', 'Comprehensions.ipynb', 'list_comprehensions.ipynb']
    all_exercises = []
    
    for notebook in notebooks:
        try:
            exercises = extract_examples_from_notebook(notebook)
            all_exercises.extend(exercises)
        except Exception as e:
            print(f"Error processing {notebook}: {str(e)}")
    
    practice_data = {
        "practice_types": {
            "comprehensions": {
                "exercises": all_exercises
            },
            "for_loops": {
                "exercises": []  # Ready for future expansion
            }
        }
    }
    
    with open('code_practice_exercises.json', 'w') as f:
        json.dump(practice_data, f, indent=2)

if __name__ == "__main__":
    create_practice_json() 