from fastapi import FastAPI
from app.service.translate import translate_topic, translate_task, translate_or_update_first_page
from app.forum.get import save_all_topic_ids

import datetime

app = FastAPI(title="TransForum", version="0.0.1")


@app.put("/topic/{topic_id}")
async def topic(topic_id: int):
    return translate_topic(topic_id)


@app.put("/page/{page_id}")
async def page(page_id: int):
    return translate_or_update_first_page(page_id)


@app.get("/sync/topic_ids")
async def sync_topic_ids():
    save_all_topic_ids(datetime.datetime.now() - datetime.timedelta(days=365*2))
    return {"message": f"successful"}


@app.post("/topic/task")
async def topic_task():
    return translate_task()
