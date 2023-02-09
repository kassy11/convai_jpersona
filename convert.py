import argparse
import json
import openpyxl
import random
from tqdm import tqdm

SHEET_NAME = {"PERSONA_LIST": "ペルソナリスト", "DIALOG": "対話"}
SPEAKER_IDS = ["A", "B"]
SPEAKER_B_GREETING = "こんにちは。"

# See: https://simpletransformers.ai/docs/convAI-data-formats/#data-formats
CONVERTED_KEYS = {
    "PERSONALITY": "personality",
    "UTTERANCES": "utterances",
    "CANDIDATES": "candidates",
    "HISTORY": "history",
}


def get_data(data_file_path):
    wb = openpyxl.load_workbook(data_file_path, data_only=True)
    persona_data = _get_persona_data(wb)
    dialog_data, all_utterance = _get_dialog_data(wb)
    return persona_data, dialog_data, all_utterance


def _get_persona_data(wb):
    ws = wb[SHEET_NAME["PERSONA_LIST"]]

    persona_data = {}
    for lines in ws:
        if lines[0].value == "No":
            continue

        pid, persona_a, persona_b = [v.value for v in lines][1:4]
        persona_data[pid] = {}
        persona_data[pid][SPEAKER_IDS[0]] = persona_a.split("\n")
        persona_data[pid][SPEAKER_IDS[1]] = persona_b.split("\n")

    # persona_data {'persona id': {'A': ['aaa', 'bbb'], 'B': ['cccc', 'ddd']}}
    return persona_data


def _get_dialog_data(wb):
    ws = wb[SHEET_NAME["DIALOG"]]
    dialog_data = {}
    all_utterance = []

    for lines in ws:
        if lines[0].value == "No":
            continue

        pid, speaker_id, dialog = [v.value for v in lines][1:4]
        if pid not in dialog_data:
            dialog_data[pid] = {}
        if speaker_id not in dialog_data[pid] and speaker_id in SPEAKER_IDS:
            dialog_data[pid][speaker_id] = []

        dialog_data[pid][speaker_id].append(dialog)
        all_utterance.append(dialog)

    all_utterance = list(set(all_utterance))

    # dialog_data {'persona id': {'A': ['aaa', 'bbb'], 'B': ['cccc', 'ddd']}}
    return dialog_data, all_utterance


def _remove_element(target_list, element):
    return list(filter(lambda x: x != element, target_list))


def _get_incorrect_candidates(all_utterance, correct_utterance, sample_size):
    if correct_utterance in all_utterance:
        incorrect_utterance = _remove_element(all_utterance, correct_utterance)
        assert len(incorrect_utterance) == len(all_utterance) - 1
    else:
        incorrect_utterance = all_utterance
    incorrect_candidates = random.sample(incorrect_utterance, sample_size)
    return incorrect_candidates


def convert(
    persona_data, dialog_data, all_utterance, num_candidates, converted_data_size
):
    converted_data = []
    for pid, persona in tqdm(persona_data.items()):
        for speaker_id in SPEAKER_IDS:  # ['A', 'B']
            converted_dict = {}
            converted_dict[CONVERTED_KEYS["PERSONALITY"]] = []
            converted_dict[CONVERTED_KEYS["UTTERANCES"]] = []
            converted_dict[CONVERTED_KEYS["PERSONALITY"]] = persona[speaker_id]

            speaker_dialogs = dialog_data[pid][speaker_id]
            another_speaker_id = list(set(SPEAKER_IDS) - set([speaker_id]))[0]
            another_speaker_dialogs = dialog_data[pid][another_speaker_id]

            # If the conversation started with A, add greeting to B first element
            if speaker_id == SPEAKER_IDS[0]:
                another_speaker_dialogs = [SPEAKER_B_GREETING] + another_speaker_dialogs

            previous_speaker_dialog = ""
            previous_history = []
            # WARN: If the length of dialogs of A and B are different, match the shorter one
            for (speaker_dialog, another_speaker_dialog) in zip(
                speaker_dialogs, another_speaker_dialogs
            ):
                incorrect_candidates = _get_incorrect_candidates(
                    all_utterance, speaker_dialog, num_candidates - 1
                )
                # The last candidate is the ground truth response observed in the conversational data,
                # others is randomly selected
                candidates = incorrect_candidates + [speaker_dialog]

                if not previous_speaker_dialog:
                    history = previous_history + [another_speaker_dialog]
                else:
                    history = previous_history + [
                        previous_speaker_dialog,
                        another_speaker_dialog,
                    ]

                utterance_data = {
                    CONVERTED_KEYS["CANDIDATES"]: candidates,
                    CONVERTED_KEYS["HISTORY"]: history,
                }
                converted_dict[CONVERTED_KEYS["UTTERANCES"]].append(utterance_data)

                previous_history = history
                previous_speaker_dialog = speaker_dialog

            converted_data.append(converted_dict)
            if converted_data_size and len(converted_data) == converted_data_size:
                return converted_data
    return converted_data


def main(args):
    persona_data, dialog_data, all_utterance = get_data(args.data_file_path)
    converted_data = convert(
        persona_data,
        dialog_data,
        all_utterance,
        args.num_candidates,
        args.converted_data_size,
    )

    converted_data_size = len(converted_data)
    train_data_size = int(converted_data_size * args.split_ratio)

    train_data = converted_data[:train_data_size]
    valid_data = converted_data[train_data_size:]
    print("train data size = {}".format(len(train_data)))
    print("valid data size = {}".format(len(valid_data)))

    output_data = {"train": train_data, "valid": valid_data}

    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = "./data"

    with open(
        out_dir + "/converted_{}.json".format(converted_data_size),
        "w",
        encoding="utf-8",
    ) as f:
        if args.is_indent:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(output_data, f, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_file_path",
        default="./data/japanese_persona_chat.xlsx",
        help="Relative path to input .xlsx file.",
    )
    parser.add_argument(
        "--out_dir",
        help="Relative dir to output .json file.",
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
        "--is_indent",
        default=False,
        type=bool,
        help="Whether to indent the converted .json file.",
    )

    parser.add_argument(
        "--split_ratio",
        default=0.8,
        type=float,
        help="Ratio of split between training data and evaluation data after conversion.",
    )
    args = parser.parse_args()
    main(args)
