import hashlib
import os
from PIL import Image
import streamlit as st


def process_images(uploaded_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for uploaded_file in uploaded_files:
        # Generate a unique key for each file
        file_hash = hashlib.md5(uploaded_file.read()).hexdigest()
        uploaded_file.seek(0)  # Reset file pointer after reading

        # Add text input for custom file name
        custom_name = st.text_input(
            f"Enter custom name for {uploaded_file.name} (without extension):",
            value=os.path.splitext(uploaded_file.name)[0],
            key=f"custom_name_{file_hash}",  # Unique key for this input
        )

        # Process the uploaded image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded {uploaded_file.name}", use_column_width=True)

            # Add a download button to save the image
            if custom_name:
                output_path = os.path.join(output_directory, f"{custom_name}.jpg")
                image.save(output_path, "JPEG")
                st.success(f"Image saved as {output_path}")
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")


def main():
    st.title("Image Cropper")

    uploaded_files = st.file_uploader(
        "Upload one or more images:",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    output_directory = "processed_images"

    if uploaded_files:
        process_images(uploaded_files, output_directory)
    else:
        st.warning("No valid images to process.")


if __name__ == "__main__":
    main()
