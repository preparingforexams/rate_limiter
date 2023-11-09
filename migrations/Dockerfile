FROM flyway/flyway:10.0

COPY sql /flyway/sql
COPY flyway.conf /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
