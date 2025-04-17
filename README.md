# Image Background Remover

A beautiful and easy-to-use tool built with Python and Streamlit that automatically removes backgrounds from images.

## Features

- Clean, modern dark-themed UI
- Drag and drop image upload
- Automatic background removal using the rembg library
- Real-time processing with progress indication
- High-quality image download
- Supports PNG, JPG, and JPEG formats
- Mobile-responsive design

## Screenshots

The application features a side-by-side view showing:
- Original uploaded image
- Background-removed result
- Download option for the processed image

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the application with:
```
streamlit run bg_remover.py
```

The application will open in your default web browser at http://localhost:8501.

## Deployment

To deploy this application on Streamlit Cloud or other platforms:

1. Make sure both `requirements.txt` and `packages.txt` are in your repository
2. The `requirements.txt` file contains all Python dependencies
3. The `packages.txt` file contains system dependencies needed by OpenCV and rembg
4. For Streamlit Cloud:
   - Connect your GitHub repository
   - Select the `bg_remover.py` as the main file
   - Deploy the app

If you encounter any dependency errors during deployment, check the logs for specific missing packages.

## How It Works

This application uses the [rembg](https://github.com/danielgatis/rembg) library, which is built on deep learning models specialized in image segmentation. The process includes:

1. Upload your image through the interface
2. The image is processed by rembg's neural network model
3. The background is identified and made transparent
4. The result is presented for viewing and download

## Dependencies

- streamlit
- rembg
- Pillow
- numpy
- onnxruntime

## Limitations

- Processing time depends on image size and complexity
- Very large images may be automatically resized
- Maximum file size: 200MB (configurable)
- Best results are achieved with images that have clear subject/background separation 