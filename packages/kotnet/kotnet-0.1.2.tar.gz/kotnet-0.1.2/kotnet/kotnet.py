import time
import sys
import random
from colorama import Fore, Back, Style, init
from tqdm import tqdm

init()

class KotNet:
    def __init__(self):
        self.log_colors = {
            'INFO': Fore.CYAN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED
        }

    def slow_print(self, text, delay=0.05):
        """Замедленный вывод текста"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def color_print(self, text, fg="white", bg=None):
        """Цветной текст с возможностью выбора фона"""
        color = getattr(Fore, fg.upper(), Fore.WHITE)
        background = getattr(Back, bg.upper(), '') if bg else ''
        print(f"{background}{color}{text}{Style.RESET_ALL}")

    def bordered_text(self, text, style='single'):
        """Текст в рамке с разными стилями"""
        border_map = {
            'single': ('┌', '─', '┐', '│', '└', '┘'),
            'double': ('╔', '═', '╗', '║', '╚', '╝')
        }
        b = border_map.get(style, border_map['single'])
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        print(f"{b[0]}{b[1] * (max_len + 2)}{b[2]}")
        for line in lines:
            print(f"{b[3]} {line.ljust(max_len)} {b[3]}")
        print(f"{b[4]}{b[1] * (max_len + 2)}{b[5]}")

    def progress_bar(self, total=100, duration=5):
        """Прогресс-бар с настраиваемым total"""
        for _ in tqdm(range(total), ncols=75, unit='%'):
            time.sleep(duration / total)

    def spinner(self, duration=5):
        """Анимированный спиннер"""
        symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        while time.time() < end_time:
            for s in symbols:
                print(f'\r{s} Processing...', end='', flush=True)
                time.sleep(0.1)

    def table(self, data, headers):
        """Отображение таблицы"""
        cols = len(headers)
        # Вычисление ширины столбцов
        col_width = [
            max(len(str(row[i])) for row in (data + [headers]))
            for i in range(cols)
        ]
        
        print('┌' + '┬'.join('─' * (w + 2) for w in col_width) + '┐')
        print('│' + '│'.join(f' {h.ljust(col_width[i])} ' for i, h in enumerate(headers)) + '│')
        print('├' + '┼'.join('─' * (w + 2) for w in col_width) + '┤')
        for row in data:
            print('│' + '│'.join(f' {str(cell).ljust(col_width[i])} ' for i, cell in enumerate(row)) + '│')
        print('└' + '┴'.join('─' * (w + 2) for w in col_width) + '┘')

    def blink_text(self, text, interval=0.5):
        """Мигающий текст"""
        end_time = time.time() + interval * 10  # 5 циклов
        while time.time() < end_time:
            print(f'\r{text}', end='', flush=True)
            time.sleep(interval)
            print('\r' + ' ' * len(text), end='', flush=True)
            time.sleep(interval)
        print()

    def shadow_text(self, text):
        """Текст с тенью"""
        print(Fore.WHITE + text)
        print(' ' * 2 + Fore.BLACK + Style.BRIGHT + text + Style.RESET_ALL)

    def log(self, message, level='INFO'):
        """Логирование с уровнем"""
        color = self.log_colors.get(level.upper(), Fore.WHITE)
        print(f"{color}[{level}] {message}{Style.RESET_ALL}")

    def animate_title(self, text, delay=0.1):
        """Анимация заголовка"""
        for i in range(1, len(text)+1):
            print(f"\r{Fore.GREEN}{text[:i]}", end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)

    def format_number(self, number):
        """Форматирование чисел"""
        return f"{number:,}"

    def format_bytes(self, bytes):
        """Форматирование байтов"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} TB"

# Пример использования
if __name__ == "__main__":
    kn = KotNet()
    
    kn.slow_print("Добро пожаловать в KotNet!", 0.05)
    kn.color_print("Это цветной текст!", fg="red", bg="white")
    kn.bordered_text("Важное сообщение", style='double')
    
    print("\nПрогресс бар:")
    kn.progress_bar(total=20, duration=2)
    
    print("\nСпиннер:")
    kn.spinner(duration=2)
    
    print("\nТаблица:")
    kn.table(
        data=[
            ["Alice", 25],
            ["Bob", 30],
            ["Charlie", 35]
        ],
        headers=["Имя", "Возраст"]
    )
    
    print("\nМигающий текст:")
    kn.blink_text("Внимание! Важное сообщение!", interval=0.3)
    
    print("\nТекст с тенью:")
    kn.shadow_text("Текст с эффектом тени")
    
    print("\nЛогирование:")
    kn.log("Система запущена", "INFO")
    kn.log("Недостаточно памяти", "WARNING")
    kn.log("Критическая ошибка!", "ERROR")
    
    time.sleep(2.5)
    print("\nАнимированный заголовок:")
    kn.animate_title("KotNet Framework", delay=0.07)
    
    time.sleep(1.5)
    print("\nФорматирование данных:")
    print(kn.format_number(1_234_567))  # 1,234,567
    print(kn.format_bytes(1_500_000))   # 1.43 MB