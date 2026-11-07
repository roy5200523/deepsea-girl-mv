import sys; sys.path.insert(0, ".")
from shotlist import timeline, lyrics
L = lyrics()
rows = ["| # | 时间 | 时长 | 运镜 | 画面 | 同期歌词 |", "|---|---|---|---|---|---|"]
for sid, s, e, key, mo, note in timeline():
    ly = next((x[2] for x in L if s - 0.3 <= x[0] < e - 0.3), "")
    rows.append(f"| {sid} | {int(s//60)}:{s%60:05.2f} | {e-s:.1f}s | {mo} | {note} | {ly} |")
open("shotlist_v2.md", "w", encoding="utf-8").write("\n".join(rows) + "\n")
print(len(rows) - 2, "rows")
