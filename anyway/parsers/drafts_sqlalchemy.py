    # markers_query = sa.select([Involved,
    #                           AccidentMarker.severity,
    #                           AccidentMarker.one_lane,
    #                           AccidentMarker.multi_lane,
    #                           AccidentMarker.speed_limit,
    #                           AccidentMarker.created,
    #                           AccidentMarker.yishuv_symbol,
    #                           AccidentMarker.geo_area,
    #                           AccidentMarker.day_night,
    #                           AccidentMarker.day_in_week,
    #                           AccidentMarker.traffic_light,
    #                           AccidentMarker.region,
    #                           AccidentMarker.district,
    #                           AccidentMarker.natural_area,
    #                           AccidentMarker.municipal_status,
    #                           AccidentMarker.yishuv_shape,
    #                           AccidentMarker.street1,
    #                           AccidentMarker.street2,
    #                           AccidentMarker.home,
    #                           AccidentMarker.junction,
    #                           AccidentMarker.urban_intersection,
    #                           AccidentMarker.non_urban_intersection,
    #                           AccidentMarker.day_night,
    #                           AccidentMarker.day_in_week,
    #                           AccidentMarker.didnt_cross]) \
    #     .select_from(join(AccidentMarker, Involved)) \
    #     .where(AccidentMarker.geom.intersects(pol_str)) \
    #     .where(AccidentMarker.provider_and_id == Involved.provider_and_id) \
    #     .where(or_((AccidentMarker.provider_code == CONST.CBS_ACCIDENT_TYPE_1_CODE), (AccidentMarker.provider_code == CONST.CBS_ACCIDENT_TYPE_3_CODE))) \
    #     .where(AccidentMarker.created >= start_date) \
    #     .where(AccidentMarker.created < end_date) \
    #     .where(AccidentMarker.location_accuracy == LOCATION_ACCURACY_PRECISE) \
    #     .where(Involved.injured_type == INJURED_TYPE_PEDESTRIAN) \
    #     .where(AccidentMarker.yishuv_symbol != -1)

    # df = pd.read_sql_query(markers_query, db.session.bind)
##############################################################################
    # accident_query = select([AccidentMarker.provider_and_id,
    #                   AccidentMarker.severity,
    #                   AccidentMarker.one_lane,
    #                   AccidentMarker.multi_lane,
    #                   AccidentMarker.speed_limit,
    #                   AccidentMarker.created,
    #                   AccidentMarker.yishuv_symbol,
    #                   AccidentMarker.geo_area,
    #                   AccidentMarker.day_night,
    #                   AccidentMarker.day_in_week,
    #                   AccidentMarker.traffic_light,
    #                   AccidentMarker.region,
    #                   AccidentMarker.district,
    #                   AccidentMarker.natural_area,
    #                   AccidentMarker.municipal_status,
    #                   AccidentMarker.yishuv_shape,
    #                   AccidentMarker.street1,
    #                   AccidentMarker.street2,
    #                   AccidentMarker.home,
    #                   AccidentMarker.junction,
    #                   AccidentMarker.urban_intersection,
    #                   AccidentMarker.non_urban_intersection,
    #                   AccidentMarker.day_night,
    #                   AccidentMarker.day_in_week,
    #                   AccidentMarker.didnt_cross]) \
    #                 .where(AccidentMarker.geom.intersects(pol_str)) \
    #                 .where(AccidentMarker.provider_and_id == Involved.provider_and_id) \
    #                 .where(or_((AccidentMarker.provider_code == CONST.CBS_ACCIDENT_TYPE_1_CODE), (AccidentMarker.provider_code == CONST.CBS_ACCIDENT_TYPE_3_CODE))) \
    #                 .where(AccidentMarker.created >= start_date) \
    #                 .where(AccidentMarker.created < end_date) \
    #                 .where(AccidentMarker.location_accuracy == LOCATION_ACCURACY_PRECISE) \
    #                 .where(AccidentMarker.yishuv_symbol != -1) \
    #                 .alias()

    # query_obj = db.session.query(Involved) \
    #     .join(accident_query, accident_query.c.provider_and_id == Involved.provider_and_id) \
    #     .filter(Involved.injured_type == INJURED_TYPE_PEDESTRIAN)
