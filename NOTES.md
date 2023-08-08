## Create postgres container with credentials
```
docker run -e POSTGRES_PASSWORD=developer -e POSTGRES_USER=developer -e POSTGRES_DB=db_pytrinfo -p 5432:5432 postgres:12.12

```
- Access
    - `docker exec -it <CONTAINER_ID> sh`
    - `psql --username=developer -d db_pytrinfo`
