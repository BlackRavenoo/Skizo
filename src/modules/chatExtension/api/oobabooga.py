from modules.chatExtension.api.openai import _openai_response

from config import modules_config

if modules_config["chat"]["oobabooga_host"] is None:
    raise Exception("OOBABOOGA_HOST is not set")

completion =  _openai_response(url=modules_config["chat"]["oobabooga_host"]+"/v1/completions")
chat_completion = _openai_response(url=modules_config["chat"]["oobabooga_host"]+"/v1/chat/completions")

#['choices'][0]['text']
