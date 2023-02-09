import argparse


def main(args):
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO: ここは基本的に指定せずに、ConvAIの引数と合わせるべきかも
    parser.add_argument(
        "--train_file_path",
        default="./data/converted.json",
        help="Relative path to train .json file.",
    )
    parser.add_argument(
        "--converted_data_size",
        type=int,
        help="Data size to be converted. If no value, all data will be converted.",
    )

    parser.add_argument(
        "--num_candidates",
        default=5,
        type=int,
        help="Number of candidates for training.",
    )

    parser.add_argument(
        "--num_candidates",
        default=5,
        type=int,
        help="Number of candidates for training.",
    )

    args = parser.parse_args()
    main(args)
