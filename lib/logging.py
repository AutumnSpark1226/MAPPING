debugging_enabled = True

def log(text: str, origin: str):
    if debugging_enabled:
        print("[" + origin + "] " + text)
