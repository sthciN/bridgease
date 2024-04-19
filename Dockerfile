FROM mindsdb/mindsdb:v24.3.5.0

RUN pip install --upgrade pip && \
    pip install mindsdb[rag] \
    pip install mindsdb[openai]

# ENTRYPOINT [ "sh", "-c", "python -m mindsdb --config=/root/mindsdb_config.json --api=http,mysql,mongodb" ]


# docker run --name postgres -e POSTGRES_PASSWORD=admin -p 5432:5432 -v ~/Startup/product/postgres_data:/var/lib/postgresql/data -d postgres:latest