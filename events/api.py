from starlette.requests import Request
from objects.responses import ajson
from decorators import web, required_params
from objects import glob
import numpy as np

beatmap_search = frozenset({
    "s"    
})
@web(url="/api/beatmaps")
@required_params({"s"})
async def get_beatmaps(req: Request):
    arg = req.query_params

    results = await glob.db.fetchall(
        "SELECT * FROM beatmaps WHERE MATCH(song_name) AGAINST (%s) ORDER BY beatmapset_id LIMIT 10",
        ['"'+arg["s"]+'"']
    )
        

    return ajson(results)
