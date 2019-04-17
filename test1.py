# Parse tasks created with:
#
# https://geolocalisation.ffvl.fr/sites/all/modules/tasks/tasks.html
#
# You need to have a Waypoints file to create tasks. See the testfiles folder
# for that
import xml.etree.ElementTree as ET

def parse_waypoints(inputfile, format=None):
    root = ET.parse(inputfile).getroot()

    # deal with the namespaces
    ns={'ns': 'http://www.topografix.com/GPX/1/1'}

    for wp in root.findall('.//ns:rtept', ns):
        lat, lon = wp.attrib['lat'], wp.attrib['lon']
        r = wp.find('ns:radius', ns)
        assert r is not None, 'Defect waypoint, no radious found'
        radius = r.text



