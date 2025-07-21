import aiohttp
import pprint
import json
from dotenv import load_dotenv
from database.models import Dish
import os
load_dotenv()
token = os.getenv("TOKEN_AI")
name_model = 'meta-llama/Llama-3.2-90B-Vision-Instruct'

async def run(target_dish:Dish):    
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        data = {
            "model": name_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Представь что ты повар."
                },
                {
                    "role": "user",
                    "content": 
                    (f"Тебя попросили описать блюдо - {target_dish.name}: выдать историческую справку, "
                    "а также выдать расчет БЖУ. Формат ответа строгий:"
                    "Историческая справка"
                    f"Расчет БЖУ с учетом следующих характеристик блюда: {target_dish.properties}"
                    "Рекомендации")
                }
            ]
        }
        result = ""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                if 'choices' in result:
                    result = result['choices'][0]['message']['content']
                    if "<think>" in result:
                        result = result.split("</think>")[-1]
        return result
