from fastapi import APIRouter, Query
from ..core.db import fetch_all

router = APIRouter()

@router.get("/now")
def stats_now(stream_id: int | None = Query(None, ge=1)):
    filter_sql = "AND stream_id = :sid" if stream_id else ""
    params = {"sid": stream_id} if stream_id else {}
    sql = f"""
        SELECT stream_id, COUNT(*) persons_last_60s
        FROM detection_snapshots
        WHERE ts > SYSTIMESTAMP - INTERVAL '60' SECOND
          {filter_sql}
        GROUP BY stream_id
        ORDER BY persons_last_60s DESC
    """
    return fetch_all(sql, params)

@router.get("/hour")
def stats_hour(stream_id: int | None = Query(None, ge=1)):
    filter_sql = "AND stream_id = :sid" if stream_id else ""
    params = {"sid": stream_id} if stream_id else {}
    sql = f"""
        SELECT stream_id,
               CAST(TRUNC(ts, 'MI') AS TIMESTAMP) AS bucket_minute,
               SUM(persons_total) AS persons
        FROM detection_snapshots
        WHERE ts > SYSTIMESTAMP - INTERVAL '1' HOUR
          {filter_sql}
        GROUP BY stream_id, TRUNC(ts, 'MI')
        ORDER BY bucket_minute
    """
    return fetch_all(sql, params)

@router.get("/top_streams")
def stats_top_streams():
    sql = """
        SELECT stream_id, SUM(persons_total) persons_last_10m
        FROM detection_snapshots
        WHERE ts > SYSTIMESTAMP - INTERVAL '10' MINUTE
        GROUP BY stream_id
        ORDER BY persons_last_10m DESC
        FETCH FIRST 5 ROWS ONLY
    """
    return fetch_all(sql)
