
import json
import numpy

class JsonOutputClass:

    def __init__(self, args):
        self.args = args
        self.output_dict = {}
        self.output_dict["entries"] = []
        self.unloaded_rtt_ms = None

        if self.args.json_file:
            self.json_output_file = open(self.args.json_file, 'w')

    def set_unloaded_rtt_ms(self, rtt_ms):
        self.unloaded_rtt_ms = rtt_ms

    def add_entry(self, entry):
        self.output_dict["entries"].append(entry)

    def create_aggregate_stats(self):
        loaded_rtt_ms_list = []
        receiver_throughput_rate_mbps_list = []
        excess_buffered_bytes_list = []
        receiver_pps_list = []
        pkt_loss_percent_list = []

        for entry in self.output_dict["entries"]:

            sender_throughput_rate_mbps = entry["sender_throughput_rate_mbps"]
            receiver_throughput_rate_mbps = entry["receiver_throughput_rate_mbps"]
            throughput_rate_ratio = abs(sender_throughput_rate_mbps - receiver_throughput_rate_mbps) / receiver_throughput_rate_mbps

            # only add entries that capture then flow when it is at max bloat potential
            if (  (self.args.udp and entry["pkt_loss_percent"] > 0) or
                ((not self.args.udp) and throughput_rate_ratio < 0.03) and (receiver_throughput_rate_mbps > 1.0)  ):

                loaded_rtt_ms_list.append(entry["loaded_rtt_ms"])
                receiver_throughput_rate_mbps_list.append(entry["receiver_throughput_rate_mbps"])
                excess_buffered_bytes_list.append(entry["excess_buffered_bytes"])
                receiver_pps_list.append(entry["receiver_pps"])
                pkt_loss_percent_list.append(entry["pkt_loss_percent"])

        num_samples = len(loaded_rtt_ms_list)
        if num_samples < 10:
            if not self.args.quiet:
                print("WARNING: not enough valid samples for summary statistics: {} samples.  Increase the duration of the run using the '-t' option.".format(num_samples))
            return

        summary_dict = self.output_dict["summary"] = {}

        summary_dict["num_samples"] = num_samples

        summary_dict["unloaded_rtt_ms"] = self.unloaded_rtt_ms

        p50, p90, p99 = numpy.percentile(loaded_rtt_ms_list, [50, 90, 99])
        summary_dict["loaded_rtt_ms"] = {}
        summary_dict["loaded_rtt_ms"]["p50"] = p50
        summary_dict["loaded_rtt_ms"]["p90"] = p90
        summary_dict["loaded_rtt_ms"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(receiver_throughput_rate_mbps_list, [50, 90, 99])
        summary_dict["receiver_throughput_rate_mbps"] = {}
        summary_dict["receiver_throughput_rate_mbps"]["p50"] = p50
        summary_dict["receiver_throughput_rate_mbps"]["p90"] = p90
        summary_dict["receiver_throughput_rate_mbps"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(excess_buffered_bytes_list, [50, 90, 99])
        summary_dict["excess_buffered_bytes"] = {}
        summary_dict["excess_buffered_bytes"]["p50"] = p50
        summary_dict["excess_buffered_bytes"]["p90"] = p90
        summary_dict["excess_buffered_bytes"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(receiver_pps_list, [50, 90, 99])
        summary_dict["receiver_pps"] = {}
        summary_dict["receiver_pps"]["p50"] = p50
        summary_dict["receiver_pps"]["p90"] = p90
        summary_dict["receiver_pps"]["p99"] = p99

        p50, p90, p99 = numpy.percentile(pkt_loss_percent_list, [50, 90, 99])
        summary_dict["pkt_loss_percent"] = {}
        summary_dict["pkt_loss_percent"]["p50"] = p50
        summary_dict["pkt_loss_percent"]["p90"] = p90
        summary_dict["pkt_loss_percent"]["p99"] = p99

    def write_output(self):
        self.create_aggregate_stats()

        # write to stdout
        if (self.args.quiet < 2) and ("summary" in self.output_dict):
            str_out = json.dumps(self.output_dict["summary"], indent=4)
            print(str_out)

        # write to file if requested
        if self.args.json_file:
            json.dump(self.output_dict, self.json_output_file, indent=4)
            self.json_output_file.close()
