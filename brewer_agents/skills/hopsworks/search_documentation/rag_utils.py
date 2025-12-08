from openai import OpenAI


def get_embedding(text: str, openai_client: OpenAI) -> list[float] | None:
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    except Exception:
        return None
