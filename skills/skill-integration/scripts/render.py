#!/usr/bin/env python3
"""Render skill-integration snapshots into one Cypher CREATE statement.

Usage: render.py <local.json|-> <their.json> <out.cypher>
Pass '-' as local.json to render the their side only.

Validates the snapshots first; on any problem prints them to stderr and exits 1
without writing the output file.
"""
import json
import re
import sys

KINDS = {'Skill', 'Agent', 'Command', 'Hook', 'Rule'}
TYPES = {'INVOKES', 'FLOWS_TO', 'REFERENCES'}


def q(s):
    s = s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    return "'" + re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', s) + "'"


def key(k):
    return '`%s`' % k if re.search(r'[^A-Za-z0-9_]', k) else k


def scalar(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return repr(v)
    return q(str(v))


def props(d):
    out = []
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, list) and v and all(not isinstance(x, (list, dict)) for x in v) \
                and len({type(x) for x in v}) == 1:
            out.append('%s: [%s]' % (key(k), ', '.join(scalar(x) for x in v)))
        elif isinstance(v, (list, dict)):
            out.append('%s: %s' % (key(k + '_json'), q(json.dumps(v, ensure_ascii=False))))
        else:
            out.append('%s: %s' % (key(k), scalar(v)))
    return ', '.join(out)


def check(snap, side, errors):
    ids = {}
    for n in snap.get('nodes', []):
        if n['kind'] not in KINDS:
            errors.append('%s: node %s has unknown kind %s' % (side, n['id'], n['kind']))
        if 'name' not in n.get('props', {}):
            errors.append('%s: node %s has no name' % (side, n['id']))
        if n['id'] in ids:
            errors.append('%s: duplicate node id %s' % (side, n['id']))
        ids[n['id']] = n
    seen = set()
    for r in snap.get('rels', []):
        k = (r['from'], r['type'], r['to'])
        if r['type'] not in TYPES:
            errors.append('%s: unknown relationship type %s' % (side, r['type']))
        for end in (r['from'], r['to']):
            if end not in ids:
                errors.append('%s: relationship %s -> %s points to missing node %s' % (side, r['from'], r['to'], end))
        if k in seen:
            errors.append('%s: duplicate relationship %s' % (side, k))
        if not r.get('reason'):
            errors.append('%s: relationship %s has no reason' % (side, k))
        seen.add(k)
    return ids


def render(snap, prefix, label, lines, rels):
    var = {}
    for n in snap.get('nodes', []):
        v = '%s%d' % (prefix, len(var) + 1)
        var[n['id']] = v
        p = dict(n['props'])
        if snap.get('repo') and snap.get('commit'):
            p['url'] = '%s/blob/%s/%s' % (snap['repo'].rstrip('/'), snap['commit'], n['file'])
        lines.append('  (%s:%s:%s {%s})' % (v, label, n['kind'], props(p)))
    for r in snap.get('rels', []):
        rels.append('  (%s)-[:%s {reason: %s}]->(%s)' % (var[r['from']], r['type'], q(r['reason']), var[r['to']]))


def main():
    local_path, their_path, out = sys.argv[1:4]
    load = lambda p: {'nodes': [], 'rels': []} if p == '-' else json.load(open(p, encoding='utf-8'))
    local, their = load(local_path), load(their_path)
    errors = []
    check(local, 'local', errors)
    check(their, 'their', errors)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    head = ['// source: %s' % their.get('source', ''), '// commit: %s' % their.get('commit', '')]
    body, rels = [], []
    if local_path != '-':
        body.append('  // local')
        render(local, 'l', 'local', body, rels)
    body.append('  // their')
    render(their, 't', 'their', body, rels)
    body += ['  // relationships'] + rels
    items = [i for i, l in enumerate(body) if not l.startswith('  //')]
    for i in items[:-1]:
        body[i] += ','
    if items:
        body[items[-1]] += ';'
    open(out, 'w', encoding='utf-8').write('\n'.join(head + ['CREATE'] + body) + '\n')
    count = lambda s, f: len(s.get(f, []))
    print('local %d nodes / %d rels, their %d nodes / %d rels -> %s' % (
        count(local, 'nodes'), count(local, 'rels'), count(their, 'nodes'), count(their, 'rels'), out))


if __name__ == '__main__':
    main()
