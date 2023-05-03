import aiohttp
import asyncio
import requests

key = '64c7e00c68104cf5ac819fa7eb8807cb'


# Функции для парсинга instructions, т.к. они всегда написаны по разному и порой через жопу
def recursion_delete(string):
    if string.find('<') > -1:
        return recursion_delete(string[:string.find('<')] + string[string.find('>') + 1:])
    else:
        return string


def instruction_parser(instruction):
    if instruction[:8] == '<ol><li>':
        instruction = instruction.split('</li><li>')
    elif instruction[:3] == '<p>':
        instruction = instruction.split('</p><p>')
    elif '\n' in instruction and '\n\n' not in instruction:
        instruction = instruction.split('\n')
    elif '\n\n' in instruction:
        instruction = instruction.split('\n\n')
    else:
        return instruction, 0
    for i in instruction:
        instruction[instruction.index(i)] = recursion_delete(i)
    return instruction, 1


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


# запрашивает у пользователя строку тегов
async def get_random_recipe(tags=''):
    global key
    if tags == 'nothing':
        tags = ''
    text = 'Oh, there are no recipes for these tags'

    req = await get_response('https://api.spoonacular.com/recipes/random',
                             params={'tags': tags, 'apiKey': key})
    data = req
    try:
        for recipe in data['recipes']:
            text = f'Here is a random recipe for u:\n\n'
            title = recipe['title']
            img = recipe['image']
            recipe_id = recipe['id']
            price = round(recipe['pricePerServing'] / 100, 2)  # цена за 1 порцию
            time = recipe['readyInMinutes']  # время приготовления
            servings = recipe['servings']  # количество порций
            ingredients = recipe['extendedIngredients']
            text += f'{title}\n\n' \
                    f'id: {recipe_id}\n' \
                    f'time: {time} min\n' \
                    f'price per serving: {price}$\n' \
                    f'servings: {servings}\n' \
                    f'total cost: {round(price * servings, 2)}$\n' \
                    f'ingredients:\n'

            # Добавление ингредиентов
            for ingredient in ingredients:
                measures = ingredient['measures']['metric']
                text += f'   •{ingredient["name"]} ({measures["amount"]} {measures["unitShort"]})\n'

            instruction = recipe['instructions']
            text += '\nInstruction:\n'
            if instruction_parser(instruction)[1] == 0:
                text += f'  {instruction_parser(instruction)[0]}\n'
            else:
                instruction = instruction_parser(instruction)[0]
                for step in instruction:
                    text += f'  {instruction.index(step) + 1}){step}\n'

            text += f'\n{img}'
    except:
        text += ''
        return text, 0

    return text, 1


async def find_a_recipe(query, number):
    global key
    req = await get_response('https://api.spoonacular.com/recipes/complexSearch',
                             params={'query': query, 'number': number,
                                     'apiKey': key})
    data = req
    count = 0
    recipes_count = len(data['results'])
    answer = f'Here {"are" if recipes_count > 1 else "is"} {recipes_count} ' \
             f'{"recipes" if recipes_count > 1 else "recipe"} with "{query}":\n'
    for recipe in data['results']:
        count += 1
        answer += f'{count}){recipe["title"]}, id - {recipe["id"]}\n'
    return answer


async def get_recipe_inf(recipe_id):
    global key
    try:
        req = await get_response(f'https://api.spoonacular.com/recipes/{recipe_id}/information',
                                 params={'id': recipe_id, 'apiKey': key})
        recipe = req
        answer = ''
        title = recipe['title']
        img = recipe['image']
        price = round(recipe['pricePerServing'] / 100, 2)  # цена за 1 порцию
        time = recipe['readyInMinutes']  # время приготовления
        servings = recipe['servings']  # количество порций
        ingredients = recipe['extendedIngredients']
        answer = f'{title}\n\n' \
                 f'time: {time} min\n' \
                 f'price per serving: {price}$\n' \
                 f'servings: {servings}\n' \
                 f'total cost: {round(price * servings, 2)}$\n' \
                 f'ingredients:\n'
        for ingredient in ingredients:
            measures = ingredient['measures']['metric']
            answer += f'   •{ingredient["name"]} ({measures["amount"]} {measures["unitShort"]})\n'

        instruction = recipe['instructions']
        answer += '\nInstruction:\n'
        if instruction_parser(instruction)[1] == 0:
            answer += f'  {instruction_parser(instruction)[0]}\n'
        else:
            instruction = instruction_parser(instruction)[0]
            for step in instruction:
                answer += f'  {instruction.index(step) + 1}){step}\n'

        answer += f'\n{img}'

        return answer, 1
    except:
        return 'There`s no such ID', 0

# print(asyncio.run(get_random_recipe('irish')))
# print(asyncio.run(find_a_recipe('pasta', 0)))
# print(asyncio.run(get_recipe_inf(1161745)))
