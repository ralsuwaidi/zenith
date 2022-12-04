import re


def get_opt(prompt: str):
    options = {}
    parsed = prompt.split(" ")
    for i in parsed:
        if ":" in i:
            arg_split = i.split(":")
            if arg_split[0] != "" and arg_split[1] != "":
                try:
                    arg_split[1] = int(arg_split[1])
                except:
                    pass
                options[arg_split[0]] = arg_split[1]

    return(options)


def remove_opt(prompt: str):
    prompt_text = prompt
    parsed = prompt.split(" ")
    for i in parsed:
        if ":" in i:
            arg_split = i.split(":")
            print(i)
            if arg_split[0] != "" and arg_split[1] != "":
                prompt_text = prompt_text.replace(i,"")

    # remove double spacing
    prompt_text = re.sub(' +', ' ', prompt_text)
    return prompt_text

def is_too_large(prompt: str):
    if len(prompt.split(" ")) > 1400:
        return True
    return False