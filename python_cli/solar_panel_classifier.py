import click
import pandas as pd


def load_caffe2_model():
    """
    Loads the caffe2 model
    """

    return None


def load_test_images(test_file_dir: click.Path):
    """
    This loads in the test images specified by the user
    """
    return []

def run_classifier(model, image):
    """
    This runs the given model against the specified image
    """

    return None
def write_image_classification(output, df: pd.DataFrame):
    """
    This function will append the output of the model to the pandas 
    dataframe. We can then later serialize the dataframe as having multiple export 
    options.
    """
    return None

def export_with_type(format_specifier, df: pd.DataFrame):
    """
    This function takes a string list of export specifiers and attempts to serialize our df into
    that format. It will default to CSV because I like CSV.
    """
    return None


#
# Below is the CLI shell to actuate above functionality
#

@click.command()
@click.option("--test_files", help="Specifies directory where images to be classified are", type=click.Path())
@click.option("--export", help="Specifies how to provide results", type=click.Choice(['CSV'], case_sensitive=False))
@click.option("--seg_images", help="Include segmented output images for each input image", default=False)
def classify_images(test_files, export, seg_images):
    model = load_caffe2_model()
    if model is not None:
        print("Model loaded successfully")
    else:
        print("Error reading model")

    # should load images from user specified file path
    test_images = load_test_images(test_files)

    # set up pandas dataframe for storing classification results
    # TODO: Include other metadata we can gather from the model
    df = pd.DataFrame([], columns=["Image_Path", "HasSolarPanel", "Confidence"])

    for image in test_images:
        output = run_classifier(model, image)
        if seg_images:
            write_image_debuginfo(output)
            # Default is going to be csv because fuck it
        write_image_classification(output, df)

    if export is None or export == "CSV":
        export_with_type("CSV", df)


if __name__ == "__main__":
    classify_images()
