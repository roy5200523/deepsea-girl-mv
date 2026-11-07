"""深海少女 MV v2 — shot list.

Timing: 136.9 BPM, bar = 1.7531 s, bar 0 downbeat at 0.16 s.  Cuts land on bar or half-bar lines.
Each shot: (id, start_bar, image_key, motion, note)
  motion codes (render stage): push / pull / pan-l / pan-r / tilt-u / tilt-d / sink / rise / shake / drift
  image_key: which storyboard painting it uses. A painting can feed 2-3 shots (different crop / layer / motion),
             so ~95 shots come from ~70 paintings.
"""
BPM = 136.9
BAR = 240 / BPM
T0 = 0.16


def t(bar):
    return round(T0 + bar * BAR, 3)


# DF = 大肥鱼 (whale girl), CK = 小克 (orange girl)
SHOTS = [
    # ---- Intro / A1: alone, sinking (0 – 18.9s)
    ("c001", 0.0, "a01_title_sea", "tilt-d", "黑场→纸纹水面，手写标题「…」逐笔写出"),
    ("c002", 2.0, "a02_df_sink_far", "sink", "远景：DF 从光里往下掉，很小"),
    ("c003", 4.0, "a03_df_face_eyes", "push", "近脸：半睁的眼，睫毛上的气泡"),
    ("c004", 5.0, "a04_df_hand_drift", "drift", "特写：手指松开，一个小鲸鱼发夹飘走"),
    ("c005", 6.0, "a05_df_hug_knees", "pull", "蜷起来抱膝，发丝像墨水散开"),
    ("c006", 7.0, "a06_df_from_below", "rise", "仰拍：她的剪影挡住遥远的水面"),
    ("c007", 8.0, "a07_df_sideview_dark", "pan-l", "侧面中景，光越来越少"),
    ("c008", 9.0, "a08_df_closed_eyes", "push", "闭眼，吐出最后一串泡泡"),
    # ---- A2: the light (18.9 – 36.6s)
    ("c009", 10.5, "a09_beam_arrives", "tilt-d", "一束暖橙光刺下来（拍点闪白）"),
    ("c010", 11.5, "a10_df_eyes_open", "push", "眼睛猛地睁开，瞳孔里映出橙光"),
    ("c011", 12.5, "a11_df_reach_up", "rise", "伸手向上，手指张开（只一只手入画）"),
    ("c012", 13.5, "a12_light_fingers", "drift", "光从指缝漏下来"),
    ("c013", 14.5, "a13_wave_swirl", "shake", "暗流卷来，画面旋转"),
    ("c014", 15.5, "a14_df_tumble", "shake", "她被卷走翻滚，头发乱成一团"),
    ("c015", 16.5, "a15_ck_glimpse_blur", "push", "模糊的一瞥：光晕里的 CK 背影"),
    ("c016", 17.5, "a16_ck_glimpse_smile", "pull", "CK 侧脸微笑（柔焦，像隔着眼泪）"),
    ("c017", 18.5, "a17_df_hand_chest", "push", "DF 手按胸口，脸有点红"),
    # ---- Pre-chorus: illumination (36.6 – 43.2s), fast half-bar cuts
    ("c018", 20.75, "a18_jelly_lights", "pan-r", "水母灯海亮起"),
    ("c019", 21.25, "a19_jelly_close", "drift", "近景发光水母"),
    ("c020", 21.75, "a20_df_among_lights", "push", "DF 在灯里转身张望"),
    ("c021", 22.25, "a21_lights_bokeh", "pan-l", "散景光点"),
    ("c022", 22.75, "a22_df_suspicious", "push", "「…」DF 回头，眼神躲闪"),
    ("c023", 23.5, "a23_df_eye_macro", "push", "眼睛大特写，瞳孔里两个光点"),
    # ---- Chorus 1 (43.2 – 61.5s)
    ("c024", 24.5, "b01_df_dive_down", "sink", "「…」主视觉：DF 头朝下坠落，长发向上"),
    ("c025", 25.5, "b02_df_sink_side", "sink", "侧面跟拍下沉"),
    ("c026", 26.5, "b03_df_shell", "push", "钻进巨大的贝壳/珊瑚洞"),
    ("c027", 27.5, "b04_df_sleeve_hide", "pull", "用开衫袖子遮脸"),
    ("c028", 28.5, "b05_df_peek", "push", "「…」从洞口偷看"),
    ("c029", 29.5, "b06_ck_far_above", "tilt-u", "她的视角：很高很远的 CK 在光里游"),
    ("c030", 30.5, "b07_df_blush_look", "push", "DF 脸红，盯着看"),
    ("c031", 31.5, "b08_two_vertical", "tilt-u", "竖构图：下暗上亮，两人之间隔着大片黑水"),
    ("c032", 32.5, "b09_ck_swim_close", "pan-r", "CK 游过，头发拖出光尾"),
    ("c033", 33.5, "b10_df_hug_tail", "pull", "DF 抱住自己的尾巴，偷偷笑了一下"),
    # ---- Interlude 1 (61.5 – 64.0s)
    ("c034", 34.5, "b11_godrays_whale", "rise", "空镜：海底仰望光柱，远处鲸影"),
    ("c035", 35.5, "b12_marine_snow", "drift", "空镜：海洋雪"),
    # ---- A3: sleepless (64.0 – 78.5s)
    ("c036", 36.0, "c01_df_lie_anemone", "pull", "躺在发光海葵上睁着眼"),
    ("c037", 37.0, "c02_df_turn_over", "drift", "翻身，抱着枕头一样的海绵"),
    ("c038", 38.0, "c03_df_count_bubbles", "push", "数气泡，手指点泡泡"),
    ("c039", 39.0, "c04_df_stare_up", "tilt-u", "盯着上方，嘴里小声念着什么"),
    ("c040", 40.0, "c05_ck_wings", "rise", "「…」CK 张开双臂，头发和披肩像翅膀"),
    ("c041", 41.0, "c06_ck_spin", "pan-l", "CK 在光里转圈"),
    ("c042", 42.0, "c07_ck_face_free", "push", "CK 闭眼享受水流"),
    ("c043", 43.0, "c08_df_watching_rock", "push", "「…」DF 躲在岩石后看呆了"),
    ("c044", 44.0, "c09_df_heart_eyes", "push", "DF 托腮发呆"),
    # ---- A4: eyes meet (78.5 – 92.4s)
    ("c045", 45.0, "c10_light_curtain", "tilt-d", "光再次像帘子倾泻"),
    ("c046", 46.0, "c11_df_entranced", "push", "DF 看入迷，嘴微张"),
    ("c047", 47.0, "c12_eyes_meet_ck", "push", "「…」CK 的眼睛（特写）"),
    ("c048", 47.5, "c13_eyes_meet_df", "push", "DF 的眼睛（特写），瞳孔一缩"),
    ("c049", 48.0, "c14_ck_turn_back", "pan-r", "CK 回头，向她伸手"),
    ("c050", 49.0, "c15_df_hide_beret", "shake", "DF 慌张用贝雷帽遮脸"),
    ("c051", 50.0, "c16_df_fake_look_away", "drift", "「…」假装看别处，耳鳍抖动"),
    ("c052", 51.0, "c17_df_ears_red", "push", "红透的耳鳍特写"),
    # ---- Chorus 2 (92.4 – 109.3s)
    ("c053", 52.0, "d01_df_dive_flustered", "sink", "「…」故意扎进黑暗，满脸通红"),
    ("c054", 53.0, "d02_df_cheeks_dark", "push", "黑暗中发光的红脸颊"),
    ("c055", 54.0, "d03_df_cover_face", "pull", "双手捂脸在黑暗里打滚"),
    ("c056", 55.0, "d04_ck_puzzled_above", "drift", "上方 CK 歪头疑惑"),
    ("c057", 56.0, "d05_df_hands_heart", "push", "「…」双手按胸口，胸口亮起小小暖光"),
    ("c058", 57.0, "d06_df_try_rise", "rise", "鼓起勇气往上游"),
    ("c059", 58.0, "d07_ink_tendrils", "shake", "「…」墨色触手缠住脚踝"),
    ("c060", 59.0, "d08_ink_pull_down", "sink", "被拖回黑暗，伸出的手抓空"),
    ("c061", 60.0, "d09_ink_close", "shake", "墨水爬上手臂（特写）"),
    # ---- Bridge (109.3 – 126.1s)
    ("c062", 62.0, "e01_dirty_clothes", "tilt-d", "「…」低头看染黑的开衫"),
    ("c063", 63.0, "e02_mirror_crack", "push", "破碎镜片里扭曲的笑脸"),
    ("c064", 64.0, "e03_mirror_shatter", "shake", "镜片碎开"),
    ("c065", 65.0, "e04_df_turn_away", "pan-l", "「…」转身背对光"),
    ("c066", 66.0, "e05_ck_reach_worried", "push", "CK 担心地伸出手"),
    ("c067", 67.0, "e06_df_shout", "shake", "「…」DF 回头大喊，泪和气泡炸开"),
    ("c068", 68.0, "e07_push_light_away", "shake", "挥手推开暖光，光碎成花瓣"),
    ("c069", 69.0, "e08_ck_stunned", "pull", "CK 愣住，手停在半空"),
    ("c070", 70.0, "e09_df_cry_close", "push", "DF 哭泣大特写"),
    # ---- Interlude 2 (126.1 – 138.1s): across the dark
    ("c071", 71.0, "f01_tears_to_lights", "drift", "眼泪变成蓝橙光泡"),
    ("c072", 72.0, "f02_wide_apart", "pull", "大远景：左下 DF 蜷着哭，右上 CK 手按胸口，中间大片黑"),
    ("c073", 73.0, "f03_ck_side_sad", "push", "CK 侧脸，眼睛湿了"),
    ("c074", 74.0, "f04_df_peek_back", "push", "DF 偷偷回头看她"),
    ("c075", 75.0, "f05_split_screen", "drift", "分屏：两人同时抬手又放下"),
    ("c076", 76.0, "f06_ck_lantern", "drift", "CK 把一朵发光小花放进水流，漂向 DF"),
    ("c077", 77.0, "f07_flower_reach_df", "push", "花漂到 DF 面前"),
    # ---- B: melt / vanish (138.1 – 153.3s)
    ("c078", 78.0, "g01_face_each_other", "push", "「…」两人隔着很近的距离对视"),
    ("c079", 79.0, "g02_chest_glow", "push", "DF 胸口发光，光像墨水在水里化开"),
    ("c080", 80.0, "g03_ck_soft_smile", "pull", "CK 温柔地笑"),
    ("c081", 81.0, "g04_almost_touch", "push", "两只手指尖几乎相碰"),
    ("c082", 82.0, "g05_ck_fade", "drift", "「…」CK 化作光点消失"),
    ("c083", 83.0, "g06_df_shock", "push", "DF 瞳孔放大"),
    ("c084", 84.0, "g07_petal_alone", "drift", "只剩一片橙色花瓣"),
    ("c085", 85.0, "g08_dark_empty", "pull", "空荡荡的黑"),
    # ---- C: search, reach (153.3 – 164.2s)
    ("c086", 87.5, "h01_df_search_swim", "pan-r", "「…」拼命往深处游"),
    ("c087", 88.5, "h02_df_search_close", "shake", "焦急的脸，头发往后飘"),
    ("c088", 89.5, "h03_abyss_glow", "sink", "深渊底部一点微弱橙光"),
    ("c089", 90.5, "h04_df_dive_toward", "sink", "她朝那点光俯冲"),
    ("c090", 91.5, "h05_df_reach_down", "push", "「…」把手伸到极限"),
    ("c091", 92.5, "h06_hands_grasp", "push", "两只手在黑暗里握住，光炸开（拍点闪白）"),
    # ---- C2: ほらね (164.2 – 170.6s)
    ("c092", 93.5, "i01_ck_horane", "push", "「…」CK 从光里笑着出现"),
    ("c093", 94.25, "i02_hair_color_bloom", "rise", "DF 发梢从蓝亮成渐变彩光"),
    ("c094", 95.0, "i03_tail_glow", "pan-r", "尾巴亮起生物荧光"),
    ("c095", 95.75, "i04_df_moved_tears", "push", "DF 含泪，不可置信地看着自己的手"),
    # ---- Final chorus (170.6 – 189.5s)
    ("c096", 96.5, "j01_ck_pull_arm", "rise", "「…」CK 拉住她的手臂往上"),
    ("c097", 97.5, "j02_marine_snow_bless", "drift", "祝福的海洋雪"),
    ("c098", 98.5, "j03_df_first_smile", "push", "DF 第一次笑，带着眼泪"),
    ("c099", 99.5, "j04_rise_together", "rise", "「…」两人手牵手上升"),
    ("c100", 100.5, "j05_fish_school", "pan-l", "鱼群围着她们旋转"),
    ("c101", 101.5, "j06_forehead_touch", "push", "两人额头相抵"),
    ("c102", 102.5, "j07_ck_laugh", "push", "CK 大笑"),
    ("c103", 103.5, "j08_df_laugh", "push", "DF 大笑"),
    ("c104", 104.5, "j09_surface_near", "rise", "水面越来越亮"),
    # ---- Interlude 3 (189.5 – 195.7s): ascent
    ("c105", 106.0, "k01_surface_from_below", "rise", "空镜：从下仰望水面，光碎成金色"),
    ("c106", 107.0, "k02_hands_silhouette", "rise", "牵着的两只手的剪影贴近水面"),
    ("c107", 108.0, "k03_breach_moment", "push", "破水前一瞬"),
    ("c107b", 110.0, "k04_hands_break_surface", "rise", "水面上方：牵着的手先破水而出"),
    # ---- Last line (195.7 – 209.8s): out of the sea
    ("c108", 111.5, "l01_breach_splash", "rise", "「…」冲出海面，水花（白闪）"),
    ("c109", 112.5, "l02_sky_leap", "pan-r", "跃到空中，尾巴和缎带像翅膀"),
    ("c110", 113.5, "l03_df_face_sun", "push", "DF 第一次见到太阳的脸"),
    ("c111", 114.5, "l04_ck_face_sun", "push", "CK 看着她笑"),
    ("c112", 115.5, "l05_fall_back_sea", "drift", "两人落回水面溅起光"),
    # ---- Outro (209.8 – 217.5s): sunset rock
    ("c113", 117.0, "m01_rock_wide", "pull", "夕阳礁石大远景"),
    ("c114", 118.5, "m02_lean_shoulder", "push", "依偎：CK 的头靠在 DF 肩上"),
    ("c115", 119.5, "m03_hands_on_rock", "drift", "礁石上十指相扣的手（特写）"),
    ("c116", 120.5, "m04_end_card", "pull", "手写落款「…」，淡出"),
]
END = 217.4
BEAT = BAR / 4


def lyrics():
    """[(start, end, text)]. Uses lyrics_times.txt if present, else the placeholder file."""
    from pathlib import Path
    p = Path(__file__).with_name("lyrics_times.txt")
    if not p.exists():
        p = Path(__file__).with_name("lyrics_times.example.txt")
    if not p.exists():
        return []
    rows = p.read_text(encoding="utf-8").splitlines()
    return [(float(s), float(e), txt) for s, e, txt in (r.split("|") for r in rows)]


def timeline():
    """[(id, start_s, end_s, image_key, motion, note)].

    Shot cuts start on the bar grid; the cut nearest each lyric start (within 1.1 s) moves to the beat just before
    the vocal, so pictures change with the words and still land on a beat.
    """
    starts = [t(s[1]) for s in SHOTS]
    for ls, _, _ in lyrics():
        i = min(range(len(starts)), key=lambda k: abs(starts[k] - ls))
        if abs(starts[i] - ls) < 1.1:
            b = (ls - 0.06 - T0) // BEAT
            new = round(T0 + b * BEAT, 3)
            lo = starts[i - 1] + 2 * BEAT if i > 0 else 0
            hi = starts[i + 1] - 2 * BEAT if i + 1 < len(starts) else END
            if lo <= new <= hi:
                starts[i] = new
    starts[0] = 0.0
    starts.append(END)
    out = []
    for k, (sid, _, key, motion, note) in enumerate(SHOTS):
        assert starts[k + 1] - starts[k] > 0.6, (sid, starts[k], starts[k + 1])
        out.append((sid, starts[k], starts[k + 1], key, motion, note))
    return out
