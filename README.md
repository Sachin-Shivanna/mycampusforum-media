# mycampusforum-media

Public image hosting for MyCampusForum's LinkedIn posts (scheduled via Buffer, which needs public image URLs).

- `linkedin/YYYY-MM/YYYY-MM-DD-<topic>.png` — one 1200×1200 image per post
- `screenshots/` — redacted app screenshots used as source material (no real institution names or emails)
- `tools/` — image generator

Raw URL pattern: `https://raw.githubusercontent.com/Sachin-Shivanna/mycampusforum-media/main/<path>`

## Instagram
- `instagram/YYYY-MM/YYYY-MM-DD-<slug>[-NN].png|.mp4` — 1080×1350 posts/carousels, 1080×1920 Reels
- `tools/make_ig.py spec.json OUT_DIR` — cover / tip / shot / quote / poll / meme / cta slides (see docstring)
- `tools/make_reel.py spec.json OUT.mp4` — "slides" Reels from screenshots, or "clip" Reels cut from `assets/video/story-of-growth-720p.mp4`
- `tools/ig_specs/` — example specs (week 1)
