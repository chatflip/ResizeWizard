# ResizeWizard

ResizeWizard is a simple and user-friendly web application for resizing images. Users can easily upload images through their browser and resize them to their desired dimensions.

## Features

- Image upload functionality
- Custom image resizing
- Resized image download

## Requirement

- Python >= 3.10
- Poetry >= 1.8

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ResizeWizard.git
cd ResizeWizard
```

2. Create and activate a virtual environment:

```bash
poetry install
```

## Usage

1. set environment variables:

```bash
export SECRET_KEY=hoge
```

2. Run the application:

```bash
python run.py
```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Click the "Choose File" button to upload an image.

4. Enter the desired width and height for your resized image.

5. Click the "Resize" button.

6. The resized image will be automatically downloaded.

## Development

- The `app/` directory contains the main application logic.
- The `templates/` directory contains HTML templates.
- The `static/` directory contains CSS files.

## Author

[chatflip](https://github.com/chatflip)
