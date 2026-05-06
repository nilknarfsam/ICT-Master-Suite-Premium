"""Tokens de design da UI Premium.

Documenta cores, spacing, radius, tipografia e descricoes de sombra em
estruturas Python puras. Os arquivos QSS (`base.qss`, `light.qss`)
reproduzem estes mesmos valores hardcoded — esta convencao deliberada
mantem a Subfase 4.1 simples e evita placeholder substitution antes da
hora. Em rodada futura (Subfase 4.6) avaliaremos um pre-processador.

Os tokens tambem servem como contrato neutro: na futura migracao
Electron/React (Fase 6) podem ser exportados via `as_dict()` para
geracao de design tokens em CSS/Tailwind.
"""

from typing import Any, Dict, Tuple

COLORS: Dict[str, str] = {
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "success": "#16a34a",
    "error": "#dc2626",
    "warning": "#d97706",
    "info": "#0891b2",
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",
    "bg_app": "#f4f7f6",
    "bg_card": "#ffffff",
    "bg_subtle": "#f8fafc",
    "border": "#e2e8f0",
    "border_strong": "#cbd5e1",
}

STATUS_COLORS: Dict[str, Dict[str, str]] = {
    "pass": {"text": "#166534", "bg": "#dcfce7", "border": "#86efac"},
    "fail": {"text": "#991b1b", "bg": "#fee2e2", "border": "#fca5a5"},
    "warning": {"text": "#92400e", "bg": "#fef3c7", "border": "#fcd34d"},
    "info": {"text": "#155e75", "bg": "#cffafe", "border": "#67e8f9"},
    "neutral": {"text": "#334155", "bg": "#f1f5f9", "border": "#cbd5e1"},
}

SPACING_SCALE: Tuple[int, int, int, int, int, int] = (4, 8, 12, 16, 24, 32)

SPACING: Dict[str, int] = {
    "xs": SPACING_SCALE[0],
    "sm": SPACING_SCALE[1],
    "md": SPACING_SCALE[2],
    "lg": SPACING_SCALE[3],
    "xl": SPACING_SCALE[4],
    "xxl": SPACING_SCALE[5],
}

RADIUS: Dict[str, int] = {
    "sm": 4,
    "md": 8,
    "lg": 12,
}

FONT: Dict[str, Any] = {
    "family_sans": "Segoe UI, Arial, sans-serif",
    "family_mono": "Consolas, Courier New, monospace",
    "size_xs": 11,
    "size_sm": 12,
    "size_md": 13,
    "size_lg": 14,
    "size_xl": 16,
    "size_xxl": 18,
}

SHADOWS: Dict[str, str] = {
    "card": "0 1px 2px rgba(15, 23, 42, 0.06)",
    "card_hover": "0 4px 12px rgba(15, 23, 42, 0.10)",
    "overlay": "0 8px 24px rgba(15, 23, 42, 0.18)",
}


def as_dict() -> Dict[str, Any]:
    """Retorna agregado serializavel dos tokens.

    Util para futuras exportacoes (JSON, Tailwind config) na fase
    Electron/React. Hoje nao e consumido pela UI desktop.
    """
    return {
        "colors": dict(COLORS),
        "status_colors": {k: dict(v) for k, v in STATUS_COLORS.items()},
        "spacing": dict(SPACING),
        "spacing_scale": list(SPACING_SCALE),
        "radius": dict(RADIUS),
        "font": dict(FONT),
        "shadows": dict(SHADOWS),
    }
