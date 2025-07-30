import json
import logging
import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List
from pdf2image import convert_from_path
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from dotenv import load_dotenv
from PIL import Image
import io
import base64
import PyPDF2  # Added for PDF validation

from .prompts import prompt_text_powerbi

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("../powerbi_evaluator.log"), logging.StreamHandler()]
)

class GeminiFlashModel:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        logger.info("Initializing GeminiFlashModel with model: %s", model_name)
        api_key = os.getenv("GEMINI_API_KEY") or api_key
        if not api_key:
            logger.error("API key not found in environment variables or provided argument")
            raise ValueError("API key not found in .env file or environment variables.")
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        logger.info("GeminiFlashModel initialized successfully with endpoint: %s", self.endpoint)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def evaluate(self, question_answer_pairs: List[Dict[str, str]]) -> Dict[str, any]:
        logger.info("Starting evaluation of %d question-answer pairs", len(question_answer_pairs))
        combined_content = "\n\n".join(
            f"Question {i}:\n{qa['question']}\n\nAnswer {i}:\n{qa['answer']}\n"
            for i, qa in enumerate(question_answer_pairs, 1)
        )
        logger.debug("Prepared combined content for evaluation: %s", combined_content[:100] + "..." if len(combined_content) > 100 else combined_content)

        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt_text_powerbi(combined_content)}]}]}
        logger.info("Sending API request to %s", self.endpoint)
        response = requests.post(f"{self.endpoint}?key={self.api_key}", headers=headers, json=data)

        if response.status_code != 200:
            logger.error("API request failed: Status %d, Response: %s", response.status_code, response.text)
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        response_data = response.json()
        if not response_data.get("candidates"):
            logger.error("API response missing candidates: %s", response_data)
            raise ValueError("No candidates in API response")
        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        logger.info("Received API response, parsing generated text")
        return self._parse_response(generated_text)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def evaluate_visuals(self, question: str, image_folder: str) -> Dict[str, any]:
        logger.info("Starting visual evaluation for question: %s", question)
        folder_path = Path(image_folder)
        images = list(folder_path.glob("*.png"))[:3]
        if not images:
            logger.error("No PNG images found in folder: %s", image_folder)
            raise ProcessingError(f"No PNG images found in {image_folder}")
        logger.info("Found %d PNG images for evaluation: %s", len(images), [img.name for img in images])

        prompt = (
            "Evaluate the Power BI report visuals based on the given task.\n\n"
            f"Task: {question}\n\n"
            f"Screenshots: {[str(img.name) for img in images]}\n\n"
            "Focus on:\n"
            "- Clarity: Are visuals clear and easy to understand?\n"
            "- Appropriateness: Are visual types suitable for the data and task?\n"
            "- Layout and Design: Is the layout organized with logical flow?\n"
            "- Readability: Are labels, titles, and legends clear and not overcrowded?\n"
            "- Color Usage: Are colors effective, consistent, and accessible?\n"
            "- Interactivity: (If visible) Do slicers or filters enhance usability?\n\n"
            "Do not consider DAX, data sources, or advanced efficiency.\n"
            "Provide feedback in a supportive manner for beginners.\n\n"
            "Structure as: Score: [SCORE], Feedback: [FEEDBACK]"
        )
        parts = [{"text": prompt}]
        for img in images:
            logger.debug("Processing image: %s", img.name)
            try:
                with Image.open(img) as pil_img:
                    if pil_img.size[0] == 0 or pil_img.size[1] == 0:
                        logger.error("Invalid image dimensions for %s", img.name)
                        raise ProcessingError(f"Invalid image dimensions for {img.name}")
                    pil_img.thumbnail((1024, 1024))
                    img_buffer = io.BytesIO()
                    pil_img.save(img_buffer, format="PNG")
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                        }
                    })
            except Exception as e:
                logger.error("Failed to process image %s: %s", img.name, str(e))
                raise ProcessingError(f"Failed to process image {img.name}: {str(e)}")
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": parts}]}
        logger.info("Sending visual evaluation API request to %s", self.endpoint)
        response = requests.post(f"{self.endpoint}?key={self.api_key}", headers=headers, json=data)
        if response.status_code != 200:
            logger.error("Visual API request failed: Status %d, Response: %s", response.status_code, response.text)
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        response_data = response.json()
        if not response_data.get("candidates"):
            logger.error("Visual API response missing candidates: %s", response_data)
            raise ValueError("No candidates in API response")
        output_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        logger.info("Received visual API response, parsing output")
        score_match = re.search(r"Score:\s*(\d+)(?:/100)?", output_text)
        feedback_match = re.search(r"Feedback:\s*(.*)", output_text, re.DOTALL)
        result = {
            "score": int(score_match.group(1)) if score_match else 0,
            "feedback": feedback_match.group(1).strip() if feedback_match else "No visual feedback generated",
            "issues": []
        }
        if not score_match:
            result["issues"].append("Failed to parse score from visual API response")
            logger.warning("Failed to parse score from visual API response")
        if not feedback_match:
            result["issues"].append("Failed to parse feedback from visual API response")
            logger.warning("Failed to parse feedback from visual API response")
        logger.info("Visual evaluation completed: Score=%d, Feedback=%s", result["score"], result["feedback"][:50] + "..." if len(result["feedback"]) > 50 else result["feedback"])
        return result

    def _parse_response(self, text: str) -> Dict[str, any]:
        logger.info("Parsing API response text")
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
                        logger.info("Parsed score: %d", result["score"])
                    except ValueError:
                        result["issues"].append("Failed to parse score from API response")
                        logger.error("Failed to parse score from response: %s", line)
                        continue
                elif score_found:
                    feedback_lines.append(line)
            if feedback_lines:
                result["feedback"] = "\n".join(feedback_lines).strip()
                logger.debug("Parsed feedback: %s", result["feedback"][:50] + "..." if len(result["feedback"]) > 50 else result["feedback"])
            return result
        except Exception as e:
            result["issues"].append(str(e))
            logger.error("Error parsing response: %s", str(e))
            return result

class PowerBIProcessor:
    def extract_datamodel(self, pbit_file_path: str) -> Dict:
        logger.info("Extracting data model from PBIT file: %s", pbit_file_path)
        if not os.path.exists(pbit_file_path):
            logger.error("PBIT file does not exist: %s", pbit_file_path)
            raise ProcessingError(f"PBIT file not found: {pbit_file_path}")
        folder_path = os.path.dirname(pbit_file_path)
        file_name = os.path.splitext(os.path.basename(pbit_file_path))[0]
        zip_file = os.path.join(folder_path, f"{file_name}.zip")
        export_path = os.path.join(folder_path, "export")
        logger.debug("Cleaning up temporary files: %s, %s", zip_file, export_path)
        self._cleanup(zip_file, export_path)
        try:
            logger.info("Renaming PBIT to ZIP: %s -> %s", pbit_file_path, zip_file)
            os.rename(pbit_file_path, zip_file)
            if not zipfile.is_zipfile(zip_file):
                logger.error("File is not a valid ZIP: %s", zip_file)
                raise ProcessingError(f"File is not a valid ZIP: {zip_file}")
            logger.info("Extracting ZIP contents to: %s", export_path)
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(export_path)
            schema_path = os.path.join(export_path, "DataModelSchema")
            txt_path = os.path.join(export_path, "DataModelSchema.txt")
            logger.debug("Renaming schema file: %s -> %s", schema_path, txt_path)
            os.rename(schema_path, txt_path)
            logger.info("Reading DataModelSchema file: %s", txt_path)
            with open(txt_path, "r", encoding="utf-16-le") as file:
                data = json.load(file)
                logger.info("Successfully extracted data model from PBIT file")
                return data
        except UnicodeDecodeError as e:
            logger.error("Failed to decode DataModelSchema: %s", str(e))
            raise ProcessingError(f"Invalid encoding in DataModelSchema: {e}")
        except Exception as e:
            logger.error("Failed to extract DataModelSchema: %s", str(e))
            raise ProcessingError(f"Failed to extract DataModelSchema: {e}")
        finally:
            logger.debug("Cleaning up temporary files after extraction")
            self._cleanup(zip_file, export_path)

    def extract_model_data(self, data: Dict) -> Dict:
        logger.info("Extracting model data from data model")
        try:
            tables = data.get("model", {}).get("tables", [])
            relationships = data.get("model", {}).get("relationships", [])
            result = {
                "Calculated Measures": self._get_measures(tables),
                "Tables": self._get_tables_and_columns(tables),
                "Relationships": self._get_relationships(relationships)
            }
            logger.info("Extracted model data: %d measures, %d tables, %d relationships",
                        len(result["Calculated Measures"]), len(result["Tables"]), len(result["Relationships"]))
            return result
        except Exception as e:
            logger.error("Failed to extract model data: %s", str(e))
            raise ProcessingError(f"Failed to extract model data: {e}")

    def process_pdf(self, pdf_path: str, output_dir: str = "outputimages", num_pages: int = 3) -> List[str]:
        logger.info("Processing PDF file: %s", pdf_path)
        try:
            if not os.path.exists(pdf_path):
                logger.error("PDF file does not exist: %s", pdf_path)
                raise ProcessingError(f"PDF file not found: {pdf_path}")
            # Validate PDF
            try:
                with open(pdf_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    if len(pdf_reader.pages) == 0:
                        logger.error("PDF is empty: %s", pdf_path)
                        raise ProcessingError(f"PDF is empty: {pdf_path}")
                    logger.info("PDF validated, contains %d pages", len(pdf_reader.pages))
            except Exception as e:
                logger.error("Invalid PDF file: %s", str(e))
                raise ProcessingError(f"Invalid PDF file: {str(e)}")
            logger.debug("Creating output directory: %s", output_dir)
            os.makedirs(output_dir, exist_ok=True)
            logger.info("Converting PDF pages to images (max %d pages)", num_pages)
            pages = convert_from_path(pdf_path, first_page=1, last_page=min(num_pages, len(pdf_reader.pages)))
            if not pages:
                logger.error("No pages converted from PDF: %s", pdf_path)
                raise ProcessingError(f"No pages converted from PDF: {pdf_path}")
            image_paths = []
            for i, page in enumerate(pages):
                image_path = os.path.join(output_dir, f"page_{i + 1}.png")
                logger.debug("Saving page %d as PNG: %s", i + 1, image_path)
                page.save(image_path, "PNG")
                image_paths.append(image_path)
            logger.info("Successfully processed %d pages from PDF", len(image_paths))
            return image_paths
        except Exception as e:
            logger.error("Failed to process PDF: %s", str(e))
            raise ProcessingError(f"Failed to process PDF: {str(e)}")
        finally:
            logger.debug("Not removing PDF file to allow debugging: %s", pdf_path)

    def extract_zip(self, zip_path: str, extract_path: str) -> tuple[str, str | None]:
        logger.info("Extracting ZIP file: %s", zip_path)
        try:
            if not os.path.exists(zip_path):
                logger.error("ZIP file does not exist: %s", zip_path)
                raise ProcessingError(f"ZIP file not found: {zip_path}")
            if not zipfile.is_zipfile(zip_path):
                logger.error("File is not a valid ZIP: %s", zip_path)
                raise ProcessingError(f"File is not a valid ZIP: {zip_path}")
            logger.debug("Creating extraction directory: %s", extract_path)
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                logger.info("Extracting ZIP contents to: %s", extract_path)
                zip_ref.extractall(extract_path)
            pbit_files = list(Path(extract_path).glob("*.pbit"))
            pdf_files = list(Path(extract_path).glob("*.pdf"))
            logger.info("Found %d PBIT files and %d PDF files in ZIP", len(pbit_files), len(pdf_files))
            if not pbit_files:
                logger.error("No PBIT files found in ZIP")
                raise ProcessingError("ZIP file must contain at least one .pbit file")
            if len(pbit_files) > 1:
                logger.error("Multiple PBIT files found in ZIP: %s", [str(p) for p in pbit_files])
                raise ProcessingError("ZIP file contains multiple .pbit files")
            pdf_path = str(pdf_files[0]) if pdf_files else None
            logger.info("Extracted PBIT file: %s, PDF file: %s", str(pbit_files[0]), pdf_path)
            return str(pbit_files[0]), pdf_path
        except Exception as e:
            logger.error("Failed to extract ZIP file: %s", str(e))
            raise ProcessingError(f"Failed to extract ZIP file: {e}")

    @staticmethod
    def _get_measures(tables: List[Dict]) -> List[Dict]:
        logger.debug("Extracting measures from tables")
        measures = []
        for table in tables:
            if "measures" in table:
                for measure in table["measures"]:
                    measures.append({
                        "Table": table["name"],
                        "Name": measure["name"],
                        "Expression": " ".join(measure.get("expression", "")) if isinstance(measure.get("expression"), list) else measure.get("expression", ""),
                        "FormatString": measure.get("formatString", "")
                    })
        logger.debug("Extracted %d measures", len(measures))
        return measures

    @staticmethod
    def _get_tables_and_columns(tables: List[Dict]) -> List[Dict]:
        logger.debug("Extracting tables and columns")
        table_info = []
        for table in tables:
            columns = [{"Column Name": col["name"], "Data Type": col.get("dataType", "Unknown"), "Source Column": col.get("sourceColumn", "N/A"), "Calculated": col.get("type") == "calculated"} for col in table.get("columns", [])]
            expressions = [part["source"]["expression"] for part in table.get("partitions", []) if part["source"].get("expression")]
            table_info.append({"Table Name": table["name"], "Columns": columns, "Expressions": expressions})
        logger.debug("Extracted %d tables", len(table_info))
        return table_info

    @staticmethod
    def _get_relationships(relationships: List[Dict]) -> List[Dict]:
        logger.debug("Extracting relationships")
        result = [{"From Table": rel["fromTable"], "From Column": rel["fromColumn"], "To Table": rel["toTable"], "To Column": rel["toColumn"], "Join Behavior": rel.get("joinOnDateBehavior", "N/A")} for rel in relationships]
        logger.debug("Extracted %d relationships", len(result))
        return result

    @staticmethod
    def _cleanup(*paths: str):
        logger.debug("Cleaning up paths: %s", paths)
        for path in paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    logger.debug("Removing file: %s", path)
                    os.remove(path)
                else:
                    logger.debug("Removing directory: %s", path)
                    shutil.rmtree(path, ignore_errors=True)
        logger.debug("Cleanup completed")

class PowerBIEvaluator:
    def __init__(self, api_key: str):
        logger.info("Initializing PowerBIEvaluator")
        self.api_key = api_key
        self.model = GeminiFlashModel(api_key)
        self.processor = PowerBIProcessor()
        logger.info("PowerBIEvaluator initialized successfully")

    def evaluate(self, questions: List[str], answer_path: str) -> Dict[str, any]:
        logger.info("Starting evaluation for file: %s with %d questions", answer_path, len(questions))
        try:
            _, ext = os.path.splitext(answer_path)
            ext = ext.lower()
            extract_path = os.path.join(os.path.dirname(answer_path), "temp_extract")
            pbit_path = None
            pdf_path = None

            # Handle input file type
            logger.debug("Checking file extension: %s", ext)
            if ext == ".zip":
                logger.info("Processing ZIP file")
                pbit_path, pdf_path = self.processor.extract_zip(answer_path, extract_path)
            elif ext == ".pbit":
                logger.info("Processing PBIT file directly")
                pbit_path = answer_path
                pdf_path = None
            else:
                logger.error("Invalid file type: %s", ext)
                return {
                    "score": 0,
                    "feedback": f"Invalid file type: {ext}. Expected .pbit or .zip",
                    "issues": ["Invalid file type"],
                    "recommendations": []
                }

            try:
                # Extract and process the data model from .pbit
                logger.info("Extracting data model from PBIT")
                data_model = self.processor.extract_datamodel(pbit_path)
                logger.info("Extracting model data")
                model_data = self.processor.extract_model_data(data_model)
                answers = [json.dumps(model_data)] * len(questions)
                logger.info("Evaluating DAX with %d question-answer pairs", len(questions))
                dax_result = self.model.evaluate([{"question": q, "answer": a} for q, a in zip(questions, answers)])

                # Initialize result with DAX evaluation
                result = {
                    "score": dax_result["score"],
                    "feedback": f"DAX Feedback:\n{dax_result['feedback']}",
                    "issues": dax_result["issues"],
                    "recommendations": dax_result["recommendations"]
                }
                logger.info("DAX evaluation completed: Score=%d", dax_result["score"])

                # Process PDF and evaluate visuals if present
                if pdf_path:
                    logger.info("Processing PDF for visual evaluation: %s", pdf_path)
                    try:
                        image_paths = self.processor.process_pdf(pdf_path)
                        if not image_paths:
                            logger.error("No images generated from PDF: %s", pdf_path)
                            raise ProcessingError("No images generated from PDF")
                        logger.info("Evaluating visuals with question: %s", questions[0])
                        visual_result = self.model.evaluate_visuals(questions[0], "outputimages")
                        result["score"] = (dax_result["score"] + visual_result["score"]) // 2
                        result["feedback"] += f"\n\nVisual Feedback:\n{visual_result['feedback']}"
                        result["issues"].extend([f"Visual: {i}" for i in visual_result.get("issues", [])])
                        result["recommendations"].extend(visual_result.get("recommendations", []))
                        logger.info("Visual evaluation completed: Score=%d", visual_result["score"])
                    except ProcessingError as e:
                        logger.warning("Failed to process PDF, proceeding with DAX evaluation only: %s", str(e))
                        result["issues"].append(f"Visual evaluation skipped: {str(e)}")
                        result["recommendations"].append("Ensure a valid PDF with Power BI visuals is provided")
                    except Exception as e:
                        logger.error("Unexpected error during visual evaluation: %s", str(e))
                        result["issues"].append(f"Visual evaluation failed: {str(e)}")
                        result["recommendations"].append("Check PDF file and API connectivity")
                else:
                    logger.info("No PDF provided, skipping visual evaluation")

                logger.info("Evaluation completed successfully")
                return result
            finally:
                logger.debug("Cleaning up temporary files and directories")
                self.processor._cleanup(extract_path, "outputimages")
        except Exception as e:
            logger.exception("Failed to evaluate Power BI file %s: %s", answer_path, str(e))
            self.processor._cleanup(extract_path, "outputimages")
            return {
                "score": 0,
                "feedback": f"Error processing file: {str(e)}",
                "issues": [str(e)],
                "recommendations": ["Check file formats and API connectivity", "Review logs for detailed errors"]
            }

class ProcessingError(Exception):
    pass