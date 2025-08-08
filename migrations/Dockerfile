FROM flyway/flyway:11.11

LABEL org.opencontainers.image.source = "https://github.com/preparingforexams/rate_limiter"

ARG DIALECT

RUN groupadd --system --gid 500 app \
  && useradd --system --uid 500 --gid app --no-create-home app

USER 500

COPY $DIALECT/sql /flyway/sql
COPY $DIALECT/flyway.toml /flyway/conf

CMD [ "migrate", "-skipCheckForUpdate" ]
