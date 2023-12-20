FROM flyway/flyway:10.4

COPY sql /flyway/sql
COPY flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
