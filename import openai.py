import openai

openai.api_key = "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"  # Replace with your new key

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]