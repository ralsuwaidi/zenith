
import utils

prompt = "this is a test for how to get a prompt an option is test:value presence_penalty:2 this is true: i mean :dw car:"

options = utils.get_opt(prompt=prompt)
clean_prompt = utils.remove_opt(prompt)

default_opts = {
    "engine":"text-babbage-001",
    "temperature":0.7,
    "max_tokens":1200,
    "top_p":1,
    "frequency_penalty":0,
    "presence_penalty":0,
}
default_opts.update(options)

print(default_opts)
print(clean_prompt)