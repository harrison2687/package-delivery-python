# Susan Harrison - 000854062
# C950 OA
from datetime import timedelta
import re


class Package(object):
    EOD_TIMESTAMP = timedelta(hours=17)
    SPECIAL_PACKAGES = [13, 15, 19]
    DELIVERED = 'Delivered at {}'
    ON_TRUCK = 'On Truck - Left Hub At: {}'
    AT_HUB = 'Waiting at Hub'

    def __init__(self, identifier, street, city, zipcode, deadline, weight, notes, destination):
        self.identifier = int(identifier)
        self.street = street
        self.city = city
        self.zipcode = zipcode
        self.deadline = self._convert_to_timestamp(deadline)
        self.weight = weight
        self.notes = notes
        self.destination = destination

        self.delivered_at = None
        self.ready_at = timedelta(hours=8)
        self.left_hub_at = None
        self.on_truck = False
        self.truck_availability = [1, 2]
        self.notes = notes

        self._modify(notes)

    def inline_report(self, time):
        report = self.report(time)

        return report[1:].replace('\n', ' ')

    def report(self, time=timedelta(hours=17)):
        return """
        ID: {}
        ADDRESS: {}
        ZIP: {}
        DEADLINE: {}
        WEIGHT: {}
        STATUS: {}\
        """.format(
            self.identifier,
            self.street,
            self.zipcode,
            self.deadline,
            self.weight,
            self._delivery_status(time)
        )

    def has_deadline(self):
        return self.deadline != self.EOD_TIMESTAMP

    def _deadline(self):
        if self.deadline == self.EOD_TIMESTAMP:
            return '{} (EOD)'.format(self.deadline)

        return '{}'.format(self.deadline)

    def high_priority(self):
        return self.has_deadline() or self.notes != 'None' or self.identifier in self.SPECIAL_PACKAGES

    # assigning a delivery status based on the timestamp
    def _delivery_status(self, time):
        if time > self.delivered_at:
            return self.DELIVERED.format(self.delivered_at)
        elif time > self.left_hub_at:
            return self.ON_TRUCK.format(self.left_hub_at)

        return self.AT_HUB

    # converting the EOD note into a timestamp
    def _convert_to_timestamp(self, time_string):
        if time_string == 'EOD':
            return self.EOD_TIMESTAMP

        (hour, minute, sec) = time_string.split(':')
        return timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))

    # modifying values to address a wrong address, and a delayed note
    # also putting in a catch for items that can only be on truck 2
    def _modify(self, notes):
        if re.match('Wrong address listed', notes):
            self.ready_at = timedelta(hours=10, minutes=20)
            self.street = '410 S State St'
            self.zip = 84111
        elif re.match('Delayed', notes):
            self.ready_at = timedelta(hours=9, minutes=5)
        elif re.match('Can only be on truck 2', notes):
            self.truck_availability = [2]
