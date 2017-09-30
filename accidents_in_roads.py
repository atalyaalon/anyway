"""
Get accidents around a location. The input is currently the schools CSV list obtained by the project's team
This script is a standalone (using the API itself and not directly to DB) and can be run without setting up dev env.
Script support python 2.7+
To run:
python accidents_around_location.py <input_file> [flags]

"""
import argparse
from anyway.models import Marker


def calc_markers(markers):
    DEADLY_WEIGHT = 7
    HARD_WEIGHT = 5
    LIGHT_WEIGHT = 1
    severities = [x["severity"] for x in markers]
    light_count = severities.count(3)
    hard_count = severities.count(2)
    deadly_count = severities.count(1)

    return {'grade': deadly_count * DEADLY_WEIGHT + hard_count * HARD_WEIGHT + light_count * LIGHT_WEIGHT,
            'light': light_count,
            'hard': hard_count,
            'deadly': deadly_count
            }

def get_accidents_in_road(road_num):
    markers = Marker.get_road1_markers(road_num)
    accidents = []
    for idx in range(markers.count()):
        marker = markers[idx]
        accident = {}
        accident['km'] = marker.km
        accident['locationAccuracy'] = marker.locationAccuracy
        accident['road1'] = marker.road1
        accident['road2'] = marker.road2
        accident['address'] = marker.address
        accident['latitude'] = marker.latitude
        accident['longitude'] = marker.longitude
        accident['severity'] = marker.severity
        accident['provider_code'] = marker.provider_code
        accident['created'] = marker.created
        accidents.append(accident)
    markers_data = calc_markers(accidents)
    accidents_details = dict()
    accidents_details['ROAD_NUM'] = road_num
    accidents_details['GRADE'] = markers_data['grade']
    accidents_details['DEADLY'] = markers_data['deadly']
    accidents_details['HARD'] = markers_data['hard']
    accidents_details['LIGHT'] = markers_data['light']
    return accidents_details, accidents


def main(road_num):
    return get_accidents_in_road(road_num)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--road_num', default=1, type=int, help='road number')
    args = parser.parse_args()
    accidents_details, accidents = main(args.road_num)
    print(accidents_details)
