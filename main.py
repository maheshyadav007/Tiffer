import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import create_mask

print("begin")
# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
print("selecting image")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
print("after selecting image")
realtime_update = st.sidebar.checkbox("Update in realtime", True)


if bg_image:
    image = Image.open(bg_image)
    width, height = image.size
    width = int(width/2)
    height = int(height/2)
else:
    width, height = 512, 512
print(width, height)
# Create a canvas component



canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=height,
    width = width,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)
# print('after imgae selection')
# Do something interesting with the image data and paths
# if canvas_result.image_data is not None:
#     st.image(canvas_result.image_data, width = width)
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)

print(objects.columns)

mask_origin_x = float(objects.left)
mask_origin_y = float(objects.top)
mask_width = float(objects.width)
mask_height = float(objects.height)
mask_angle = float(objects.angle)
mask_scale_x = float(objects.scaleX)
mask_scale_y = float(objects.scaleY)
mask_width = mask_width * mask_scale_x
mask_height = mask_height * mask_scale_y
print(mask_origin_x, mask_origin_y, mask_width, mask_height, mask_angle)



# Example usage
origin_x = mask_origin_x
origin_y = mask_origin_y
mask_height = mask_height
mask_width = mask_width
mask_angle = mask_angle

mask = create_mask(height, width, origin_x, origin_y, mask_height, mask_width, mask_angle)

# Display the mask
# st.image(mask, caption='Mask Image', width=width)
# print(mask)

from diffusers import StableDiffusionInpaintPipeline
import torch
import time


text_input = st.text_input("Prompt to modify your image...")


# Function to perform a specific task
def perform_task():
    # Perform your specific task here
    # st.write("Task Completed!")
    st.session_state.task_in_progress = True

    # st.write("Button clicked with text:", text_input)
    # .button("Running...", key = run_button_key)
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-inpainting",
        torch_dtype=torch.float16,
    )
    pipe.to("mps")
    prompt = text_input
    #image and mask_image should be PIL images.
    #The mask structure is white for inpainting and black for keeping as is
    start = time.time()
    output_image = pipe(prompt=prompt, image=image, mask_image=mask).images[0]
    end = time.time()

    image.save("./yellow_cat_on_park_bench.png")
    st.image(output_image, width=width, caption=f"Inpaint Output. Time taken: {end-start:.2f} seconds")
    st.session_state.task_in_progress = False
    st.session_state.task_completed = True



if 'task_in_progress' not in st.session_state:
    st.session_state.task_in_progress = False

if 'task_completed' not in st.session_state:
    st.session_state.task_completed = False

if st.button("Run Inpainting"):
    perform_task()

if st.session_state.task_in_progress:
    st.button("Running...")
# elif st.session_state.task_completed:
#     st.button("Run", disabled=False)
# else:
#     st.button("Run")