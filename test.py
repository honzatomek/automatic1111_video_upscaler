import webuiapi
from PIL import Image

# Open the image file
image = Image.open("temp_frames/frame0001.jpg")
image2 = Image.open("temp_frames/frame0002.jpg")

# create API client with custom host, port
api = webuiapi.WebUIApi(host='192.168.50.210', port=7860)

result4 = api.extra_batch_images(images=[image, image2],
                                 upscaler_1=webuiapi.Upscaler.ESRGAN_4x,
                                 upscaling_resize_w=1920, upscaling_resize_h=1080)

    
result4.images[0].save("output_image.jpg")
result4.images[1].save("output_image2.jpg")