import openai
import re
import textwrap
from content_old.base import Homework, PythonHomework
from sheet.base import Solution, PythonSolution
from telegram import Telegram
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

class HomeworkChecker:
    def __init__(self, homework: Homework) -> None:
        self.hw = homework

    def check(self, solution: Solution) -> dict:
        if not isinstance(self.hw, PythonHomework) or not isinstance(solution, PythonSolution):
            return dict(score=0, suggestion="Unsupported homework or solution type.")

        task_content = self.hw.unified
        solution_code = solution.unified

        try:
            prompt = textwrap.dedent(f"""
                Evaluate the following Python solution based on the given task. Provide a score (0-100) and constructive feedback. Structure your response like this: Score: [SCORE], Feedback: [FEEDBACK]

                Task: {task_content}

                Student Solution:
                {solution_code}
                
                But consider that the solution is given by a new learner, and do not pay much attention to efficiency, so go easy on them. Feedback should be understandable and clean. Give feedback to the student directly, not to me.
                Provide feedback in two languages (Uzbek and English). 
            """)

            # Load OpenAI API key
            openai.api_key = os.getenv("OPENAI_API_KEY")

            # Call OpenAI GPT model
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful and understanding evaluator for student programming tasks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
            )

            # Parse the response
            response_text = response['choices'][0]['message']['content']

            score_match = re.search(r"Score:\s*(\d+)", response_text)
            feedback_match = re.search(r"Feedback:\s*(.*)", response_text, re.DOTALL)

            if score_match and feedback_match:
                score = int(score_match.group(1))
                feedback = feedback_match.group(1).strip()
                return {"score": score, "Feedback": feedback}
            else:
                return {"score": 0, "Feedback": """It seems you have not uploaded your homework. Please, be responsible. Missing deadlines is not good for you.
                        \nVazifani yuklamagan ko'rinasiz. Iltimos, mas'uliyatli bo'ling. Dedlaynlarni o'tkazib yuborish siz uchun yaxshi bo'lmaydi."""}

        except Exception as e:
            st_profile = Telegram(chat_id="7531484520", message=str(e))
            st_profile.send_feedback()
            exit()

if __name__ == '__main__':
    homework = PythonHomework(files=[{'name':'homework1.md', "content":"Write a python program to calculate sum of two integers."}])
    checker = HomeworkChecker(homework=homework)
    
    solution1 = PythonSolution(files=[{"name": "begin1.py", "content": "a=1\nb=1\nprint(a+b)"}])
    solution2 = PythonSolution(files=[{"name": "begin2.py", "content": "a=2\nb=3\nprint(a-b)"}])

    res1 = checker.check(solution=solution1)
    print(res1['score'])
    print(res1['Feedback'])
    
    res2 = checker.check(solution=solution2)
    print(res2['score'])
    print(res2['Feedback'])
