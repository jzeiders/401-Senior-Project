import click
import pandas as pd
import requests
import math
import shutil
import os
import errno

from caffe2.python import core, workspace


def load_caffe2_model():
    """
    Loads the caffe2 model. The function will load the initial network and
    weights from the specified folder, initialize the network, and then
    return a caffe2 predictor.
    """
    MODEL_LOCATION = "model"
    INIT_NAME = "init_net.pb"
    PREDICT_NAME = "predict_net.pb" 
    init_path = os.path.join(MODEL_LOCATION, INIT_NAME)
    predict_path = os.path.join(MODEL_LOCATION, PREDICT_NAME)

    # Check that files exist
    if not os.path.exists(init_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), init_path)

    if not os.path.exists(predict_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), predict_path)
    
    # initialize the neural net
    with open(init_path) as f:
        init_net = f.read()
    with open(predict_path) as f:
        predict_net = f.read()

    return workspace.Predictor(init_net, predict_net)


def load_test_images(test_file_dir: click.Path):
    """
    This loads in the test images specified by the user
    """
    return []

def run_classifier(model, image):
    """
    This runs the given model against the specified image
    """
    results = p.run({'data': img})

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

def get_addresses(addresses):
    """
    This function takes a path to an address csv that has a column called "Address", from which it 
    will read all addresses to a list for convenience
    """
    df = pd.read_csv(addresses)
    return df['Address'].tolist()


def get_image(add, save_loc, API_key):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    url = base + requests.compat.quote_plus(add) + "&key=" + API_key
    img_file = add + ".jpg"
    response = requests.get(url, stream=True)
    with open(os.path.join(save_loc, img_file), 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
    if response.status_code == 200:
        print("Successfully saved image: " + img_file)
    del response


#
# Below is the CLI shell to actuate above functionality
#

# Shell for the provided subcommands
@click.group()
def solar_panel_cli():
   pass

@click.command()
@click.option("--test_files", help="Specifies directory where images to be classified are", type=click.Path())
@click.option("--export", help="Specifies how to provide results", type=click.Choice(['CSV'], case_sensitive=False))
@click.option("--seg_images", help="Include segmented output images for each input image", default=False)
def classify(test_files, export, seg_images):
    model = load_caffe2_model()
    if model is not None:
        print("Model loaded successfully")
    else:
        print("Error reading model")

    # should load images from user specified file path
    test_images = load_test_images(test_files)

    # set up pandas dataframe for storing classification results
    # TODO: Include other metadata we can gather from the model
    df = pd.DataFrame([], columns=["ImagePath", "HasSolarPanel", "Confidence"])

    for image in test_images:
        output = run_classifier(model, image)
        if seg_images:
            write_image_debuginfo(output)
            # Default is going to be csv
        write_image_classification(output, df)

    if export is None or export == "CSV":
        export_with_type("CSV", df)


@click.command()
@click.option("--output_directory", required=True, help="Specify directory to output images", type=click.Path())
@click.option("--api_key", required=True, help="Specify google API key for Google streetview API")
@click.option("--addresses", required=True, help="Path to address csv. See docs for format", type=click.Path())
def collect(output_directory, api_key, addresses):
    address_list = get_addresses(addresses) 
    for add in address_list:
        get_image(add, output_directory, api_key)
    print("Finished saving images")



solar_panel_cli.add_command(classify)
solar_panel_cli.add_command(collect)

if __name__ == "__main__":
    solar_panel_cli()
