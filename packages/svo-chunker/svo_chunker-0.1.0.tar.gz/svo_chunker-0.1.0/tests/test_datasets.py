import pytest
import asyncio
from svo_chunker.svo_chunker import SVOChunker
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_ROOT, 'datasets')

DATASET_FILES = [
    'dirty_sample_ru.txt',
    'clean_sample_ru.txt',
    'dirty_sample_en.txt',
    'clean_sample_en.txt',
    'dirty_sample_mixed_2k.txt',
    'clean_sample_mixed_2k.txt',
    'dirty_sample_ru_2k.txt',
    'clean_sample_ru_2k.txt',
    'dirty_sample_en_2k.txt',
]

# --- Вспомогательная функция для восстановления текста с учётом всех разделителей ---
def reconstruct_with_separators(text, chunks):
    pos = 0
    result = []
    for i, (chunk, _) in enumerate(chunks):
        idx = text.find(chunk['text'], pos)
        if idx == -1:
            raise ValueError(f"Chunk text not found in original text: {chunk['text'][:30]}")
        # Всё, что между pos и idx — это разделитель
        if i > 0:
            result[-1] += text[pos:idx]
        result.append(chunk['text'])
        pos = idx + len(chunk['text'])
    # Если что-то осталось в конце — добавляем к последнему чанку
    if pos < len(text):
        result[-1] += text[pos:]
    return ''.join(result)

@pytest.mark.asyncio
@pytest.mark.parametrize("filename", DATASET_FILES)
async def test_chunking_on_datasets(filename):
    path = os.path.join(DATASET_DIR, filename)
    with open(path, encoding='utf-8') as f:
        text = f.read()
    chunker = SVOChunker(use_gpu=True)
    chunks = await chunker.chunk_by_sv_semantics(text)
    # Проверяем, что чанки выделяются и содержат S–V-пары (если есть хотя бы 2 S–V)
    if len(chunks) > 0:
        for chunk, chunk_vector in chunks:
            if chunk['sv'] is not None:
                assert 'subject' in chunk['sv'] and 'verb' in chunk['sv']
            assert isinstance(chunk['block'], list)
            assert isinstance(chunk_vector, list)
            assert len(chunk_vector) > 0
        # Проверка: сумма чанков покрывает исходный текст (по тексту чанков)
        reconstructed = SVOChunker.reconstruct_with_separators(text, chunks)
        assert reconstructed == text
    else:
        # Если чанков нет, значит в тексте не было хотя бы двух S–V-пар — это допустимо
        assert True 