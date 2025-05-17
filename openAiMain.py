import json
import os
import requests
from openai import OpenAI
from icecream import ic
import datetime
from pprint import pprint as pp

client = OpenAI()

folder_name = "examples"
file_name = "diff_styles"
style_name = "Cartoon_Realism"
amount_of_pictures = 1

full_folder_path = os.path.join(folder_name, file_name)

if not os.path.exists(full_folder_path):
    os.makedirs(full_folder_path)

def generate_image(picture_prompt):
    global response
    print("\tGenerating image ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=picture_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    # downloads the image to a file
    bin_picture = requests.get(image_url)
    return bin_picture.content


def save_picture(file_name, picture):
    print("\t\tsaving image ...")
    file = open(file_name, "wb")
    file.write(picture)
    file.close()




# if not os.path.exists(file_name):
#     os.mkdir(file_name)

# read prompt from file prompt.txt
with open("prompt.txt", "r") as f:
    picture_prompt = f.read()

# read json from file styles.json
with open('styles.json', 'r') as json_file:
    # Load the JSON data into a Python dictionary
    styles_map = json.load(json_file)



style_description = styles_map[style_name]["description"]
style_palette = styles_map[style_name]["palette"]
# add cartoon_style and cartoon_palette to prompt
picture_prompt = picture_prompt + "\nstyle:" + style_description + "\ncolors:" + style_palette



def gen_variants(picture_prompt, file_name, folder_name, num_of_pictures=1):
    for style_name, style_info in styles_map.items():
        print("Style Name:", style_name)
        style_description = style_info["description"]
        style_palette = style_info["palette"]
        # add cartoon_style and cartoon_palette to prompt
        picture_prompt = picture_prompt + "\nstyle:" + style_description + "\ncolors:" + style_palette

        for item in range(1, num_of_pictures+1):
            print("Iteration ", item, " of ", style_name, " style")
            try:
                # Code that may raise an exception
                # get file name with time stamp
                style_name_collapsed = style_name.replace(" ", "_")
                collapsed_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                file_name_with_path = folder_name+"/"+file_name + "/" + style_name_collapsed + "_" + file_name + "_" + collapsed_time + ".png"

                picture = generate_image(picture_prompt)
                save_picture(file_name_with_path, picture)
            except Exception as e:
                # Handle the exception if it occurs
                pp(f"style:{style_name} \nAn error occurred for item {item}: {e}")
                # Continue with the next iteration of the loop
                continue

def generate_pic_in_style(num_of_pictures, picture_prompt, file_name, folder_name,style_name=None):
    collapsed_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if style_name is not None:
        style_name = style_name
        style_description = styles_map[style_name]["description"]
        style_palette = styles_map[style_name]["palette"]
        # add cartoon_style and cartoon_palette to prompt
        picture_prompt = picture_prompt + "\nstyle:" + style_description + "\ncolors:" + style_palette
        style_name_collapsed = style_name.replace(" ", "_")
        file_name_with_path = folder_name + "/" + style_name_collapsed + "_" + file_name + "_" + collapsed_time + ".png"
    else:
        file_name_with_path = folder_name + "/" + file_name + "_" + collapsed_time + ".png"

    for i in range(1, num_of_pictures+1):
        print("Iteration ", i, " / ", num_of_pictures)
        # get file name with time stamp
        # file_name_with_path = folder_name + "/" + style_name_collapsed + "_" + file_name + "_" + collapsed_time + ".png"

        picture = generate_image(picture_prompt)

        save_picture(file_name_with_path, picture)



####  prin datetime to know when it starts

# measure timeof execution
start_time = datetime.datetime.now()
print("Start execution iteration at >>>>>>>>>>>>>>>>>", start_time)
# gen_variants(picture_prompt, file_name, folder_name)

generate_pic_in_style(amount_of_pictures, picture_prompt, file_name, full_folder_path, style_name = None)
# generate_pic_in_style(amount_of_pictures, picture_prompt, file_name, full_folder_path, style_name = style_name)
finish_time = datetime.datetime.now()
print("Start time: ", start_time)
print("Finish time: ", finish_time)
print("Total time: ", finish_time - start_time)
print("Done! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")