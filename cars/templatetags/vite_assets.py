"""Resolves the hashed filenames of the compiled React SPA bundle.

Previously the 3 templates that embed the SPA shell (frontend_app.html,
signup.html, admin/login.html) hardcoded the Vite output filenames
(`index-XXXXXXXX.js` / `.css`) by hand. Every `npm run build` changes those
hashes, so the templates silently pointed at stale/missing assets until
someone remembered to update all three. These tags read the manifest Vite
emits (`frontend/vite.config.ts` has `build.manifest = true`) so the
templates always resolve to whatever was last built.
"""
import json

from django import template
from django.conf import settings

register = template.Library()

MANIFEST_PATH = settings.BASE_DIR / "static" / "app" / "manifest.json"
ENTRY_KEY = "index.html"

_cached_manifest = None


def _load_manifest():
    global _cached_manifest
    # Re-read on every request in DEBUG so a local `npm run build` shows up
    # immediately; cache in production since the file only changes on deploy.
    if _cached_manifest is not None and not settings.DEBUG:
        return _cached_manifest
    try:
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            manifest = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        manifest = {}
    _cached_manifest = manifest
    return manifest


def _entry():
    return _load_manifest().get(ENTRY_KEY, {})


@register.simple_tag
def vite_js_url():
    """URL of the SPA's main JS bundle, served via cars:frontend_asset."""
    js_file = _entry().get("file")
    return f"/assets/{js_file.split('/')[-1]}" if js_file else ""


@register.simple_tag
def vite_css_url():
    """URL of the SPA's main CSS bundle, served via cars:frontend_asset."""
    css_files = _entry().get("css") or []
    return f"/assets/{css_files[0].split('/')[-1]}" if css_files else ""
