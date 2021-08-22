import tensorflow as tf

class DonkeyCarDataAugmentator:
  @staticmethod
  def normalize(img):
    return (img / 127.5) - 1.0
  
  @staticmethod
  def unnormalize(img):
    return (img + 1.0) * 127.5

  @staticmethod
  def clip_image(img):
    return tf.clip_by_value(img, clip_value_min=0, clip_value_max=255)

  @staticmethod
  def noiser(img, mean, stddev):
    transformed_img = DonkeyCarDataAugmentator.normalize(img)
    noise_img = tf.random.normal(shape=tf.shape(img), mean=mean, stddev=stddev)
    transformed_img = tf.add(transformed_img, noise_img)
    transformed_img = DonkeyCarDataAugmentator.unnormalize(transformed_img)
    transformed_img = DonkeyCarDataAugmentator.clip_image(transformed_img)
    return transformed_img

  @staticmethod
  def transform(img, angle, ratio_augmentation = 0.75, ratio_flip_left_right = 0.5, max_brightness = 50,
                lower_contrast = 0.75, upper_contrast = 1.5, lower_saturation = 0.0, 
                upper_saturation = 2, mean_noise = 0.0, max_noise = 0.3):
    
    random_do_augmentation = tf.random.uniform(shape=[], minval = 0., maxval = 1., dtype=tf.float32)
    if random_do_augmentation <= ratio_augmentation:
      transformed_img = tf.image.random_brightness(img, max_delta = max_brightness)
      transformed_img = DonkeyCarDataAugmentator.clip_image(transformed_img)

      transformed_img = tf.image.random_contrast(transformed_img, lower = lower_contrast, upper = upper_contrast)
      transformed_img = DonkeyCarDataAugmentator.clip_image(transformed_img)
      
      transformed_img = tf.image.random_saturation(transformed_img, lower = lower_saturation, upper = upper_saturation)
      transformed_img = DonkeyCarDataAugmentator.clip_image(transformed_img)

      random_noise_gain = tf.random.uniform(shape=[], minval = 0.0, maxval = max_noise, dtype=tf.float32)
      transformed_img = DonkeyCarDataAugmentator.noiser(transformed_img, mean_noise, random_noise_gain)
    else:
      transformed_img = img
    
    random_do_flip = tf.random.uniform(shape=[], minval = 0., maxval = 1., dtype=tf.float32)
    if random_do_flip <= ratio_flip_left_right:
      transformed_img = tf.image.flip_left_right(transformed_img)
      angle *= -1
    
    return transformed_img, angle