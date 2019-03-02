from aerofiles.igc import Reader
from opensoar.competition.soaringspot import get_info_from_comment_lines
from opensoar.task.trip import Trip
from opensoar.task.waypoint import Waypoint
from opensoar.task.race_task import RaceTask
import json

with open('race_task_completed.igc', 'r') as f:
    parsed_igc_file = Reader().read(f)

# example.igc comes from soaringspot and contains task inforamtion
#task, _, _ = get_info_from_comment_lines(parsed_igc_file)
#_, trace = parsed_igc_file['fix_records']
#
#trip = Trip(task, trace)
#task_distance_covered = sum(trip.distances)
#
#print (task_distance_covered)

with open('task_2018-08-16.json', 'r') as f:
    jobj = json.loads(f.read())

waypoint_list = []
print ("\nWaypoint list:")
for turnpoint in jobj['turnpoints']:
    lon = turnpoint['waypoint']['lon']
    lat = turnpoint['waypoint']['lat']
    name = turnpoint['waypoint']['name']
    r_min = 0
    r_max = turnpoint['radius']
    # Cylindric area
    a_min = 0.0
    a_max = 180.0
    s_line = False
    sector_orientation = 'fixed'
    distance_correction = None
    orientation_angle = 0

    if 'type' in turnpoint:
        if turnpoint['type'].lower() == 'sss':
            if jobj['sss']['direction'] == 'ENTER':
                print ("ENTER CYLINDER DETECTED")
                r_min = r_max
                r_max = 10000000

    w = Waypoint(name,
                 lat, lon,
                 r_min, a_min,
                 r_max, a_max,
                 s_line,
                 sector_orientation,
                 distance_correction,
                 orientation_angle)
    waypoint_list.append(w)

#waypoint_list = waypoint_list[0:6]


r = RaceTask(waypoint_list)

d = (r.calculate_task_distances())

for i in range(len(waypoint_list)):
    w = waypoint_list[i]
    print (w, w.r_max, 'm')
    if i != len(waypoint_list) - 1:
        cum_dist = sum(d[:i])
        #print ("{:0.3f}km".format(cum_dist/1000))

print ("\nDistances list:")
print (d)

print ("\nTotal distance:")
print (sum(d))