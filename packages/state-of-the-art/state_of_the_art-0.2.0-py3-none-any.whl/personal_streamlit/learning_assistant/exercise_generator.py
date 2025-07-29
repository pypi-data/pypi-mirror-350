
from typing import Tuple
from state_of_the_art.utils.llm.llm import LLM


class ExerciseGenerator:
    def __init__(self):
        self.llm = LLM()
    
    def generate_exercise(self, topic: str, temperature: float = 0.0):
        print(f"Generating exercise with temperature {temperature}")
        prompt = f""" You are a learning assistant. You are given a topic and you need to generate an exercise.
Beyond the exercersise you also generate a bit of extra knowledge about the topic that relates to the exercise in the form of 1 or 2 sentences.
Generate not more than 3 options.
Give options for the exercise and the correct answer.
Generate only one question
Mark the correct answer with [CORRECT].
Below the exercise also explain the correct answer.

Structure:
Insight / Context
Question
Options
Explanation

Topic: {{text}}
"""
        response = self.llm.call(prompt, topic, temperature)
        return response



class AnswerChecker:
    def __init__(self):
        self.llm = LLM()
    
    def correct_answer(self, exercise: str, given_answer: str) -> Tuple[bool, str]:
        # break down in lines and get the number of option with a [CORRECT]
        lines = exercise.split("\n")
        for line in lines:
            if "[CORRECT]" in line:
                correct_line = line
                break
        correct_answer = correct_line[0]
        # lowercase everything
        correct_answer = correct_answer.lower()
        given_answer = given_answer.lower() 
        return correct_answer == given_answer, correct_answer
