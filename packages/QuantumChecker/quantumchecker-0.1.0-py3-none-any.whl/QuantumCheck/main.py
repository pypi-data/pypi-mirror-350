import logging
import os
from typing import List, Dict
from python_evaluator import PythonEvaluator
from sql_evaluator import SQLEvaluator
from powerbi_evaluator import PowerBIEvaluator
from ssis_evaluator import SSISEvaluator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HomeworkEvaluator:
    EXTENSION_TO_TYPE = {
        ".py": "python",
        ".sql": "sql",
        ".zip": "powerbi",
        ".dtsx": "ssis",
        ".DTSX": "ssis",
        ".txt": "text",
        ".md": "text"
    }

    @staticmethod
    def parse_questions(md_content: str) -> List[str]:
        questions = [q.strip() for q in md_content.strip().split("\n\n") if q.strip()]
        if not questions:
            raise ValueError("No valid questions found in the question content")
        return questions

    def evaluate_from_content(self, question_content: str, answer_path: str, api_key: str) -> Dict[str, any]:
        try:
            questions = self.parse_questions(question_content)
        except Exception as e:
            logger.error("Failed to parse question content: %s", str(e))
            raise ValueError(f"Failed to parse question content: {str(e)}")

        answer_path = answer_path.strip()
        logger.info("Processing answer_path: %s", answer_path)
        _, ext = os.path.splitext(answer_path)
        ext = ext.lower()
        logger.info("Extracted extension: %s", ext)
        file_type = self.EXTENSION_TO_TYPE.get(ext, "text")
        logger.info("Detected file type: %s for file: %s", file_type, answer_path)

        if not os.path.exists(answer_path):
            logger.error("Answer file not found: %s", answer_path)
            raise FileNotFoundError(f"Answer file not found: {answer_path}")

        if file_type == "python":
            evaluator = PythonEvaluator(api_key)
            evaluation = evaluator.evaluate(questions, answer_path)
        elif file_type == "sql":
            evaluator = SQLEvaluator(api_key)
            evaluation = evaluator.evaluate(questions, answer_path)
        elif file_type == "powerbi":
            evaluator = PowerBIEvaluator(api_key)
            evaluation = evaluator.evaluate(questions, answer_path)
        elif file_type == "ssis":
            evaluator = SSISEvaluator(api_key)
            evaluation = evaluator.evaluate(questions, answer_path)
        else:
            logger.warning("Unrecognized file type '%s', defaulting to text (Python parser)", file_type)
            evaluator = PythonEvaluator(api_key)
            evaluation = evaluator.evaluate(questions, answer_path)

        return {
            "mark": evaluation["score"],
            "feedback": evaluation["feedback"]
        }


