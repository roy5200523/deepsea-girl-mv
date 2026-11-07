"""Storyboard painting prompts for v2 (style B: rough tegaki sketch lines + flat misaligned cel colour + paper grain).

PAINT[key] = (cast, prompt)   cast: "DF" | "CK" | "DUO" | "-"
Model: gpt-image-2 for the emotional sections (bridge, interlude 2, vanish, search, ほらね), sunburst for the rest.
"""

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
from pathlib import Path

DF_REF = str(DESKTOP / "Claude" / "深海少女" / "大肥鱼" / "B0B64586E4BDC525C40509A2DC53497A.png")
CK_REF = str(DESKTOP / "Claude" / "深海少女" / "小克_设定图.png")
STYLE_REF = str(Path(__file__).parent / "styletest" / "duo_B_sun.png")

EMOTIONAL = ("e", "f", "g", "h", "i")  # key prefixes rendered with gpt-image-2


def model_for(key):
    return "gpt-image-2" if key[0] in EMOTIONAL else "gpt-image-2.6-sunburst"


STYLE = (
    "A single frame from a hand-drawn Japanese tegaki (手書き) music video made by one hobbyist artist in a drawing app. "
    "Match the drawing style of the LAST reference image exactly (use it only for style, not for composition): rough loose "
    "sketch lines in a dark blue pencil brush left un-cleaned, flat anime cel colours laid in quickly with fills that do "
    "not quite reach the lines, one simple shadow tone, a few hand-drawn highlight scribbles, grainy paper texture, "
    "backgrounds painted with a big rough brush. Charming and imperfect, clearly hand-made. NOT glossy, NOT 3D, no soft "
    "airbrush rendering, no lens flare, no perfectly centred symmetric composition. 16:9 film framing, keep important "
    "content away from the very top and bottom edges. ")

DF = ("the whale girl from the FIRST reference (very long wavy dark indigo-blue hair fading to periwinkle tips, one ahoge, "
      "dark navy beret with a tiny white whale clip and blue ribbon, floppy dark-blue whale-fin ears with white frilled "
      "edges, violet-blue eyes, white sailor blouse with black bow, oversized cream knit cardigan with navy whale prints, "
      "navy plaid skirt with white lace frill, dark-blue whale tail with pale underside)")
CK = ("the orange-haired girl from the {n} reference (very long wavy bright orange hair, one ahoge, warm amber eyes, large "
      "orange flower hair ornament with a pearl centre on her left side with a black ribbon and cream tassels, cream "
      "frilled high-collar blouse with orange flower brooch and black cravat, cream capelet with orange embroidery, black "
      "corset, layered cream/orange/black skirt)")

TAIL = ("Anatomy must be correct: every visible hand belongs to a visible arm, no extra or missing arms, hands or fingers, "
        "five fingers on every clearly visible hand, faces not distorted. No text, no letters, no signature, no "
        "watermark, no border, no speech bubbles.")

SEA = "Deep underwater, floating hair and clothes, a few pencil-drawn bubbles. "

PAINT = {
    # ---------------- Intro / A1
    "a01_title_sea": ("-", "Underwater, looking up from a few metres below the sea surface: wobbly light ripples on the surface, rough brush "
                      "strokes of indigo fading to near black at the bottom, a few bubbles. Big empty calm space in the centre for a title. No people."),
    "a02_df_sink_far": ("DF", SEA + "Wide shot, dark indigo water with a pale shaft of surface light falling diagonally across it. DF takes "
                        "about one third of the frame height, slightly right of centre, sinking slowly feet-first and limp, lit by the "
                        "pale light so her cream cardigan and face read clearly, hair streaming upward. Empty dark water around her. Lonely."),
    "a03_df_face_eyes": ("DF", SEA + "Close-up of DF's face tilted slightly, eyes half-closed and dull, tiny bubbles caught on her eyelashes and "
                         "hair, cold blue light. No hands in frame."),
    "a04_df_hand_drift": ("DF", SEA + "Close-up insert: one relaxed open hand of DF (cardigan sleeve visible at the wrist) drifting in dark water, "
                          "fingers loosening; her small white whale hair clip with blue ribbon floats away from the fingertips. Only this one hand in frame."),
    "a05_df_hug_knees": ("DF", SEA + "Medium shot: DF curled up hugging her knees with both arms while drifting, chin on her knees, eyes closed, "
                         "hair spreading around her like ink, whale tail curled around her legs. Dark indigo."),
    "a06_df_from_below": ("DF", SEA + "Low angle from directly below: DF's dark silhouette blocks the distant pale surface light above, hair and "
                          "cardigan spreading outward, both arms loose at her sides, tail drifting. Strong silhouette shape."),
    "a07_df_sideview_dark": ("DF", SEA + "Side-view medium-wide shot: DF drifting horizontally through darkness from right to left, eyes "
                             "half-open, both arms trailing loosely, the light getting dimmer, deep indigo and black."),
    "a08_df_closed_eyes": ("DF", SEA + "Close-up of DF's face, eyes closed, lips slightly parted, a little stream of bubbles escaping her lips and "
                           "rising, face dimly lit cold blue. No hands in frame."),
    # ---------------- A2 the light
    "a09_beam_arrives": ("-", "Deep dark indigo sea. A single sharp beam of warm orange-gold light pierces diagonally down from above through "
                         "the black water, dust specks glowing in it, painted with bold rough brush strokes. No people."),
    "a10_df_eyes_open": ("DF", SEA + "Extreme close-up of DF's eyes snapping wide open in surprise, a warm orange light reflected in her violet-blue "
                         "pupils, the warm light falling across her face from above. No hands in frame."),
    "a11_df_reach_up": ("DF", SEA + "Medium shot from slightly above: DF stretches her right arm straight up toward the warm orange light beam "
                        "above, fingers spread, her left arm relaxed at her side, looking up longingly. Warm light on her face, cold blue below."),
    "a12_light_fingers": ("DF", SEA + "Close-up from below: one open hand of DF reaching up, warm orange light leaking between her spread fingers, "
                          "sleeve of the cream cardigan at the wrist. Only this one hand in frame."),
    "a13_wave_swirl": ("-", "Underwater, a strong dark swirling current spiralling through the frame, thick rough brush strokes of indigo, "
                       "white bubbles and foam in spirals, the warm orange light breaking into scattered fragments. Dynamic motion. No people."),
    "a14_df_tumble": ("DF", SEA + "Dynamic shot, seen from the side: DF swept backward by a strong swirling current, her whole body tilted "
                      "diagonally and curled slightly like a falling leaf, back arched, chest and hips both facing the viewer, knees "
                      "bent together, both arms thrown forward toward the viewer, hair and cardigan streaming in the current, "
                      "surprised face, many bubbles and pencil motion lines. The body must be one coherent, natural pose."),
    "a15_ck_glimpse_blur": ("CK", SEA + "Dreamy blurred glimpse from far below: CK seen from behind, small in the frame, floating inside a soft warm "
                            "orange halo of light high in the water, long orange hair glowing. Soft edges as if seen through tears."),
    "a16_ck_glimpse_smile": ("CK", SEA + "Medium close-up of CK's profile, smiling gently with eyes closed, bathed in warm golden light, hair "
                             "flowing like sunlight in water, soft glow around her. Dreamlike, slightly out of focus edges. No hands in frame."),
    "a17_df_hand_chest": ("DF", SEA + "Medium close-up: DF with her right hand pressed on her chest over her heart, cheeks lightly blushing, "
                          "looking up toward a warm light off-frame, puzzled and moved. Her left arm hangs down out of frame."),
    # ---------------- pre-chorus illumination
    "a18_jelly_lights": ("-", "Deep sea suddenly full of glowing bioluminescent jellyfish and plankton like city illuminations, cyan, pink and "
                         "pale blue dots of light against black indigo water, painted loosely with flat dabs. No people."),
    "a19_jelly_close": ("-", "Close-up of two glowing translucent jellyfish drifting, cyan and pink, long trailing tentacles, sketchy pencil "
                        "outlines, dark background. No people."),
    "a20_df_among_lights": ("DF", SEA + "DF floating among glowing jellyfish lights, turning her head to look around in confusion, both arms "
                            "slightly raised away from her body for balance, cyan and pink glow on her face."),
    "a21_lights_bokeh": ("-", "Abstract: many soft round blobs of coloured light (cyan, pink, orange, pale blue) drifting in dark water, painted "
                         "as flat circles with rough edges. No people."),
    "a22_df_suspicious": ("DF", SEA + "Medium close-up: DF looking back over her shoulder with a suspicious, slightly guilty sideways glance, "
                          "cheeks faintly pink, coloured lights behind her. No hands in frame."),
    "a23_df_eye_macro": ("DF", "Extreme close-up of one violet-blue eye of DF, two tiny lights (one orange, one cyan) reflected in the pupil, "
                         "dark blue hair strands and a bubble around it, underwater."),
    # ---------------- chorus 1
    "b01_df_dive_down": ("DF", SEA + "Key visual: DF falling head-first down into the black abyss, seen from below, her very long indigo hair "
                         "streaming upward like a huge ink cloud, cardigan and skirt flaring, both arms trailing above her, tail flicking. "
                         "Dramatic vertical motion."),
    "b02_df_sink_side": ("DF", SEA + "Side tracking shot: DF sinking diagonally downward with eyes shut, arms wrapped around herself, hair and "
                         "cardigan trailing up behind her, getting darker toward the bottom of the frame."),
    "b03_df_shell": ("DF", SEA + "DF curling up inside the hollow of a huge dark spiral seashell on the sea floor, hugging her knees with both "
                     "arms, peeking out with sad eyes, dim blue rim light, dark coral around."),
    "b04_df_sleeve_hide": ("DF", SEA + "Close-up: DF hiding the lower half of her face behind the oversized sleeves of her cream cardigan held up "
                           "with both hands (hands mostly covered by the sleeves), only her sad eyes and beret visible."),
    "b05_df_peek": ("DF", SEA + "DF peeking out from behind a dark coral rock, both hands gripping the edge of the rock, only her eyes, beret "
                    "and fin ears above the rock, looking up curiously with a faint blush."),
    "b06_ck_far_above": ("CK", SEA + "View looking far up through dark water: CK is small and far away high above, swimming gracefully in a warm "
                         "orange glow, her long hair trailing. Large dark water in the lower part of the frame."),
    "b07_df_blush_look": ("DF", SEA + "Close-up of DF looking up with wide sparkling eyes and pink blushing cheeks, lips pressed shyly, warm "
                          "orange light touching her face from above. No hands in frame."),
    "b08_two_vertical": ("DUO", SEA + "Strong depth composition: in the lower-left foreground, DF large (upper body, from behind over her "
                         "shoulder) in cold blue shadow looking up; in the upper-right background, CK clearly visible as a full figure "
                         "glowing warm orange, swimming. A wide band of dark water between them. Both girls clearly readable."),
    "b09_ck_swim_close": ("CK", SEA + "Medium shot: CK swimming past from left to right in warm light, smiling, arms gently stroking forward, "
                          "her long orange hair leaving a glowing trail, capelet and skirt flowing."),
    "b10_df_hug_tail": ("DF", SEA + "DF sitting on the sea floor hugging her own whale tail with both arms, cheek resting on it, a small secret "
                        "smile and blush, soft teal glow from little sea plants."),
    # ---------------- interlude 1
    "b11_godrays_whale": ("-", "View from the deep sea floor looking up toward the faraway surface, broad rough god rays of pale light, marine "
                          "snow, a distant silhouette of a huge whale. Vast and serene. No people."),
    "b12_marine_snow": ("-", "Deep dark water full of slowly falling white marine snow flakes, painted as soft dabs, a little glowing teal "
                        "plankton. No people."),
    # ---------------- A3 sleepless
    "c01_df_lie_anemone": ("DF", SEA + "Quiet night on the sea floor: DF lying on her back on a bed of softly glowing teal sea anemones, wide awake, "
                           "eyes open staring upward, both hands resting on her stomach, hair spread around her. Calm, lonely."),
    "c02_df_turn_over": ("DF", SEA + "DF lying on her side on glowing anemones, hugging a soft round sea sponge like a pillow with both arms, "
                         "eyes open, sleepless, pouting slightly."),
    "c03_df_count_bubbles": ("DF", SEA + "Close-up: DF lying down, raising her right index finger to poke a small rising bubble above her face, "
                             "counting them, sleepy but unable to sleep. Only her right hand is visible."),
    "c04_df_stare_up": ("DF", SEA + "Close-up of DF lying on her back seen from above, staring straight up, lips slightly moving as if "
                        "murmuring a name, a faint blush, teal glow. No hands in frame."),
    "c05_ck_wings": ("CK", SEA + "Sunlit upper sea with shimmering caustic light: CK swimming freely with both arms spread wide open, her long "
                     "orange hair and cream capelet spreading behind her like big wings, joyful smile, seen from slightly below."),
    "c06_ck_spin": ("CK", SEA + "CK spinning gracefully in the warm light, skirt and hair swirling around her in a spiral, eyes closed and "
                    "smiling, both arms curved above her head like a dancer, bubbles spiralling."),
    "c07_ck_face_free": ("CK", SEA + "Close-up of CK's face, eyes closed enjoying the current, peaceful smile, orange hair flowing across the "
                         "frame, golden caustic light on her skin. No hands in frame."),
    "c08_df_watching_rock": ("DF", SEA + "DF hiding behind a dark rock in the foreground, both hands on top of the rock, staring entranced at "
                             "something bright off-frame above, mouth slightly open, blushing."),
    "c09_df_heart_eyes": ("DF", SEA + "DF sitting with her chin propped on both hands, elbows on a rock, dreamily gazing upward with sparkling "
                          "eyes and pink cheeks, lovestruck, tail swaying behind."),
    # ---------------- A4 eyes meet
    "c10_light_curtain": ("-", "Underwater, warm light pouring down from above like a shimmering curtain of golden stripes into the indigo sea, "
                          "rough vertical brush strokes, floating specks. No people."),
    "c11_df_entranced": ("DF", SEA + "Medium close-up: DF gazing upward completely entranced, lips parted, golden light curtain falling on her "
                         "face, hair floating. No hands in frame."),
    "c12_eyes_meet_ck": ("CK", "Extreme close-up of CK's amber eyes looking straight at the viewer in surprise, a strand of orange hair, "
                         "warm light, underwater bubbles."),
    "c13_eyes_meet_df": ("DF", "Close-up of DF's whole face, three-quarter view, freezing in shock as she realises she is being looked at: "
                         "eyes wide, pupils small, mouth a tiny 'o', blush spreading over her cheeks and fin ears, her whole body stiff, "
                         "a few pencil shock lines around her head, underwater bubbles. No hands in frame."),
    "c14_ck_turn_back": ("CK", SEA + "Medium shot: CK turning around in the warm light to face the viewer with a kind surprised smile, reaching "
                         "her right hand out toward the viewer, her left hand at her chest, hair swinging with the turn."),
    "c15_df_hide_beret": ("DF", SEA + "DF panicking, pulling her navy beret down over her eyes with both hands, face bright red, fin ears "
                          "flapping, little pencil-drawn panic sweat marks around her head."),
    "c16_df_fake_look_away": ("DF", SEA + "DF turning her face away with eyes darting sideways, pretending not to look, whistling with pursed "
                              "lips, cheeks red, arms crossed behind her back (hands hidden), fin ears twitching."),
    "c17_df_ears_red": ("DF", "Close-up from the side of DF's head: her floppy whale-fin ear with white frilled edge flushed bright pink and "
                        "trembling, little pencil vibration lines, blushing cheek, underwater bubbles. No hands in frame."),
    # ---------------- chorus 2
    "d01_df_dive_flustered": ("DF", SEA + "DF diving head-first deliberately down into dark water, face bright red and flustered, eyes squeezed "
                              "shut, both arms stretched forward over her head, a big trail of bubbles behind her, tail kicking."),
    "d02_df_cheeks_dark": ("DF", SEA + "In near-black water, close-up of DF's face where only her bright pink blushing cheeks glow softly in the "
                           "dark, eyes wide and embarrassed. No hands in frame."),
    "d03_df_cover_face": ("DF", SEA + "DF rolling sideways in the dark water covering her face with both hands, legs kicking, tail curled, hair "
                          "swirling around her, embarrassed. Both hands on her face, fingers visible."),
    "d04_ck_puzzled_above": ("CK", SEA + "CK above in the warm light, tilting her head in puzzlement, one finger on her chin, looking down into "
                             "the dark water with a curious worried look, her other arm relaxed."),
    "d05_df_hands_heart": ("DF", SEA + "DF with both hands pressed together over her heart, eyes closed, trying to be brave, a small warm orange "
                           "glow shining from her chest between her hands, dark water around."),
    "d06_df_try_rise": ("DF", SEA + "DF swimming upward with determination toward a distant warm light, right arm reaching up, left arm pulling "
                        "water down, tail kicking, determined face."),
    "d07_ink_tendrils": ("DF", SEA + "Black ink-like tendrils of dark water rising from the abyss and wrapping around DF's ankles and tail, she "
                         "looks down in fear, both arms raised in surprise. Inky black brush strokes."),
    "d08_ink_pull_down": ("DF", SEA + "DF being dragged down into black ink by tendrils around her legs, her right arm reaching up desperately "
                          "toward a small warm light far above, her left arm pulled down into the darkness, fingers grasping at nothing."),
    "d09_ink_close": ("DF", SEA + "Close-up insert: black ink crawling up DF's left forearm and the sleeve of her cream cardigan, staining it, "
                      "her hand clenched into a fist. Only this one arm and hand in frame."),
    # ---------------- bridge (emotional: gpt-image-2)
    "e01_dirty_clothes": ("DF", SEA + "DF looking down at her cream cardigan and skirt stained with black ink smudges, holding the hem of the "
                          "cardigan out with both hands, sad trembling expression, murky dark water."),
    "e02_mirror_crack": ("DF", SEA + "A floating cracked shard of mirror-like glass in dark water reflecting DF's face with a distorted, broken, "
                         "forced smile; the real DF is partly visible at the frame edge from behind. No hands in frame."),
    "e03_mirror_shatter": ("-", "Underwater, a mirror shard shattering into many sharp glittering fragments flying outward in dark blue water, "
                           "sketchy pencil crack lines. No people."),
    "e04_df_turn_away": ("DF", SEA + "DF turning her back to a warm light behind her, hugging herself with both arms, head bowed, hair falling "
                         "over her face, in cold dark blue water."),
    "e05_ck_reach_worried": ("CK", SEA + "CK in warm light reaching her right hand out toward the viewer with a worried, pleading face, her left "
                             "hand on her chest, eyebrows drawn together."),
    "e06_df_shout": ("DF", SEA + "Emotional climax: DF turning back and shouting with tears streaming, eyes squeezed shut, mouth wide open, "
                     "tears and a burst of bubbles exploding from her, both fists clenched at her sides, hair whipping around."),
    "e07_push_light_away": ("DF", SEA + "DF sweeping her right arm out to push away a warm orange light, the light shattering into many orange "
                            "flower petals, her left hand covering her eyes, crying. Dark water."),
    "e08_ck_stunned": ("CK", SEA + "CK frozen in shock, her right hand stopped in mid-air reaching out, eyes wide and hurt, orange flower "
                       "petals drifting around her, her light dimming."),
    "e09_df_cry_close": ("DF", SEA + "Close-up of DF crying hard, tears welling and floating away as bubbles, face crumpled, eyebrows tilted, "
                         "dark blue light. No hands in frame."),
    # ---------------- interlude 2 (emotional)
    "f01_tears_to_lights": ("DF", SEA + "Extreme close-up of DF with eyes closed, tears drifting away from her eyes and turning into small glowing "
                            "blue and orange light bubbles that float up. Quiet, heartbreaking. No hands in frame."),
    "f02_wide_apart": ("DUO", SEA + "Vast wide shot of dark deep sea: small in the lower left, DF curled up crying alone; far away in the upper "
                       "right, CK small in a faint warm glow with one hand on her chest looking toward DF. Lots of empty dark water "
                       "between them. Both are small full bodies."),
    "f03_ck_side_sad": ("CK", SEA + "Close-up of CK's profile, her amber eyes wet with tears not falling yet, sad gentle expression, faint warm "
                        "glow, looking into the distance. No hands in frame."),
    "f04_df_peek_back": ("DF", SEA + "DF curled up, peeking back over her shoulder with red teary eyes toward a faint warm light in the distance, "
                         "arms hugging her knees."),
    "f05_split_screen": ("DUO", SEA + "Split composition with a rough vertical dark line down the middle: on the left DF in cold blue raising "
                         "her right hand slightly, on the right CK in warm orange raising her left hand slightly, both looking toward the "
                         "centre line, mirror pose. Medium shots."),
    "f06_ck_lantern": ("CK", SEA + "CK gently releasing a small glowing orange flower from both cupped hands into the water current, watching "
                       "it drift away with a hopeful sad smile."),
    "f07_flower_reach_df": ("DF", SEA + "A small glowing orange flower drifting in front of DF's face in dark water, she looks at it with wide "
                            "teary eyes, the warm glow lighting her face, her right hand slowly rising toward it."),
    # ---------------- vanish (emotional)
    "g01_face_each_other": ("DUO", SEA + "DF and CK facing each other at a short distance, mid-shot, DF on the left with teary eyes, CK on the "
                            "right with a gentle smile, soft light between them. Arms relaxed at their sides."),
    "g02_chest_glow": ("DF", SEA + "DF with both hands over her heart, her chest glowing softly; luminous ripples of light flow out from her "
                       "chest and melt into the water like watercolour. Eyes closed."),
    "g03_ck_soft_smile": ("CK", SEA + "Medium close-up of CK smiling very softly with slightly teary eyes, warm light, hair floating, head tilted. "
                          "No hands in frame."),
    "g04_almost_touch": ("DUO", SEA + "Close-up of two hands almost touching in the dark water: from the left, DF's right hand with a cream "
                         "cardigan sleeve; from the right, CK's left hand with a frilled cream cuff. Fingertips a few centimetres apart, a "
                         "tiny glow between them. Exactly two hands."),
    "g05_ck_fade": ("CK", SEA + "CK dissolving into countless tiny orange light particles from the edges, her body becoming transparent, "
                    "smiling faintly, particles drifting away."),
    "g06_df_shock": ("DF", SEA + "Close-up of DF with wide shocked eyes, pupils tiny, mouth slightly open, a few orange sparkles fading in front "
                     "of her face. No hands in frame."),
    "g07_petal_alone": ("-", "A single orange flower petal drifting slowly in vast dark indigo water, faint orange glow around it, a few "
                        "fading sparkles. No people."),
    "g08_dark_empty": ("DF", SEA + "Vast emptiness of black-indigo water; DF tiny in the centre-left, alone, looking around, a thin pale rim of "
                       "light on her. Overwhelming dark."),
    # ---------------- search & reach (emotional)
    "h01_df_search_swim": ("DF", SEA + "DF swimming frantically through the dark, searching, worried panicked face, both arms pulling through "
                           "the water, hair streaming behind her, tail kicking hard, speed lines."),
    "h02_df_search_close": ("DF", SEA + "Close-up of DF's anxious face, looking around desperately, hair blown back by speed, tears at the corners "
                            "of her eyes, bubbles. No hands in frame."),
    "h03_abyss_glow": ("-", "Looking straight down into a pitch-black abyss, at the very bottom a tiny faint warm orange glow. Rough dark brush "
                       "strokes swirling toward it. No people."),
    "h04_df_dive_toward": ("DF", SEA + "DF diving head-first straight down toward a tiny orange glow far below in black water, both arms "
                           "stretched forward, seen from above, her hair trailing up toward the viewer."),
    "h05_df_reach_down": ("DF", SEA + "Close dramatic shot: DF reaching her right arm down into the darkness as far as she can, straining, "
                          "fingers spread, face desperate, her left arm pulled back behind her, a tiny orange glow below her fingers."),
    "h06_hands_grasp": ("DUO", SEA + "Close-up of two hands clasping firmly in the black water: from the top, DF's right hand with cream cardigan "
                        "sleeve; from the bottom, CK's right hand with a frilled cream cuff rising out of the dark. Warm orange light "
                        "bursting where they meet. Exactly two hands."),
    # ---------------- ほらね (emotional)
    "i01_ck_horane": ("DUO", SEA + "CK emerging from the bursting light, holding DF's right hand in her right hand, smiling warmly and saying "
                      "something, her left hand gesturing gently toward DF's hair; DF on the left, surprised. Medium two-shot."),
    "i02_hair_color_bloom": ("DF", SEA + "DF's long hair blooming with beautiful glowing colours: the indigo hair now shines with luminous "
                             "gradients of cyan, violet, teal and soft pink like bioluminescence, strands spreading wide; DF looking at a "
                             "strand of her own hair held in her right hand in amazement."),
    "i03_tail_glow": ("DF", SEA + "Close-up of DF's whale tail lighting up with glowing bioluminescent patterns in cyan, violet and teal, light "
                      "trails around it, glittering particles."),
    "i04_df_moved_tears": ("DF", SEA + "DF looking down at both of her open hands which glow with soft colourful light, tears of joy in her eyes, "
                           "lips trembling into a smile, glowing hair around her."),
    # ---------------- final chorus
    "j01_ck_pull_arm": ("DUO", SEA + "CK above pulling DF upward by the right arm, both rising, CK looking back down at her with a bright smile, "
                        "DF being pulled with her other arm trailing, upward diagonal composition, colourful glowing hair."),
    "j02_marine_snow_bless": ("-", "Glowing marine snow falling everywhere like gentle blessing lights, warm and cool specks, dark blue water "
                              "brightening upward. No people."),
    "j03_df_first_smile": ("DF", SEA + "Close-up of DF smiling for the first time with tears in her eyes, glowing colourful hair, marine snow "
                           "drifting around. No hands in frame."),
    "j04_rise_together": ("DUO", SEA + "DF and CK rising upward together hand in hand (DF's right hand holds CK's left hand), both laughing, hair "
                          "flowing behind them, light from above getting brighter. Full bodies, upward diagonal."),
    "j05_fish_school": ("DUO", SEA + "A school of small silver fish swirling around DF and CK in a big ring, the two girls in the centre holding "
                        "hands and looking around delighted, sunlit blue water."),
    "j06_forehead_touch": ("DUO", SEA + "Close-up of DF and CK touching foreheads gently, both eyes closed, soft happy smiles, their hair "
                           "(colourful glowing indigo and orange) mixing together around them. No hands in frame."),
    "j07_ck_laugh": ("CK", SEA + "Close-up of CK laughing happily with eyes squeezed shut, bright warm light, hair bouncing. No hands in frame."),
    "j08_df_laugh": ("DF", SEA + "Close-up of DF laughing happily with her mouth open, eyes curved, glowing colourful hair, bright water. No "
                     "hands in frame."),
    "j09_surface_near": ("-", "Underwater looking up, the bright sea surface very close above, dazzling sun breaking through ripples, many "
                         "bubbles rising, turquoise and gold. No people."),
    # ---------------- ascent
    "k01_surface_from_below": ("-", "Straight up at the ocean surface from just below: golden light shattering through the waves in broken "
                               "shapes, rays fanning down, bubbles. No people."),
    "k02_hands_silhouette": ("DUO", SEA + "Silhouettes from below: two joined hands (one hand of each girl) reaching up toward the bright surface, "
                             "their dark silhouettes against the golden light, hair trailing below. Exactly two joined hands."),
    "k03_breach_moment": ("DUO", SEA + "Just below the bright surface, DF and CK rushing upward side by side, faces lit gold, about to break the "
                          "surface, holding hands, determined happy faces."),
    "k04_hands_break_surface": ("DUO", "Above the sea at sunrise, at water level: two joined hands bursting out of the sparkling sea surface "
                                "first, water droplets flying, pastel orange sky. Exactly two joined hands, one from each girl."),
    # ---------------- out of the sea
    "l01_breach_splash": ("DUO", "Above the ocean at sunrise: DF and CK bursting out of the sea surface together holding hands, a big splash of "
                          "sparkling water droplets, pastel orange and blue sky with clouds, joyful."),
    "l02_sky_leap": ("DUO", "DF and CK leaping high in the sky above the sea holding hands, DF's whale tail and CK's ribbons and hair spreading "
                     "like wings, water droplets glittering, big pastel sunrise sky. Joyful, liberating."),
    "l03_df_face_sun": ("DF", "Above the sea, close-up of DF's wet face seeing the sun for the first time, eyes wide with wonder, golden light, "
                        "wet colourful hair, water droplets. No hands in frame."),
    "l04_ck_face_sun": ("CK", "Above the sea, close-up of CK looking at someone off-frame with a tender loving smile, wet orange hair, golden "
                        "sunrise light, water droplets. No hands in frame."),
    "l05_fall_back_sea": ("DUO", "DF and CK falling back into the sparkling sea together, laughing, holding hands, a ring of splash and light "
                          "around them, sunrise reflections."),
    # ---------------- outro
    "m01_rock_wide": ("DUO", "Wide shot of a calm sea at golden sunset, a small rock in the sea, DF and CK sitting together on it seen from "
                      "behind, small in the frame, the sun low on the horizon, warm orange sky reflected on the water."),
    "m02_lean_shoulder": ("DUO", "Medium shot at sunset on a sea rock: DF and CK sitting side by side seen from slightly behind and to the side, "
                          "CK's head resting on DF's shoulder, both smiling gently, DF's whale tail in the water, warm orange sky."),
    "m03_hands_on_rock": ("DUO", "Close-up insert at sunset: two hands with fingers interlaced resting on a wet sea rock, one with a cream knit "
                          "cardigan sleeve (whale girl), one with a frilled cream cuff (orange girl), warm golden light, sparkling sea "
                          "behind. Exactly two hands."),
    "m04_end_card": ("-", "Calm sea at dusk after sunset, purple and orange sky, the first stars, a gentle horizon, a small empty rock with "
                     "one orange flower petal on it. Calm, lots of empty sky for text. No people."),
}


def build(key):
    cast, body = PAINT[key]
    ck_n = "SECOND" if cast == "DUO" else "FIRST"
    if cast == "DF":
        refs, who = [DF_REF, STYLE_REF], "DF is " + DF + ". "
    elif cast == "CK":
        refs, who = [CK_REF, STYLE_REF], "CK is " + CK.format(n="FIRST") + ". "
    elif cast == "DUO":
        refs, who = [DF_REF, CK_REF, STYLE_REF], "DF is " + DF + ". CK is " + CK.format(n=ck_n) + ". "
    else:
        refs, who = [STYLE_REF], ""
    prompt = STYLE + who + "\n\nScene: " + body + "\n\n" + TAIL
    return prompt, refs, model_for(key), cast
