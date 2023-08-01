
import os
import matplotlib.pyplot as plt


def plot_images_on_grid(image_dir, image_files, output_file):
    # number of rows and columns in grid
    num_rows = 3
    num_cols = 3

    # figure size for square grid
    fig_width = 9.0  # cm
    fig_height = 9.0
    dpi = 300  # dpi resolution

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height), dpi=dpi)

    for i, ax in enumerate(axs.flat):
        if i < len(image_files):
            image_path = os.path.join(image_dir, image_files[i])
            img = plt.imread(image_path)
            ax.imshow(img)
            ax.axis('off')
        else:
            ax.set_visible(False)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


# removed 'if __name__ == "__main__":' above this and got rid of indents below
image_directory = "/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/"
image_files = [
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",
        "orbit03475-Ls1843-angle0345-binning0133x0019-heq-globe.png",
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",
        "orbit03475-Ls1843-angle0345-binning0133x0019-heq-globe.png",
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",
        "orbit03475-Ls1843-angle0345-binning0133x0019-heq-globe.png",
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",
        "orbit03475-Ls1843-angle0345-binning0133x0019-heq-globe.png",
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",

        # above is just two dummy images over and over again
        # add more then, for final project will need code to add all as created
    ]
output_file = "sample_grid.png"

plot_images_on_grid(image_directory, image_files, output_file)


### end ###
