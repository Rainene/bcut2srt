import sys
import os
import json
from time import strftime, gmtime


def bcut2srt(fname):
    srt_contents = []
    with open(fname, encoding="utf-8") as f:
        temp_src = json.load(f)
        tracks = temp_src["tracks"]
        for track_num, track in enumerate(tracks, 1):
            clips = track["clips"]
            for clip_num, clip in enumerate(clips, 1):
    #             判断是否为字幕的内容
                if clip["AssetInfo"]["displayName"] == "字幕":
            #         srt字幕序号
                    num = str(clip_num)
            #         分离千进制毫秒
                    start_time = clip["inPoint"] // 1000
                    start_time_ms = clip["inPoint"] - start_time * 1000
                    end_time = clip["outPoint"] // 1000
                    end_time_ms = clip["outPoint"] - end_time * 1000
            #         格式化输出时:分:秒.毫秒
                    clip_time = strftime("%H:%M:%S", gmtime(start_time)) + "," + str(start_time_ms) + " --> " + strftime("%H:%M:%S", gmtime(end_time)) + "," + str(end_time_ms)
            #         字幕内容
                    sub = clip["AssetInfo"]["content"]

                    srt_content = "\n".join([num, clip_time, sub, "\n"])
                    srt_contents.append(srt_content)
    return srt_contents

if __name__ == "__main__":
    path = os.path.abspath("./")
    print("""
========================================================================================

Bcut2srt tool is developed by Rainene in 2023/07/09.
You can input a josn file created by Bcut software with caption recognition.
The output srt file format is like:
...

306
00:16:34,966 --> 00:16:37,400
第二部分就是会伤到这个电机

...

该脚本目前只会对视频轨道中采用“字幕”类型的部分进行处理并提取成所需的srt字幕格式。
获取转换后的srt字幕可以放到诸如Aegisub、shotcut等软件中进行进一步处理或直接构成外挂字幕。

特别说明：本脚本仅是为了方便视频创作者提供快速获取字幕，供个人学习使用。
========================================================================================

    """)
    fname = input("请输入所需转换文件的文件路径：\n")
    print("正在进行Bcut2srt......")
    srt_subtitles = bcut2srt(fname)
    print("Json文件转换SRT字幕格式完成！")
    with open("./subtitles.srt", "w", encoding="utf-8") as f:
        subtitles = "".join(srt_subtitles)
        f.write(subtitles)
        print("SRT字幕文件保存完成！\n文件保存在%s" % (path +"\\" + "subtitles.srt"))
        f.close()
    input("请输入回车键退出脚本...\n")
    sys.exit(0)