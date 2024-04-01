import requests
import base64
import json


# Function to convert an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def upscale_img(image_path, output_path, width, height):
    # Your image path here

    # Convert image to base64
    base64_image = image_to_base64(image_path)


    # base64_image = "data:image/png;base64," + base64_image
    # print(base64_image)

    # API URL
    url = "http://192.168.50.210:7860/sdapi/v1/img2img"

    # Prepare the headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # Prepare the data
    data = {
        "init_images": [base64_image],
        "cfg_scale": 5,
        "steps": 26,
        "width": width,
        "height": height,
        "sampler_index": "DPM++ 2M Karras",
        "model": "juggernaut-xl",
        "denoising_strength": 0.01,
    }

    # Make the request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful.")

        #print(response.text)
        base64_image_data = response.json()["images"][0]

        # Decode the base64 string
        image_data = base64.b64decode(base64_image_data)

        # Write the image data to a file
        with open(output_path, "wb") as file:
            file.write(image_data)
    else:
        print("Request failed with status code:", response.status_code)
        print("Error:", response.text)
        return False
