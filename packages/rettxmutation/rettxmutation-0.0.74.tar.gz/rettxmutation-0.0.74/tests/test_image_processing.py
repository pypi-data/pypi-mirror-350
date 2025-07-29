import numpy as np
import cv2
from rettxmutation.analysis.document_processing import DynamicDocumentPreprocessor


def test_preprocess_image_basic():
    # 1. Create a synthetic 100x100 black BGR image (3-channel)
    black_image = np.zeros((100, 100, 3), dtype=np.uint8)

    # 2. Encode to bytes (PNG format, for instance)
    success, black_image_bytes = cv2.imencode(".png", black_image)
    assert success, "Failed to encode synthetic image"
    black_image_bytes = black_image_bytes.tobytes()

    # 3. Instantiate the preprocessor with your desired parameters
    preprocessor = DynamicDocumentPreprocessor(
        sharpen=True,
        sharpen_threshold=10,
        binarize=True,
        use_otsu=False,
        brightness_threshold=10,
        contrast_threshold=10,
        alpha=1.5,
        beta=40
    )

    # 4. Run the preprocessing
    processed_io = preprocessor.preprocess_image(black_image_bytes)
    assert processed_io is not None, "Preprocessing returned None"

    # 5. Decode the processed image from the returned BytesIO
    processed_data = np.frombuffer(processed_io.getvalue(), np.uint8)
    processed_image = cv2.imdecode(processed_data, cv2.IMREAD_UNCHANGED)
    assert processed_image is not None, "Failed to decode processed image"

    # 6. Now you can perform various checks on `processed_image`
    # For instance, verify it's still 100x100:
    assert processed_image.shape[0] == 100
    assert processed_image.shape[1] == 100

    # Optional: Check some pixel values if you expect a certain output
    # e.g. black image might remain mostly black or become white after thresholding
    top_left_pixel = processed_image[0, 0]
    # For a binarized grayscale image, expect 0 or 255
    assert top_left_pixel in (0, 255), f"Pixel value not as expected: {top_left_pixel}"


def test_preprocess_image_basic_apply_otsu():
    # 1. Create a synthetic 100x100 black BGR image (3-channel)
    black_image = np.zeros((100, 100, 3), dtype=np.uint8)

    # 2. Encode to bytes (PNG format, for instance)
    success, black_image_bytes = cv2.imencode(".png", black_image)
    assert success, "Failed to encode synthetic image"
    black_image_bytes = black_image_bytes.tobytes()

    # 3. Instantiate the preprocessor with your desired parameters, this time using Otsu thresholding
    preprocessor = DynamicDocumentPreprocessor(
        sharpen=True,
        sharpen_threshold=10,
        binarize=True,
        use_otsu=True,
        brightness_threshold=10,
        contrast_threshold=10,
        alpha=1.5,
        beta=40
    )

    # 4. Run the preprocessing
    processed_io = preprocessor.preprocess_image(black_image_bytes)
    assert processed_io is not None, "Preprocessing returned None"

    # 5. Decode the processed image from the returned BytesIO
    processed_data = np.frombuffer(processed_io.getvalue(), np.uint8)
    processed_image = cv2.imdecode(processed_data, cv2.IMREAD_UNCHANGED)
    assert processed_image is not None, "Failed to decode processed image"

    # 6. Now you can perform various checks on `processed_image`
    # For instance, verify it's still 100x100:
    assert processed_image.shape[0] == 100
    assert processed_image.shape[1] == 100
