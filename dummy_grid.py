
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
image_directory = "/Users/jmzator/Desktop/iuvs_maven_globes/first_globes_for_poster_print_sample"
image_files = [
        "globe_orbit_18001.png",
        "globe_orbit_18102.png",
        "globe_orbit_18111.png",
        "globe_orbit_18119.png",
        "globe_orbit_18120.png",
        "globe_orbit_18152.png",
        "globe_orbit_18166.png",
        "globe_orbit_18172.png",
        "globe_orbit_18173.png",

        # above is just two dummy images over and over again
        # add more then, for final project will need code to add all as created
    ]
output_file = "sample_grid.png"

plot_images_on_grid(image_directory, image_files, output_file)


### end ###
