from starlette.requests import Request
from objects.responses import ajson
from decorators import web
from objects import glob
from datetime import datetime

@web(url="/api/bancho_graph")
async def get_beatmaps(req: Request):
    results = await glob.db.fetchall(
        "SELECT users_osu AS users, registered_users AS registered, time FROM bancho_stats ORDER BY time DESC LIMIT 421"
    )

    # .strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    for row in results:
        row["label"] = datetime.fromtimestamp(row["time"]).strftime('%Y-%m-%d %H:%M:%S')

    results.reverse()
    return ajson(results)
