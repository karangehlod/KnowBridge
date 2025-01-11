import openai

openai.api_key = "your_openai_api_key"

def summarize_data(graph_data):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following data: {graph_data}",
        max_tokens=4000
    )
    return response.choices[0].text.strip()
