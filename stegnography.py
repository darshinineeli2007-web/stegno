from PIL import Image


def encode(image_path, secret_file, output_path):
    with open(secret_file, "r", encoding="utf-8") as file:
        message = file.read()

    image = Image.open(image_path).convert("RGB")

    binary_message = "".join(format(ord(char), "08b") for char in message)
    binary_message += "1111111111111110"

    pixels = list(image.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message is too large for this image.")

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel

        channels = [r, g, b]

        for i in range(3):
            if bit_index < len(binary_message):
                channels[i] = (channels[i] & 254) | int(binary_message[bit_index])
                bit_index += 1

        new_pixels.append(tuple(channels))

    encoded_image = Image.new("RGB", image.size)
    encoded_image.putdata(new_pixels)
    encoded_image.save(output_path)

    print("Message successfully hidden!")
    print("Output:", output_path)


def decode(image_path):
    image = Image.open(image_path).convert("RGB")

    binary_data = ""

    for pixel in image.getdata():
        for value in pixel:
            binary_data += str(value & 1)

    end_marker = "1111111111111110"

    message_bits = binary_data.split(end_marker)[0]

    message = ""

    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i + 8]

        if len(byte) == 8:
            message += chr(int(byte, 2))

    print("Extracted message:")
    print(message)


print("================================")
print("      IMAGE STEGANOGRAPHY")
print("================================")
print("1. Hide secret message")
print("2. Extract secret message")

choice = input("Enter your choice: ")

if choice == "1":
    encode(
        "cover.png",
        "secret.txt",
        "stego_output.png"
    )

elif choice == "2":
    decode("stego_output.png")

else:
    print("Invalid choice.")