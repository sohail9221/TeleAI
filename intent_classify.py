import ollama

def get_user_intent(query: str) -> str:
    """
    Classifies the user's query into one of the predefined intents:
    ['Menu', 'GeneralInfo', 'Reservations', 'OrderTracking'].

    :param model: The name of the Ollama model to use.
    :param query: The user's input query.
    :return: Identified intent as a string.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that classifies user queries into specific intent categories "
                "to help retrieve relevant information from a database. Your task is to determine which category the "
                "query belongs to from the following options:\n\n"
                "- **Menu**: If the query is about food items, their prices, ingredients, or availability.\n"
                "- **GeneralInfo**: If the query is about restaurant details like timings, location, policies, or general FAQs.\n"
                "- **Reservations**: If the query is about booking a table, reservation timings, or availability.\n"
                "- **OrderTracking**: If the query is about checking the status of an order, whether it is in preparation, ready, or out for delivery.\n\n"
                "Your response must strictly be one of the four categories: ['Menu', 'GeneralInfo', 'Reservations', 'OrderTracking']."
                "Do not provide explanations—only return the category name and name only.always choose one even if not sure. "
            )
        },
        {"role": "user", "content": query}
    ]

    response = ollama.chat(model="deepseek-r1:1.5b", messages=messages)
    return response['message']['content'].strip()
