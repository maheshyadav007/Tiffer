# from PIL import Image

# # Load images
# background = Image.open("yellow_background.png")  # Assuming a solid yellow background
# mango_slices = Image.open("mango_slices.png")  # Transparent background
# mango_drink = Image.open("mango_drink.png")  # Transparent background





# # Resize images if necessary
# # A4 at 300 DPI: 2480 x 3508 pixels
# width, height = 1024, 1024

# background = background.resize((height, width))
# # Assuming mango_drink and mango_slices are appropriately sized, otherwise resize them similarly

# # Create a new image for the final output
# final_image = Image.new("RGBA", (height, width))

# # Paste the background
# final_image.paste(background, (0, 0))

# # Position and paste the mango drink image
# # Calculate positions: slightly off-center and towards the bottom
# drink_x = (width - mango_drink.width) // 2 + 100  # slight shift to the right
# drink_y = height - mango_drink.height - 200  # slight raise from the bottom
# final_image.paste(mango_drink, (drink_x, drink_y), mango_drink)

# # Position and paste the mango slices
# # Example position: flying out from the drink
# slice_x = drink_x + 150  # Starting right of the drink
# slice_y = drink_y - mango_slices.height // 2  # Starting from the middle of the drink height
# final_image.paste(mango_slices, (slice_x, slice_y), mango_slices)

# # Save the final image
# final_image.save("mango_drink_poster.png")

# print("Poster created successfully!")

from PIL import Image

# Load images
background = Image.open("yellow_background.png")  # Assuming a solid yellow background
mango_slices = Image.open("mango_slices.png")  # Transparent background
mango_drink = Image.open("mango_drink.png")  # Transparent background

height, width = 1024, 1024
# Resize images if necessary
# A4 at 300 DPI: 2480 x 3508 pixels
background = background.resize((height, width))
# Assuming mango_drink and mango_slices are appropriately sized, otherwise resize them similarly

# Create a new image for the final output
final_image = Image.new("RGBA", (height, width))

# Paste the background
final_image.paste(background, (0, 0))

# Position and paste the mango drink image
# Calculate positions: slightly off-center and towards the bottom
drink_x = (width - mango_drink.width) // 2 + 100  # slight shift to the right
drink_y = height - mango_drink.height - 200  # slight raise from the bottom
final_image.paste(mango_drink, (drink_x, drink_y), mango_drink)

# Position and paste the mango slices at the bottom of the canvas
# Example position: starting at the bottom and possibly overlapping slightly with the drink
slice_x = (width - mango_slices.width) // 2  # Centering the slices horizontally
slice_y = height - mango_slices.height - 100  # Near the bottom, slightly raised to avoid the edge
final_image.paste(mango_slices, (slice_x, slice_y), mango_slices)

# Save the final image
final_image.save("mango_drink_poster.png")

print("Poster created successfully!")