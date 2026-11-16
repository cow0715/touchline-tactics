import csv
import json
from pathlib import Path
import sys

root = Path(__file__).parent
source = "https://github.com/metrica-sports/sample-data"

def tracking(path, team):
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.reader(file)
        next(rows)
        ids = [f"{team}:{cell}" for cell in next(rows) if cell]
        next(rows)
        frames = {}
        for row in rows:
            if row:
                values = [None if cell.strip().lower() in ("", "nan") else float(cell) for cell in row[3:]]
                frames[int(row[1])] = (int(row[0]), float(row[2]), values)
        return ids, frames

def sample_base(game, players, length, width):
    return dict(version=1, title=f"Metrica 샘플 경기 {game}", source=f"{source}/tree/master/data/Sample_Game_{game}",
        sourceName="Metrica Sports", teams=dict(home="A팀",away="B팀"), players=players,
        pitch=dict(length=length,width=width))

def convert_csv(game):
    def path(suffix):
        return root / ((f"game{game}-" if game>1 else "") + suffix + ".csv")
    home, left = tracking(path("RawTrackingData_Home_Team"), "home")
    away, right = tracking(path("RawTrackingData_Away_Team"), "away")
    ids = home+away
    players = [dict(id=id,team=id.split(":")[0],label=id.split(":")[1]) for id in ids]
    events = []
    with path("RawEventsData").open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            team = row["Team"].lower()
            def player(key):
                return f'{team}:{row[key].removeprefix("Player")}' if row[key] else None
            events.append(dict(frame=int(row["Start Frame"]),endFrame=int(row["End Frame"]) or None,
                type=row["Type"],subtype=row["Subtype"],team=team,actor=player("From"),target=player("To")))
    marks = {event[key] for event in events for key in ("frame","endFrame")}
    frames = []
    shared = sorted(left.keys() & right.keys())
    assert len(shared)>10000 and len(shared)==len(left)==len(right), f"Tracking CSVs incomplete for game {game}"
    for frame in shared:
        if frame%5 and frame not in marks and frame!=shared[0]:
            continue
        period,time,h = left[frame]
        other_period,other_time,a = right[frame]
        assert (period,time)==(other_period,other_time)
        ball = h[-2:] if None not in h[-2:] else a[-2:]
        if None in ball:
            ball=[None,None]
        values = h[:-2]+a[:-2]+ball
        assert len(values)==2*(len(ids)+1)
        frames.append([frame,time,period,*[None if v is None else round(v*(105 if i%2==0 else 68),2) for i,v in enumerate(values)]])
    d=sample_base(game,players,105,68)
    return dict(d,frames=frames,events=events)

def compact(value):
    return json.dumps(value,ensure_ascii=False,separators=(",",":"),allow_nan=False)

def main():
    if len(sys.argv)==2 and sys.argv[1] in ("--csv-1","--csv-2"):
        game=int(sys.argv[1][-1])
        match=convert_csv(game)
        (root/f"metrica-{game}.json").write_text(compact(match),encoding="utf-8")
        print(game,len(match["frames"]),len(match["events"]))
        return
    samples=[]
    for game in (1,2,3):
        match_path=root/f"metrica-{game}.json"
        if not match_path.is_file():
            continue
        match=json.loads(match_path.read_text(encoding="utf-8"))
        demo=root/f"metrica-demo-{game}.json"
        if demo.is_file():
            match["demo"]=json.loads(demo.read_text(encoding="utf-8-sig"))
        flank=root/f"flank-{game}.json"
        if flank.is_file():
            match["flank"]=json.loads(flank.read_text(encoding="utf-8"))
        samples.append(match)
        print(game,len(match["frames"]),len(match["events"]),len(match["players"]))
    assert samples
    template=(root/"app.html").read_text(encoding="utf-8")
    tactics=json.loads((root.parent/"outputs"/"tactics-dataset.json").read_text(encoding="utf-8"))
    html=template.replace("__METRICA_SAMPLES__",compact(samples)).replace("__TACTICS_DATASET__",compact(tactics))
    (root.parent/"outputs"/"tactics-lab.html").write_text(html,encoding="utf-8")

if __name__=="__main__":
    main()
