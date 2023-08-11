import os
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw


# Disable Tensorflow debugging info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class HandwrittenDigitRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Digit Recognition App AI | by Ilija")
        self.root.iconbitmap("assets/icons/hdra_icon.ico")
        self.root.resizable(False, False)
        self.left_column, self.right_column = self.layout()
        self.canvas, self.submit_button, self.clear_button, self.prediction_label, self.prediction_result_label,\
            self.confidence_label, self.confidence_result_label = self.widgets(self.left_column, self.right_column)

        # Bind the mouse events that perform specific actions on canvas object
        self.canvas.bind("<Button-1>", self.initiate_draw_state)  # commence drawing on click (left mouse button)
        self.canvas.bind("<B1-Motion>", self.draw)  # move mouse or finger on touchpad to control draw direction
        self.canvas.bind("<Enter>", lambda event: self.canvas.config(cursor="pencil"))  # pencil cursor on canvas hover
        self.canvas.bind("<Leave>", lambda event: self.canvas.config(cursor="arrow"))  # arrow cursor otherwise

        # Initialize variables
        self.is_drawing = False  # flag indicating App is in non-drawing state by default
        self.last_x, self.last_y = None, None

        # Initialize Keras model (name:HandWrittenDigitClassifier)
        self.model = tf.keras.models.load_model("assets/models/HWDigitsClassifier.keras")

    def layout(self):
        # Main Frame (overarching container of all app widgets)
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0)

        # Left Column (contains drawing canvas)
        left_column = tk.Frame(frame)
        left_column.grid(row=0, column=1)

        # Separator (separates the left canvas column from the right interactive column)
        separator = ttk.Separator(frame, orient=tk.VERTICAL)
        separator.grid(row=0, column=2, sticky="ns", padx=2, pady=2)

        # Right Column (contains buttons & display)
        right_column = tk.Frame(frame, height=472, width=180)
        right_column.grid(row=0, column=3, sticky="n")

        return left_column, right_column

    def widgets(self, left_clmn, right_clmn):
        # Drawing Canvas
        canvas = tk.Canvas(left_clmn, width=450, height=476, bg='black')
        canvas.grid(row=0, column=1)

        # Submit Button
        submit_button = tk.Button(right_clmn, text='Submit', width=18, height=2,
                                  justify="center", cursor="hand2", font=("Verdana", 12, "bold"),
                                  command=self.generate_prediction)
        submit_button.grid(row=0, column=3, padx=5, pady=5, sticky="n")

        # Clear Button
        clear_button = tk.Button(right_clmn, text='Clear', width=18, height=2,
                                 justify="center", cursor="hand2", font=("Verdana", 12, "bold"),
                                 command=self.clear_canvas)
        clear_button.grid(row=1, column=3, padx=5)

        # Display Prediction
        prediction_label = tk.Label(right_clmn, text="", font=("Verdana", 16, "bold"))
        prediction_result_label = tk.Label(right_clmn, text="", font=("Verdana", 64, "bold"))
        prediction_label.grid(row=2, column=3, padx=5)
        prediction_result_label.grid(row=3, column=3, padx=5)

        # Display Confidence
        confidence_label = tk.Label(right_clmn, text="", font=("Verdana", 16, "bold"))
        confidence_result_label = tk.Label(right_clmn, text="", font=("Verdana", 20, "bold"))
        confidence_label.grid(row=4, column=3, padx=5)
        confidence_result_label.grid(row=5, column=3, padx=5)

        return canvas, submit_button, clear_button,\
            prediction_label, prediction_result_label, confidence_label, confidence_result_label

    def get_canvas_coords(self, x, y):
        # Prevent drawing off canvas area
        canvas_width = self.canvas.winfo_width()  # get canvas width dimension
        canvas_height = self.canvas.winfo_height()  # get canvas height dimension

        x = min(max(x, 0) + 8, canvas_width - 8)  # ensure x-coordinate is within the canvas boundaries
        y = min(max(y, 0) + 8, canvas_height - 8)  # ensure y-coordinate is within the canvas boundaries

        return x, y

    def initiate_draw_state(self, event):
        # Upon clicking left mouse button ("<Button-1>") run this function code
        self.is_drawing = True  # set is_drawing flag to True, indicating App is in drawing state
        # Get mouse x & y position via event bind and save each coordinate last position into their seperate variables
        self.last_x, self.last_y = self.get_canvas_coords(event.x, event.y)
        self.draw(event)

    def draw(self, event):
        # When App draw state is initialized (is_drawing = True)
        if self.is_drawing:
            # Track + save mouse x & y coordinates on canvas via event
            x, y = self.get_canvas_coords(event.x, event.y)
            # If last_x & last_y have values (hold the previous coordinates of the mouse pointer on the canvas)
            if self.last_x is not None and self.last_y is not None:
                # Indicates user moved the mouse after clicking the left mouse button (proceed to create/draw line)
                self.canvas.create_line(self.last_x, self.last_y, x, y,
                                        fill='white', width=16, capstyle=tk.ROUND, joinstyle=tk.ROUND,
                                        smooth=True)

            # Save each coordinate last position into their seperate variables
            self.last_x, self.last_y = x, y

    def capture_canvas_content(self):
        # Create a new PIL Image
        img = Image.new("L", (self.canvas.winfo_width(), self.canvas.winfo_height()), color=0)

        # Create an ImageDraw object
        image_draw = ImageDraw.Draw(img)

        # Draw the canvas content onto the PIL Image
        for i in self.canvas.find_all():
            coords_tuple = (i,)
            coords = self.canvas.coords(coords_tuple)
            if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                x1, y1 = self.get_canvas_coords(coords[0], coords[1])
                x2, y2 = self.get_canvas_coords(coords[2], coords[3])
                image_draw.line((x1, y1, x2, y2), fill='white', width=16)

        return img

    def generate_prediction(self):
        img = self.capture_canvas_content()
        img = img.resize((28, 28))

        # OPTIONAL #1: Uncomment to view canvas capture image (pre-array, pre-normalization & pre-reshape) w/ matplot
        # import matplotlib.pyplot as plt
        # plt.imshow(img, cmap='gray')
        # plt.show()

        # OPTIONAL #2: Uncomment to save canvas capture image as png
        # img.save("canvas_content.png")

        # Process image to fit model and improve efficiency
        img_array = np.array(img)  # turn img into ndarray object
        img_array = img_array / 255.0  # normalize to from [0, 255] to [0, 1]
        img_array = img_array.reshape(1, 28, 28, 1)  # reshape to match Keras model input

        # Get model prediction and confidence
        predict_image = self.model.predict(img_array)
        prediction = np.argmax(predict_image[0])
        confidence = np.max(predict_image[0]) * 100

        # Configure model results into labels for display purposes
        self.prediction_label.configure(text="\nAI model\n identified digit:\n")
        self.prediction_result_label.configure(text=str(prediction), fg="blue")
        self.confidence_label.configure(text="\n\nConfidence level:")
        self.confidence_result_label.configure(text="{:.2f}%".format(confidence))

    def clear_canvas(self):
        self.canvas.delete("all")


if __name__ == "__main__":
    app = tk.Tk()
    hdra = HandwrittenDigitRecognitionApp(app)
    app.mainloop()
