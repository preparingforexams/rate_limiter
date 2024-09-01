create table usages
(
    context_id   TEXT        not null,
    user_id      TEXT        not null,
    time         timestamptz not null,
    reference_id TEXT,
    response_id  TEXT,
    primary key (context_id, user_id, time)
);

create index usages_by_ids on usages (context_id asc, user_id asc, time desc);
