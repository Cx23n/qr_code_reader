import tkinter as tk

import cv2
from tkinterdnd2 import DND_FILES, TkinterDnD


def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def process_image(file_path):
    if file_path:
        img = cv2.imread(file_path)
        detector = cv2.QRCodeDetector()
        retval, decoded_info, pts, straight_qrcode = detector.detectAndDecodeMulti(img)

        if retval:
            result_label.config(text=f"{decoded_info[0] if decoded_info else ''}")
        else:
            result_label.config(text="No QR Code found in the image")


def on_drop(event):
    file_path = event.data
    process_image(file_path)


def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)


def copy_text():
    text = result_label.cget("text")
    copy_to_clipboard(text)


# Create the main window
root = TkinterDnD.Tk()
root.title("QR Code Reader")

# Set the initial dimensions of the window (width x height)
root.geometry("800x600")

# Create a label to display the result with wrapping
result_label = tk.Label(root, text="Drop an image into this window", font=("Arial", 12), wraplength=700,
                        justify="center")
result_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Center both horizontally and vertically

# Enable drag and drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Configure grid weights to allow centering
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=copy_text)

# Bind right-click event to show context menu
result_label.bind("<Button-3>", show_context_menu)

# Start the main event loop
root.mainloop()
