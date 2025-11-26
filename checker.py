import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


load_dotenv(dotenv_path=".env")


class HomeworkChecker:
    def __init__(self, homework: str) -> None:
        self.homework = homework
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # e.g. "gpt-35-turbo" or "gpt-4o"
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  # e.g. "2024-05-01-preview"
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0  # deterministic scoring
        )


    def check(self, solution: str) -> dict:
        # Prompt instructing model to score and give feedback
        prompt = f"""
You are an expert Machine Learning Python instructor.

### Homework Task:
{self.homework}

### Student Solution:
{solution}

---

Evaluate the solution carefully and return a JSON dictionary only:

{{
  "score": <integer from 0 to 100>,
  "feedback": "<detailed feedback in markdown format>"
}}

Scoring Criteria:
- Correctness of logic
- Code accuracy
- Explanation clarity
- Completeness
- ML concept understanding

Important rules:
- Be strict but fair
- Provide actionable suggestions
- Highlight mistakes clearly
- Praise good parts too
- Return JSON only, no extra text
"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()

            # Sometimes model may wrap JSON in markdown — remove it if present
            if content.startswith("```"):
                content = content.split("```")[-2]

            # Convert to dict safely
            result = json.loads(content)

        except Exception as e:
            # fallback result if model fails to output valid JSON
            return {
                "score": 0,
                "feedback": f"Error during LLM evaluation: {str(e)}"
            }

        return result


if __name__ == '__main__':
    from lesson import Lesson
    from sheet import SpreadSheet

    SHEET_URL = os.getenv('SHEET_URL')

    # Assuming that Telegram bot provided this
    user_id = '1'
    lesson_number = 3
    subject = 'ml'


    lesson = Lesson(lesson_number=lesson_number, subject=subject)
    homework: str = lesson.homework # Markdown format

    sheet = SpreadSheet(sheet_url=SHEET_URL)
    student = sheet.get_student_by_id(telegram_id=user_id)
    solution: str = student.get_solution(lesson_number=lesson_number, subject=subject) # Markdown format
    
    checker = HomeworkChecker(homework=homework)

    res = checker.check(solution=solution)
    print(res['score'])
    print(res['feedback'])

    

