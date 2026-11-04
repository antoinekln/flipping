"""Build generateur.html (single file) = generateur_src.html + template.html + page-flip.js.
Run:  python make_template.py && python build.py   (from this folder)"""
import json
src = open('generateur_src.html', encoding='utf-8').read()
tpl = open('template.html', encoding='utf-8').read()
lib = open('page-flip.js', encoding='utf-8').read()
def js(s): return json.dumps(s, ensure_ascii=False).replace('</', '<\\/')
out = src.replace('/*TEMPLATE*/""', js(tpl)).replace('/*LIB*/""', js(lib))
open('generateur.html', 'w', encoding='utf-8').write(out)
print('generateur.html', len(out))
