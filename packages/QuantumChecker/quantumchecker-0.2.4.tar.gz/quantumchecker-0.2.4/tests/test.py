from QuantumCheck import HomeworkEvaluator

if __name__ == "__main__":
    evaluator = HomeworkEvaluator()

    primary_api_key = "AIzaSyD0ptgEixhLLjCWjkyxhqDsUzO16ytQq2c"
    question = "How to write print in python"

    backup_keys = [
        "BACKUP_KEY_1",
        "BACKUP_KEY_2",
        "BACKUP_KEY_3",
        "BACKUP_KEY_4",
        "BACKUP_KEY_5",
    ]

    result = evaluator.evaluate_from_content(
        question_content="How to write print in python",
        answer_path="../tests/answer/answer.py",
        api_key=primary_api_key,
        backup_api_keys=backup_keys
    )

    print(result)





