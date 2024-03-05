FROM flyway/flyway:10.9

COPY sql /flyway/sql
COPY flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
