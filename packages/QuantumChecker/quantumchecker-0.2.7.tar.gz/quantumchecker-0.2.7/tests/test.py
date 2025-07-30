from pprint import pprint

from QuantumCheck import HomeworkEvaluator

if __name__ == "__main__":
    evaluator = HomeworkEvaluator()

    primary_api_key = "AIzaSyD0ptgEixhLLjCWjkyxhqDsUzO16ytQq2c"
    question = "Create a dashboard"

    backup_keys = [
        "BACKUP_KEY_1",
        "BACKUP_KEY_2",
        "BACKUP_KEY_3",
        "BACKUP_KEY_4",
        "BACKUP_KEY_5",
    ]

    result = evaluator.evaluate_from_content(
        question_content="Fuck You",
        answer_path="../tests/answer/real.zip",
        api_key=primary_api_key,
        backup_api_keys=backup_keys
    )

    pprint(result)





