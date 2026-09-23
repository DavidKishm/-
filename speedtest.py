import sys
import time
import urllib.request

REQUESTS = 10          # это как у вас в условии сколько раз стучаться
CHUNK = 1024 * 1024    # читаем по 1 МБ за раз. Ну это обычное правило, так принято чтобы не нагружать сильно


def download(url):     # Скачиваем и считаем время
    start = time.time()
    size = 0
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            size += len(chunk)
    return time.time() - start, size


def main():
    if len(sys.argv) < 2:
        print("Использование: python speedtest.py <url>")
        return
    url = sys.argv[1]
    print(f"Качаем с: {url}")
    print(f"Запросов: {REQUESTS}\n")
    times = []
    sizes = []
    for i in range(1, REQUESTS + 1):
        try:
            elapsed, size = download(url)
        except Exception as e:
            print(f"Запрос {i}: ошибка — {e}")
            continue

        speed = size / elapsed / 1024 / 1024  # МБ/с
        times.append(elapsed)
        sizes.append(size)

        print(f"Запрос {i}: {elapsed:.2f} сек, "
              f"{size / 1024 / 1024:.2f} МБ, "
              f"{speed:.2f} МБ/с")

    if not times:
        print("Ни один запрос не удался")
        return

    avg_time = sum(times) / len(times)
    avg_size = sum(sizes) / len(sizes)
    avg_speed = avg_size / avg_time / 1024 / 1024

    print("Итог")
    print(f"Успешных запросов: {len(times)} из {REQUESTS}")
    print(f"Среднее время запроса: {avg_time:.2f} сек")
    print(f"Средний размер: {avg_size / 1024 / 1024:.2f} МБ")
    print(f"Средняя скорость: {avg_speed:.2f} МБ/с ({avg_speed * 8:.2f} Мбит/с)")


if __name__ == "__main__":
    main()
