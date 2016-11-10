from .decorator import temp_file


@temp_file
def write_file(msg, output):
    with open(output, 'w+') as f:
        f.write(msg)