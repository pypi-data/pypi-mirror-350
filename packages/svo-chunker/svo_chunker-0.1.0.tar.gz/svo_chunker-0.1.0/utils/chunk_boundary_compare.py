#!/usr/bin/env python3
import numpy as np
import asyncio
from embed_client.async_client import EmbeddingServiceAsyncClient

def cosine_delta(vec_block, vec_sv):
    return 1 - np.dot(vec_block, vec_sv) / (np.linalg.norm(vec_block) * np.linalg.norm(vec_sv) + 1e-8)

async def process_pair(pair_lines, client):
    # Каждая строка: left | right
    left1, right1 = [s.strip() for s in pair_lines[0].split('|')]
    left2, right2 = [s.strip() for s in pair_lines[1].split('|')]
    # S–V для примера: берём первые два слова левого чанка и первые два слова правого чанка (грубая эвристика)
    sv1 = ' '.join(left1.split()[:2])
    sv2 = ' '.join(right1.split()[:2])
    # Получить эмбеддинги
    emb_sv = await client.cmd("embed", params={"texts": [sv1, sv2]})
    emb_sv = emb_sv.get('result', emb_sv)
    if isinstance(emb_sv, dict) and 'embeddings' in emb_sv:
        emb_sv = emb_sv['embeddings']
    emb_chunks = await client.cmd("embed", params={"texts": [left1, right1, left2, right2]})
    emb_chunks = emb_chunks.get('result', emb_chunks)
    if isinstance(emb_chunks, dict) and 'embeddings' in emb_chunks:
        emb_chunks = emb_chunks['embeddings']
    # Вариант 1
    delta1_1 = cosine_delta(emb_chunks[0], emb_sv[0])
    delta1_2 = cosine_delta(emb_chunks[1], emb_sv[1])
    sum1 = delta1_1 + delta1_2
    # Вариант 2
    delta2_1 = cosine_delta(emb_chunks[2], emb_sv[0])
    delta2_2 = cosine_delta(emb_chunks[3], emb_sv[1])
    sum2 = delta2_1 + delta2_2
    print("=== Boundary Comparison ===")
    print(f"Variant 1: ['{left1}'] | ['{right1}']")
    print(f"  delta1 = {delta1_1:.4f}, delta2 = {delta1_2:.4f}, sum = {sum1:.4f}")
    print(f"Variant 2: ['{left2}'] | ['{right2}']")
    print(f"  delta1 = {delta2_1:.4f}, delta2 = {delta2_2:.4f}, sum = {sum2:.4f}")
    print(f"Difference (sum1 - sum2): {sum1 - sum2:.4f}")
    if sum1 > sum2:
        print("[MAXIMIZATION] Variant 1 is selected (sum1 > sum2)")
    elif sum2 > sum1:
        print("[MAXIMIZATION] Variant 2 is selected (sum2 > sum1)")
    else:
        print("[MAXIMIZATION] Both variants are equal")
    print()

async def main():
    # Чтение пар из файла
    with open('utils/boundary_pairs.txt', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    pairs = [lines[i:i+2] for i in range(0, len(lines), 2)]
    async with EmbeddingServiceAsyncClient("http://localhost", 8001) as client:
        for pair_lines in pairs:
            await process_pair(pair_lines, client)

if __name__ == "__main__":
    asyncio.run(main()) 