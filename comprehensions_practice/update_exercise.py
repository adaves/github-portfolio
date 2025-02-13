import json

def update_exercise(exercise_id, updated_data):
    # Load the JSON file
    with open('code_practice_exercises.json', 'r') as f:
        data = json.load(f)
    
    # Find and update the specific exercise
    exercises = data['practice_types']['comprehensions']['exercises']
    for exercise in exercises:
        if exercise['id'] == exercise_id:
            exercise.update(updated_data)
            break
    
    # Save the updated JSON file
    with open('code_practice_exercises.json', 'w') as f:
        json.dump(data, f, indent=2)

# Example usage:
updated_data = {
    "id": "comp_1",  # Keep the same ID
    "prompt": "Create a list comprehension that flattens a 2D matrix into a single list.\n\nGiven matrix: [[1,2,3], [4,5,6], [7,8,9]]\n\nExpected output: [1,2,3,4,5,6,7,8,9]\n\nHint: You'll need two for loops in your comprehension - one for rows and one for elements.",
    "sample_solution": "[num for row in matrix for num in row]",
    "test_cases": [
        {
            "input": {"matrix": [[1,2,3], [4,5,6], [7,8,9]]},
            "expected_output": [1,2,3,4,5,6,7,8,9]
        },
        {
            "input": {"matrix": [[1,1], [2,2]]},
            "expected_output": [1,1,2,2]
        }
    ],
    "context": "Nested list comprehension for flattening 2D lists",
    "difficulty": "medium",
    "tags": ["list", "comprehension", "nested", "2D"]
}

if __name__ == "__main__":
    update_exercise("comp_1", updated_data) 