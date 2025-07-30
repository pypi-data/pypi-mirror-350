import pytest
import asyncio
from svo_chunker.svo_chunker import SVOChunker

TEST_TEXTS = [
    # Russian
    "Пошел я на улицу гулять а там идет дождь я был Вынужден вернуться и одеть одежду пока я одевался дождь закончился",
    # English
    "I went outside to walk but it started to rain I had to return and put on my coat while I was dressing the Rain stopped"
]

@pytest.mark.asyncio
@pytest.mark.parametrize("text", TEST_TEXTS)
async def test_chunking(text):
    chunker = SVOChunker(use_gpu=True)
    chunk_pairs = await chunker.chunk_by_sv_semantics(text)
    assert len(chunk_pairs) > 0
    for chunk, chunk_vector in chunk_pairs:
        assert 'subject' in chunk['sv'] and 'verb' in chunk['sv']
        assert isinstance(chunk['block'], list)
        assert isinstance(chunk_vector, list)
        assert len(chunk_vector) > 0

if __name__ == "__main__":
    for text in TEST_TEXTS:
        asyncio.run(test_chunking(text)) 