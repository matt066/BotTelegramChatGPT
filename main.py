import telegram
import requests
from telegram import bot
from telegram.ext import Updater, MessageHandler, Filters
import logging

# Habilitar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Insira aqui a sua chave de API do Telegram
telegram_api_key = 'API-KEY-HERE'

# Insira aqui a sua chave de API do ChatGPT
chatgpt_api_key = 'API-KEY-HERE'

# Crie um objeto updater do Telegram
updater = Updater(token=telegram_api_key, use_context=True)

# Crie um objeto dispatcher para o updater
dispatcher = updater.dispatcher

# Defina uma função para processar as mensagens recebidas pelo bot
def process_message(update, context):
    # Obtenha a mensagem recebida
    message = update.message.text
    logger.info(f"Mensagem recebida: {message}")

    # Chame a API do ChatGPT para gerar uma resposta
    chatgpt_url = 'https://api.openai.com/v1/engines/text-davinci-003-playground/completions'
    data = {
        'prompt': message,
        'max_tokens': 1000,
        'temperature': 0.7,
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {chatgpt_api_key}'
    }
    response = requests.post(chatgpt_url, json=data, headers=headers)

    # Registre as informações relevantes no log
    logger.info(f"Chamada para a API do ChatGPT: {chatgpt_url}")
    logger.info(f"Corpo da requisição: {data}")
    logger.info(f"Cabeçalhos da requisição: {headers}")
    logger.info(f"Código de status da resposta: {response.status_code}")
    logger.info(f"Corpo da resposta: {response.json()}")

    response_data = response.json()

    # Verifique se a chave 'choices' está presente na resposta
    if 'choices' not in response_data:
        error_message = 'Desculpe, não consegui entender o que você disse.'
        context.bot.send_message(chat_id=update.message.chat_id, text=error_message)
        return

    chatgpt_response = response_data['choices'][0]['text']

    logger.info(f"Resposta gerada: {chatgpt_response}")

    # Envie a resposta gerada pelo ChatGPT para o usuário do Telegram
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=chatgpt_response)

# Registre a função process_message como um manipulador de mensagens do bot
message_handler = MessageHandler(Filters.text, process_message)
dispatcher.add_handler(message_handler)

# Inicie o bot do Telegram
updater.start_polling()