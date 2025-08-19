from typing import List, Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class StreamIn(BaseModel):
    name: str
    source: Union[str, int]  # 0 for webcam, path, or RTSP/HTTP URL

class StreamOut(StreamIn):
    id: int

STREAMS: List[StreamOut] = []

@router.get("", response_model=List[StreamOut])
def list_streams():
    return STREAMS

@router.post("", response_model=StreamOut, status_code=201)
def create_stream(payload: StreamIn):
    new_id = (max((s.id for s in STREAMS), default=0) + 1)
    new = StreamOut(id=new_id, **payload.model_dump())
    STREAMS.append(new)
    return new

@router.delete("/{stream_id}", status_code=204)
def delete_stream(stream_id: int):
    for i, s in enumerate(STREAMS):
        if s.id == stream_id:
            del STREAMS[i]
            return
    raise HTTPException(status_code=404, detail="Stream not found")
