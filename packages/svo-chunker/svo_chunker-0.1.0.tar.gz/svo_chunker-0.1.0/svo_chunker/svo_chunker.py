"""
SVO-based semantic chunker

Semantic chunking algorithm based on SVO and vector proximity.
"""

from langdetect import detect
import spacy
import stanza
from natasha import Doc, NewsEmbedding, NewsSyntaxParser, Segmenter, MorphVocab
from typing import List, Dict, Any, Optional
import asyncio
from embed_client.async_client import EmbeddingServiceAsyncClient
import numpy as np
import re
import os
import urllib.request
import fasttext
import logging
import subprocess

__version__ = '0.1.0'

class SVOChunker:
    """
    Semantic chunker based on SVO triplets and vector proximity.
    """
    _stanza_ru = None
    _stanza_en = None
    _stanza_uk = None
    _fasttext_model = None
    _spacy_en = None
    _natasha_ru = None

    def __init__(self, use_gpu: bool = False, logger=None, load_models=None):
        self.models = {}
        self.use_gpu = use_gpu
        if logger is not None and isinstance(logger, logging.Logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger("SVOChunker")
            if not self.logger.hasHandlers():
                handler = logging.StreamHandler()
                formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.logger.info(f"SVOChunker initialized with use_gpu={self.use_gpu}")
        self.ensure_models_downloaded()
        # fastText model path
        self.fasttext_model_path = os.path.join(os.path.expanduser('~'), '.cache', 'fasttext', 'lid.176.bin')
        # --- Eagerly load selected NLP models ---
        if load_models is None or load_models == 'all':
            load_models = ['fasttext', 'ru', 'en', 'uk']
        elif isinstance(load_models, str):
            load_models = [load_models]
        self.logger.info(f"[INIT] Loading models: {load_models}")
        # fastText
        if 'fasttext' in load_models or any(x in load_models for x in ['ru', 'en', 'uk']):
            if SVOChunker._fasttext_model is None:
                self.logger.info(f"Loading fastText model from {self.fasttext_model_path} ...")
                SVOChunker._fasttext_model = fasttext.load_model(self.fasttext_model_path)
                self.logger.info("fastText model loaded.")
            self.fasttext_model = SVOChunker._fasttext_model
        # Natasha RU
        if 'ru' in load_models or 'natasha_ru' in load_models:
            if SVOChunker._natasha_ru is None:
                emb = NewsEmbedding()
                SVOChunker._natasha_ru = {
                    'segmenter': Segmenter(),
                    'morph_vocab': MorphVocab(),
                    'emb': emb,
                    'syntax': NewsSyntaxParser(emb)
                }
                self.logger.info("[INIT] Natasha RU loaded.")
            self.models['ru'] = SVOChunker._natasha_ru
        # spaCy EN
        if 'en' in load_models or 'spacy_en' in load_models:
            if SVOChunker._spacy_en is None:
                SVOChunker._spacy_en = spacy.load('en_core_web_sm')
                self.logger.info("[INIT] spaCy EN loaded.")
            self.models['en'] = SVOChunker._spacy_en
        # Stanza RU
        if 'ru' in load_models or 'stanza_ru' in load_models:
            if SVOChunker._stanza_ru is None:
                SVOChunker._stanza_ru = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[INIT] Stanza RU loaded.")
        # Stanza EN
        if 'en' in load_models or 'stanza_en' in load_models:
            if SVOChunker._stanza_en is None:
                SVOChunker._stanza_en = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[INIT] Stanza EN loaded.")
        # Stanza UK
        if 'uk' in load_models or 'stanza_uk' in load_models:
            if SVOChunker._stanza_uk is None:
                SVOChunker._stanza_uk = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[INIT] Stanza UK loaded.")
        self.logger.info("[INIT] Selected NLP models loaded.")

    def ensure_models_downloaded(self):
        """
        Ensure all required models are downloaded and ready (fastText, spacy, natasha). Stanza models must be installed manually via install script or README instructions.
        """
        # fastText model lid.176.bin
        fasttext_model_url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'
        fasttext_model_path = os.path.join(os.path.expanduser('~'), '.cache', 'fasttext', 'lid.176.bin')
        os.makedirs(os.path.dirname(fasttext_model_path), exist_ok=True)
        if not os.path.exists(fasttext_model_path):
            self.logger.info(f"[MODEL] Downloading fastText model lid.176.bin ...")
            urllib.request.urlretrieve(fasttext_model_url, fasttext_model_path)
            self.logger.info(f"[MODEL] fastText model downloaded: {fasttext_model_path}")
        else:
            self.logger.info(f"[MODEL] fastText model already exists: {fasttext_model_path}")
        # spaCy en_core_web_sm
        try:
            import spacy
            spacy.load('en_core_web_sm')
            self.logger.info("[MODEL] spaCy en_core_web_sm is ready.")
        except Exception:
            self.logger.info("[MODEL] Downloading spaCy en_core_web_sm ...")
            os.system('python -m spacy download en_core_web_sm')
            self.logger.info("[MODEL] spaCy en_core_web_sm downloaded.")
        # Natasha NewsEmbedding (downloads on first use)
        try:
            from natasha import NewsEmbedding
            _ = NewsEmbedding()
            self.logger.info("[MODEL] Natasha NewsEmbedding is ready.")
        except Exception as e:
            self.logger.error(f"[MODEL][ERROR] Natasha NewsEmbedding: {e}")

    def detect_language(self, text):
        """
        Detect language of the input text.
        """
        return detect(text)

    def split_by_language(self, text):
        """
        Split text into blocks of the same language (ru/en/unknown) using fastText for each sentence.
        Returns list of (lang, text_block) tuples.
        """
        sents = re.split(r'(?<=[.!?])\s+', text)
        blocks = []
        current_lang = None
        current_block = []
        for sent in sents:
            sent = sent.strip()
            if not sent:
                continue
            try:
                pred = self.fasttext_model.predict(sent.replace("\n", " "))
                lang = pred[0][0].replace('__label__', '')
                score = pred[1][0]
                # fastText иногда путает короткие фрагменты, поэтому ru/en/unknown, остальное — unsupported
                if lang not in ('ru', 'en') or score < 0.6:
                    lang = 'unknown'
            except Exception as e:
                self.logger.warning(f"[WARN] fastText error: {e}, fallback to langdetect")
                try:
                    lang = self.detect_language(sent)
                    if lang not in ('ru', 'en'):
                        lang = 'unknown'
                except Exception:
                    lang = 'unknown'
            if current_lang is None:
                current_lang = lang
            if lang != current_lang:
                blocks.append((current_lang, ' '.join(current_block)))
                current_block = [sent]
                current_lang = lang
            else:
                current_block.append(sent)
        if current_block:
            blocks.append((current_lang, ' '.join(current_block)))
        for lang, block in blocks:
            self.logger.debug(f"[INFO] Language block: {lang}, length: {len(block)}")
        return blocks

    def load_model(self, lang):
        """
        Load NLP model for the given language. Автоматически докачивает модель при ошибке.
        """
        try:
            if lang == 'ru':
                if 'ru' not in self.models:
                    if SVOChunker._natasha_ru is None:
                        SVOChunker._natasha_ru = {
                            'segmenter': Segmenter(),
                            'morph_vocab': MorphVocab(),
                            'emb': NewsEmbedding(),
                            'syntax': NewsSyntaxParser()
                        }
                    self.models['ru'] = SVOChunker._natasha_ru
                if SVOChunker._stanza_ru is None:
                    SVOChunker._stanza_ru = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                return self.models['ru']
            elif lang == 'en':
                if 'en' not in self.models:
                    if SVOChunker._spacy_en is None:
                        SVOChunker._spacy_en = spacy.load('en_core_web_sm')
                    self.models['en'] = SVOChunker._spacy_en
                if SVOChunker._stanza_en is None:
                    SVOChunker._stanza_en = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                return self.models['en']
            elif lang == 'uk':
                if SVOChunker._stanza_uk is None:
                    SVOChunker._stanza_uk = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                return None
            else:
                raise ValueError(f"Unsupported language: {lang}")
        except Exception as e:
            self.logger.warning(f"[load_model] Model load failed for lang={lang}: {e}. Trying to auto-download...")
            # Автодокачка нужной модели
            if lang == 'ru':
                self.ensure_model_available('natasha')
                self.ensure_model_available('stanza_ru')
            elif lang == 'en':
                self.ensure_model_available('spacy_en')
                self.ensure_model_available('stanza_en')
            elif lang == 'uk':
                self.ensure_model_available('stanza_uk')
            else:
                raise ValueError(f"Unsupported language: {lang}")
            # Повторная попытка
            try:
                if lang == 'ru':
                    if 'ru' not in self.models:
                        if SVOChunker._natasha_ru is None:
                            SVOChunker._natasha_ru = {
                                'segmenter': Segmenter(),
                                'morph_vocab': MorphVocab(),
                                'emb': NewsEmbedding(),
                                'syntax': NewsSyntaxParser()
                            }
                        self.models['ru'] = SVOChunker._natasha_ru
                    if SVOChunker._stanza_ru is None:
                        SVOChunker._stanza_ru = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                    return self.models['ru']
                elif lang == 'en':
                    if 'en' not in self.models:
                        if SVOChunker._spacy_en is None:
                            SVOChunker._spacy_en = spacy.load('en_core_web_sm')
                        self.models['en'] = SVOChunker._spacy_en
                    if SVOChunker._stanza_en is None:
                        SVOChunker._stanza_en = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                    return self.models['en']
                elif lang == 'uk':
                    if SVOChunker._stanza_uk is None:
                        SVOChunker._stanza_uk = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                    return None
                else:
                    raise ValueError(f"Unsupported language: {lang}")
            except Exception as e2:
                self.logger.error(f"[load_model] Model load failed after auto-download for lang={lang}: {e2}")
                raise

    def parse(self, text):
        """
        Tokenize and parse the text using the appropriate model.
        """
        lang = self.detect_language(text)
        model = self.load_model(lang)
        if lang == 'ru':
            segmenter = model['segmenter']
            morph_vocab = model['morph_vocab']
            emb = model['emb']
            syntax = model['syntax']
            doc = Doc(text)
            doc.segment(segmenter)
            doc.tag_morph(emb)
            doc.parse_syntax(syntax)
            for token in doc.tokens:
                token.lemmatize(morph_vocab)
            return {'lang': 'ru', 'doc': doc}
        elif lang == 'en':
            doc = model(text)
            return {'lang': 'en', 'doc': doc}

    def parse_with_pos(self, text: str, force_lang: str = None) -> List[Dict[str, Any]]:
        """
        Universal method: returns list of tokens with POS and dependency info for the detected language.
        force_lang — if set, use this language instead of auto-detect.
        """
        lang = force_lang if force_lang else self.detect_language(text)
        if lang == 'ru':
            if SVOChunker._stanza_ru is None:
                self.logger.info(f"[SVOChunker] Downloading or loading Stanza model for language: ru (use_gpu={self.use_gpu}) ...")
                SVOChunker._stanza_ru = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[SVOChunker] Stanza model for 'ru' loaded.")
                self.logger.info(f"[SVOChunker] Stanza RU device: {SVOChunker._stanza_ru.device}")
            nlp = SVOChunker._stanza_ru
        elif lang == 'en':
            if SVOChunker._stanza_en is None:
                self.logger.info(f"[SVOChunker] Downloading or loading Stanza model for language: en (use_gpu={self.use_gpu}) ...")
                SVOChunker._stanza_en = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[SVOChunker] Stanza model for 'en' loaded.")
                self.logger.info(f"[SVOChunker] Stanza EN device: {SVOChunker._stanza_en.device}")
            nlp = SVOChunker._stanza_en
        elif lang == 'uk':
            if SVOChunker._stanza_uk is None:
                self.logger.info(f"[SVOChunker] Downloading or loading Stanza model for language: uk (use_gpu={self.use_gpu}) ...")
                SVOChunker._stanza_uk = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma,depparse', use_gpu=self.use_gpu)
                self.logger.info("[SVOChunker] Stanza model for 'uk' loaded.")
                self.logger.info(f"[SVOChunker] Stanza UK device: {SVOChunker._stanza_uk.device}")
            nlp = SVOChunker._stanza_uk
        else:
            raise ValueError(f"Unsupported language: {lang}")
        tokens = []
        for sent in nlp(text).sentences:
            for word in sent.words:
                tokens.append({
                    'text': word.text,
                    'lemma': word.lemma,
                    'pos': word.upos,
                    'head': word.head,
                    'deprel': word.deprel,
                    'id': word.id,
                    'sent_id': sent.sent_id if hasattr(sent, 'sent_id') else None
                })
        return tokens

    def extract_sv_pairs(self, tokens: List[Dict[str, Any]]) -> List[Dict[str, Optional[Dict[str, Any]]]]:
        """
        Extract S–V pairs from list of tokens (Stanza output).
        Returns list of dicts: {'subject': subj_token, 'verb': verb_token}
        """
        sv_pairs = []
        for token in tokens:
            # Universal Dependencies: nsubj, nsubj:pass, csubj — subject
            if token['deprel'] and token['deprel'].startswith('nsubj') or token['deprel'] == 'csubj':
                subj = token
                head_id = token['head']
                # find head (verb/predicate)
                verb = next((t for t in tokens if t['id'] == head_id and t['pos'] in ('VERB', 'AUX')), None)
                if verb:
                    sv_pairs.append({'subject': subj, 'verb': verb})
        return sv_pairs

    async def chunk_by_sv_semantics(self, text: str, base_url: str = "http://localhost", port: int = 8001, window: int = 3) -> list:
        """
        Splits the text into chunks based on S–V pairs with boundary optimization by cosine deviation.
        If no S–V pairs are found in a block, returns the block as a single chunk with its embedding.
        If only one S–V pair is found in a block, returns the block as a single chunk with its embedding.
        window — maximum boundary shift (in tokens) from the midpoint between S–V pairs.
        Returns a list of chunks: {'start': int, 'end': int, 'sv': (subj, verb), 'block': [tokens], 'score': float}
        """
        blocks = self.split_by_language(text)
        all_chunks = []
        token_offset = 0
        block_offset = 0  # абсолютное смещение блока в исходном тексте
        text_len = len(text)
        async with EmbeddingServiceAsyncClient(base_url, port) as client:
            for lang, block in blocks:
                search_start = block_offset
                block_start = text.find(block, search_start)
                if block_start == -1:
                    block_start = text.find(block)
                    if block_start == -1:
                        self.logger.error(f"[CHUNKER] Block not found in text: '{block[:40]}'")
                        block_start = 0
                block_end = block_start + len(block)
                # --- Если язык не поддерживается, просто векторизуем блок как отдельный чанк ---
                if lang not in ('ru', 'en', 'uk'):
                    try:
                        emb_block_resp = await client.cmd("embed", params={"texts": [block]})
                        emb_block = emb_block_resp.get('result', emb_block_resp)
                        if isinstance(emb_block, dict) and 'embeddings' in emb_block:
                            emb_block = emb_block['embeddings']
                        emb_block = np.array(emb_block)[0] if isinstance(emb_block, (list, np.ndarray)) else emb_block
                    except Exception as e:
                        self.logger.error(f"Embedding service error (unknown block): {e}")
                        emb_block = []
                    all_chunks.append((
                        {
                            'start': token_offset,
                            'end': token_offset,
                            'sv': None,
                            'block': [],
                            'tokens': [],
                            'text': text[block_start:block_end],
                            'score': 0.0
                        },
                        emb_block.tolist() if hasattr(emb_block, 'tolist') else emb_block
                    ))
                    block_offset = block_end
                    continue
                tokens = self.parse_with_pos(block, force_lang=lang)
                sv_pairs = self.extract_sv_pairs(tokens)
                texts = [t['text'] for t in tokens]
                try:
                    emb_tokens_resp = await client.cmd("embed", params={"texts": texts})
                    emb_tokens = emb_tokens_resp.get('result', emb_tokens_resp)
                    if isinstance(emb_tokens, dict) and 'embeddings' in emb_tokens:
                        emb_tokens = emb_tokens['embeddings']
                    emb_tokens = np.array(emb_tokens)
                except Exception as e:
                    self.logger.error(f"Embedding service error: {e}")
                    token_offset += len(tokens)
                    block_offset = block_end
                    continue
                # --- Границы чанков ---
                if len(sv_pairs) < 2:
                    # Один чанк на весь блок
                    chunk_vector = np.sum(emb_tokens, axis=0)
                    chunk_text = text[block_start:block_end]
                    all_chunks.append((
                        {
                            'start': token_offset,
                            'end': token_offset + len(tokens),
                            'sv': sv_pairs[0] if sv_pairs else None,
                            'block': tokens,
                            'tokens': tokens,
                            'text': chunk_text,
                            'score': 0.0
                        },
                        chunk_vector.tolist()
                    ))
                    token_offset += len(tokens)
                    block_offset = block_end
                    continue
                # Если S–V-пар >= 2, вычисляем boundaries по токенам
                sv_centers = [(min(pair['subject']['id'], pair['verb']['id']), max(pair['subject']['id'], pair['verb']['id'])) for pair in sv_pairs]
                sv_centers = [int(np.mean(c)) for c in sv_centers]
                boundaries = [0]
                for i in range(1, len(sv_centers)):
                    mid = (sv_centers[i-1] + sv_centers[i]) // 2
                    boundaries.append(mid)
                boundaries.append(len(tokens))
                # Переводим boundaries из токенов в символы исходного текста
                token_char_offsets = []
                idx = 0
                for t in tokens:
                    t_text = t['text']
                    start = block.find(t_text, idx)
                    if start == -1:
                        start = idx
                    token_char_offsets.append(start)
                    idx = start + len(t_text)
                # Добавляем конец блока
                token_char_offsets.append(len(block))
                # boundaries по символам
                boundaries_chars = [block_start + (token_char_offsets[b] if b < len(token_char_offsets) else len(block)) for b in boundaries]
                # Формируем чанки по этим границам
                for i in range(len(boundaries_chars)-1):
                    start_idx = boundaries[i]
                    end_idx = boundaries[i+1]
                    chunk_tokens = tokens[start_idx:end_idx]
                    chunk_vector = np.sum(emb_tokens[start_idx:end_idx], axis=0)
                    chunk_text = text[boundaries_chars[i]:boundaries_chars[i+1]]
                    all_chunks.append((
                        {
                            'start': token_offset + start_idx,
                            'end': token_offset + end_idx,
                            'sv': sv_pairs[i] if i < len(sv_pairs) else None,
                            'block': chunk_tokens,
                            'tokens': chunk_tokens,
                            'text': chunk_text,
                            'score': 0.0  # (опционально: можно добавить score)
                        },
                        chunk_vector.tolist()
                    ))
                token_offset += len(tokens)
                block_offset = block_end
        return all_chunks

    @staticmethod
    def reconstruct_with_separators(text, chunks):
        """
        Reconstructs the original text from chunk list, preserving all separators between chunks.
        Args:
            text (str): The original text.
            chunks (list): List of (chunk, vector) tuples, where chunk['text'] is the chunk text.
        Returns:
            str: The reconstructed text.
        """
        logger = logging.getLogger("SVOChunker.reconstruct_with_separators")
        pos = 0
        result = []
        for i, (chunk, _) in enumerate(chunks):
            chunk_text = chunk['text']
            idx = text.find(chunk_text, pos)
            if idx == -1:
                logger.error(f"[reconstruct] Chunk {i} not found in original text: '{chunk_text[:40]}' (search from pos {pos})")
                # Добавляем всё, что осталось, к предыдущему чанку, и идём дальше
                if i == 0:
                    result.append(text[pos:])
                else:
                    result[-1] += text[pos:]
                pos = len(text)
                break
            # Всё, что между pos и idx — это разделитель
            sep = text[pos:idx]
            if i == 0:
                result.append(sep + chunk_text)
            else:
                result[-1] += sep
                result.append(chunk_text)
            logger.debug(f"[reconstruct] Chunk {i}: found at idx={idx}, sep='{sep[:20]}'")
            pos = idx + len(chunk_text)
        # Если что-то осталось после последнего чанка — добавляем к последнему
        if pos < len(text) and result:
            logger.debug(f"[reconstruct] Appending tail: '{text[pos:][:40]}'")
            result[-1] += text[pos:]
        return ''.join(result)

    def ensure_model_available(self, model_name: str):
        """
        Ensure the specified model is available. If not, download/install it.
        Supported: 'fasttext', 'spacy_en', 'stanza_ru', 'stanza_en', 'stanza_uk', 'natasha'.
        """
        try:
            if model_name == 'fasttext':
                fasttext_model_path = os.path.join(os.path.expanduser('~'), '.cache', 'fasttext', 'lid.176.bin')
                if not os.path.exists(fasttext_model_path):
                    self.logger.info(f"[ensure_model_available] Downloading fastText model lid.176.bin ...")
                    url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'
                    os.makedirs(os.path.dirname(fasttext_model_path), exist_ok=True)
                    urllib.request.urlretrieve(url, fasttext_model_path)
                    self.logger.info(f"[ensure_model_available] fastText model downloaded: {fasttext_model_path}")
                else:
                    self.logger.info(f"[ensure_model_available] fastText model already exists: {fasttext_model_path}")
            elif model_name == 'spacy_en':
                try:
                    import spacy
                    spacy.load('en_core_web_sm')
                    self.logger.info("[ensure_model_available] spaCy en_core_web_sm is ready.")
                except Exception:
                    self.logger.info("[ensure_model_available] Downloading spaCy en_core_web_sm ...")
                    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
                    self.logger.info("[ensure_model_available] spaCy en_core_web_sm downloaded.")
            elif model_name.startswith('stanza_'):
                lang = model_name.split('_')[1]
                import stanza
                try:
                    stanza.Pipeline(lang=lang, processors='tokenize,pos,lemma,depparse', download_method=None)
                    self.logger.info(f"[ensure_model_available] Stanza model for '{lang}' is ready.")
                except Exception:
                    self.logger.info(f"[ensure_model_available] Downloading Stanza model for '{lang}' ...")
                    stanza.download(lang)
                    self.logger.info(f"[ensure_model_available] Stanza model for '{lang}' downloaded.")
            elif model_name == 'natasha':
                try:
                    from natasha import NewsEmbedding
                    _ = NewsEmbedding()
                    self.logger.info("[ensure_model_available] Natasha NewsEmbedding is ready.")
                except Exception as e:
                    self.logger.error(f"[ensure_model_available] Natasha NewsEmbedding error: {e}")
            else:
                self.logger.warning(f"[ensure_model_available] Unknown model: {model_name}")
        except Exception as e:
            self.logger.error(f"[ensure_model_available] Failed to ensure model '{model_name}': {e}")

# ... further steps will be implemented in next iterations ... 