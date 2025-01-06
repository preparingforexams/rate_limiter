drop index usages_by_ids;

alter table usages
    rename to usages_old;

create table usages
(
    context_id   TEXT,
    user_id      TEXT,
    time         INT not null,
    reference_id TEXT,
    response_id  TEXT,
    primary key (context_id, user_id, time)
) strict;

create index usages_by_ids on usages (context_id asc, user_id asc, time desc);

insert into usages select * from usages_old;

drop table usages_old;
