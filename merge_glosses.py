#!/usr/bin/env python3
"""Merge glosses.py short definitions into data.json's vocab entries."""
import json
import sys
from glosses import GLOSSES

GLOSSES_LOWER = {k.lower(): v for k, v in GLOSSES.items()}


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else 'data.json'
    with open(src, encoding='utf-8') as f:
        d = json.load(f)

    missing = []
    for v in d['vocab']:
        term = v['term']
        gloss = GLOSSES.get(term) or GLOSSES_LOWER.get(term.lower())
        if gloss is None:
            missing.append(term)
            gloss = ''
        v['gloss'] = gloss

    if missing:
        print(f'WARNING: {len(missing)} vocab terms have no gloss:')
        for m in missing:
            print(' -', repr(m))
    else:
        print('All vocab terms have a gloss.')

    with open(src, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
