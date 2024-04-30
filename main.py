import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import shutil

from utils import create_mask, run_inpaint_pipeline

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
realtime_update = st.sidebar.checkbox("Update in realtime", True)


if bg_image:
    print("bg_image is not None")
    image = Image.open(bg_image)
    width, height = image.size
    width = int(width/2)
    height = int(height/2)
    original_image_path = "./temp/original_image.png"
    temp_image_path = "./temp/temp_image.png"
    image.save(original_image_path)
    shutil.copyfile(original_image_path, temp_image_path)
    temp_image = Image.open(temp_image_path)


else:
    width, height = 512, 512
print(width, height)
# Create a canvas component



canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=temp_image if bg_image else None,
    update_streamlit=realtime_update,
    height=height,
    width = width,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)
print(type(canvas_result))
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
print(objects.left)
mask_origin_x = objects.left.values[-1]
mask_origin_y = objects.top.values[-1]
mask_width = objects.width.values[-1]
mask_height = objects.height.values[-1]
mask_angle = objects.angle.values[-1]
mask_scale_x = objects.scaleX.values[-1]
mask_scale_y = objects.scaleY.values[-1]
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


text_input = st.text_input("Prompt to modify your image...")


if 'task_in_progress' not in st.session_state:
    st.session_state.task_in_progress = False

if 'task_completed' not in st.session_state:
    st.session_state.task_completed = False

if st.button("Run Inpainting"):
    st.session_state.task_in_progress = True
    start = time.time()
    output_image = run_inpaint_pipeline(prompt=text_input, image=temp_image, mask=mask)
    end = time.time()   
    
    st.image(output_image, width=width, caption=f"Inpaint Output. Time taken: {end-start:.2f} seconds")
    st.session_state.output_image = output_image
    st.session_state.task_in_progress = False
    st.session_state.task_completed = True
if st.button("Save"):
    st.session_state.output_image.save(temp_image_path)
    del st.session_state.output_image

if st.session_state.task_in_progress:
    st.button("Running...")
# elif st.session_state.task_completed:
#     st.button("Run", disabled=False)
# else:
#     st.button("Run")