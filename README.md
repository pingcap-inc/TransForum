# TransForum

It's a project that translate the [TiDB Chinese forum](https://asktug.com/) to [TiDB English forum](https://ask.pingcap.com/).

![logic](./pic/logic.png)

## Deployment

1. Prepare a `.env` file, or set these variables in other ways:

    ```property
    DEBUG=False

    TIDB_HOST='gateway**.**-****-*.prod.aws.tidbcloud.com'
    TIDB_PORT=4000
    TIDB_USER='**********'
    TIDB_PASSWORD='***********'
    TIDB_DB_NAME='******'

    OPEN_AI_API='sk-*****************'
    OPEN_AI_BASE_URL='https://api.openai.com/v1'

    EN_DISCOURSE_HOST='https://ask.pingcap.com/'
    EN_DISCOURSE_API_USERNAME='****'
    EN_DISCOURSE_API_KEY='**********'
    EN_DISCOURSE_CATEGORY_ID='**'
    ```

2. Prepare a `docker-compose.yml` file.

    ```yaml
    version: "3"
    services:
    transforum:
        image: cheesewong/trans-forum:latest
        ports:
        - 4000:4000
        environment:
        DEBUG: "${DEBUG}"
        TIDB_HOST: "${TIDB_HOST}"
        TIDB_PORT: "${TIDB_PORT}"
        TIDB_USER: "${TIDB_USER}"
        TIDB_PASSWORD: "${TIDB_PASSWORD}"
        TIDB_DB_NAME: "${TIDB_DB_NAME}"
        OPEN_AI_API: "${OPEN_AI_API}"
        OPEN_AI_BASE_URL: "${OPEN_AI_BASE_URL}"
        EN_DISCOURSE_HOST: "${EN_DISCOURSE_HOST}"
        EN_DISCOURSE_API_USERNAME: "${EN_DISCOURSE_API_USERNAME}"
        EN_DISCOURSE_API_KEY: "${EN_DISCOURSE_API_KEY}"
        EN_DISCOURSE_CATEGORY_ID: "${EN_DISCOURSE_CATEGORY_ID}"
    ```

3. Run `docker compose up -d --force-recreate --pull always`.

## Usage

- This service will run synchronizing tasks by itself after it started.
- If you want to synchronize some pages or topics manually, you can use these API:

  - GET `/sync/topic_ids`: Grab all topic IDs from original forum, save it in the database, and wait for synchronizing.
  - POST `/topic/task`: Pick a topic ID that is not synchronized, translate it into English, and publish it to English forum. This API relies on `/sync/topic_ids`, it will use topic ID list from previous API.

  - PUT `/topic/{topic_id}`: Translate and synchronize the topic by topic ID. This API does not rely on any API. And it is idempotent, which means you can call it multiple times, and the result will be the same. And if the source was updated, this API will also update the English topic.
  - PUT `/page/{page_id}`: Just like `/topic/{topic_id}`, but synchronize all topics in the page `{page_id}`. This page is ordered by update time, and `page_id` starts from `0` to keep the same logic with the Discourse.

## Develop

- You can use `.env` set on your local machine to start this project.
- You can use `python3 manage.py gen-db-classes` to create or update the data instances in `app/db/gen_instances.py` by the tables of database that you configed in `.env` or environment variables.
- `manage.py`: A file to manage the instances generate and service start.
- `Dockerfile`: A file to build the Docker image.
- `app`: The main code folder.

  - `main.py`: Defines the entrances of APIs.
  - `config`: Defines how to read config. It will read `.env` or environment variables automatically.
  - `db`: Defines database oprations.

    - `db.sql`: It is the tables creation SQL.
    - `gen_instances.py`: Do **NOT** change this file manually. You can use `python3 manage.py gen-db-classes` to create or update this file from tables of database.

  - `forum`: Defines how to get, create, and update topics of forum.
  - `models`: Defines how to call the LLM to translate topics.
  - `service`: Defines how to integrate all components together and offer the service functions.
