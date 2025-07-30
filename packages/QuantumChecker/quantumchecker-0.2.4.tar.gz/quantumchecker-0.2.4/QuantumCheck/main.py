import logging
import os
from datetime import datetime
from typing import List, Dict, Optional
from .python_evaluator import PythonEvaluator
from .sql_evaluator import SQLEvaluator
from .powerbi_evaluator import PowerBIEvaluator
from .ssis_evaluator import SSISEvaluator


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

    def _setup_logger(self, file_type: str) -> logging.Logger:
        base_log_dir = os.path.join(os.path.dirname(__file__), "logs")
        type_log_dir = os.path.join(base_log_dir, file_type)
        os.makedirs(type_log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_path = os.path.join(type_log_dir, f"evaluation_{timestamp}.log")

        logger = logging.getLogger(f"{file_type}_{timestamp}")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def parse_questions(md_content: str) -> List[str]:
        questions = [q.strip() for q in md_content.strip().split("\n\n") if q.strip()]
        if not questions:
            raise ValueError("No valid questions found in the question content")
        return questions

    def evaluate_from_content(
        self,
        question_content: str,
        answer_path: str,
        api_key: str,
        backup_api_keys: Optional[List[str]] = None,
    ) -> Dict[str, any]:
        if backup_api_keys is None:
            backup_api_keys = []

        try:
            questions = self.parse_questions(question_content)
        except Exception as e:
            base_logger = logging.getLogger("base")
            base_logger.error("Failed to parse question content: %s", str(e))
            raise ValueError(f"Failed to parse question content: {str(e)}")

        answer_path = answer_path.strip()
        _, ext = os.path.splitext(answer_path)
        ext = ext.lower()
        file_type = self.EXTENSION_TO_TYPE.get(ext, "text")

        logger = self._setup_logger(file_type)
        logger.info("Processing answer_path: %s", answer_path)
        logger.info("Extracted extension: %s", ext)
        logger.info("Detected file type: %s for file: %s", file_type, answer_path)

        if not os.path.exists(answer_path):
            logger.error("Answer file not found: %s", answer_path)
            raise FileNotFoundError(f"Answer file not found: {answer_path}")

        def create_evaluator(ftype, key):
            if ftype == "python":
                return PythonEvaluator(key)
            elif ftype == "sql":
                return SQLEvaluator(key)
            elif ftype == "powerbi":
                return PowerBIEvaluator(key)
            elif ftype == "ssis":
                return SSISEvaluator(key)
            else:
                return PythonEvaluator(key)  # default fallback

        keys_to_try = [api_key] + backup_api_keys[:5]  # max 5 backups

        last_exception = None
        for i, key in enumerate(keys_to_try):
            evaluator = create_evaluator(file_type, key)
            try:
                evaluation = evaluator.evaluate(questions, answer_path)
                logger.info(f"Evaluation complete with API key #{i + 1}: Score = {evaluation.get('score')}")
                break
            except Exception as e:
                error_msg = str(e).lower()
                if (
                    "429" in error_msg
                    or "rate limit" in error_msg
                    or "quota exceeded" in error_msg
                    or "daily limit exceeded" in error_msg
                    or "quota" in error_msg
                ):
                    logger.warning(f"API key #{i + 1} limited or quota exceeded. Trying next key if available.")
                    last_exception = e
                    continue
                else:
                    logger.error(f"Evaluation failed with API key #{i + 1}: {str(e)}")
                    raise
        else:
            logger.error("All API keys exhausted and evaluation failed.")
            if last_exception:
                raise last_exception
            else:
                raise RuntimeError("Evaluation failed for unknown reasons.")

        return {
            "mark": evaluation["score"],
            "feedback": evaluation["feedback"]
        }
