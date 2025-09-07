import importlib, os
mods = []
try:
  with open('.deploy_info') as f:
    for line in f:
      if line.startswith('ENTRY_MODULE='):
        v = line.split('=',1)[1].strip()
        if v:
          mods.append(v)
except Exception:
  pass
mods += ['app','server','main','application','run','index']
app = None
for m in mods:
  try:
    mod = importlib.import_module(m)
  except Exception:
    continue
  for fn in ('create_app','get_app'):
    fnc = getattr(mod, fn, None)
    if callable(fnc):
      try:
        app = fnc(); break
      except TypeError:
        pass
  if app is None:
    a = getattr(mod, 'app', None)
    if callable(a):
      try: app = a()
      except TypeError: app = a
    else:
      app = a
  if app is not None:
    break
if app is None:
  raise RuntimeError('Flask app not found from candidates: %r' % mods)
