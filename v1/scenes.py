"""Storyboard: scene images + lyric subtitles for 深海少女 MV."""

# --- open-source portability (added for the public release) ---
import os as _os
from pathlib import Path as _Path


def _repo_root():
    for _p in _Path(__file__).resolve().parents:
        if (_p / "README.md").exists():
            return _p
    return _Path(__file__).resolve().parent


REPO_ROOT = _repo_root()
DESKTOP = _Path(_os.environ.get("SHINKAI_DESKTOP", _Path.home() / "Desktop"))
# --- end ---

DF_REF = str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "F83CCD692922DE1571D580ECFBFC54E5.jpg")
CK_REF = str(REPO_ROOT / "img" / "claude_sheet.png")

STYLE = ("High quality Japanese anime illustration, cinematic anime film still, widescreen composition with the "
         "important content kept in the central area, soft cel shading, delicate clean line art, beautiful lighting, "
         "same character design and drawing style as the reference character sheet(s). No text, no letters, no "
         "watermark, no speech bubbles, no borders, no character sheet layout, a single scene. ")

DF = ("the whale girl from the blue-haired reference sheet: very long wavy dark navy-blue hair with lighter periwinkle "
      "ends, an ahoge, dark navy beret with a small white whale hairpin and blue ribbon, dark navy whale-fin shaped ears "
      "with white frilled edges on the sides of her head, violet-blue eyes, white blouse with sailor collar and black "
      "bow, oversized cream knit cardigan with small navy whale prints, navy plaid skirt with white lace frills, a "
      "dark blue whale tail")

CK = ("the orange-haired girl from the orange reference sheet: very long wavy bright orange hair, an ahoge, warm amber "
      "eyes, a large orange flower hair ornament with a pearl centre and a black ribbon with cream tassels, cream "
      "frilled blouse with an orange flower brooch and black cravat, cream capelet with orange embroidery, black "
      "corset, layered cream, orange and black skirt")

SEA = "deep underwater ocean, floating hair and clothes, small bubbles, "

# (id, start, end, refs, prompt)
SCENES = [
    ("s01", 0.0, 8.0, [DF_REF],
     SEA + "very dark deep blue abyss. Full body of " + DF + ", slowly sinking downward with her eyes half closed and "
     "a sad empty expression, arms drifting loosely, hair spreading like ink above her, a faint cold light far above. "
     "Lonely, melancholic, quiet."),
    ("s02", 8.0, 15.5, [DF_REF],
     SEA + "pitch dark navy water. Close-up portrait of " + DF + ", curled up and hugging her knees while drifting, "
     "eyes nearly closed, a single tiny bubble leaving her lips, her face dimly lit in cold blue. Feeling of being "
     "forgotten by everyone."),
    ("s03", 15.5, 22.4, [DF_REF],
     SEA + "dark deep sea. Seen from below, " + DF + " looks up in surprise as a single warm golden-orange beam of light "
     "pierces down through the dark water and touches her face, dust particles glowing in the beam. Wide shot, strong "
     "contrast between warm light and cold dark blue."),
    ("s04", 22.4, 29.6, [DF_REF],
     SEA + "dark blue sea with strong swirling currents. " + DF + " stretches one hand up toward a warm orange light "
     "above, but a big swirling wave of bubbles and current pulls her away and the light blurs and scatters. Dynamic "
     "motion, diagonal composition."),
    ("s05", 29.6, 36.7, [CK_REF],
     SEA + "the upper sea glowing with warm light. A dreamlike, dazzling, softly blurred glimpse of " + CK + ", "
     "floating in a halo of warm golden-orange light, smiling gently, hair glowing like sunlight in the water. "
     "Bloom, lens glow, soft focus, seen from far below as if through tears."),
    ("s06", 36.7, 43.3, [DF_REF],
     SEA + "deep sea filled with countless glowing bioluminescent jellyfish and plankton lights like city "
     "illuminations, blue, cyan and pink lights. " + DF + " floats among them, looking around in confusion, one hand "
     "on her chest. Sparkling, mysterious."),
    ("s07", 43.3, 50.5, [DF_REF],
     SEA + "deeper and darker sea, almost black. " + DF + " sinks deeper while hiding her face in her oversized "
     "cardigan sleeves, closing herself off, curled up inside a large dark seashell or coral hollow. Gloomy, but "
     "beautiful blue rim light."),
    ("s08", 50.5, 60.4, [DF_REF, CK_REF],
     SEA + "dark deep sea. " + DF + " peeks out shyly from a dark coral rock, looking up longingly, cheeks slightly "
     "blushing. Far above her, small in the distance, " + CK + " swims in a warm orange glow. Strong vertical "
     "composition with the two separated by darkness."),
    ("s09", 60.4, 64.0, [],
     "deep ocean, view looking up from the deep sea floor toward the far surface, majestic god rays of light "
     "streaming down through deep blue water, marine snow particles, a distant silhouette of a whale, no people. "
     "Beautiful, vast, serene. Japanese anime background art style."),
    ("s10", 64.0, 71.1, [DF_REF],
     SEA + "quiet night on the deep sea floor, bioluminescent coral and sea plants glowing softly. " + DF + " lies on "
     "her side on a bed of soft glowing sea anemones, wide awake, eyes open, staring upward, unable to sleep, "
     "thinking of someone. Calm, lonely, soft blue and teal."),
    ("s11", 71.1, 78.6, [CK_REF],
     SEA + "sunlit upper sea, shimmering caustic light. " + CK + " swims gracefully and freely, arms open wide, her "
     "long orange hair and the translucent ribbons of her dress spreading like large wings behind her, smiling "
     "joyfully, viewed from slightly below. Beautiful, free, radiant warm orange and turquoise."),
    ("s12", 78.6, 85.7, [DF_REF, CK_REF],
     SEA + "light pouring down again from above like a curtain. In the foreground, " + DF + " gazes upward, entranced. "
     "Above her in the light, " + CK + " has noticed her and their eyes meet across the water. Over-the-shoulder "
     "shot from behind the whale girl."),
    ("s13", 85.7, 92.4, [DF_REF, CK_REF],
     SEA + "warm light from above. " + CK + " turns around toward the viewer with a kind smile, reaching out a hand. "
     "In the foreground, " + DF + " flusters and hides half her face behind her beret, pretending not to look, cheeks "
     "red, eyes darting away."),
    ("s14", 92.4, 99.6, [DF_REF],
     SEA + "she deliberately dives downward into dark water. Close-up of " + DF + " diving head first into darkness, "
     "her cheeks bright red and glowing in the dark blue, flustered expression, bubbles trailing behind. Cute and "
     "emotional."),
    ("s15", 99.6, 109.2, [DF_REF],
     SEA + "dark sea. " + DF + " places both hands over her heart, trying to be brave, a faint warm light glowing from "
     "her chest, but tendrils of black ink-like water wrap around her arms and legs, holding her back. Tense, "
     "dramatic, dark navy and black with a small warm glow."),
    ("s16", 109.2, 116.5, [DF_REF],
     SEA + "murky dark water. " + DF + " looks down at her cream cardigan and skirt stained with black ink smudges, "
     "her reflection in a cracked shard of mirror-like glass shows a distorted, broken forced smile. Sad, painful."),
    ("s17", 116.5, 125.1, [DF_REF, CK_REF],
     SEA + "dark water. " + DF + " turns away covering her face with both hands, crying out, tears and bubbles "
     "bursting from her. Behind her, " + CK + " is reaching toward her with a worried face, but the whale girl pushes "
     "the warm light away. Emotional climax, strong contrast."),
    ("s18", 125.1, 131.6, [DF_REF],
     SEA + "dark blue sea. Extreme close-up of " + DF + " with eyes closed, tears drifting away from her eyes and "
     "turning into small glowing blue and orange light bubbles that dissolve into the water. Quiet, heartbreaking, "
     "beautiful."),
    ("s18b", 131.6, 138.1, [DF_REF, CK_REF],
     SEA + "vast dark deep blue sea. Wide shot: small in the lower left, " + DF + " drifts alone curled up and "
     "crying in the darkness. Far away on the right, " + CK + " floats in a faint warm orange glow, one hand on her "
     "chest, looking at the whale girl with a sad and worried face, not daring to come closer. Lots of empty dark "
     "water between them, a few drifting glowing particles. Lonely and tender."),
    ("s19", 138.1, 144.4, [DF_REF, CK_REF],
     SEA + "dark water slowly lit by warm light. " + DF + " and " + CK + " face each other at a small distance, the "
     "whale girl's chest glowing softly as feelings overflow and melt into the water as luminous ripples, the orange "
     "girl smiling gently. Tender and sad."),
    ("s20", 144.4, 152.4, [DF_REF],
     SEA + "dark deep sea. " + DF + " looks up with wide shocked eyes: in front of her there is only empty darkness "
     "and a few fading orange sparkles and a single drifting orange flower petal where someone was a moment ago. "
     "Sudden loss, cold blue."),
    ("s21", 152.4, 160.4, [DF_REF],
     SEA + "vast pitch black abyss. " + DF + " swims frantically through the darkness, searching, worried and panicked "
     "expression, hair streaming behind her, a tiny faint orange glow far away at the bottom of the abyss. Dynamic "
     "motion, sense of urgency."),
    ("s22", 160.4, 164.2, [DF_REF, CK_REF],
     SEA + "black abyss. Dramatic close shot: " + DF + " reaches her hand as far as she can down into the darkness, "
     "and a hand of " + CK + " emerges from the dark below and grasps it, warm light bursting where their hands meet. "
     "Focus on the joined hands, faces partly visible."),
    ("s23", 164.2, 170.5, [DF_REF, CK_REF],
     SEA + "the darkness turns into a beautiful glowing sea. " + CK + " holds both hands of " + DF + " and smiles "
     "warmly; the whale girl's hair, ears and tail now shine with beautiful glowing blue, violet and teal "
     "bioluminescent colours, she looks surprised and moved, tears in her eyes."),
    ("s24", 170.5, 177.9, [DF_REF, CK_REF],
     SEA + "glowing marine snow falling everywhere like gentle blessing lights. " + CK + " pulls " + DF + " upward by "
     "the arm, both rising, the whale girl smiling for the first time with tears. Upward diagonal composition, warm "
     "and cool light mixing."),
    ("s25", 177.9, 188.3, [DF_REF, CK_REF],
     SEA + "bright sunlit blue water with rays of light. " + DF + " and " + CK + " swim upward together hand in hand "
     "toward the shining surface, both laughing happily, hair flowing, a school of small silver fish around them. "
     "Hopeful."),
    ("s26", 188.3, 195.8, [],
     "underwater view looking straight up at the bright ocean surface, dazzling sunlight breaking through the "
     "rippling surface, countless bubbles rising, light rays, turquoise and gold, no people. Japanese anime "
     "background art, breathtaking."),
    ("s27", 195.8, 205.0, [DF_REF, CK_REF],
     "Above the ocean at sunrise. " + DF + " and " + CK + " burst out of the sea surface and leap high into the sky "
     "together, holding hands, a big splash of sparkling water droplets around them, the whale girl's tail and the "
     "orange girl's ribbons spreading like wings, pastel orange and blue sky with clouds. Joyful, liberating, epic."),
    ("s28", 205.0, 214.0, [DF_REF, CK_REF],
     "Calm sea at golden sunset, sparkling water surface. " + DF + " and " + CK + " sit together on a rock by the "
     "sea, leaning shoulder to shoulder and smiling gently, the orange girl's head tilted against the whale girl's, "
     "seen from slightly behind and to the side, warm orange sky reflecting on the sea. Peaceful happy ending."),
]

# 歌词原文有版权，公开版不包含。把你的歌词放到同目录的 lyrics.json：
# [{"start": 0.9, "end": 4.6, "jp": "...", "cn": "..."}, ...]
def _load_lyrics():
    import json, pathlib

    p = pathlib.Path(__file__).with_name("lyrics.json")
    if not p.exists():
        return []
    return [(x["start"], x["end"], x.get("jp", ""), x.get("cn", "")) for x in json.loads(p.read_text(encoding="utf-8"))]


LYRICS = _load_lyrics()

