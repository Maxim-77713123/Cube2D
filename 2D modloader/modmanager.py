import os
import zipfile
import requests
import pygame
import io
from pathlib import Path
import time
import git

# Чтение настроек из файла
def read_settings():
    settings = {}
    with open('modsettings.txt', 'r') as f:
        for line in f.readlines():
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=')
            settings[key.strip()] = value.strip()
    return settings

# Инициализация экрана для анимации загрузки
def initialize_loading_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Загрузка модов...")
    font = pygame.font.Font(None, 36)
    return screen, font

# Анимация прогресса
def show_loading_animation(screen, font, progress):
    screen.fill((0, 0, 0))  # Черный фон

    # Прогресс бар
    bar_width = 600
    bar_height = 30
    pygame.draw.rect(screen, (255, 255, 255), (100, 250, bar_width, bar_height))  # Бар фона
    pygame.draw.rect(screen, (0, 255, 0), (100, 250, bar_width * progress, bar_height))  # Заполненный прогресс

    # Текст
    text = font.render(f"Загрузка: {int(progress * 100)}%", True, (255, 255, 255))
    screen.blit(text, (350, 300))

    pygame.display.flip()

# Скачивание архива с модами с GitHub
def download_mod_from_github(repo_url, mod_name, mods_dir, screen, font):
    print(f"Скачиваем мод: {mod_name} из {repo_url}...")
    
    # URL для скачивания ZIP-архива
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    
    # Скачиваем архив с модами
    response = requests.get(zip_url)
    
    if response.status_code == 200:
        mod_path = os.path.join(mods_dir, mod_name)
        if not os.path.exists(mod_path):
            os.makedirs(mod_path)
        
        zip_file_path = os.path.join(mod_path, f'{mod_name}.zip')
        
        with open(zip_file_path, 'wb') as f:
            total_length = int(response.headers.get('content-length'))
            downloaded = 0
            
            # Загружаем файл по частям
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = downloaded / total_length
                    show_loading_animation(screen, font, progress)
                    time.sleep(0.1)  # Задержка для анимации загрузки

        print(f"Мод {mod_name} скачан. Разархивируем...")
        
        # Разархивируем мод
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(mod_path)

        os.remove(zip_file_path)  # Удаляем архив
        print(f"Мод {mod_name} успешно установлен!")
    else:
        print(f"Ошибка при скачивании мода {mod_name}.")

# Клонирование репозитория с модами (вместо скачивания zip)
def clone_mod_repo(repo_url, mod_name, mods_dir):
    mod_path = os.path.join(mods_dir, mod_name)
    if not os.path.exists(mod_path):
        os.makedirs(mod_path)
    
    # Используем git для клонирования репозитория
    try:
        print(f"Клонируем репозиторий {repo_url}...")
        git.Repo.clone_from(repo_url, mod_path)
        print(f"Мод {mod_name} успешно клонирован!")
    except Exception as e:
        print(f"Ошибка при клонировании репозитория: {e}")

# Основная функция для загрузки модов из настроек
def install_mods_from_settings():
    settings = read_settings()
    mods_dir = settings['MODS_DIR']
    mod_repo_url = settings['MODS_REPO_URL']  # URL репозитория с модами
    mod_name = "example_mod"  # Пример имени мода, который будет скачан (замените на актуальное имя мода)

    # Инициализируем экран для анимации загрузки
    screen, font = initialize_loading_screen()

    # Скачиваем мод из GitHub
    download_mod_from_github(mod_repo_url, mod_name, mods_dir, screen, font)

    pygame.quit()

# Основной запуск
if __name__ == "__main__":
    install_mods_from_settings()  # Устанавливаем моды
