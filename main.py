import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import shutil

from utils import create_mask, run_inpaint_pipeline
st.set_page_config(layout="wide")  # Set the page layout to wide

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
    # print("debug 1", image.size)
    # image = image.resize((1024, 1024), resample=Image.BILINEAR)


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

col1, col2 = st.columns([.6, .4])

with col1:

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



def get_response(model, messages = None, stream = None):
    return "This is response from AI"
def display_messages():
    for message in st.session_state.messages:
        print(message)
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# with st.container(height=None):
# custom_css = """
# <style>
# /* Target the chat input box */
# div[data-baseweb="input"] input[type="text"].stTextInput {
#     padding: 1px 1px !important; /* Adjust padding as needed */
#     margin: 1px 0 !important; /* Adjust margin as needed */
# }
# </style>
# """

# # Apply custom CSS using st.markdown
# st.markdown(custom_css, unsafe_allow_html=True)
with col2:
    with st.container(height=512):

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state.messages = []
  
        display_messages()

        prompt = st.chat_input("What is up?")
        if st.button("Clear all messages"):
            st.session_state.messages = []
            st.experimental_rerun()

        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

            stream = "No Model Selected...Getting no response from AI"
            
            if st.session_state.current_chosen_model == "dalle_3":
                stream = "Getting response from Dall E 3"
            elif st.session_state.current_chosen_model == "sd_2":
                stream = "Getting response from SD 2"
            elif st.session_state.current_chosen_model == "sam":
                stream = "Getting response from SAM"

            # stream = get_response(
            #     model=st.session_state["openai_model"],
            #     # messages=[
            #     #     {"role": m["role"], "content": m["content"]}
            #     #     for m in st.session_state.messages
            #     # ],
            #     stream=True,
            # )
            # response = st.write(stream)
            # with st.chat_message("assistant"):
            #     st.markdown(stream)
            st.session_state.messages.append({"role": "assistant", "content": stream})
            st.experimental_rerun()
        model_name_placeholder_mapping = {"None": "None", "Dall E 3": "dalle_3", "SD 2": "sd_2", "SAM": "sam"}
        option = st.radio("", ["None", "Dall E 3", "SD 2", "SAM"], format_func=lambda x: x, index=0, horizontal = True, on_change = None)
        st.session_state.current_chosen_model = model_name_placeholder_mapping[option]
        if option == "None":
            st.write("You selected Option 1. Task 1 will be executed.")
            # Code for Task 1
        elif option == "Dall E 3":
            st.write("You selected Option 2. Task 2 will be executed.")
            # Code for Task 2
        elif option == "SD 2":
            st.write("You selected Option 3. Task 3 will be executed.")
            # Code for Task 3
        elif option == "SAM":
            st.write("You selected Option 4. Task 4 will be executed.")
            # Code for Task 4

        




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