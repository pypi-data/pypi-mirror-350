# Mantarix Obfuscator

from base64 import b85encode
from gzip import compress
from random import choices
from pathlib import Path

def hexadecimal(code: str = None) -> str:
    code = "".join([f"\\x{car:0>2x}" for car in code.encode()])
    code = f"_=exec;_('{code}')"
    return code

def base85(code: str = None) -> str:
    code = b85encode(code.encode())
    code = (
        code
    ) = ("from base64 import b85decode as _;___=bytes.decode;"f"__=exec;__(___(_({code})))")
    return code

def xor_code(code: str = None, password: str = None) -> str:
    password = password
    if password:
        ask_password = True
        password = password.encode()
        password_lenght = len(password)
    else:
        ask_password = False
        password = choices(list(range(256)), k=40)
        password_lenght = 40
    code = [
        char ^ password[i % password_lenght]
        for i, char in enumerate(code.encode())
    ]
    if ask_password:
        code = (
            "_=input('Password: ').encode();__=len(_);___=exec;_____='';"
            f"\nfor _______,______ in enumerate({code}):_____+=chr"
            "(______^_[_______%__])\n___(_____)"
        )
    else:
        code = (
            f"_={password};__=len(_);___=exec;_____='';\nfor _______,_____"
            f"_ in enumerate({code}):_____+=chr(______^_[_______%__])"
            "\n___(_____)"
        )
    return code

def gzip(code: str = None) -> str:
    code = compress(code.encode())
    code = (
        code
    ) = f"from gzip import decompress as __;_=exec;_(__({code}))"
    return code

def obfuscate_code(code: str) -> str:
    return hexadecimal(base85(xor_code(gzip(code))))

def obfuscate_folder(folder_path: str,prefix:str="",suffix:str=""):
    folder = Path(folder_path)
    for file in list(folder.rglob("*.py")):
        file_path = Path(file)
        file_path_out = file_path.parent.joinpath(prefix+file_path.stem+suffix+".py")
        with open(file_path.as_posix(), "r", encoding="utf-8") as f:
            code = f.read()
        obfuscated = obfuscate_code(code)
        with open(file_path_out.as_posix(), "w", encoding="utf-8") as f:
            f.write(obfuscated)