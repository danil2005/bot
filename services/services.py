def create_questionnaire_text(data: dict) -> str:
    return (
        "Вот ваша анкета:\n\n"
        f"Имя - {data['name']}\n"
        f"Возраст - {data['old']}\n"
        f"Пол - {data['gender']}\n"
        f"Рост - {data['height']}\n"
        f"Вес - {data['weight']}\n"
        "\nВсе верно?"
    )
