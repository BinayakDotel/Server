import tensorflow as tf
from PIL import Image

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0],
       [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4000)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)

class SuperResolution:
    def __init__(self):
        self.model= tf.saved_model.load("./models/SRGAN_model/")
        
    def predict(self, image_path, name):
        image= self.preprocess_image(image_path)
        prediction= self.model(image)
        prediction= tf.squeeze(prediction)
        self.write_to_file(prediction, f"enhanced_{name}")
        
    def preprocess_image(self, image_path):
        """ Loads image from path and preprocesses to make it model ready
            Args:
                image_path: Path to the image file
        """
        image = tf.image.decode_image(tf.io.read_file(image_path))
        
        # If PNG, remove the alpha channel. The model only supports
        # images with 3 color channels.
        if image.shape[-1] == 4:
            image = image[...,:-1]
        size = (tf.convert_to_tensor(image.shape[:-1]) // 4) * 4
        image = tf.image.crop_to_bounding_box(image, 0, 0, size[0], size[1])

        image = tf.cast(image, tf.float32)
        return tf.expand_dims(image, 0)
    
    def write_to_file(self, image, filename):
        if not isinstance(image, Image.Image):
            image = tf.clip_by_value(image, 0, 255)
            image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
        image.save(f"./static/output_images/{filename}")
        print(f"Saved as output_images/{filename}")
        
        
                
        