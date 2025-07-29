
import json
import numpy

class JsonOutputClass:

    def __init__(self, args):
        self.args = args

        self.json_output_file = open(args.json_file, 'w')

        self.output_dict = {}
        self.output_dict["entries"] = []

    def set_unloaded_rtt_ms(self, rtt_ms):
        if "unloaded_rtt_ms" not in self.output_dict:
            self.output_dict["unloaded_rtt_ms"] = rtt_ms

    def add_entry(self, entry):
        self.output_dict["entries"].append(entry)

    def create_aggregate_stats(self):
        loaded_rtt_ms_list = []
        receiver_throughput_rate_mbps_list = []
        excess_buffered_bytes_list = []
        receiver_pps_list = []
        pkt_loss_percent_list = []

        for entry in self.output_dict["entries"]:
            loaded_rtt_ms_list.append(entry["loaded_rtt_ms"])
            receiver_throughput_rate_mbps_list.append(entry["receiver_throughput_rate_mbps"])
            excess_buffered_bytes_list.append(entry["excess_buffered_bytes"])
            receiver_pps_list.append(entry["receiver_pps"])
            pkt_loss_percent_list.append(entry["pkt_loss_percent"])

        p50, p90, p99 = numpy.percentile(loaded_rtt_ms_list, [50, 90, 99])
        self.output_dict["loaded_rtt_ms"] = {}
        self.output_dict["loaded_rtt_ms"]["p50"] = p50
        self.output_dict["loaded_rtt_ms"]["p90"] = p90
        self.output_dict["loaded_rtt_ms"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(receiver_throughput_rate_mbps_list, [50, 90, 99])
        self.output_dict["receiver_throughput_rate_mbps"] = {}
        self.output_dict["receiver_throughput_rate_mbps"]["p50"] = p50
        self.output_dict["receiver_throughput_rate_mbps"]["p90"] = p90
        self.output_dict["receiver_throughput_rate_mbps"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(excess_buffered_bytes_list, [50, 90, 99])
        self.output_dict["excess_buffered_bytes"] = {}
        self.output_dict["excess_buffered_bytes"]["p50"] = p50
        self.output_dict["excess_buffered_bytes"]["p90"] = p90
        self.output_dict["excess_buffered_bytes"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(receiver_pps_list, [50, 90, 99])
        self.output_dict["receiver_pps"] = {}
        self.output_dict["receiver_pps"]["p50"] = p50
        self.output_dict["receiver_pps"]["p90"] = p90
        self.output_dict["receiver_pps"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(pkt_loss_percent_list, [50, 90, 99])
        self.output_dict["pkt_loss_percent"] = {}
        self.output_dict["pkt_loss_percent"]["p50"] = p50
        self.output_dict["pkt_loss_percent"]["p90"] = p90
        self.output_dict["pkt_loss_percent"]["p99"] = p99

    def write_output_file(self):
        self.create_aggregate_stats()
        json.dump(self.output_dict, self.json_output_file, indent=4)
        self.json_output_file.close()
