import logging
import requests
from prompts import prompt_text_python
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class GeminiFlashModel:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def evaluate(self, question_answer_pairs: List[Dict[str, str]]) -> Dict[str, any]:
        logger.info("Starting evaluation of %d Python question-answer pairs", len(question_answer_pairs))

        combined_content = "\n\n".join(
            f"Question {i}:\n{qa['question']}\n\nAnswer {i}:\n{qa['answer']}\n"
            for i, qa in enumerate(question_answer_pairs, 1)
        )


        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt_text_python(combined_content)}]}]}

        response = requests.post(f"{self.endpoint}?key={self.api_key}", headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")

        response_data = response.json()
        if not response_data.get("candidates"):
            raise ValueError("No candidates in API response")

        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_response(generated_text)

    def _parse_response(self, text: str) -> Dict[str, any]:
        result = {"score": 0, "feedback": "Evaluation not returned by API.", "issues": [], "recommendations": []}
        try:
            lines = text.split("\n")
            score_found = False
            feedback_lines = []
            for line in lines:
                line = line.strip()
                if not score_found and line.startswith("OVERALL SCORE:") and "/100" in line:
                    try:
                        result["score"] = int(line.split(":")[1].split("/")[0].strip())
                        score_found = True
                    except ValueError:
                        result["issues"].append("Failed to parse score from API response")
                        continue
                elif score_found:
                    feedback_lines.append(line)
            if feedback_lines:
                result["feedback"] = "\n".join(feedback_lines).strip()
            return result
        except Exception as e:
            result["issues"].append(str(e))
            return result

class PythonAnswerParser:
    @staticmethod
    def parse(content: str, question_count: int) -> List[str]:
        answers = [a.strip() for a in content.strip().split("\n\n") if a.strip()]
        if not answers:
            logger.warning("No valid answers found, returning placeholders")
        return answers + ["No answer provided."] * (question_count - len(answers))

class PythonEvaluator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = GeminiFlashModel(api_key)

    def evaluate(self, questions: List[str], answer_path: str) -> Dict[str, any]:
        try:
            with open(answer_path, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            logger.error("Failed to read answer file %s: %s", answer_path, str(e))
            return {"score": 0, "feedback": f"Error reading file: {str(e)}", "issues": [str(e)]}

        answers = PythonAnswerParser.parse(content, len(questions))
        if len(answers) != len(questions):
            logger.warning("Mismatch: %d questions but %d answers", len(questions), len(answers))

        return self.model.evaluate([{"question": q, "answer": a} for q, a in zip(questions, answers)])