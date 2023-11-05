import argparse
import logging
import pandas as pd


def parse_rtt_by_flow(data, sampling_rate):
    # calculate rtt
    data["rtt_s"] = (data["reply_rx"] - data["test_tx"])

    # Calculate time window
    min_timestamp = data["test_tx"].min()
    data["Time"] = ((data["test_tx"] - min_timestamp) // sampling_rate) * sampling_rate
    
    # Get session IDs
    ssids = data["ssid"].unique()

    # Calculate average per flow
    res_df = data[["Time", "rtt_s"]]
    res_df = res_df.groupby(res_df['Time']).mean().reset_index()

    for ssid in ssids:
        temp_df = data.loc[data['ssid'] == ssid][["Time", "rtt_s"]]
        res_df[ssid] = temp_df.groupby(temp_df['Time']).mean()
    
    res_df = res_df.rename(columns={"rtt_s": "Aggregate-Flow"})
    
    return res_df

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_file", type=str, required=True, help="Path the STAMP result raw file")
    parser.add_argument("--out_file", type=str, required=True, help="Output file path")
    parser.add_argument("--sampling_rate", type=float, default=1.0, help="The sampling rate for the RTT value")
    parser.add_argument("--sep", type=str, default=',', help="Separator used for the output file" )
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M')

    # Parse RTT from raw data
    logging.info("Collecting raw data form '%s'" % args.raw_file)
    
    raw_data_df = pd.read_csv(args.raw_file)
    # Sort by test_pkt_tx_timestamp
    raw_data_df.sort_values(by=['test_tx'], inplace=True)
    raw_data_df.reset_index(drop=True, inplace=True)

    rtt_data_df = parse_rtt_by_flow(raw_data_df, 1)
    rtt_data_df.to_csv(args.out_file, index=False, sep=args.sep)

    logging.info("RTT result saved to '%s'" % args.out_file)


if __name__ == "__main__":
    main()
