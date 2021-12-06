class Dataset:
    def __init__(self, labels):
        self.labels = {}
        for label_id, label in labels.items():
            self.labels[label_id] = label if type(label) is tuple else (label, (0, 0, 0))

    def get_label_color(self, label_id, bgr=False):
        if bgr:
            return self.labels[label_id][1][::-1] if label_id in self.labels else None
        else:
            return self.labels[label_id][1] if label_id in self.labels else None

    def get_label_ids(self):
        return self.labels.keys()

    def get_label_name(self, label_id):
        return self.labels[label_id][0] if label_id in self.labels else None


DATASETS = {}


DATASETS['MAVFine14'] = Dataset({
    0: 'business_jet',
    1: 'business_propeller',
    2: 'commercial_jet',
    3: 'commercial_propeller',
    4: 'military_fighter_jet',
    5: 'military_fighter_propeller',
    6: 'military_helicopter',
    7: 'military_transporter_jet',
    8: 'military_transporter_propeller',
    9: 'transporter_jet',
    10: 'transporter_propeller',
    11: 'utility_helicopter',
    12: 'utility_jet',
    13: 'utility_propeller'})


DATASETS['MAVSeg'] = Dataset({
    0: ('void', (0, 0, 0)),
    1: ('aircraft', (188, 188, 188)),
    2: ('apron_runway', (27, 37, 61)),
    3: ('building', (0, 84, 132)),
    4: ('indoor', (96, 58, 79)),
    5: ('sky', (209, 159, 141)),
    6: ('vegetation', (29, 98, 38)),
    7: ('water', (61, 41, 13))})


DATASETS['UAVFine9'] = Dataset({
    0: 'amateur_copter',
    1: 'semi-pro_copter',
    2: 'military_copter',
    3: 'amateur_fixed-wing',
    4: 'semi-pro_fixed-wing',
    5: 'military_fixed-wing',
    6: 'amateur_heli',
    7: 'semi-pro_heli',
    8: 'military_heli'})


DATASETS['UAVSeg'] = Dataset({
    0: ('void', (0, 0, 0)),
    1: ('aircraft', (188, 188, 188)),
    2: ('apron_runway', (61, 37, 27)),
    3: ('building', (132, 84, 0)),
    4: ('indoor', (79, 58, 96)),
    5: ('sky', (141, 159, 209)),
    6: ('vegetation', (38, 98, 29)),
    7: ('water', (13, 41, 61))})
