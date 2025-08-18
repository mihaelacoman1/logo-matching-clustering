# Logo Matching & Clustering Project

  This project performs logo matching and clustering by:
  - Downloading and processing logos from websites
  - Automatically scraping logo images
  - Clustering similar logos based on visual features

# Setup

  In order to setup and run this project you first need to install the required python packages. To do this, it is recommended that you use a virtual environment such as `conda` (Windows) or `virtual-env` (Linux)

For Windows:
- Navigate to `setup/Windows` and run `setup.bat`.

For Linux:
- Navigate to `setup/Linux` and run `setup.sh`.

After the packages were installed, navigate to the root directory and run `python main.py`.

# Idea/Workflow
  Long story short, the idea behind the code was to scrape the logos from the given websites and vector embed them, i.e. convert them from an image to a vector. This conversion is not random. It should follow the rule that visually similar logos should have vectors which point to points which are close to each other. One way to do this is to have a neural network that was trained to achieve such thing.

  When possible, it is highly advised to use pre-trained and free neural networks and this was the case for this project. ResNet50 was used, which is a neural network for classyfing images. The network was "hacked" to do vector embedding by excluding the last layer, i.e. the classification layer, thus leaving us with the vector embedding.

  Now, having the vector embedding, it is time to group similar logos together. This was achieved with K Means Clustering provided by scikit-learn.

  A big part of this project was URL fixing, as most websites didn't come in a clean URL, but had to go through a validation / fix step in order to get usable logos (see `validate_and_fix_url` in `utils/logos.py`)

  For fetching the URLs mentioned previously `Beautiful Soup` was used. It looked for logos in the source code of the websites, searching for `link`, `meta` and `img` tags which could contain logo URLs (see `get_website_logo` in `utils/logos.py`).
