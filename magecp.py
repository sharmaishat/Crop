import hashlib
import os
import zipfile
from PIL import Image
import streamlit as st


def process_images(uploaded_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    cropped_images = []

    for uploaded_file in uploaded_files:
        # Reset file pointer after reading for hash generation
        uploaded_file.seek(0)
        
        # Generate a unique key for each file
        file_hash = hashlib.md5(uploaded_file.read()).hexdigest()
        uploaded_file.seek(0)  # Reset file pointer after reading for image processing

        # Add text input for custom file name
        custom_name = st.text_input(
            f"Enter custom name for {uploaded_file.name} (without extension):",
            value=os.path.splitext(uploaded_file.name)[0],
            key=f"custom_name_{file_hash}",  # Unique key for this input
        )

        # Process the uploaded image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded {uploaded_file.name}", use_container_width=True)  # Changed here

            # Add a crop function (basic example)
            left, top, right, bottom = st.slider(
                "Select crop region (left, top, right, bottom)", 
                0, image.width, 0, image.height, (0, 0, image.width, image.height)
            )

            cropped_image = image.crop((left, top, right, bottom))
            st.image(cropped_image, caption="Cropped Image", use_container_width=True)  # Changed here

            # Save the cropped image to the output directory
            if custom_name:
                output_path = os.path.join(output_directory, f"{custom_name}.jpg")
                cropped_image.save(output_path, "JPEG")
                cropped_images.append(output_path)
                st.success(f"Image saved as {output_path}")
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")

    return cropped_images


def zip_images(cropped_images, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in cropped_images:
            zipf.write(file, os.path.basename(file))  # Add files to the zip archive


def main():
    # Set page layout first
    st.set_page_config(page_title="Image Cropper", layout="wide")  # Set page layout

    st.title("Image Cropper")

    uploaded_files = st.file_uploader(
        "Upload one or more images:",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    output_directory = "processed_images"

    if uploaded_files:
        cropped_images = process_images(uploaded_files, output_directory)

        if cropped_images:
            zip_filename = "cropped_images.zip"
            zip_images(cropped_images, zip_filename)

            # Provide a download link for the zip file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download All Cropped Images as ZIP",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip",
                )
        else:
            st.warning("No images processed.")
    else:
        st.warning("No valid images to process.")


if __name__ == "__main__":
    main()

