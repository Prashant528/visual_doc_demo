import cv2
import numpy as np

# Define image size
width, height = 1024, 768

# Create a blank white image
image = cv2.imread('screen.png')
if image is None:
    raise FileNotFoundError("Background image not found. Please check the file path.")
# Resize the image to the given window size
width, height = 1024, 768
image = cv2.resize(image, (width, height))

# Define circle parameters
center_coordinates = (804, 737)  # Given coordinates
radius = 30  # You can adjust this size as needed
radius2 = 50  # You can adjust this size as needed

color = (0, 0, 255)  # Red color in BGR
thickness = 5  # Fill the circle

# Draw the circle
cv2.circle(image, center_coordinates, radius, color, thickness)
cv2.circle(image, center_coordinates, radius2, color, thickness)


# Display the image
cv2.imshow('Image with Circle', image)
cv2.waitKey()
cv2.destroyAllWindows()

# Save the image
cv2.imwrite('image_annotated.png', image)
