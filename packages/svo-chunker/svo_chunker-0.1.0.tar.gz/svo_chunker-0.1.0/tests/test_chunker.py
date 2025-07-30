import pytest
from svo_chunker.svo_chunker import SVOChunker

RU_TEXT = "Я открыл дверь и увидел кота. Кот сидел на окне."
EN_TEXT = "I opened the door and saw a cat. The cat was sitting on the window."

@pytest.mark.parametrize("text,lang,expected_sv_count", [
    (RU_TEXT, 'ru', 2),
    (EN_TEXT, 'en', 2),
])
def test_extract_sv_pairs(text, lang, expected_sv_count):
    chunker = SVOChunker(use_gpu=True)
    tokens = chunker.parse_with_pos(text)
    sv_pairs = chunker.extract_sv_pairs(tokens)
    assert len(sv_pairs) == expected_sv_count
    for pair in sv_pairs:
        assert 'subject' in pair and 'verb' in pair
        assert pair['subject']['pos'] in ('PRON', 'NOUN', 'PROPN')
        assert pair['verb']['pos'] in ('VERB', 'AUX')

# Интеграционный тест с реальным сервисом эмбеддингов (если доступен)
import asyncio
@pytest.mark.asyncio
async def test_chunk_by_sv_semantics_real():
    chunker = SVOChunker(use_gpu=True)
    text = RU_TEXT
    chunk_pairs = await chunker.chunk_by_sv_semantics(text)
    assert isinstance(chunk_pairs, list)
    for chunk, chunk_vector in chunk_pairs:
        assert isinstance(chunk, dict)
        assert 'block' in chunk and 'sv' in chunk
        assert isinstance(chunk['block'], list)
        if chunk['sv'] is not None:
            assert 'subject' in chunk['sv'] and 'verb' in chunk['sv']
        assert isinstance(chunk_vector, list)
        assert len(chunk_vector) > 0
    reconstructed = SVOChunker.reconstruct_with_separators(text, chunk_pairs)
    assert reconstructed == text

# Пример теста для примера из examples/test_chunking.py
@pytest.mark.asyncio
async def test_chunking_example():
    chunker = SVOChunker(use_gpu=True)
    text = "Пошел я на улицу гулять а там идет дождь я был вынужден вернуться и одеть одежду пока я одевался дождь закончился"
    chunk_pairs = await chunker.chunk_by_sv_semantics(text)
    assert len(chunk_pairs) > 0
    for chunk, chunk_vector in chunk_pairs:
        if chunk['sv'] is not None:
            assert 'subject' in chunk['sv'] and 'verb' in chunk['sv']
        assert isinstance(chunk['block'], list)
        assert isinstance(chunk_vector, list)
        assert len(chunk_vector) > 0
    reconstructed = SVOChunker.reconstruct_with_separators(text, chunk_pairs)
    assert reconstructed == text 