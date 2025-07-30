import logging
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .prompts import prompt_text_ssis

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
        logger.info("Starting evaluation of %d SSIS question-answer pairs", len(question_answer_pairs))

        combined_content = "\n\n".join(
            f"Question {i}:\n{qa['question']}\n\nAnswer {i}:\n{qa['answer']}\n"
            for i, qa in enumerate(question_answer_pairs, 1)
        )

        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt_text_ssis(combined_content)}]}]}

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

class SSISAnswerParser:
    @staticmethod
    def parse(filepath: str, question_count: int) -> List[str]:
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            summary = []

            for elem in root.iter():
                if "Executable" in elem.tag or "task" in elem.tag.lower():
                    task_name = elem.get("Name", "Unnamed Task")
                    task_type = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                    summary.append(f"Task: {task_name} ({task_type})")

            for conn in root.findall(".//DTS:ConnectionManager", namespaces={"DTS": "www.microsoft.com/SqlServer/Dts"}):
                conn_name = conn.get("DTS:ObjectName", "Unnamed Connection")
                conn_type = conn.find(".//DTS:ObjectData", namespaces={"DTS": "www.microsoft.com/SqlServer/Dts"})
                if conn_type is not None:
                    if "FlatFileConnectionManager" in conn_type.tag:
                        file_path = conn_type.find(".//Property[@Name='FileName']").text
                        columns = [col.find(".//Property[@Name='Name']").text for col in conn_type.findall(".//Column")]
                        summary.append(f"Flat File Connection: {conn_name} (File: {file_path}, Columns: {', '.join(columns)})")
                    elif "OleDbConnectionManager" in conn_type.tag:
                        conn_string = conn_type.find(".//Property[@Name='ConnectionString']").text
                        summary.append(f"SQL Server Connection: {conn_name} (ConnectionString: {conn_string})")

            for component in root.findall(".//component"):
                comp_name = component.get("name", "Unnamed Component")
                comp_type = component.get("componentClassID", "").split(".")[-1]
                if comp_type == "FlatFileSource":
                    summary.append(f"Flat File Source: {comp_name}")
                elif comp_type == "DataConversion":
                    output_cols = [col.get("name") for col in component.findall(".//outputColumn")]
                    summary.append(f"Data Conversion: {comp_name} (Outputs: {', '.join(output_cols)})")
                elif comp_type == "OLEDBDestination":
                    table_name = component.find(".//property[@name='TableName']").text
                    summary.append(f"SQL Server Destination: {comp_name} (Table: {table_name})")

            for path in root.findall(".//path"):
                start_id = path.get("startId", "Unknown")
                end_id = path.get("endId", "Unknown")
                summary.append(f"Data Flow Path: {start_id} -> {end_id}")

            for log_provider in root.findall(".//DTS:LogProvider", namespaces={"DTS": "www.microsoft.com/SqlServer/Dts"}):
                log_name = log_provider.get("DTS:ObjectName", "Unnamed Log")
                log_file = log_provider.get("DTS:ConfigString", "Unknown")
                events = [event.text.strip() for event in log_provider.findall(".//LogEvent")]
                summary.append(f"Log Provider: {log_name} (File: {log_file}, Events: {', '.join(events)})")

            combined_summary = "\n".join(summary)[:2000] or "No components found in SSIS package"
            logger.info("Parsed SSIS summary: %s", combined_summary)
            return [combined_summary] * question_count
        except ET.ParseError as e:
            logger.error("Invalid SSIS package file: %s", str(e))
            return [f"Invalid SSIS package file: {str(e)}"] * question_count

class SSISEvaluator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = GeminiFlashModel(api_key)

    def evaluate(self, questions: List[str], answer_path: str) -> Dict[str, any]:
        answers = SSISAnswerParser.parse(answer_path, len(questions))
        if len(answers) != len(questions):
            logger.warning("Mismatch: %d questions but %d answers", len(questions), len(answers))
        return self.model.evaluate([{"question": q, "answer": a} for q, a in zip(questions, answers)])