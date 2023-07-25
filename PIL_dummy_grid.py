# copied over from main.py and removed from there, will likely
# use matplotlib only for this project, but keeping this PIL
# python image library code that works until get new code
# block that works as intended

# make this a callable function if keep it...

########
# this code fills in dummy images into printable grid
# can change the 'square_size' and 'grid_size' parameter below
# to get different number of globes of varying sizes on the sheet
# based upon meeting with Nick & Kyle on 2023-07-17 with different
# size printouts, for now targeting the size that fits 4 columns
# and six rows of globes on the 8.5 x 11 printout (which would be

# square_size = 15 and grid_size = 6, 4

# will need to see how that looks on the 42 inch paper rolls then
# after get approval with some actual globe images

from PIL import Image, ImageDraw

square_size = 15  # cm
grid_size = (6, 4)  # number of squares in the grid (rows, columns)
margin = 0.1  # cm
output_file = "grid.png"

# image size in pixels
image_width = int((grid_size[0] * square_size + (grid_size[0] + 1) * margin) * 37.7952755906)
image_height = int((grid_size[1] * square_size + (grid_size[1] + 1) * margin) * 37.7952755906)

# blank image
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# add grid lines
for i in range(grid_size[0] + 1):
    x = i * (square_size + margin) * 37.7952755906 + margin * 37.7952755906
    draw.line([(x, margin * 37.7952755906), (x, image_height - margin * 37.7952755906)], fill="black")

for j in range(grid_size[1] + 1):
    y = j * (square_size + margin) * 37.7952755906 + margin * 37.7952755906
    draw.line([(margin * 37.7952755906, y), (image_width - margin * 37.7952755906, y)], fill="black")

# add png dummy file for testing printed size for viewing
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        # calculate position of square in pixels
        x = (i + 1) * margin * 37.7952755906 + i * square_size * 37.7952755906
        y = (j + 1) * margin * 37.7952755906 + j * square_size * 37.7952755906

        png_file = Image.open("/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png")

        # resize to fit in the square
        png_file.thumbnail((square_size * 37.7952755906, square_size * 37.7952755906))
        image.paste(png_file, (int(x), int(y)))

# save final image
image.save(output_file)

#### end ####