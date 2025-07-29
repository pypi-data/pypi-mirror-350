# StereotacticFrame

A python package to detect a stereotactic frame in MR and CT images

# Installation

Use pip to install the package:

```pip install StereotacticFrame```


# Install from source

Use git to clone the repository:

```git clone github.com/dwml/StereotacticFrame.git```

Use cd to get into the directory:

```cd StereotacticFrame```

Use uv to install the package. For installation instructions for uv see their documentation [here](https://docs.astral.sh/uv/getting-started/installation/). After uv is installed and your working directory is the FrameRegistration directory, run:

```uv build```

# Usage

The package has a command line interface that can be run using

```frame_registration calculate image_path modality transform_path```

The *image_path* should be the path to the input image, the *modality* should be one of **MR** or **CT** and *transform_path* is an optional path of the output transform. Since this is still under development a log file can be produced using:

```frame_registration calculate image_path modality transform_path log_path --loggin-on```

One can apply the transform using:

```frame_registration apply image_path transform_path output_image_path```

# Issues

Since this package is only tested on our own imaging it would not be strange if it does not work adequately on your data. If so please submit an issue at the [issue page](https://github.com/dwml/StereotacticFrame/issues).

# Warning

> [!CAUTION]
> In no circumstances can one use this package for clinical purposes. It is not thoroughly tested on a variety of images and should therefore only be used for research purposes.
