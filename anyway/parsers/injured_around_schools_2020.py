# pylint: disable=no-member
import logging
import os
import shutil
from datetime import datetime

import math
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, not_, and_

from anyway.backend_constants import BE_CONST
from anyway.models import (
    SchoolWithDescription,
    InjuredAroundSchool,
    InjuredAroundSchoolAllData,
    InvolvedMarkerView
)
from anyway.utilities import init_flask, time_delta, chunks
from anyway.app_and_db import db

SUBTYPE_ACCIDENT_WITH_PEDESTRIAN = 1
LOCATION_ACCURACY_PRECISE = True
LOCATION_ACCURACY_PRECISE_INT = 1
AGE_GROUPS = [1, 2, 3, 4]
INJURED_TYPE_PEDESTRIAN = 1
INJURED_TYPES = [1, 6, 7]
VEHICLE_TYPES = [15, 21, 23]
CONTENT_ENCODING = "utf-8"
HEBREW_ENCODING = "cp1255"
ANYWAY_UI_FORMAT_MAP_ONLY = "https://www.anyway.co.il/?zoom=17&start_date={start_date}&end_date={end_date}&lat={latitude}&lon={longitude}&show_fatal=1&show_severe=1&show_light=1&approx={location_approx}&accurate={location_accurate}&show_markers=1&show_discussions=0&show_urban=3&show_intersection=3&show_lane=3&show_day=7&show_holiday=0&show_time=24&start_time=25&end_time=25&weather=0&road=0&separation=0&surface=0&acctype={acc_type}&controlmeasure=0&district=0&case_type=0&show_rsa=0&age_groups=1234&map_only=true"
ANYWAY_UI_FORMAT_WITH_FILTERS = "https://www.anyway.co.il/?zoom=17&start_date={start_date}&end_date={end_date}&lat={latitude}&lon={longitude}&show_fatal=1&show_severe=1&show_light=1&approx={location_approx}&accurate={location_accurate}&show_markers=1&show_discussions=0&show_urban=3&show_intersection=3&show_lane=3&show_day=7&show_holiday=0&show_time=24&start_time=25&end_time=25&weather=0&road=0&separation=0&surface=0&acctype={acc_type}&controlmeasure=0&district=0&case_type=0&show_rsa=0&age_groups=1234"
DATE_INPUT_FORMAT = "%d-%m-%Y"
DATE_URL_FORMAT = "%Y-%m-%d"
SCHOOL_DATA_DIR = 'schools_data'

def get_bounding_box(latitude, longitude, distance_in_km):
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)

    radius = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius * math.cos(latitude)

    lat_min = latitude - distance_in_km / radius
    lat_max = latitude + distance_in_km / radius
    lon_min = longitude - distance_in_km / parallel_radius
    lon_max = longitude + distance_in_km / parallel_radius
    rad2deg = math.degrees

    return rad2deg(lat_min), rad2deg(lon_min), rad2deg(lat_max), rad2deg(lon_max)


def acc_inv_query(longitude, latitude, distance, start_date, end_date, school):
    lat_min, lon_min, lat_max, lon_max = get_bounding_box(latitude, longitude, distance)
    baseX = lon_min
    baseY = lat_min
    distanceX = lon_max
    distanceY = lat_max
    pol_str = "POLYGON(({0} {1},{0} {3},{2} {3},{2} {1},{0} {1}))".format(
        baseX, baseY, distanceX, distanceY
    )

    query_obj = (
        db.session.query(InvolvedMarkerView)
        .filter(InvolvedMarkerView.geom.intersects(pol_str))
        .filter(
            or_(
                (InvolvedMarkerView.provider_code == BE_CONST.CBS_ACCIDENT_TYPE_1_CODE),
                (InvolvedMarkerView.provider_code == BE_CONST.CBS_ACCIDENT_TYPE_3_CODE),
            )
        )
        .filter(InvolvedMarkerView.accident_timestamp >= start_date)
        .filter(InvolvedMarkerView.accident_timestamp < end_date)
        .filter(InvolvedMarkerView.location_accuracy == LOCATION_ACCURACY_PRECISE_INT)
        .filter(InvolvedMarkerView.age_group.in_(AGE_GROUPS))
        .filter(InvolvedMarkerView.injury_severity <= 3)
        # .with_entities(InvolvedMarkerView.geom,
        #                InvolvedMarkerView.injured_type,
        #                InvolvedMarkerView.injured_type_hebrew,
        #                InvolvedMarkerView.involve_vehicle_type,
        #                InvolvedMarkerView.involve_vehicle_type_hebrew,
        #                InvolvedMarkerView.injury_severity,
        #                InvolvedMarkerView.injury_severity_hebrew,
        #                InvolvedMarkerView.speed_limit,
        #                InvolvedMarkerView.speed_limit_hebrew,
        #                InvolvedMarkerView.provider_code,
        #                InvolvedMarkerView.accident_timestamp,
        #                InvolvedMarkerView.location_accuracy,
        #                InvolvedMarkerView.age_group,
        #                InvolvedMarkerView.age_group_hebrew,
        #                InvolvedMarkerView.accident_year,
        #                InvolvedMarkerView.injury_severity,
        #                InvolvedMarkerView.cross_location,
        #                InvolvedMarkerView.cross_location_hebrew,
        #                )
    )

    df = pd.read_sql_query(query_obj.statement, query_obj.session.bind)
    df["school_id"] = school.school_id
    df["school_type"] = school.school_type
    df["school_name"] = school.school_name
    df["school_yishuv_name"] = school.yishuv_name
    df["school_longitude"] = school.longitude
    df["school_latitude"] = school.latitude
    df_path = os.path.join(SCHOOL_DATA_DIR ,str(school.school_id) + '.csv')
    if not os.path.exists(SCHOOL_DATA_DIR):
        os.mkdir(SCHOOL_DATA_DIR)
    df.to_csv(df_path)
    return df


def get_injured_around_schools(start_date, end_date, distance):
    schools = (
        db.session.query(SchoolWithDescription)
        .filter(
            not_(and_(SchoolWithDescription.latitude == 0, SchoolWithDescription.longitude == 0)),
            not_(
                and_(
                    SchoolWithDescription.latitude == None, SchoolWithDescription.longitude == None
                )
            ),
            or_(
                SchoolWithDescription.school_type == "גן ילדים",
                SchoolWithDescription.school_type == "בית ספר",
            ),
        )
        .all()
    )

    for idx, school in enumerate(schools):
        if idx % 100 == 0:
            logging.info(idx)
        df_curr = acc_inv_query(
            longitude=school.longitude,
            latitude=school.latitude,
            distance=distance,
            start_date=start_date,
            end_date=end_date,
            school=school,
        )

def import_to_datastore(start_date, end_date, distance, batch_size):
    if os.path.exists(SCHOOL_DATA_DIR):
        shutil.rmtree(SCHOOL_DATA_DIR)
    os.mkdir(SCHOOL_DATA_DIR)
    get_injured_around_schools(
            start_date, end_date, distance
            )

def parse(start_date, end_date, distance, batch_size):
    started = datetime.now()
    total = import_to_datastore(
        start_date=start_date, end_date=end_date, distance=distance, batch_size=batch_size
    )
    logging.info("Total: {0} rows in {1}".format(total, time_delta(started)))
