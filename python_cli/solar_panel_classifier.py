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
    df = pd.Dataframe([], columns = ["Image_Path", "HasSolarPanel", "Confidence"]

    for image in test_images:
        output = run_classifier(model, image)
        if seg_images:
            write_image_debuginfo(output)
        if export is None or export == "CSV":
            # Default is going to be csv because fuck it




if __name__ == "__main__":
    classify_images()
