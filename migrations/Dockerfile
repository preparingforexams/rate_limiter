FROM flyway/flyway:10.17

ARG DIALECT

COPY $DIALECT/sql /flyway/sql
COPY $DIALECT/flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
