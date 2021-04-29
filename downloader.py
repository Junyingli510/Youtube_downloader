from youtube_transcript_api import YouTubeTranscriptApi
import json
import os, sys


def convert_ts_hms(ts):
    h = int(ts / 3600)
    m = int((ts % 3600) / 60)
    s = round(ts % 60, 3)

    return [h, m, s]


def convert_ts_str(h, m, s):
    s_str = "{:05d}".format(int(s * 1000))
    ts_str = "{:02d}:{:02d}:".format(h, m) + s_str[:2] + "," + s_str[2:]
    return ts_str


def create_srt_from_info(video_info):
    video_id, title = video_info.split("\t")
    video_id = video_id.replace("https://www.youtube.com/watch?v=", "")

    save_dir = os.path.join(os.getcwd(), "result")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    srt_fname = os.path.join(save_dir, f"{title}.srt")

    if os.path.exists(srt_fname):
        print("\tAlready exists")
        return

    try:
        rows = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print("\tNo Script.")
        return

    full_rows = []
    for i, row in enumerate(rows):
        dur = row['duration']
        st = row['start']
        [h1, m1, s1] = convert_ts_hms(st)
        ts_str1 = convert_ts_str(h1, m1, s1)

        [h2, m2, s2] = convert_ts_hms(st + dur)
        ts_str2 = convert_ts_str(h2, m2, s2)

        txt = row['text']

        row_str = [str(i + 1), " --> ".join([ts_str1, ts_str2]), txt]

        full_rows.append("\n".join(row_str))

    with open(srt_fname, "w+") as fp:
        fp.write("\n\n".join(full_rows))
        fp.flush()

    print("\tDone.")


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 2:
        raise ValueError('Please provide the file name of youtube ids.')

    url_script_name = sys.argv[1]

    # id_rows = open("Season1.txt", "r").read().splitlines()
    rows = open(url_script_name, "r").read().splitlines()

    for i, row in enumerate(rows):
        # video_id = "mpFLlzVhr9c"
        print(f"{i}.{row} is processing")
        create_srt_from_info(row)
