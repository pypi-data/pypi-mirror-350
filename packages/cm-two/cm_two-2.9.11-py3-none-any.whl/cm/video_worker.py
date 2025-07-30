from __future__ import print_function

import time
import uuid
from imutils.video import VideoStream
from PIL import Image, ImageDraw
from PIL import ImageTk
import tkinter as tki
import threading
import imutils
import cv2


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)),
                (w - rad, h - rad))
    im.putalpha(alpha)
    return im


class PhotoBoothApp:
    def __init__(self, url, outputPath, root, canvas,
                 width=300, height=300,
                 pos_x=500, pos_y=500, zoomed_x=1000, zoomed_y=1000,
                 zoomed_video_width=1000, zoomed_video_height=700,
                 root_zoom_callback_func=None,
                 root_hide_callback_func=None,
                 cam_type=None):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.url = url
        self.vs = VideoStream(url).start()
        self.zoomed = False
        self.cam_type = cam_type
        self.zoomed_video_width = zoomed_video_width
        self.zoomed_video_height = zoomed_video_height
        self.outputPath = outputPath
        self.root_zoom_callback_func = root_zoom_callback_func
        self.root_hide_callback_funct = root_hide_callback_func
        self.frame = None
        self.can_show = False
        self.can_zoom = True
        self.thread = None
        self.stopEvent = None
        self.zoomed_x = zoomed_x
        self.zoomed_y = zoomed_y
        # initialize the root window and image panel
        self.root = root
        self.init_x, self.init_y = pos_x, pos_y
        self.place_x, self.place_y = pos_x, pos_y
        self.init_video_width, self.init_video_height = width, height
        self.video_width, self.video_height = width, height
        self.panel = None
        self.image_id = None
        self.canvas = canvas
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=(), daemon=True)
        self.thread.start()
        #self.root.after(100, self.videoLoop)
        # set a callback to handle when the window is closed
        # self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        reconnect_interval = 5  # секунд
        last_reconnect_attempt = 0

        while True:
            if self.stopEvent.is_set():
                return

            try:
                if not self.can_show:
                    if self.image_id is not None:
                        self.canvas.delete(self.image_id)
                        self.image_id = None
                    time.sleep(0.1)
                    continue

                # 👇 Проверяем внутренний VideoCapture
                if not self.vs.stream.isOpened():
                    now = time.time()
                    if now - last_reconnect_attempt > reconnect_interval:
                        print(f"[{self.cam_type}] Камера недоступна, переподключение...")
                        self.vs.stream.release()
                        self.vs.stream = cv2.VideoCapture(self.url)
                        last_reconnect_attempt = now
                    time.sleep(1)
                    continue

                frame = self.vs.read()
                if frame is None:
                    print(f"[{self.cam_type}] Пустой кадр, ждём...")
                    time.sleep(1)
                    continue

                frame = cv2.resize(frame, (self.video_width, self.video_height))
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                tk_image = ImageTk.PhotoImage(image)

                if not hasattr(self, 'image_id') or self.image_id is None:
                    self.image_id = self.canvas.create_image(
                        self.place_x, self.place_y, image=tk_image)
                    self.canvas.tag_raise(self.image_id)
                    self.canvas.tag_bind(self.image_id, '<Button-1>', self.img_callback)
                else:
                    self.canvas.itemconfig(self.image_id, image=tk_image)
                    self.canvas.tag_raise(self.image_id)
                    self.canvas.coords(self.image_id, self.place_x, self.place_y)

                self.tk_image = tk_image

            except Exception as e:
                print(f"[{self.cam_type}] [videoLoop error]", e)
                time.sleep(1)

            time.sleep(0.05)

    def videoLoopOld(self):
        while True:
            if self.stopEvent.is_set():
                return

            try:
                if not self.can_show:
                    if self.image_id is not None:
                        self.canvas.delete(self.image_id)
                        self.image_id = None
                    time.sleep(0.1)
                    continue
                    #self.root.after(33, self.videoLoop)
                    #return

                if not self.vs.isOpened():
                    print(f"[{self.cam_type}] Camera not opened")
                    time.sleep(2)
                    continue

                # Чтение и обработка кадра
                frame = self.vs.read()
                frame = imutils.resize(frame,
                                       width=self.video_width,
                                       height=self.video_height)

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                tk_image = ImageTk.PhotoImage(image)

                # Создание image_id, если его ещё нет
                if not hasattr(self, 'image_id') or self.image_id is None:
                    self.image_id = self.canvas.create_image(
                        self.place_x, self.place_y, image=tk_image)
                    self.canvas.tag_raise(self.image_id)
                    self.canvas.tag_bind(self.image_id, '<Button-1>', self.img_callback)
                else:
                    self.canvas.itemconfig(self.image_id, image=tk_image)
                    self.canvas.tag_raise(self.image_id)
                    self.canvas.coords(self.image_id, self.place_x, self.place_y)  # переместить изображение!
                    #self.canvas.itemconfig(self.image_id, lev)
                # Храним изображение, чтобы оно не исчезло
                self.tk_image = tk_image

            except Exception as e:
                print("[videoLoop error]", e)

            #self.root.after(100, self.videoLoop)
            time.sleep(0.05)
        #self.root.after(100, self.videoLoop)

    def hide_callback(self, root_calback=True):
        self.video_width = self.init_video_width
        self.video_height = self.init_video_height
        self.place_x = self.init_x
        self.place_y = self.init_y
        self.can_show = True
        if self.root_hide_callback_funct and root_calback:
            self.root_hide_callback_funct(self.cam_type)
            self.zoomed = False

    def set_new_params(self, x=None, y=None, width=None, height=None):
        if width:
            self.video_width = width
        if height:
            self.video_height = height
        if x:
            self.place_x = x
        if y:
            self.place_y = y
        #if hasattr(self, 'image_id') and self.image_id is not None:
            #self.canvas.coords(self.image_id, self.place_x, self.place_y)
            #self.can_show = True
            #self.canvas.tag_raise(self.image_id)

    def zoom_callback(self, root_calback=True):
        self.video_width = self.zoomed_video_width
        self.video_height = self.zoomed_video_height
        self.place_x = self.zoomed_x
        self.place_y = self.zoomed_y
        self.can_show = True
        if self.root_zoom_callback_func and root_calback:
            self.root_zoom_callback_func(self.cam_type)
        self.zoomed = True

    def img_callback(self, *args):
        if not self.can_zoom:
            return
        self.can_show = False
        if self.zoomed:
            self.hide_callback()
        else:
            self.zoom_callback()

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

    def stop_video(self):
        self.can_show = False

    def play_video(self):
        self.can_show = True

def start_video_stream(root, canvas, xpos, ypos, v_width, v_height,
                       cam_login, cam_pass, cam_ip, zoomed_x, zoomed_y,
                       zoomed_video_width, zoomed_video_height,
                       cam_type=None,
                       cam_port=554,
                       zoom_callback_func=None, hide_callback_func=None):
    url = f"rtsp://{cam_login}:{cam_pass}@{cam_ip}:{cam_port}/Streaming/Channels/102"

    inst = PhotoBoothApp(url, "output", root=root, canvas=canvas, width=v_width,
                         height=v_height, pos_x=xpos, pos_y=ypos,
                         zoomed_x=zoomed_x,
                         zoomed_y=zoomed_y,
                         root_zoom_callback_func=zoom_callback_func,
                         root_hide_callback_func=hide_callback_func,
                         cam_type=cam_type,
                         zoomed_video_width=zoomed_video_width,
                         zoomed_video_height=zoomed_video_height)
    return inst

