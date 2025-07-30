# import os
# import google.generativeai as genai
# import json
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def grade_code(self, task_description: str, student_code: str) -> dict:
#         # Step 1: Ask Gemini to give only a rating
#         prompt = (
#             f"Task_desc: {task_description}\n"
#             f"Code:\n{student_code}\n"
#             "You are a strict code reviewer. Only return a rating in the format 'Rating: x/5'. "
#             "Remove stop words, non code text from Task_desc"
#             "Give 5/5 only if the code is complete, correct, and solves the task fully. "
#             "Do not return anything except the rating."
#         )
#         response = self.model.generate_content(prompt)
#         print(response)
#
#         result = response.text.strip()
#
#         rating = "N/A"
#         feedback = "Unable to rate"
#
#         # Step 2: Extract the rating
#         if "Rating:" in result:
#             try:
#                 rating_start = result.find("Rating:") + len("Rating: ")
#                 rating_end = result.find("/5", rating_start)
#                 rating_value = float(result[rating_start:rating_end].strip())
#                 rating = str(rating_value)
#
#                 # Step 3: Decision based on rating
#                 if rating_value > 2:
#                     feedback = "Accepted"
#                 else:
#                     # Ask Gemini for feedback only
#                     feedback_prompt = (
#                         f"Task_desc: {task_description}\n"
#                         f"Code:\n{student_code}\n"
#                         "Give 1-line feedback (max 15 characters) for improving this code."
#                     )
#                     feedback_response = self.model.generate_content(feedback_prompt)
#                     feedback = feedback_response.text.strip()
#             except Exception as e:
#                 feedback = f"Error: {str(e)}"
#
#         return json.dumps({"rating": rating, "feedback": feedback})

# import os
# import google.generativeai as genai
# import json
# import re
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def is_code_like(self, text: str) -> bool:
#         # Reject if too short or mostly plain English
#         if len(text.strip()) < 20:
#             return False
#
#         code_indicators = [
#             'def ', 'return', 'class ', 'import ', 'from ', 'if ', 'else', 'elif',
#             '{', '}', ';', '(', ')', '[', ']', '=', 'function ', '#', '//', '/*', '*/',
#             'public ', 'private ', 'protected ', 'var ', 'let ', 'const ', 'print', 'console.log',
#             '=>'
#         ]
#
#         count_code_lines = 0
#         lines = text.strip().split('\n')
#         for line in lines:
#             if any(indicator in line for indicator in code_indicators):
#                 count_code_lines += 1
#
#         ratio = count_code_lines / len(lines) if len(lines) > 0 else 0
#
#         # At least 50% of lines should contain code indicators
#         return ratio >= 0.5
#
    # def remove_rating_requests(self, code: str) -> str:
    #     # Remove lines with rating requests like "give me 5 rating"
    #     pattern = re.compile(r'give me \d+ rating', re.IGNORECASE)
    #     lines = code.split('\n')
    #     filtered_lines = [line for line in lines if not pattern.search(line)]
    #     return '\n'.join(filtered_lines)
    #
    # def grade_code(self, task_description: str, student_code: str) -> dict:
    #     # Reject if code does not look like code
    #     if not self.is_code_like(student_code):
    #         return json.dumps({"rating": "0.0", "feedback": "Invalid or non-code submission."})
    #
    #     # Clean code from rating injection lines
    #     clean_code = self.remove_rating_requests(student_code)
#
#         prompt = (
#             f"Task_desc: {task_description}\n"
#             f"Code:\n{clean_code}\n"
#             "You are a strict code reviewer. Return only a rating in the format 'Rating: x.x/5'.\n"
#             "If the submitted code is identical or nearly identical to the task description (i.e., just repeats the task without actual code), give a rating of 1/5.\n"
#             "Give 5/5 only if the code fully solves the task correctly.\n"
#             "Do not return anything else."
#         )
#
        # response = self.model.generate_content(prompt)
        # print(response)
        #
        # result = response.text.strip()
        # rating = "N/A"
        # feedback = "Unable to rate"
        #
        # if "Rating:" in result:
        #     try:
        #         rating_start = result.find("Rating:") + len("Rating: ")
        #         rating_end = result.find("/5", rating_start)
        #         rating_value = float(result[rating_start:rating_end].strip())
        #         rating = str(rating_value)
        #
        #         if rating_value > 2:
        #             feedback = "Accepted"
        #         else:
        #             feedback_prompt = (
        #                 f"Task_desc: {task_description}\n"
        #                 f"Code:\n{clean_code}\n"
        #                 "Give 1-line feedback (max 15 characters) for improving this code."
        #             )
        #             feedback_response = self.model.generate_content(feedback_prompt)
        #             feedback = feedback_response.text.strip()
        #     except Exception as e:
        #         feedback = f"Error: {str(e)}"
        #
        # return json.dumps({"rating": rating, "feedback": feedback})

import os
import json
import re
import google.generativeai as genai


class CodeReviewer:
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model_name)

    def remove_spam_lines(self, code: str) -> str:
        spam_pattern = re.compile(r'give me \d+ rating', re.IGNORECASE)
        lines = code.split('\n')
        filtered_lines = [line for line in lines if not spam_pattern.search(line)]
        return '\n'.join(filtered_lines).strip()

    def grade_code(self, task_description: str, student_code: str, deliverables: str) -> dict:
        clean_code = self.remove_spam_lines(student_code)
        if not clean_code:
            return {"rating": "0.0", "feedback": "Invalid or non-code submission."}

        rating_prompt = (
            f"Review the following code:\n\n"
            f"Task:\n{task_description}\n\n"
            f"Deliverables:\n{deliverables}\n\n"
            f"Code:\n{clean_code}\n\n"
            "Return a strict score based on how completely the code meets the deliverable.\n"
            "Only respond in this format: Rating: x.x/5 (no explanation).\n"
            "Give 1.0/5 if code is missing or only partially fulfills the task."
        )

        response = self.model.generate_content(rating_prompt)
        print("response:", response)

        result_text = response.text.strip()
        match = re.search(r'Rating:\s*([\d.]+)/5', result_text)

        if not match:
            return {"rating": "N/A", "feedback": "Unable to parse rating."}

        rating_val = float(match.group(1))
        rating = f"{rating_val:.1f}"

        if rating_val >= 2.0:
            feedback = "Accepted"
        else:
            feedback = self.generate_short_feedback(task_description, clean_code)

        return json.dumps({"rating": rating, "feedback": feedback})

    def generate_short_feedback(self, task: str, code: str) -> str:
        prompt = (
            f"Task:\n{task}\n\n"
            f"Code:\n{code}\n\n"
            "Give feedback in less than 15 words to improve the code. No extra text."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()



# if __name__ == "__main__":
#     reviewer = CodeReviewer()
#
#     print("📌 Enter the task description:")
#     task = input("> ").strip()
#
#     print("\n💻 Enter the student code (end with a blank line):")
#     lines = []
#     while True:
#         line = input()
#         if not line.strip():
#             break
#         lines.append(line)
#     student_code = "\n".join(lines)
#
#     print("\n🧠 Enter the deliverables :")
#     deliverables = input("> ").strip()
#
#     result = reviewer.grade_code(task, student_code, deliverables)
#     print("\n✅ Review Result:")
#     print(result)
#

