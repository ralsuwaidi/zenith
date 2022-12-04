import logging
from os import environ as env
import utils
import constants

import telebot
import openai


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(env["TELEGRAM_BOT_KEY"])
openai.api_key = env["OPENAI_API_KEY"]


@bot.message_handler(func=lambda message: True)
def get_response(message):

    # openAI default options
    default_opts = {
        "engine": "text-babbage-001",
        # "temperature": 0.5, # https://beta.openai.com/docs/api-reference/completions/create#completions/create-temperature
        "max_tokens": 16,  # https://beta.openai.com/docs/api-reference/completions/create#completions/create-max_tokens
        # "top_p": 1,   # https://beta.openai.com/docs/api-reference/completions/create#completions/create-top_p
        "n": 1,  # https://beta.openai.com/docs/api-reference/completions/create#completions/create-n
        "stop": ['"""'],  # https://beta.openai.com/docs/api-reference/completions/create#completions/create-stop
        "presence_penalty": 0,  # https://beta.openai.com/docs/api-reference/completions/create#completions/create-presence_penalty
        # https://beta.openai.com/docs/api-reference/completions/create#completions/create-frequency_penalty
        "frequency_penalty": 0,
    }

    # save additional options from prompt
    options = utils.get_opt(message.text)

    # remove options from prompt
    clear_prompt = utils.remove_opt(message.text)

    # dont parse text if more than 1400 words
    if utils.is_too_large(clear_prompt):
        bot.send_message(message.chat.id,
                         f'Error: The text is too long, did not parse',
                         )
        return

    if "cmd" in options:
        command = options["cmd"]
        if command == "options" or command == "option":
            for k, v in default_opts.items():
                bot.send_message(message.chat.id,
                                 f'{k}:{v}',
                                 )
        elif command == "models":
            for k, v in constants.models.items():
                bot.send_message(message.chat.id,
                                 f'{k}\n\n{v}',
                                 )
        else:
            bot.send_message(message.chat.id,
                             f'Couldnt find specific command',
                             )
        return

    default_opts.update(options)
    response = openai.Completion.create(
        **default_opts,
        prompt='"""\n{}\n"""'.format(message.text),
    )

    bot.send_message(message.chat.id,
                     f'{response["choices"][0]["text"]}',
                     parse_mode="Markdown")


bot.infinity_polling()
