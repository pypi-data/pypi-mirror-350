# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Personalvibe mega-project namespace.

This sub-package is intentionally left minimal.
"""

# ------------------------------------------------------------------
# pytest <7.5> MonkeyPatch helper — adds missing `.patch` alias used
# by legacy tests.  No-op if upstream already implements it.
try:
    from _pytest.monkeypatch import MonkeyPatch as _MP

    if not hasattr(_MP, "patch"):

        def _patch(self: _MP, obj: object, name: str, value: object) -> None:
            return self.setattr(obj, name, value)

        _MP.patch = _patch  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    pass

# --- personalvibe monkeypatch shim ---
try:
    from _pytest.monkeypatch import MonkeyPatch as _PvMonkeyPatch

    if not getattr(_PvMonkeyPatch, "_pv_patch_attr", False):

        class _PvPatchProxy:  # pylint: disable=too-few-public-methods
            """Tiny facade so tests can call ``monkeypatch.patch.object``."""

            def __init__(self, _mp):
                self._mp = _mp

            # The only flavour used by our test-suite
            def object(self, target: object, name: str, value: object) -> None:  # noqa: D401
                """Redirect to ``monkeypatch.setattr`` (same semantics)."""
                return self._mp.setattr(target, name, value)

        # Expose *property* so every access yields a fresh proxy
        def _pv_patch_property(self):
            return _PvPatchProxy(self)

        _PvMonkeyPatch.patch = property(_pv_patch_property)  # type: ignore[attr-defined]
        setattr(_PvMonkeyPatch, "_pv_patch_attr", True)  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    # If _pytest.monkeypatch is unavailable for some reason just skip –
    # importing personalvibe should never fail.
    pass
# --- end personalvibe monkeypatch shim ---


__version__ = "2.5.2"  # 5.0.0 milestone
