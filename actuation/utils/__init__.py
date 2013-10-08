
def append_slash_if_absent( file_path ):
    return file_path if file_path.endswith( "/" ) else file_path + "/"