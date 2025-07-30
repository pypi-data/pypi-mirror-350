
class RadarStatus:
    def __init__(self):
        self.valid_lrr = None
        self.valid_nr = None
        self.lrr_status = {
            "drop_rate": None,
            "valid_time_sync_rate": None,
            "valid_calibration_rate": None,
            "high_latency_rate": None,
        }
        self.nr_status = {
            "drop_rate": None,
            "valid_time_sync_rate": None,
            "valid_calibration_rate": None,
            "high_latency_rate": None,
        }
