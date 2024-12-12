FROM flyway/flyway:11.1

LABEL org.opencontainers.image.source = "https://github.com/preparingforexams/rate_limiter"

ARG DIALECT

COPY $DIALECT/sql /flyway/sql
COPY $DIALECT/flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
