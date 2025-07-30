
def process_path(path: str) -> str:
    """
    处理路径字符串，确保其符合特定格式要求
    """
    if path.startswith('/apps/Webdisk/'):
        return path
    elif path.startswith('/'):
        return '/apps/Webdisk' + path
    else:
        return '/apps/Webdisk/' + path

