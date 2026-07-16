#!/usr/bin/env python3
"""
Extract vocab / underline / quiz / grammar-source data directly from the
source docx (英語(Writing&Reading).docx) for the Narnia study tool.

Reads run-level w:highlight (GRAY_25 = vocab word/phrase, YELLOW = teacher-
flagged "important sentence") and w:u (underline = translation-drill phrase)
formatting instead of going through a pandoc Markdown round-trip, so that:
  - single-word underlines are no longer dropped
  - adjacent runs with identical formatting are merged into one span instead
    of being fragmented by Word's internal run boundaries / nested marks

Usage:
    python3 extract_from_docx.py <path-to-docx> <output-dir>

Outputs (in <output-dir>):
    data.json       -- {vocab: [...], underline: [...], quiz: [...], yellow_sentences: [...]}
"""
import sys
import re
import json
import docx
from docx.enum.text import WD_COLOR_INDEX


def is_japanese(text):
    for ch in text:
        code = ord(ch)
        if (0x3040 <= code <= 0x30FF) or (0x4E00 <= code <= 0x9FFF) or (0xFF00 <= code <= 0xFFEF):
            return True
    return False


def is_separator(text):
    t = text.strip()
    if not t:
        return True
    core = re.sub(r'[_\s\d]', '', t)
    return len(core) == 0


def classify_run(run):
    hl = run.font.highlight_color
    highlight = None
    if hl == WD_COLOR_INDEX.GRAY_25:
        highlight = 'vocab'
    elif hl == WD_COLOR_INDEX.YELLOW:
        highlight = 'sentence'
    underline = bool(run.underline)
    return highlight, underline


def build_spans(paragraph):
    """Merge consecutive runs with identical (highlight, underline) formatting.
    Returns list of dicts: {text, highlight, underline}
    """
    spans = []
    for run in paragraph.runs:
        text = run.text
        if text == '':
            continue
        highlight, underline = classify_run(run)
        if spans and spans[-1]['highlight'] == highlight and spans[-1]['underline'] == underline:
            spans[-1]['text'] += text
        else:
            spans.append({'text': text, 'highlight': highlight, 'underline': underline})
    return spans


def render_html(spans):
    # 'sentence' (yellow) highlighting is a translation-annotation signal, not a
    # vocab target -- render it as plain text so it doesn't clutter context HTML.
    # NOTE: only fix typos here, never strip whitespace -- these spans still
    # carry the leading/trailing spaces that separate them from their neighbors.
    parts = []
    for sp in spans:
        t = fix_typos(sp['text'])
        if sp['highlight'] == 'vocab':
            inner = f'<mark>{t}</mark>' if not sp['underline'] else f'<mark><u>{t}</u></mark>'
        else:
            inner = f'<u>{t}</u>' if sp['underline'] else t
        parts.append(inner)
    return ''.join(parts)


# Known typos in the source docx that would otherwise leak into vocab cards.
TEXT_FIXES = {
    'hidé': 'hide',
    've been away': "'ve been away",
}


def fix_typos(t):
    return TEXT_FIXES.get(t, t)


def clean_term(t):
    """Used only for extracted term/underline strings (already .strip()-ed),
    never for in-context span text -- stripping here is safe/intended."""
    t = fix_typos(t)
    return t.strip().strip(';:,.!').strip()


def word_count(s):
    return len(re.findall(r"[A-Za-z']+", s))


# Bare function words that carry no learning value as a standalone flashcard
# (they still appear normally inside sentence context / underline drills).
VOCAB_DROP = {
    'and', 'as', 'if', 'a', 'on', 'with', 'out', 'to', 'it', 'of the', 'not', 'up',
}


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else 'source.docx'
    outdir = sys.argv[2] if len(sys.argv) > 2 else '.'

    doc = docx.Document(src)
    paras = doc.paragraphs
    n = len(paras)

    chapter = 0
    pairs = []  # {chapter, para, en_text, jp_text}

    i = 0
    while i < n:
        text = paras[i].text.strip()
        if not text:
            i += 1
            continue
        if text.upper().startswith('CHAPTER'):
            chapter += 1
            i += 1
            continue
        if is_separator(text):
            i += 1
            continue
        if is_japanese(text):
            # chapter subtitle lines mix EN(JP) in one paragraph, or stray JP line
            i += 1
            continue
        # candidate english paragraph -> look ahead for its japanese translation
        j = i + 1
        while j < n and (not paras[j].text.strip() or is_separator(paras[j].text.strip())):
            j += 1
        if j >= n:
            break
        jp_text = paras[j].text.strip()
        if not is_japanese(jp_text):
            i += 1
            continue
        pairs.append({'chapter': chapter, 'para': paras[i], 'en_text': text, 'jp_text': jp_text})
        i = j + 1

    vocab = []
    underline = []
    quiz = []
    yellow_sentences = []

    for pair in pairs:
        spans = build_spans(pair['para'])
        en_html = render_html(spans)
        en_text = pair['en_text']
        jp_text = pair['jp_text']
        chap = pair['chapter']

        quiz.append({'en': en_text, 'jp': jp_text, 'chapter': chap})

        # vocab: lightGray-highlighted spans, words/short idioms (<=8 words)
        for sp in spans:
            if sp['highlight'] == 'vocab':
                term = clean_term(sp["text"].strip())
                if not term or term.lower() in VOCAB_DROP:
                    continue
                wc = word_count(term)
                if 1 <= wc <= 8:
                    vocab.append({
                        'term': term,
                        'enHtml': en_html,
                        'jp': jp_text,
                        'chapter': chap,
                    })

        # underline: any underlined span (including single words now)
        for sp in spans:
            if sp['underline']:
                term = clean_term(sp["text"].strip())
                if not term:
                    continue
                underline.append({
                    'underline': term,
                    'enHtml': en_html,
                    'jp': jp_text,
                    'chapter': chap,
                })

        # yellow "important sentence" markers, collect the full english sentence
        # they occur in, for grammar-question source material
        has_yellow = any(sp['highlight'] == 'sentence' for sp in spans)
        if has_yellow:
            yellow_sentences.append({'en': en_text, 'jp': jp_text, 'chapter': chap})

    print(f'pairs: {len(pairs)}')
    print(f'vocab: {len(vocab)}')
    print(f'underline: {len(underline)}')
    print(f'quiz: {len(quiz)}')
    print(f'yellow_sentences: {len(yellow_sentences)}')

    with open(f'{outdir}/data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'vocab': vocab,
            'underline': underline,
            'quiz': quiz,
            'yellow_sentences': yellow_sentences,
        }, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
