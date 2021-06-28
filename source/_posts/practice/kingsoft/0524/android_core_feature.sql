declare start_date date default '2021-05-21';
declare end_date date default '2021-05-17';
declare interval_days default 1;

set interval_days = 17;
set start_date = date_add(current_date(), interval -1 day);
set end_date = date_add(start_date, interval -1 * interval_days day);

with top40_country as (
    select
        *
    from (
        select
            country,
            count(distinct google_id) as uv
        from 
            `wps-data-analysis.wps_active.user_engagement_v3`
        where
            date >= end_date and date <= start_date
        group by 
            country
        order by 
            uv desc
        limit 40
    )
    union all (
        select
            country,
            count(distinct google_id) as uv
        from 
            `wps-data-analysis.wps_active.user_engagement_v3`
        where 
            country = 'Japan' and
            date >= end_date and date <= start_date
        group by
            country
    ) 
),
active as (
    select
        * 
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'active' as metrics
        from 
            `wps-data-analysis.wps_active.user_engagement_v3`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'active' as metrics
        from
            `wps-data-analysis.wps_active.user_engagement_v3`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by date
    )
),
cloud as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'cloud' as metrics
        from 
            `wps-data-analysis.wps_active.android_core_feature_cloud`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date 
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'cloud' as metrics
        from
            `wps-data-analysis.wps_active.android_core_feature_cloud`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by date
    )
    
),
openfile as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'openfile' as metrics
        from 
           `wps-data-analysis.wps_active.android_core_feature_view_edit`
        where
            country in (select country from top40_country) and
            if_view > 0 and
            date >= end_date and date <= start_date 
        group by
            country,
            date
        order by
            country,
            date 
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'openfile' as metrics
        from 
           `wps-data-analysis.wps_active.android_core_feature_view_edit`
        where
            country in (select country from top40_country) and
            if_view > 0 and
            date >= end_date and date <= start_date
        group by
            date
        order by
            date
    )
),
edit as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'edit' as metrics
        from 
           `wps-data-analysis.wps_active.android_core_feature_view_edit`
        where
            country in (select country from top40_country) and
            if_edit > 0 and
            date >= end_date and date <= start_date 
        group by
            country,
            date
        order by
            country,
            date 
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'edit' as metrics
        from 
           `wps-data-analysis.wps_active.android_core_feature_view_edit`
        where
            country in (select country from top40_country) and
            if_edit > 0 and
            date >= end_date and date <= start_date
        group by
            date
        order by
            date
    )  
),
first_open_v3 as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'first_open_v3' as metrics,
        from 
            `wps-data-analysis.wps_active.first_open_v3`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date 
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'first_open_v3' as metrics
        from
            `wps-data-analysis.wps_active.first_open_v3`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by date
    )  
),
login_base as (
    select 
        a.date,
        a.google_id,
        a.country
    from 
        (
            SELECT  --判断是否登录的
                DISTINCT a1.google_id,
                IF (a2.google_id IS NOT NULL, 1, 0) AS is_login,--判断非空则为登录用户
                a1.date,
                a1.country
        FROM (  ---全量活跃用户
            SELECT
                date,
                google_id,
                country
            FROM 
                `wps-data-analysis.wps_active.user_engagement_v3`
            WHERE 
                date >= end_date and date <= start_date 
        ) a1
        LEFT JOIN ( --全量登录用户
            SELECT
                DISTINCT google_id,
                date
                FROM  `wps-data-analysis.wps_active.user_engagement_v3`
            WHERE
                date >= end_date and date <= start_date
                AND REGEXP_CONTAINS(user_id,'^[0-9]+$')
        ) a2 --判断user_id为数字
        ON
            a1.google_id=a2.google_id
        ) a  
        where
            a.is_login = 1 -- 登录用户数量
),
login as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'login' as metrics
        from 
            login_base
        where
            country in (select country from top40_country)
        group by
            country,
            date
        order by
            country,
            date
    )
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'login' as metrics
        from
            login_base
        group by
            date
        order by 
            date
    )
),
share as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct google_id) as uv,
            'share' as metrics
        from 
            `wps-data-analysis.wps_active.android_core_feature_share`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date 
    ) as each_country
    union all (
        select
            '0All' as country,
            date,
            count(distinct google_id) as uv,
            'share' as metrics
        from
            `wps-data-analysis.wps_active.android_core_feature_share`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by date
    )
)
select
    *
from
    active
union all (select * from cloud)
union all (select * from openfile)
union all (select * from edit)
union all (select * from first_open_v3)
union all (select * from login)
union all (select * from share)
order by 
    metrics, country, date