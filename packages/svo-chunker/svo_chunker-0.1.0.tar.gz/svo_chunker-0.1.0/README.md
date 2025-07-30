# SVO Semantic Chunker

## Описание

Алгоритм смыслового чанкования текста на основе SVO-троек и векторного распределения. Поддержка русского, английского и украинского языков. Выход — JSONL или SQLite с оценкой уверенности чанков.

## Description

Semantic text chunking algorithm based on SVO triplets and vector proximity. Supports Russian, English, and Ukrainian. Output: JSONL or SQLite with chunk confidence scoring.

- Границы чанков оптимизируются по **максимизации** семантического отклонения между блоком и его S–V-ядром (vector proximity, maximization).

---

## Поддерживаемые языки / Supported languages
- Русский (ru)
- Английский (en)
- Украинский (uk)
- Смешанные тексты (автоматическое разбиение на языковые блоки)

---

## Быстрый старт / Quickstart

```bash
pip install svo-chunker
python -m spacy download en_core_web_sm
```

### Python API
```python
from svo_chunker.svo_chunker import SVOChunker
# CPU (по умолчанию)
chunker = SVOChunker()
# Явно включить GPU (если доступен)
chunker_gpu = SVOChunker(use_gpu=True)

# Пример для смешанного текста (русский, английский, украинский)
text = "Вона відкрила вікно. She went to the kitchen. Она испугалась."
chunk_pairs = await chunker.chunk_by_sv_semantics(text)
for chunk, chunk_vector in chunk_pairs:
    print(f"Chunk: {chunk}\nVector: {chunk_vector[:5]}...\n")
```

### Формат вывода / Output format
`chunk_by_sv_semantics` возвращает список кортежей `(chunk_dict, chunk_vector)`, где:
- `chunk_dict` — словарь с полями:
  - `start`, `end` — индексы токенов
  - `sv` — словарь с S–V парой (`subject`, `verb`)
  - `block` — список токенов
  - `score` — float, метрика качества
- `chunk_vector` — list[float], эмбеддинг чанка

### Fallback-эвристика по алфавиту
Если язык не определён автоматически, используется эвристика:
- Если есть уникальные украинские буквы (`ї`, `є`, `ґ`) — `uk`
- Если кириллица без уникальных украинских — `ru`
- Если латиница — `en`
- Иначе блок пропускается

### CLI
```bash
python -m svo_chunker.utils.chunk_text_cli.py -i input.txt -o output.jsonl --host http://localhost --port 8001 --show-vectors
```
- По умолчанию используется CPU. Для GPU используйте SVOChunker(use_gpu=True) в своем скрипте.

---

## Best practices
- Для больших и смешанных текстов используйте пакетную обработку и GPU.
- Для грязных данных — алгоритм устойчив к ошибкам и автоматически разбивает на языковые блоки.
- Для тестирования используйте датасеты из папки `datasets/`.

---

## Примеры / Examples
См. папку svo_chunker/examples/ (есть примеры для всех языков и смешанных текстов)

---

## TODO
- SVO extraction
- Chunk boundary detection
- Residual allocation
- Confidence scoring
- Output formatting (JSONL/SQLite)

## Установка моделей Stanza

Перед первым запуском необходимо вручную скачать модели Stanza для всех поддерживаемых языков:

```bash
python -c "import stanza; [stanza.download(lang) for lang in ['ru', 'en', 'uk']]"
```

Это действие требуется выполнить только один раз (или при обновлении моделей). После этого пакет будет использовать локальные копии моделей без повторных скачиваний.

## ⚠️ Загрузка моделей Stanza (RU/EN/UK)

Перед первым использованием необходимо скачать модели Stanza для русского, английского и украинского языков:

```bash
python -c "import stanza; stanza.download('ru'); stanza.download('en'); stanza.download('uk')"
```

Если вы запускаете тесты или используете пакет впервые, этот шаг обязателен. Иначе код попытается скачать модели автоматически при первом запуске (может "зависнуть" без интернета).

## ⚠️ Download Stanza models (RU/EN/UK)

Before first use, you must download Stanza models for Russian, English, and Ukrainian:

```bash
python -c "import stanza; stanza.download('ru'); stanza.download('en'); stanza.download('uk')"
```

If you run tests or use the package for the first time, this step is required. Otherwise, the code will try to download models automatically on first run (may hang if no internet).

---

## Использование в Docker/контейнерах

### 1. Скачивание моделей при сборке контейнера

В Dockerfile:
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# Скачиваем модели Stanza в /models/stanza_resources
RUN python -c "import stanza; stanza.download('ru', dir='/models/stanza_resources'); stanza.download('en', dir='/models/stanza_resources'); stanza.download('uk', dir='/models/stanza_resources')"
ENV STANZA_RESOURCES_DIR=/models/stanza_resources
CMD ["python", "your_script.py"]
```

### 2. Монтирование volume с моделями

На хосте:
```bash
python -c "import stanza; stanza.download('ru'); stanza.download('en'); stanza.download('uk')"
```
Запуск контейнера:
```bash
docker run -v ~/stanza_resources:/root/stanza_resources ...
```

### 3. Явное указание пути к моделям в коде
```python
import stanza
stanza.download('ru', dir='/models/stanza_resources')
nlp = stanza.Pipeline(lang='ru', dir='/models/stanza_resources')
```

### 4. Рекомендации для production/CI/CD
- Всегда используйте переменную окружения `STANZA_RESOURCES_DIR` или параметр `dir`.
- Не храните большие модели внутри кода — используйте volume или отдельный слой Docker.
- Документируйте путь к моделям для всех участников команды. 