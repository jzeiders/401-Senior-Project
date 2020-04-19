import click 


@click.command()
@click.option("--test_files", help="Specifies directory where images to be classified are", type=click.Path())
@click.option("--export", help="Specifies how to provide results", type=click.Choice(['CSV'], case_sensitive=False))
def classify_images(test_files, export):
    click.echo('Classifying..')



if __name__ == "__main__":
    classify_images()
