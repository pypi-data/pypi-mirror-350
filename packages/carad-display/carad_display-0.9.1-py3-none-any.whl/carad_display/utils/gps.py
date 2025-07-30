import pynmea2
import serial

from shapely import wkt
from shapely.geometry import Point


def get_gps() -> list[float, float]:
    try:
        count = 0
        while True and count < 10:
            port="/dev/ttyACM0"
            ser=serial.Serial(port, baudrate=9600, timeout=0.5)
            dataout = pynmea2.NMEAStreamReader()
            newdata=ser.readline().decode('unicode_escape')

            if newdata[0:6] == "$GPRMC":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "(широта, долгота): (" + str(lat) + "," + str(lng) + ")"
                print(gps)
                return ([float(str(lat)), float(str(lng))])
            count += 1
    except Exception as e:
        print (e)
        return ([0, 0])


def is_location_in_poly(wkt_polygon: str, location: list[float, float]) -> bool:
    polygon = wkt.loads(wkt_polygon)
    print ("location:", location)
    a, b = location
    point = Point(a, b)
    return point.within(polygon)


if __name__ == "__main__":
    get_gps()