import json
from datetime import datetime
import random
import ast

class CodePractice:
    def __init__(self):
        self.exercises = self._load_exercises()
        self.scores = self._load_scores()
        
    def _load_exercises(self):
        with open('code_practice_exercises.json', 'r') as f:
            return json.load(f)['practice_types']
            
    def _load_scores(self):
        try:
            with open('scores.txt', 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []
            
    def _save_score(self, practice_type, daily_score, overall_score):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        score_line = f"{timestamp}, Type: {practice_type}, Daily Score: {daily_score}%, Overall Score: {overall_score}%\n"
        with open('scores.txt', 'a') as f:
            f.write(score_line)
            
    def _evaluate_answer(self, user_answer, exercise):
        try:
            local_ns = {}
            
            if exercise['test_cases'][0]['input']:
                local_ns.update(exercise['test_cases'][0]['input'])
            
            exec(f"result = {user_answer}", {}, local_ns)
            user_result = local_ns['result']
            
            for test_case in exercise['test_cases']:
                if test_case['input']:
                    local_ns.update(test_case['input'])
                    exec(f"result = {user_answer}", {}, local_ns)
                    user_result = local_ns['result']
                
                if user_result != test_case['expected_output']:
                    return False
            return True
            
        except Exception as e:
            print(f"Error evaluating answer: {str(e)}")
            return False
            
    def practice_session(self, practice_type=None, num_questions=5, max_attempts=3):
        if practice_type is None:
            # Let user choose practice type
            available_types = list(self.exercises.keys())
            print("\nAvailable practice types:")
            for i, p_type in enumerate(available_types, 1):
                print(f"{i}. {p_type}")
            choice = int(input("\nChoose practice type (enter number): ")) - 1
            practice_type = available_types[choice]
        
        exercises = self.exercises[practice_type]['exercises']
        selected_exercises = random.sample(exercises, min(num_questions, len(exercises)))
        
        correct = 0
        for i, exercise in enumerate(selected_exercises, 1):
            print(f"\nQuestion {i}/{num_questions}:")
            print(exercise['prompt'])
            
            if exercise['test_cases'][0]['input']:
                print(f"Input data: {exercise['test_cases'][0]['input']}")
            
            attempts = 0
            while attempts < max_attempts:
                user_answer = input("Your answer: ").strip()
                
                if self._evaluate_answer(user_answer, exercise):
                    print("Correct!")
                    correct += 1
                    break
                else:
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"Incorrect. You have {max_attempts - attempts} attempts remaining. Try again!")
                    else:
                        print("Incorrect.")
                        print(f"A sample solution: {exercise['sample_solution']}")
                
        daily_score = (correct / num_questions) * 100
        overall_score = self._calculate_overall_score(practice_type, daily_score)
        
        self._save_score(practice_type, daily_score, overall_score)
        
        print(f"\nDaily Score: {daily_score}%")
        print(f"Overall Score: {overall_score}%")

    def _calculate_overall_score(self, practice_type, daily_score):
        if not self.scores:
            return daily_score
            
        type_scores = [float(line.split(', Overall Score: ')[1].rstrip('%\n'))
                      for line in self.scores 
                      if f"Type: {practice_type}" in line]
                      
        return round((sum(type_scores) + daily_score) / (len(type_scores) + 1), 2)
        
    def export_for_ml(self, output_file='ml_training_data.json'):
        ml_data = []
        for practice_type, type_data in self.exercises.items():
            for exercise in type_data['exercises']:
                ml_data.append({
                    "prompt": exercise['prompt'],
                    "context": exercise['context'],
                    "solution": exercise['sample_solution'],
                    "type": practice_type,
                    "difficulty": exercise['difficulty'],
                    "tags": exercise['tags']
                })
        
        with open(output_file, 'w') as f:
            json.dump({"training_data": ml_data}, f, indent=2)

if __name__ == "__main__":
    practice = CodePractice()
    practice.practice_session() 