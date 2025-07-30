import os


def get_config():
    return {
        "block_start_string": os.environ['BLOCK_START_STRING']
        if 'BLOCK_START_STRING' in os.environ
        else r"{%",
        "block_end_string": os.environ['BLOCK_END_STRING']
        if 'BLOCK_END_STRING' in os.environ
        else r"%}",
        "var_start_string": os.environ['VAR_START_STRING']
        if 'VAR_START_STRING' in os.environ
        else r"{{",
        "var_end_string": os.environ['VAR_END_STRING']
        if 'VAR_END_STRING' in os.environ
        else r"}}",
        "comment_start_string": os.environ['COMMENT_START_STRING']
        if 'COMMENT_START_STRING' in os.environ
        else r"{#",
        "comment_end_string": os.environ['COMMENT_END_STRING']
        if 'COMMENT_END_STRING' in os.environ
        else r"#}",
        "template_search_path": os.getenv('TEMPLATE_SEARCH_PATH', None),
    }
