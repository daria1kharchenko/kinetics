import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import re

def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.dat")])
    df = pd.DataFrame({'nm': range(400, 601)})
    
    if file_paths:
        for file in file_paths:
            name = os.path.basename(file)

            # Використання регулярних виразів для отримання годин, хвилин і секунд
            hours = re.findall('[0-9]+(?=h)', name)
            hours = int(hours[0]) if hours else 0
            
            minutes = re.findall("[0-9]+(?=min)", name)
            minutes = int(minutes[0]) if minutes else 0
            
            seconds = re.findall("[0-9]+(?=s)", name)
            seconds = int(seconds[0]) if seconds else 0
            
            time = seconds + minutes * 60 + hours * 3600

            # Читання файлу та додавання до DataFrame
            df_file = pd.read_csv(file, sep='\s+', index_col=0, names=['nm', time])

            # Перетворюємо індекси в рядки для роботи з методом .str
            df_file.index = df_file.index.astype(str)

            # Заміняємо коми на крапки, якщо є
            df_file.index = df_file.index.str.replace(',', '.')

            # Перетворюємо індекси в float
            df_file.index = df_file.index.astype(float)

            # Перевіряємо, чи DataFrame порожній
            if not df_file.empty:
                # Приведення стовпця 'nm' до float для узгодження з файлами
                df['nm'] = df['nm'].astype(float)

                print(df_file)

                # Об'єднуємо DataFrame тільки якщо df_file не порожній
                df = pd.concat([df.set_index('nm'), df_file], axis=1).reset_index()

        # Збереження результатів у файл
        directory_path = os.path.dirname(file_paths[0])  # Отримання шляху до каталогу
        df.to_csv(os.path.join(directory_path, 'final.txt'), sep='\t', index=False)
        print("Файл 'final.txt' успішно збережено!")
        
# Створюємо вікно
root = tk.Tk()
root.title("Обробка файлів")

# Додаємо кнопку для вибору файлів
browse_button = tk.Button(root, text="Вибрати файли", command=browse_files)
browse_button.pack()

# Запускаємо головний цикл вікна
root.mainloop()
