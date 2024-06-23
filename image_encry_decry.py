from PIL import Image
import numpy as np
import random


def generate_key(num_pixels, seed):
    np.random.seed(seed)  # Seed to ensure reproducibility
    key = np.random.permutation(num_pixels)
    return key


def encrypt_image(image_path, output_path, key_path, seed):
    image = Image.open(image_path)
    pixels = np.array(image)

    h, w, c = pixels.shape  # Height, Width, Channels

    # Flatten the array
    flat_pixels = pixels.reshape(-1, c)

    # Generate encryption key
    key = generate_key(len(flat_pixels), seed)

    # Encrypt by shuffling pixels according to the key
    encrypted_pixels = flat_pixels[key]

    # Reshape back to original image shape
    encrypted_pixels = encrypted_pixels.reshape((h, w, c))

    encrypted_image = Image.fromarray(encrypted_pixels)
    encrypted_image.save(output_path)

    # Save the key
    np.save(key_path, key)
    print(f"Encryption key saved to {key_path}")


def decrypt_image(image_path, output_path, key_path, seed):
    image = Image.open(image_path)
    pixels = np.array(image)

    h, w, c = pixels.shape  # Height, Width, Channels

    # Flatten the array
    flat_pixels = pixels.reshape(-1, c)

    # Load the encryption key
    key = np.load(key_path)

    # Create an empty array to store decrypted pixels
    decrypted_pixels = np.empty_like(flat_pixels)

    # Decrypt by placing each pixel back to its original position
    decrypted_pixels[key] = flat_pixels

    # Reshape back to original image shape
    decrypted_pixels = decrypted_pixels.reshape((h, w, c))

    decrypted_image = Image.fromarray(decrypted_pixels)
    decrypted_image.save(output_path)


def main():
    while True:
        choice = input("Do you want to (e)ncrypt or (d)ecrypt an image? Enter 'q' to quit: ").lower()
        if choice == 'q':
            break
        elif choice in ['e', 'd']:
            image_path = input("Enter the image path: ")
            output_path = input("Enter the output path for the image: ")
            key_path = input("Enter the path to save/load the key: ")
            if choice == 'e':
                seed = int(input("Enter a seed value for the random key: "))
                encrypt_image(image_path, output_path, key_path, seed)
                print(f"Encrypted image is saved to {output_path}")
            else:
                seed = None  # Decryption does not need a seed
                decrypt_image(image_path, output_path, key_path, seed)
                print(f"Decrypted image is saved to {output_path}")
        else:
            print("Please enter either 'e', 'd', or 'q'")


if __name__ == '__main__':
    main()
