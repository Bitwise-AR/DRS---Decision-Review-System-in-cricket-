import tkinter as tk
import cv2
from PIL import Image, ImageTk
from functools import partial
import threading
import time

video_stream = cv2.VideoCapture("clip.mp4")
toggle_flag = True

def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def play_video(play_speed):
    global toggle_flag
    print(f"You clicked on play. Speed is {play_speed}")

    # Play the video in reverse mode
    current_frame = video_stream.get(cv2.CAP_PROP_POS_FRAMES)
    video_stream.set(cv2.CAP_PROP_POS_FRAMES, current_frame + play_speed)

    frame_grabbed, video_frame = video_stream.read()
    if not frame_grabbed:
        exit()
    video_frame = resize_with_aspect_ratio(video_frame, width=FRAME_WIDTH)
    video_frame = ImageTk.PhotoImage(image=Image.fromarray(video_frame))
    display_canvas.image = video_frame
    display_canvas.create_image(0, 0, image=video_frame, anchor=tk.NW)
    if toggle_flag:
        display_canvas.create_text(
            134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    toggle_flag = not toggle_flag


def show_pending(decision):
    # 1. Display decision pending image
    pending_frame = cv2.cvtColor(cv2.imread("images/decision-pending-cricket.png"), cv2.COLOR_BGR2RGB)
    pending_frame = resize_with_aspect_ratio(pending_frame, width=FRAME_WIDTH)
    pending_frame = ImageTk.PhotoImage(image=Image.fromarray(pending_frame))
    display_canvas.image = pending_frame
    display_canvas.create_image(0, 0, image=pending_frame, anchor=tk.NW)
    # 2. Wait for 1.5 seconds
    time.sleep(1.5)

    # 3. Display sponsor image
    sponsor_frame = cv2.cvtColor(cv2.imread("images/icc.png"), cv2.COLOR_BGR2RGB)
    sponsor_frame = resize_with_aspect_ratio(sponsor_frame, width=FRAME_WIDTH)
    sponsor_frame = ImageTk.PhotoImage(image=Image.fromarray(sponsor_frame))
    display_canvas.image = sponsor_frame
    display_canvas.create_image(0, 0, image=sponsor_frame, anchor=tk.NW)

    # 4. Wait for 2.5 seconds
    time.sleep(2.5)
    # 5. Display out/not out image
    if decision == 'out':
        decision_image = "images/out.png"
    else:
        decision_image = "images/not_out.png"
    decision_frame = cv2.cvtColor(cv2.imread(decision_image), cv2.COLOR_BGR2RGB)
    decision_frame = resize_with_aspect_ratio(decision_frame, width=FRAME_WIDTH)
    decision_frame = ImageTk.PhotoImage(image=Image.fromarray(decision_frame))
    display_canvas.image = decision_frame
    display_canvas.create_image(0, 0, image=decision_frame, anchor=tk.NW)


def give_out():
    thread = threading.Thread(target=show_pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def give_not_out():
    thread = threading.Thread(target=show_pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


# Width and height of our main screen
FRAME_WIDTH = 1050
FRAME_HEIGHT = 550

# Tkinter GUI starts here
main_window = tk.Tk()
main_window.title("Third Umpire Decision Review Kit")

# Configure grid layout
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)
main_window.rowconfigure(1, weight=0)

# Set background image
background_img = cv2.cvtColor(cv2.imread("images/background.jpg"), cv2.COLOR_BGR2RGB)
background_photo = ImageTk.PhotoImage(image=Image.fromarray(background_img))

background_label = tk.Label(main_window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Canvas for video playback
display_canvas = tk.Canvas(main_window, width=FRAME_WIDTH, height=FRAME_HEIGHT)
display_canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Load initial image
initial_img = cv2.cvtColor(cv2.imread("images/welcome.jpg"), cv2.COLOR_BGR2RGB)
initial_photo = ImageTk.PhotoImage(image=Image.fromarray(initial_img))
display_canvas.create_image(0, 0, anchor=tk.NW, image=initial_photo)

# Styling for buttons
button_style = {
    'width': 20,
    'padx': 10,
    'pady': 5,
    'bg': '#1f1f1f',
    'fg': '#ffffff',
    'font': ('Arial', 12, 'bold'),
    'relief': 'raised',
    'bd': 3
}


def on_enter(e):
    e.widget['background'] = '#3e3e3e'


def on_leave(e):
    e.widget['background'] = '#1f1f1f'


# Buttons to control playback
btn_rewind_fast = tk.Button(main_window, text="<< Rewind (fast)", command=partial(
    play_video, -25), **button_style)
btn_rewind_fast.grid(row=1, column=0, sticky='ew')
btn_rewind_fast.bind("<Enter>", on_enter)
btn_rewind_fast.bind("<Leave>", on_leave)

btn_rewind_slow = tk.Button(main_window, text="<< Rewind (slow)", command=partial(
    play_video, -2), **button_style)
btn_rewind_slow.grid(row=1, column=1, sticky='ew')
btn_rewind_slow.bind("<Enter>", on_enter)
btn_rewind_slow.bind("<Leave>", on_leave)

btn_forward_slow = tk.Button(main_window, text="Forward (slow) >>", command=partial(
    play_video, 2), **button_style)
btn_forward_slow.grid(row=1, column=2, sticky='ew')
btn_forward_slow.bind("<Enter>", on_enter)
btn_forward_slow.bind("<Leave>", on_leave)

btn_forward_fast = tk.Button(main_window, text="Forward (fast) >>", command=partial(
    play_video, 25), **button_style)
btn_forward_fast.grid(row=1, column=3, sticky='ew')
btn_forward_fast.bind("<Enter>", on_enter)
btn_forward_fast.bind("<Leave>", on_leave)

btn_out = tk.Button(main_window, text="Give Out",
                    command=give_out, **button_style)
btn_out.grid(row=2, column=0, columnspan=2, sticky='ew')
btn_out.bind("<Enter>", on_enter)
btn_out.bind("<Leave>", on_leave)

btn_not_out = tk.Button(main_window, text="Give Not Out",
                        command=give_not_out, **button_style)
btn_not_out.grid(row=2, column=2, columnspan=2, sticky='ew')
btn_not_out.bind("<Enter>", on_enter)
btn_not_out.bind("<Leave>", on_leave)

main_window.mainloop()
