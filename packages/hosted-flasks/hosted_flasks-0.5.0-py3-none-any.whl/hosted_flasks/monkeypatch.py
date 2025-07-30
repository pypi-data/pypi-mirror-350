import os
import logging

from collections import UserDict

logger = logging.getLogger(__name__)

# os.environ.get

DONT_UNLOAD_MODULES = [
  "importlib", "warnings", "builtins", "sys", "_pytest", "codecs",
  "eventlet",
  "werkzeug", "flask", "hosted_flasks",
  "cryptography", "bcrypt",
  "urllib3"
]

# keep a copy of the environment before we use any scoped environments
# it contains optionally already scoped variables, e.g. not loaded explicitly
# by the scoped modules
base_environ = os.environ.copy()

class Environment(UserDict):
  def __init__(self, scope, debug=False):
    self._scope = scope.upper().replace("-", "_") # ensure proper env var name
    self._debug = debug
    super().__init__()
    # explicitly use the original __setitem__, else we might end up with double
    # prefixes
    for k, v in base_environ.items():
      super().__setitem__(k, v)

  @classmethod
  def scope(cls, scope, debug=False):
    logger.info(f"🔧 creating fresh os.environ, for {scope}")
    # Remove loaded modules, with some exceptions ;-)

    # Reasoning: within the scope of an other hosted flask, modules have been
    # loaded, during which they could have accessed environment variables and
    # have stored their value locally, or simply got a reference to os.environ
    # and use that later on. This means that IF another hosted flask would reuse
    # them, the same environment variables would be used also. Since every
    # hosted flask should be configurable with their own variables in a fresh
    # environment, all modules should also be unloaded. Because we can't know
    # which modules have already accessed and cached variables, we need to
    # unload all of them. Due to other side-effects, like importing a class and
    # comparing objects to it, which might cause the "orginally" same class to
    # be different in two cases, some modules are excluded.
    
    # Warning: this approach is not fool proof. There can always be side-effects
    # that will mutually block. For now it holds 😇

    import sys
    for mod_name in list(sys.modules.keys()):
      keep = False
      for exception in DONT_UNLOAD_MODULES:
        if mod_name[:len(exception)] == exception:
          keep = True
          break
      if not keep:
        sys.modules.pop(mod_name, None) 
    import os
    patched_environ = cls(scope, debug=debug)
    os.environ = patched_environ
    return patched_environ

  def _get_raw(self, key):
    # utility to access env var without looking up the calling app
    return super().__getitem__(key)  # pragma: no cover

  def _log(self, msg):
    if self._debug:
      logger.info(msg) # pragma: no cover
  
  def __setitem__(self, key, value):
    # add the scope prefix
    scoped_key = f"{self._scope}_{key}"
    self._log(f"remapping {key} -> {scoped_key}")
    super().__setitem__(scoped_key, value)

  def __getitem__(self, key):
    # try a prefix first
    app_key = f"{self._scope}_{key}"
    self._log(f"  trying to get {app_key} in stead of {key}")
    try:
      value = super().__getitem__(app_key)
      self._log(f"  SUCCESS {app_key} = {value}")
      return value
    except KeyError:
      pass

    # fall back to the non-prefixed variable
    self._log(f"  FAIL: trying {key}")
    try:
      value = super().__getitem__(key)
      self._log(f"  SUCCESS: found {key}={value}")
    except KeyError:
      raise KeyError
    return value

  # solution for .get() not calling __getitem__ without contains >= 3.12
  # inspiration: https://github.com/python/cpython/issues/105524
  def __contains__(self, key):
    try:
      self[key]
    except KeyError:
      return False
    return True
