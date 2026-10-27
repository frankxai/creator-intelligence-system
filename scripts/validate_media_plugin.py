#!/usr/bin/env python3
"""Fast local/CI structural checks for skills-only media plugin. Not a full platform validator."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'plugins'/'starlight-media-excellence'
def verify(root=P):
    errors=[]
    mpath=root/'plugin.json'
    if not mpath.is_file(): return ['missing plugin.json']
    try:
        m=json.loads(mpath.read_text())
        if m.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json': errors.append('bad schema')
        if m.get('name')!='starlight-media-excellence': errors.append('identity drift')
        if not re.fullmatch(r'\d+\.\d+\.\d+',m.get('version','')): errors.append('invalid version')
        interface=m['extensions']['com.openai']['interface']
        if len(interface['shortDescription'])>30: errors.append('shortDescription > 30')
        for path in ['logo','composerIcon']:
            value=interface.get(path)
            if value and not (root/value).is_file(): errors.append('missing '+path)
        if (root/'mcp.json').exists(): errors.append('unexpected MCP configuration; preserve skills-only boundary')
    except Exception as exc:errors.append('manifest: '+str(exc))
    paths=list((root/'skills').glob('*/SKILL.md'))
    expected={'media-director','media-release-critic','media-continuity'}
    if {x.parent.name for x in paths}!=expected:errors.append('unexpected skills')
    for path in paths:
        try:
            s=path.read_text()
            if not s.startswith('---\n'): errors.append('frontmatter missing '+str(path));continue
            fm=s.split('---\n',2)[1]
            if f'name: {path.parent.name}' not in fm: errors.append('name mismatch '+str(path))
            if 'description: Use' not in fm: errors.append('trigger missing '+str(path))
            if not s.split('---\n',2)[2].strip():errors.append('instructions missing '+str(path))
        except Exception as exc:errors.append(str(exc))
    for path in root.rglob('*'):
        if path.is_symlink():errors.append('symlink '+str(path))
        if path.is_file() and any(x in path.name.lower() for x in ['.env','secret','token.json']):errors.append('sensitive filename '+str(path))
    return errors
if __name__=='__main__':
    problems=verify()
    print('MEDIA PLUGIN STRUCTURE', 'PASS' if not problems else 'FAIL',problems)
    sys.exit(bool(problems))
