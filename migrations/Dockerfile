FROM flyway/flyway:10.22

LABEL org.opencontainers.image.source = "https://github.com/preparingforexams/rate_limiter"

ARG DIALECT

COPY $DIALECT/sql /flyway/sql
COPY $DIALECT/flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
