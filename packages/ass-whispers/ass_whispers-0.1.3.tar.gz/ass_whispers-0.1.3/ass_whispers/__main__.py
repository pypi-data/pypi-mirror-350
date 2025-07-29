import argparse
import os
import faster_whisper
import json

# -m large-v2
# -d cuda
# --compute_type \"float32\"
# --task transcribe
# --language ja
# --temperature 0.4
# --best_of 8
# --beam_size 10
# --patience 2
# --repetition_penalty 1.4
# --condition_on_previous_text False
# --no_speech_threshold 0.275
# --logprob_threshold -1
# --compression_ratio_threshold 1.75
# --word_timestamp True
# --vad_filter True
# --vad_method pyannote_v3
# --sentence
# --standard_asia"

__version__ = "0.1.3"

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"

def whispers(audio: str, timestamps: str, device: str, model: str, language: str):
    """
    Transcribe audio files with Whisper
    """

    print(f"Loading whisper '{model}'...")
    model = faster_whisper.WhisperModel(
        model_size_or_path=model,
        device=device,
        compute_type="float32",
        # vad_method="pyannote_v3",
        # sentence=True,
        # standard_asia=True,
    )

    print("Extrapolating clips from timestamps...")
    with open(timestamps, "r", encoding="utf-8") as f:
        timestamp_file = json.load(f)

    clip_timestamps = []
    for ts in timestamp_file:
        clip_timestamps.append(ts["start_time"] / 1000)
        clip_timestamps.append(ts["end_time"] / 1000)

    print(f"Transcribing: {audio}")
    segments, _ = model.transcribe(
        audio,
        language=language,
        temperature=0.4,
        best_of=8,
        beam_size=10,
        patience=2,
        repetition_penalty=1.4,
        condition_on_previous_text=False,
        no_speech_threshold=0.275,
        log_prob_threshold=-1,
        compression_ratio_threshold=1.75,
        word_timestamps=True,
        vad_filter=True,
        clip_timestamps=clip_timestamps,
    )

    for segment in segments:
        start_ts = format_timestamp(segment.start)
        end_ts = format_timestamp(segment.end)
        print(f"[{start_ts} -> {end_ts}] {segment.text}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files with Whisper")
    parser.add_argument("audio", type=str, help="audio file to transcribe")
    parser.add_argument("timestamps", type=str, help="timestamps file")
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="device to use, cuda or cpu",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="large-v2",
        help="model type (e.g. large-v2, large-v3, ...)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="ja",
        help="force language (e.g. 'ja' for Japanese, 'it' for Italian)",
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()

    whispers(
        args.audio,
        args.timestamps,
        device=args.device,
        model=args.model,
        language=args.language,
    )


if __name__ == "__main__":
    main()
