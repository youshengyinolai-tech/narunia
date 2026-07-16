#!/usr/bin/env python3
"""
Cross-reference kotest.json (weekly pop-quiz fill-in-the-blank items the
student pasted in) against data.json's vocab list, tagging matches with
exam:true so the study tool can offer a "小テストの語のみ" filter.

Also appends a handful of new vocab entries for pop-quiz answers that have
no reasonable existing vocab-list match (mostly because the original
extraction only captures highlighted spans from the docx, and a few of
these words/phrases were never highlighted, or are supplementary
vocabulary -- mustache/whisker -- that isn't in the book text at all).

Run after merge_glosses.py and before build_html.py:
    python3 add_kotest_tags.py data.json kotest.json
"""
import json
import re
import sys

# Curated additions: pop-quiz answers with no existing vocab entry worth
# reusing. Context sentences (enHtml/jp) are taken from the real book text
# where available; mustache/whisker aren't in the book, so they get a
# hand-written example sentence instead.
NEW_ENTRIES = [
    {
        "term": "rows",
        "gloss": "列（並んだもの）",
        "chapter": 1,
        "enHtml": "the thought of all those long passages and <mark>rows</mark> of doors leading into empty rooms was beginning to make her feel a little creepy.",
        "jp": "長い廊下や、空っぽの部屋へと続くドアの列を思うと、少し不気味な気分になり始めていた。",
    },
    {
        "term": "row",
        "gloss": "騒動、口論（インフォーマル）",
        "chapter": 1,
        "enHtml": "\"There's sure to be a <mark>row</mark> if we're heard talking here.\"",
        "jp": "「ここで話しているのが聞こえたら、きっと怒られるわ」",
    },
    {
        "term": "set out",
        "gloss": "出発する",
        "chapter": 1,
        "enHtml": "she could still see the open doorway of the wardrobe and even catch a glimpse of the empty room from which she had <mark>set out</mark>.",
        "jp": "まだ開いたままのワードローブの扉が見え、自分が旅立った空っぽの部屋さえちらりと見えた。",
    },
    {
        "term": "room",
        "gloss": "スペース、余地（無冠詞で）",
        "chapter": 1,
        "enHtml": "going still further in and pushing the soft folds of the coats aside to make <mark>room</mark> for her.",
        "jp": "さらに奥へと進み、自分の通るスペースを作るためにコートの柔らかなかさなりを脇へ押しやった。",
    },
    {
        "term": "aside",
        "gloss": "脇へ（set asideで「取っておく」）",
        "chapter": 1,
        "enHtml": "going still further in and pushing the soft folds of the coats <mark>aside</mark> to make room for her.",
        "jp": "さらに奥へと進み、自分の通るスペースを作るためにコートの柔らかなかさなりを脇へ押しやった。",
    },
    {
        "term": "intended",
        "gloss": "意図した",
        "chapter": 2,
        "enHtml": "and then it stopped as if it had been going to say something it had not <mark>intended</mark> but had remembered in time.",
        "jp": "まるで言おうとしていたこととは別のことを口にしようとしたが、間一髪で思い出したかのように、彼は言葉を止めた。",
    },
    {
        "term": "respects",
        "gloss": "点（in other respectsで「他の点では」）",
        "chapter": 3,
        "enHtml": "It was a beautiful face in other <mark>respects</mark>, but proud and cold and stern.",
        "jp": "他の点では美しい顔だったが、高慢で冷たく、厳格な表情を浮かべていた。",
    },
    {
        "term": "stern",
        "gloss": "厳格な、厳しい",
        "chapter": 3,
        "enHtml": "It was a beautiful face in other respects, but proud and cold and <mark>stern</mark>.",
        "jp": "他の点では美しい顔だったが、高慢で冷たく、厳格な表情を浮かべていた。",
    },
    {
        "term": "looking out",
        "gloss": "面している、外を見ている",
        "chapter": 1,
        "enHtml": "a long, low room with two windows <mark>looking out</mark> in one direction and two in another.",
        "jp": "そこは細長い低めの部屋で、一方向には窓が二つ、もう一方向にも窓が二つあった。",
    },
    {
        "term": "mustache",
        "gloss": "口ひげ",
        "chapter": 1,
        "enHtml": "He had a small <mark>mustache</mark> under his nose.",
        "jp": "彼は鼻の下に小さな口ひげを生やしていた。",
    },
    {
        "term": "whisker",
        "gloss": "頬ひげ",
        "chapter": 1,
        "enHtml": "The old man had thick <mark>whiskers</mark> on his cheeks.",
        "jp": "その老人は頬に濃い頬ひげを生やしていた。",
    },
]


def norm(s):
    s = s.lower().strip()
    s = re.sub(r'^(the|a|an)\s+', '', s)
    return s


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else 'data.json'
    kotest_path = sys.argv[2] if len(sys.argv) > 2 else 'kotest.json'

    data = json.load(open(data_path, encoding='utf-8'))
    kotest = json.load(open(kotest_path, encoding='utf-8'))

    vocab = data['vocab']
    tagged = 0
    for item in kotest:
        ans = norm(item['answer'])
        for v in vocab:
            tn = norm(v['term'])
            if tn == ans or (len(ans) > 3 and (ans in tn or tn in ans)):
                if not v.get('exam'):
                    v['exam'] = True
                    tagged += 1
                break

    existing_terms = {v['term'].lower() for v in vocab}
    added = 0
    for entry in NEW_ENTRIES:
        if entry['term'].lower() in existing_terms:
            continue
        vocab.append({**entry, 'exam': True})
        added += 1

    print(f'tagged {tagged} existing vocab entries as exam:true')
    print(f'added {added} new vocab entries')
    print(f'total vocab: {len(vocab)}')

    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
