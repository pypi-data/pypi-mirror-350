import io
import cv2
import logging
import numpy as np


logger = logging.getLogger(__name__)


class DynamicDocumentPreprocessor:
    def __init__(
        self,
        dpi=300,
        # Sharpening
        sharpen=True,
        sharpen_threshold=100,  # Laplacian variance threshold
        # Binarization
        binarize=True,
        use_otsu=False,
        binarization_block_size=11,
        binarization_C=2,
        # Brightness/contrast
        brightness_threshold=100,
        contrast_threshold=50,
        alpha=1.2,
        beta=30
    ):
        """
        Initialize the DynamicDocumentPreprocessor with default parameters.

        :param dpi: Resolution for PDF-to-image conversion (not used directly here).
        :param sharpen: Whether to apply sharpening when image is detected as blurry.
        :param sharpen_threshold: Laplacian variance threshold to consider an image blurry.
        :param binarize: Whether to apply binarization at the end of processing.
        :param use_otsu: If True, uses OTSU's threshold instead of adaptive threshold.
        :param binarization_block_size: Block size for adaptive thresholding.
        :param binarization_C: Constant subtracted from the mean in adaptive thresholding.
        :param brightness_threshold: If mean brightness is below this, apply brightness correction.
        :param contrast_threshold: If contrast is below this, apply contrast enhancement (hist. eq).
        :param alpha: The scale factor (gain) for brightness/contrast correction.
        :param beta: The offset (bias) for brightness/contrast correction.
        """
        self.dpi = dpi

        # Sharpening params
        self.default_sharpen = sharpen
        self.default_sharpen_threshold = sharpen_threshold

        # Binarization params
        self.default_binarize = binarize
        self.default_use_otsu = use_otsu
        self.default_binarization_block_size = binarization_block_size
        self.default_binarization_C = binarization_C

        # Brightness/contrast params
        self.default_brightness_threshold = brightness_threshold
        self.default_contrast_threshold = contrast_threshold
        self.default_alpha = alpha
        self.default_beta = beta

    def preprocess_image(
        self,
        image_bytes: bytes,
        dpi=None,
        sharpen=None,
        sharpen_threshold=None,
        binarize=None,
        use_otsu=None,
        binarization_block_size=None,
        binarization_C=None,
        brightness_threshold=None,
        contrast_threshold=None,
        alpha=None,
        beta=None
    ):
        """
        Preprocess a single image with customizable parameters.

        :param image_bytes: Input image bytes.
        :param dpi: Override DPI if needed.
        :param sharpen: Override sharpen flag.
        :param sharpen_threshold: Override sharpen threshold.
        :param binarize: Override binarize flag.
        :param use_otsu: Override use_otsu flag.
        :param binarization_block_size: Override binarization block size.
        :param binarization_C: Override binarization C.
        :param brightness_threshold: Override brightness threshold.
        :param contrast_threshold: Override contrast threshold.
        :param alpha: Override alpha for brightness/contrast correction.
        :param beta: Override beta for brightness/contrast correction.
        :return: Preprocessed image as bytes or None if processing fails.
        """
        # Use the provided parameters or fallback to defaults
        dpi = dpi if dpi is not None else self.dpi
        sharpen = sharpen if sharpen is not None else self.default_sharpen
        sharpen_threshold = sharpen_threshold if sharpen_threshold is not None else self.default_sharpen_threshold
        binarize = binarize if binarize is not None else self.default_binarize
        use_otsu = use_otsu if use_otsu is not None else self.default_use_otsu
        binarization_block_size = (
            binarization_block_size
            if binarization_block_size is not None
            else self.default_binarization_block_size
        )
        binarization_C = binarization_C if binarization_C is not None else self.default_binarization_C
        brightness_threshold = brightness_threshold if brightness_threshold is not None else self.default_brightness_threshold
        contrast_threshold = contrast_threshold if contrast_threshold is not None else self.default_contrast_threshold
        alpha = alpha if alpha is not None else self.default_alpha
        beta = beta if beta is not None else self.default_beta

        # Log the parameters being used
        logger.debug(
            f"Preprocessing image with parameters: "
            f"sharpen={sharpen}, sharpen_threshold={sharpen_threshold}, "
            f"binarize={binarize}, use_otsu={use_otsu}, "
            f"binarization_block_size={binarization_block_size}, binarization_C={binarization_C}, "
            f"brightness_threshold={brightness_threshold}, contrast_threshold={contrast_threshold}, "
            f"alpha={alpha}, beta={beta}, dpi={dpi}"
        )

        # Decode image from bytes
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("Failed to decode image from bytes")
            return None

        # Convert to grayscale
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Step 1: Analyze brightness and contrast
        brightness, contrast = self._analyze_brightness_and_contrast(grayscale)
        logger.debug(f"Brightness: {brightness:.2f}, Contrast: {contrast:.2f}")

        # Step 2: Correct brightness and contrast if needed
        grayscale = self._correct_brightness_and_contrast(
            grayscale,
            brightness,
            contrast,
            brightness_threshold,
            contrast_threshold,
            alpha,
            beta
        )

        # Step 3: Apply sharpening if the image is blurry
        if sharpen and self._is_blurry(grayscale, threshold=sharpen_threshold):
            logger.debug("Image is blurry, applying sharpening...")
            grayscale = self._sharpen_image(grayscale)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            grayscale = cv2.erode(grayscale, kernel, iterations=1)

        # Step 4: Apply binarization if enabled
        if binarize:
            logger.debug("Applying binarization...")
            grayscale = self._binarize_image(
                grayscale,
                use_otsu=use_otsu,
                block_size=binarization_block_size,
                C=binarization_C
            )

        # Encode the preprocessed image back to bytes
        success, encoded_img = cv2.imencode('.png', grayscale)
        if not success:
            logger.error("Failed to encode the preprocessed image")
            return None
        return io.BytesIO(encoded_img.tobytes())

    def _analyze_brightness_and_contrast(self, gray_image):
        """
        Analyze the brightness and contrast of a grayscale image.

        :param gray_image: Input grayscale image.
        :return: Tuple of (brightness, contrast).
        """
        brightness = np.mean(gray_image)
        contrast = np.std(gray_image)
        return brightness, contrast

    def _correct_brightness_and_contrast(
        self,
        gray_image,
        brightness,
        contrast,
        brightness_threshold,
        contrast_threshold,
        alpha,
        beta
    ):
        """
        Correct brightness and/or contrast if they fall below configured thresholds.

        :param gray_image: Input grayscale image.
        :param brightness: Calculated brightness of the image.
        :param contrast: Calculated contrast (std) of the image.
        :param brightness_threshold: Threshold for brightness correction.
        :param contrast_threshold: Threshold for contrast enhancement.
        :param alpha: Gain for brightness/contrast correction.
        :param beta: Bias for brightness/contrast correction.
        :return: Possibly modified grayscale image.
        """
        output = gray_image.copy()

        # Increase brightness if below threshold
        if brightness < brightness_threshold:
            logger.debug("Increasing brightness...")
            output = cv2.convertScaleAbs(output, alpha=alpha, beta=beta)

        # Enhance contrast if below threshold
        if contrast < contrast_threshold:
            logger.debug("Enhancing contrast with histogram equalization...")
            output = cv2.equalizeHist(output)

        return output

    def _sharpen_image(self, gray_image):
        """
        Sharpen the image using a simple unsharp mask approach.

        :param gray_image: Input grayscale image.
        :return: Sharpened grayscale image.
        """
        logger.debug("Applying sharpening via unsharp mask...")
        blurred = cv2.GaussianBlur(gray_image, (3, 3), 0)
        sharpened = cv2.addWeighted(gray_image, 1.5, blurred, -0.5, 0)
        return sharpened

    def _is_blurry(self, gray_image, threshold=100):
        """
        Determine if an image is blurry using the Laplacian variance method.

        :param gray_image: Input grayscale image.
        :param threshold: Variance threshold to consider an image blurry.
        :return: True if the image is blurry, False otherwise.
        """
        laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        logger.debug(f"Laplacian variance (sharpness): {laplacian_var:.2f}")
        return laplacian_var < threshold

    def _binarize_image(self, gray_image, use_otsu, block_size, C):
        """
        Binarize the image using either OTSU or adaptive thresholding.

        :param gray_image: Input grayscale image.
        :param use_otsu: Whether to use OTSU's thresholding.
        :param block_size: Block size for adaptive thresholding.
        :param C: Constant subtracted from the mean in adaptive thresholding.
        :return: Binary (thresholded) image.
        """
        if use_otsu:
            logger.debug("Applying OTSU threshold...")
            _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            return binary
        else:
            logger.debug("Applying adaptive Gaussian threshold...")
            return cv2.adaptiveThreshold(
                gray_image,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                block_size,
                C
            )
