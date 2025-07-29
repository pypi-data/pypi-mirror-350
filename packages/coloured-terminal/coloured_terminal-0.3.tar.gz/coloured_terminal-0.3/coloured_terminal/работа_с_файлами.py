РАЗДЕЛИТЕЛЬ_ЗНАЧЕНИЙ = "_____++_*$$#!!~#@$$^&*(("
РАЗДЕЛИТЕЛЬ_ПАР = "vbhj xc78677@#$%^&*)()"
def write_file(text: str, path: str):
    try:
        with open(path, mode="w", encoding="utf-8") as file:
            file.write(text)
    except Exception as write_er:
        print(f"Произошла ошибка \"{write_er}\"")
        return False
    return True

def read_file(path: str):
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return file.read()
    except Exception as read_er:
        print(f"Произошла ошибка \"{read_er}\"")
        return False
    return True

def словарь_в_текст(словарь: dict):
    результат = ""
    for пара in словарь.items():
        ключ, значение = пара
        текстовая_пара = f"{ключ}{РАЗДЕЛИТЕЛЬ_ЗНАЧЕНИЙ}{значение}" # type: ignore
        результат += текстовая_пара + РАЗДЕЛИТЕЛЬ_ПАР # type: ignore
    return результат[:-len(РАЗДЕЛИТЕЛЬ_ПАР)] # type: ignore

def текст_в_словарь(текст: str):
    результат = {}
    пары = текст.split(РАЗДЕЛИТЕЛЬ_ПАР) # type: ignore
    for пара in пары:
        ключ, значение = пара.split(РАЗДЕЛИТЕЛЬ_ЗНАЧЕНИЙ, 1) # type: ignore
        результат[ключ] = значение
    return результат

def преобразовать_все_словари(список_словарей: list):
    текст = ""
    for словарь in список_словарей:
        текст += словарь_в_текст(словарь) + "\n"
    return текст

def текст_в_словари(текст: str):
    список = []
    for строка in текст.splitlines():
        словарь = текст_в_словарь(строка)
        список.append(словарь)
    return список

if __name__ == "__main__":
    список_словарей = [{"ключ1": "значение1", "ключ2": "значение2"},{"ключ3": "значение3", "ключ4": "значение4"}]
    текст = преобразовать_все_словари(список_словарей)
    обратно = текст_в_словари(текст)
    print(список_словарей == обратно)