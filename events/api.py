from starlette.requests import Request
from starlette.responses import Response
from objects.responses import ajson
from decorators import web, required_params
from objects import glob
from datetime import datetime

@web(url="/api/beatmaps")
@required_params({"s"})
async def get_beatmaps(req: Request):
    arg = req.query_params

    results = await glob.db.fetchall(
        "SELECT * FROM beatmaps WHERE MATCH(song_name) AGAINST (%s) ORDER BY beatmapset_id LIMIT 10",
        ['"'+arg["s"]+'"']
    )
        

    return ajson(results)

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

@web(url="/api/ainu_count")
async def get_registered_users(req: Request):
    results = await glob.db.fetch(
        "SELECT COUNT(*) as d FROM users"
    )

    return Response(str(results["d"]))
