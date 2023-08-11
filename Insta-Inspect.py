# Insta - Inspect!
# A real world application of Computer Vision library EasyOCR

import streamlit as st  #streamlit==1.25.0
import cv2  #opencv-python==4.7.0.72
import easyocr #easyocr==1.6.2

def main():
    # st.title(":red[Insta-Inspect] 👀")
    # st.subheader("Check Before You Upload!")
    
    # st.title(":red[Insta-Inspect] 👀")
    st.markdown("<p style='text-align: center;font-size: 48px; color: red;'>Insta-Inspect 👀</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;font-size: 24px;'>Check Before You Upload!</p>", unsafe_allow_html=True)

    # Load the images to be displayed and chosen from
    image_paths = {
        "Image 1": r"DemoImages/1.jpg",  # Replace with the actual image path
        "Image 2": r"DemoImages/2.jpg",
           "Image 3": r"DemoImages/3.jpg"   # Replace with the actual image path
    }

    st.write("Select an image:")
    # Display the original images and let the user select one
    selected_image = st.radio("", list(image_paths.keys()))

    # Load the selected image
    image_path = image_paths[selected_image]
    image = cv2.imread(image_path)

    if image is None:
        st.error("Error loading the selected image.")
        return

    st.image(image, caption='Selected Image', width=300)  # Display the selected image

    run_button = st.button(":red[Check For Sensitive Content] 🔍")
    st.write("Wait A Few Moments Please!")
    st.write("If only this code had GPU access to run faster..")

    if run_button:
        reader = easyocr.Reader(['en'])

        results = reader.readtext(image)

        if results:
            st.warning("⚠️ Text Detected! Have A Look!")
            detected_text = "\n".join([text for (_, text, _) in results])
            # st.text(f"Detected Text: {detected_text}")

        processed_image = image.copy()
        for (bbox, text, prob) in results:
            x_min, y_min = [int(val) for val in bbox[0]]
            x_max, y_max = [int(val) for val in bbox[2]]
            cv2.rectangle(processed_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(processed_image, (x_min, y_min - 20), (x_min + text_size[0] + 2, y_min - 2), (220, 220, 220), cv2.FILLED)
            cv2.putText(processed_image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 0), 2)

        # st.image(processed_image, caption='Processed Image', width=300)  # Display the processed image
        col1, col2 = st.columns(2)

        with col1:
            st.image(processed_image, caption='Processed Image', width=300)  # Display the processed image

        with col2:
            st.write(":violet[Detected Text] ✅")
            st.text(detected_text)


        # st.write("Choose whether you want to upload or not! You are welcome!!")
        st.markdown("<p style='text-align: center; font-style: italic; color:orange;font-size: 24px;'>Decide whether you want to upload or not! You are welcome!!</p>", unsafe_allow_html=True)
if __name__ == '__main__':
    main()
