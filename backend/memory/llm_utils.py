from openai import OpenAI
import ast

class LLMUtils:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, user_input: str, system_prompt: str, ast_parse_response: bool = False):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
            )
            content = response.choices[0].message.content
            if ast_parse_response:
                return ast.literal_eval(content)
            return content
        except Exception as e:
            raise RuntimeError(f"Error getting response: {e}")
            
    
    def embed(self, text: str):
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Error embedding text: {e}")