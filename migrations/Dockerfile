FROM flyway/flyway:10.5

COPY sql /flyway/sql
COPY flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
