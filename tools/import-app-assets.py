#!/usr/bin/env python3
"""Import and optimize brand + app assets from the local app repos.

This is a developer tool, not a build step: run it by hand and commit the
results. GitHub Pages builds the site with plain Jekyll and never runs this.

    python3 tools/import-app-assets.py

Sources live outside this repo (the Flutter app repos and the Bullets brand
folder), so the optimized output committed here is what the site actually
serves. Two source paths need care:

  * Drawwii's store screenshots are gitignored in the drawwii repo — they only
    exist on the machine that generated them. Back up the PNGs in
    tools/store_screenshots/output/ before relying on this, or regenerate them
    there. If they are missing, this script fails loudly rather than shipping a
    site with holes in it.

  * The brand logo lives on the Desktop, not in a repo. If it moves, update
    BRAND_LOGO / BRAND_HEADER below.

Requires Pillow (pip install Pillow).
"""

from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
APPS_SRC = Path("/Users/jyr/StudioProjects/bullets")
BRAND_LOGO = Path("/Users/jyr/Desktop/Bullets/bullets.png")
BRAND_HEADER = Path("/Users/jyr/Desktop/Bullets/header.png")

# The logo's squircle fill. The site background matches it so the squircle
# dissolves into the page and only the white mark reads.
BG = (19, 20, 22)

SHOT_WIDTH = 640  # displayed ~320px wide, so 2x for retina
SHOT_QUALITY = 78
ICON_SIZE = 512
ICON_QUALITY = 86

# Screenshots are renamed to a uniform NN-name.webp scheme; the source repos
# each use their own convention (underscores, no zero padding).
APPS = {
    "cineepp": {
        "icon": APPS_SRC / "cineepp/assets/common/app-icon.png",
        "shots_dir": APPS_SRC / "cineepp/store-assets/screenshots/ios/en",
        "shots": [
            ("01-korean.png", "01-korean"),
            ("02-discover.png", "02-discover"),
            ("03-movie.png", "03-movie"),
            ("04-series.png", "04-series"),
            ("05-trailers.png", "05-trailers"),
            ("06-save.png", "06-save"),
            ("07-activity.png", "07-activity"),
        ],
        # TMDB attribution logo — required alongside the attribution text.
        "extra": [(APPS_SRC / "cineepp/assets/images/logo/tmdb.png", "tmdb.png")],
    },
    "pilmie": {
        "icon": APPS_SRC / "pilmie/assets/prod/app-icon.png",
        "shots_dir": APPS_SRC / "pilmie/store/ios/en",
        "shots": [
            ("01-home.png", "01-home"),
            ("02-shelf.png", "02-shelf"),
            ("03-profile.png", "03-profile"),
            ("04-review_detail.png", "04-review_detail"),
            ("05-book_detail.png", "05-book_detail"),
        ],
    },
    "drawwii": {
        "icon": APPS_SRC / "drawwii/assets/common/app-icon.png",
        "shots_dir": APPS_SRC / "drawwii/tools/store_screenshots/output/ios/en",
        "shots": [
            ("01_draw.png", "01-draw"),
            ("02_eraser_before_after.png", "02-eraser_before_after"),
            ("03_bg_remove.png", "03-bg_remove"),
            ("04_templates.png", "04-templates"),
            ("05_stickers.png", "05-stickers"),
            ("06_habit.png", "06-habit"),
            ("07_gallery.png", "07-gallery"),
        ],
    },
    "unrearix": {
        "icon": APPS_SRC / "unrearix/assets/common/app-icon.png",
        "shots_dir": APPS_SRC / "unrearix/store-screenshots/en/ios",
        "shots": [
            ("1_player.png", "01-player"),
            ("2_music.png", "02-music"),
            ("3_artist.png", "03-artist"),
            ("4_videos.png", "04-videos"),
            ("5_create.png", "05-create"),
            ("6_lounge.png", "06-lounge"),
        ],
    },
}


def require(path: Path) -> Path:
    if not path.exists():
        raise SystemExit(f"missing source: {path}")
    return path


def flatten(im: Image.Image) -> Image.Image:
    """Composite transparency onto the site background instead of onto white."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, BG)
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def resize_to_width(im: Image.Image, width: int) -> Image.Image:
    height = round(im.height * width / im.width)
    return im.resize((width, height), Image.LANCZOS)


def import_brand() -> None:
    out = REPO / "assets/brand"
    out.mkdir(parents=True, exist_ok=True)

    logo = Image.open(require(BRAND_LOGO)).convert("RGBA")
    # Keep alpha on the mark itself so it sits on any surface.
    logo.resize((256, 256), Image.LANCZOS).save(out / "logo.png", optimize=True)
    logo.resize((32, 32), Image.LANCZOS).save(out / "favicon-32.png", optimize=True)
    # Apple strips alpha from touch icons, so bake the background in.
    flatten(logo.resize((180, 180), Image.LANCZOS)).save(
        out / "apple-touch-icon.png", optimize=True
    )

    # The header banner is 16:9; OG wants 1.91:1. Crop height from the centre —
    # the logo and wordmark sit centred with room to spare.
    header = flatten(Image.open(require(BRAND_HEADER)))
    target_h = round(header.width / 1.905)
    top = (header.height - target_h) // 2
    og = header.crop((0, top, header.width, top + target_h))
    og.resize((1200, 630), Image.LANCZOS).save(
        out / "og-default.png", optimize=True
    )
    print(f"  brand: logo.png favicon-32.png apple-touch-icon.png og-default.png")


def import_app(slug: str, spec: dict) -> None:
    out = REPO / "assets/apps" / slug
    out.mkdir(parents=True, exist_ok=True)

    icon = flatten(Image.open(require(spec["icon"])))
    icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    icon.save(out / "icon.webp", "WEBP", quality=ICON_QUALITY, method=6)

    for src_name, dst_stem in spec["shots"]:
        src = require(spec["shots_dir"] / src_name)
        shot = resize_to_width(flatten(Image.open(src)), SHOT_WIDTH)
        shot.save(
            out / f"{dst_stem}.webp", "WEBP", quality=SHOT_QUALITY, method=6
        )

    for src, dst_name in spec.get("extra", []):
        Image.open(require(src)).save(out / dst_name, optimize=True)

    size = sum(f.stat().st_size for f in out.iterdir()) / 1024
    print(f"  {slug}: {len(spec['shots'])} shots + icon  ({size:.0f} KB)")


if __name__ == "__main__":
    print("importing brand assets")
    import_brand()
    print("importing app assets")
    for slug, spec in APPS.items():
        import_app(slug, spec)
    total = sum(
        f.stat().st_size for f in (REPO / "assets").rglob("*") if f.is_file()
    ) / 1024 / 1024
    print(f"done — assets/ is {total:.1f} MB")
