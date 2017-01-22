-- 马蜂窝爬虫数据库结构
-- By HJK
-- create 2017-01-15
-- update 2017-01-16
-- version 0.2

-- 目的地
create table if not exists dl_dest(
    -- 目的地ID
    dest_id        varchar(40)           primary key,
    -- 目的地名称
    name           varchar(48),
    --（行政）市／直辖市（可以和name一样）
    city           varchar(48),
    --（行政）省／州／直辖市（可以和name一样）
    province       varchar(48),
    -- 国家
    country        varchar(48),
    -- 父目的地ID
    parent_dest_id varchar(40),
    -- 马蜂窝目的地ID
    m_dest_id      int(8)
);



-- 景点
create table if not exists dl_poi(
    -- 景点ID
    poi_id          varchar(40)          primary key,
    -- 景点名
    name            varchar(48),
    -- 景点描述
    description     text,
    -- 景点地址
    poi_address     text,
    -- 景点攻略
    guidebook       text,
    -- 景点电话
    tel             varchar(20),
    -- 景点网址
    website         varchar(255),
    -- 用时参考
    expected_time   text,
    -- 交通
    traffic         text,
    -- 门票
    ticket          text,
    -- 开放时间
    business_hours  text,
    -- 评论数
    comment_count   int,
    -- 好评数
    comment_count_a int,
    -- 中评数
    comment_count_b int,
    -- 差评数
    comment_count_c int,
    -- 父景点ID（如果有）
    parent_poi_id   varchar(40),
    -- 目的地ID
    dest_id         varchar(40),
    -- 马蜂窝景点ID
    m_poi_id        int(8)
);

-- 景点图片
create table if not exists dl_poi_images(
    -- 自增ID
    idx_id          int               primary key,
    -- 景点ID
    poi_id          varchar(40),
    -- 图片URL
    image_url       text
);



