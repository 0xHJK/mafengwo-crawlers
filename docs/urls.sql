create table if not exists urls (
    id          integer     primary key,
    url         text,
    method      text,
    data        text,
    dtype       text,
    rex         text,
    selector    text,
    attr        text
);
