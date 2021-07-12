declare start_date date default '2021-05-21';
declare end_date date default '2021-05-17';
declare interval_days default 17;

set interval_days = 17;
set start_date = date_add(current_date(), interval -1 day);
set end_date = date_add(start_date, interval -1 * interval_days day);

-- 日活
with top40_country as (
    select
        *
    from (
        select
            country,
            count(distinct device_id) as uv
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            date >= end_date and date <= start_date
        group by 
            country
        order by 
            uv desc
        limit 40
    ) union distinct (
        select
            'JP',
            count(distinct device_id) as uv
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            country = 'JP' and 
            date >= end_date and date <= start_date
    )   
),
active as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct device_id) as uv,
            'active' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'active' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by 
            date
    )
),
cloud as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct device_id) as uv,
            'cloud' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.app_cloudsvr`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'cloud' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.app_cloudsvr`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by 
            date
    )
),
openfile as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct device_id) as uv,
            'openfile' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.feature_file_view`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'openfile' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.feature_file_view`
        where
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
            count(distinct device_id) as uv,
            'edit' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.feature_file_save`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'edit' as metrics
        from 
            `wps-cloud-service.wps_nginx_pc.feature_file_save`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by 
            date
    )    
),
first_open as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct device_id) as uv,
            'first_open' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_first_open_mix`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'first_open' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_first_open_mix`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by 
            date
    )
),
login as (
    select
        *
    from (
        select
            country,
            date,
            count(distinct user_id) as uv,
            'login' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            country in (select country from top40_country) and
            user_id is not null and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct user_id) as uv,
            'login' as metrics
        from 
            `wps-data-analysis.wps_metric_pc.pc_active_mix`
        where
            user_id is not null and
            date >= end_date and date <= start_date
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
            count(distinct device_id) as uv,
            'share' as metrics,
        from 
            `wps-cloud-service.wps_nginx_pc.feature_share`
        where
            country in (select country from top40_country) and
            date >= end_date and date <= start_date
        group by
            country,
            date
        order by
            country,
            date
    ) union all (
        select
            '0ALL' as country,
            date,
            count(distinct device_id) as uv,
            'share' as metrics,
        from 
            `wps-cloud-service.wps_nginx_pc.feature_share`
        where
            date >= end_date and date <= start_date
        group by
            date
        order by 
            date
    )    
)

select
    *
from active
union all (select * from cloud)
union all (select * from openfile)
union all (select * from edit)
union all (select * from first_open)
union all (select * from login)
union all (select * from share)
order by 
    metrics, country, date