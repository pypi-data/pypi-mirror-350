from setuptools import setup

setup(
    name="coloured_terminal", # Имя модуля, которое будет использоваться через pip install
    version="0.3", # версия модуля. При каждом обновлении её нужно увеличивать
    description="Писать цветными буквами в терминале", # Описание проекта, его можно не использовать
    packages=["coloured_terminal"], # Список с названиями папок, которые нужно залить
    author_email="nikitastrukalin747@icloud.com", # Почта автора
    zip_safe=False, # Пароль, можно не указываьть
    install_requires = [] # Список дополнительных модулей, которые необходимо использовать для вашего модуля
)