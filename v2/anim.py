"""Shots animated with image-to-video (plan 1: key character moments only).

ANIM[image_key] = motion prompt. The rest of the shots stay as layered stills.
Prompts describe only small, plausible motion so the drawing, faces and hands stay intact.
"""
BASE = ("Hand-drawn 2D anime, keep the exact drawing style, line art, colours and paper texture of the image. "
        "Camera stays almost still. Do not add new characters or objects. Hands keep five fingers and stay attached. ")

ANIM = {
    "a03_df_face_eyes": "Her hair and the bubbles drift slowly upward in the water; she blinks once, very slowly, eyes staying half-closed.",
    "a05_df_hug_knees": "She slowly drifts and rotates a little while hugging her knees; her long hair spreads and sways like ink in water.",
    "a10_df_eyes_open": "Her eyes widen in surprise, the warm orange light on her face brightens and flickers, hair sways gently.",
    "a11_df_reach_up": "She stretches her raised arm a little higher toward the light, fingers opening; her hair and cardigan float upward.",
    "a14_df_tumble": "She is swept and slowly rotates in the current, hair and cardigan whipping around, bubbles swirl past.",
    "a16_ck_glimpse_smile": "Her long orange hair and ribbons sway in the current, she slowly opens her eyes and smiles softly, bubbles rise.",
    "a20_df_among_lights": "She turns her head to look around; the glowing jellyfish pulse and drift slowly; her hair floats.",
    "a22_df_suspicious": "She glances sideways over her shoulder and then looks away, a slight blush; hair sways.",
    "b01_df_dive_down": "She falls slowly downward, her long hair streaming and rippling upward like ink, cardigan fluttering.",
    "b05_df_peek": "She rises a little from behind the rock to peek, eyes looking up, fin ears twitch; hair floats.",
    "b07_df_blush_look": "She stares upward, her blush deepens, eyes sparkle and she presses her lips together shyly; hair sways.",
    "b09_ck_swim_close": "She glides forward through the water with a gentle arm stroke, her long hair trailing and rippling behind her.",
    "c05_ck_wings": "She spreads her arms wider and glides upward; her hair and capelet billow out behind her like wings; light ripples.",
    "c06_ck_spin": "She turns gracefully in place, skirt and hair swirling around her, bubbles spiral.",
    "c09_df_heart_eyes": "She sways her head slightly side to side dreamily with her chin on her hands, her tail swishes slowly.",
    "c14_ck_turn_back": "She finishes turning toward the viewer, hair swinging around, and smiles warmly with her hand reaching out.",
    "c15_df_hide_beret": "She pulls her beret further down over her eyes in panic, fin ears flapping, little shaking motion.",
    "c16_df_fake_look_away": "She turns her face further away, eyes darting, fin ears twitching, hair swaying.",
    "d01_df_dive_flustered": "She dives forward and down with a kick of her tail, bubbles streaming behind her, hair trailing.",
    "d03_df_cover_face": "She rolls slowly sideways covering her face, legs kicking a little, hair swirling.",
    "d05_df_hands_heart": "The small warm glow between her hands on her chest pulses brighter; her hair floats; she breathes in.",
    "d08_ink_pull_down": "The black ink tendrils pull her slowly downward, her raised hand strains upward, hair streaming up.",
    "e06_df_shout": "She shouts with tears bursting out as bubbles, hair whipping around her, a strong shake of emotion.",
    "e08_ck_stunned": "Orange petals drift past her; her raised hand trembles and slowly lowers; her eyes glisten.",
    "e09_df_cry_close": "Tears well up and float away from her eyes as small bubbles, her lips tremble.",
    "f01_tears_to_lights": "Tears leave her closed eyes and turn into small glowing lights that float slowly upward.",
    "f03_ck_side_sad": "Her eyes glisten and she blinks slowly; her hair drifts softly in the dark water.",
    "f06_ck_lantern": "She gently releases the glowing flower from her hands and it drifts away; her hair floats.",
    "g02_chest_glow": "Soft luminous ripples of light flow out from her chest and dissolve into the water, hair floating.",
    "g05_ck_fade": "Her body dissolves into many small orange light particles that drift away while she smiles faintly.",
    "h01_df_search_swim": "She swims forward hard, arms pulling, tail kicking, hair streaming behind her.",
    "h05_df_reach_down": "She strains to reach further down, fingers stretching toward the faint glow, hair flowing.",
    "h06_hands_grasp": "The two hands tighten their grip and warm light bursts outward from where they meet.",
    "i01_ck_horane": "She smiles warmly and speaks, her free hand gesturing gently; light sparkles around them; hair floats.",
    "i02_hair_color_bloom": "Glowing colours spread along her hair from root to tips, strands floating and shimmering.",
    "i04_df_moved_tears": "Her glowing hands shimmer, tears well up, and a trembling smile spreads on her lips.",
    "j01_ck_pull_arm": "She pulls the other girl upward, both rising through the water, hair streaming, marine snow drifting.",
    "j04_rise_together": "Both girls rise upward together holding hands, laughing, hair flowing behind them.",
    "j06_forehead_touch": "They press foreheads gently, both smiling, their hair swirling together around them.",
    "l02_sky_leap": "Both girls soar through the air holding hands, hair, ribbons and tail streaming, water droplets glittering.",
    "m02_lean_shoulder": "The sea sparkles, a soft breeze moves their hair, the orange-haired girl nestles closer on the shoulder.",
}


def prompt(key):
    return BASE + ANIM[key]
