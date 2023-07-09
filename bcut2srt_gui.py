import sys
import json
from time import strftime, gmtime

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QFileDialog
from PyQt5.QtCore import pyqtSignal


class MyWindow(QWidget):

    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.trans_text = list()  # 用于存放解析出的srt数据

    def init_ui(self):
        self.setWindowTitle("Bcut2srt by Rainene V1.0")
        self.resize(600, 400)

        container = QVBoxLayout()

        content_layout = QVBoxLayout()

        self.label = QLabel("")
        self.label.resize(560, 17)
        self.label.setStyleSheet("font-size:15px;color:black")

        scroll = QScrollArea()
        scroll.setWidget(self.label)

        content_layout.addWidget(scroll)

        btns_layout = QHBoxLayout()
        
        btn_open = QPushButton("打开文件")
        btn_tran = QPushButton("转换str")
        btn_save = QPushButton("保存文本")
        btn_copy = QPushButton("复制文本")
        btn_clear = QPushButton("清屏")

        
        btns_layout.addStretch(2)
        btns_layout.addWidget(btn_open)
        btns_layout.addStretch(1)
        btns_layout.addWidget(btn_tran)
        btns_layout.addStretch(1)
        btns_layout.addWidget(btn_save)
        btns_layout.addStretch(1)
        btns_layout.addWidget(btn_copy)
        btns_layout.addStretch(1)
        btns_layout.addWidget(btn_clear)
        btns_layout.addStretch(2)

        btn_open.clicked.connect(self.open_file)
        btn_tran.clicked.connect(self.bcut2srt)
        btn_save.clicked.connect(self.save_file)
        btn_copy.clicked.connect(self.copy_text)
        btn_clear.clicked.connect(self.clear_screen)

        # 绑定自定义信号与槽
        self.my_signal.connect(self.my_slot)

        container.addLayout(content_layout)
        container.addLayout(btns_layout)

        self.setLayout(container)

    # 打开文件槽函数
    def open_file(self):
        self.fname, ftype = QFileDialog.getOpenFileName(self, "打开文件", "C:\\", "Json File(*.json);;All Files(*)")  # 返回的fname是一个URL

    # 转换bcut的json文件为srt文件的槽函数
    def bcut2srt(self):

        with open(self.fname, encoding="utf-8") as f:
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
                        # print(clip["AssetInfo"]["content"] + "\n")
                        # 更新字幕内容至label控件
                        sub = clip["AssetInfo"]["content"]

                        msg = "\n".join([num, clip_time, sub, "\n"])
                        self.my_signal.emit(msg)

    # 自定义槽函数，用于传递被解析bcut的json数据
    def my_slot(self, msg):
        # print(">>>", msg)
        self.trans_text.append(msg)
        self.label.setText("".join(self.trans_text))  # 列表元素中间用<br>连接成一个字符串，即支持HTML5的语法
        # print(self.label.frameSize().height())
        self.label.resize(560, self.label.frameSize().height() + 68)  # 这里是手动更新QLabel的尺寸
        self.label.repaint()  # 更新内容，如果不更新可能是没有显示新内容

    # 保存文件槽函数
    def save_file(self):
        fname_save, ftype_save = QFileDialog.getSaveFileName(self, "保存文件", "C:\\", "SubRip Text(*.srt);;All Files(*)")  # 返回的fname_save是一个URL
        with open(fname_save, mode="w",encoding="utf-8") as f:
            f.write("".join(self.trans_text))

    # 复制srt文本槽函数
    def copy_text(self):
        self.clipboard = QApplication.clipboard()
        self.clipboard.setText(self.label.text())

    def clear_screen(self):
        self.label.resize(560, 17)
        self.label.setText("")
        self.trans_text.clear()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())