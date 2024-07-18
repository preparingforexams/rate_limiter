FROM flyway/flyway:10.16

COPY sql /flyway/sql
COPY flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
