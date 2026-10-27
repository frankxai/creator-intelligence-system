#!/usr/bin/env python3
"""Independent byte-integrity and state-boundary validator for a rendered media pack.

Hash fidelity is not a substitute for visual QA or release authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

EXPECTED_STATES = {
    'render': {'RENDERED', 'NOT_RENDERED'},
    'qa': {'NOT_REVIEWED', 'QA_PASS', 'QA_FAIL', 'HOLD'},
    'approval': {'NOT_GRANTED', 'FOUNDER_APPROVED'},
    'publication': {'NOT_PUBLISHED', 'PUBLISHED'},
}


def verify(manifest_path: Path) -> list[str]:
    errors = []
    try:
        content = json.loads(manifest_path.read_text(encoding='utf8'))
    except (OSError, ValueError) as e:
        return [f'invalid manifest: {e}']
    if content.get('schema_version') != 'media-rendition-receipt.v1':
        errors.append('incorrect manifest schema')
    if not re.fullmatch(r'[0-9a-f]{64}', content.get('source_revision','')):
        errors.append('source revision must be SHA-256')
    if not content.get('rights') or not content.get('evidence_note'):
        errors.append('missing provenance/rights context')
    seen = set()
    records = content.get('artifacts')
    if not isinstance(records, list) or not records:
        errors.append('missing artifact list')
        records=[]
    for record in records:
        if not isinstance(record,dict):
            errors.append('invalid artifact record')
            continue
        name = record.get('path','')
        # Local, immediate children only; prevents relative path traversal and malicious read.
        if not isinstance(name,str) or name in {'.','..'} or Path(name).name != name or '\\' in name or '/' in name:
            errors.append(f'unsafe artifact path: {name!r}')
            continue
        if name in seen:
            errors.append(f'duplicate artifact: {name}')
            continue
        seen.add(name)
        path = manifest_path.parent/name
        if path.is_symlink() or not path.is_file():
            errors.append(f'missing or symlink artifact: {name}')
            continue
        data=path.read_bytes()
        if len(data)!=record.get('bytes'):
            errors.append(f'size mismatch: {name}')
        if hashlib.sha256(data).hexdigest()!=record.get('sha256'):
            errors.append(f'hash mismatch: {name}')
    states = content.get('state',{})
    for field,values in EXPECTED_STATES.items():
        if states.get(field) not in values:
            errors.append(f'invalid status: {field}')
    if states.get('approval') == 'FOUNDER_APPROVED' and states.get('qa') != 'QA_PASS':
        errors.append('approved without QA_PASS')
    if states.get('publication') == 'PUBLISHED' and states.get('approval') != 'FOUNDER_APPROVED':
        errors.append('published without exact approval')
    if states.get('publication') == 'PUBLISHED' and not content.get('publication_receipt'):
        errors.append('published without provider receipt')
    if content.get('claims', {}).get('live_product_proof') is True and content.get('kind') == 'authored-architecture-illustration':
        errors.append('conceptual illustration claiming live product proof')
    return errors


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);args=p.parse_args()
    errors=verify(args.manifest)
    print('MEDIA MANIFEST', 'PASS' if not errors else 'FAIL')
    for x in errors:print(' -',x)
    raise SystemExit(bool(errors))
