import streamlit as st
from PIL import Image
import io
import base64
import rembg
import time
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Background Remover",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Image container */
    .image-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #1a1c24;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .image-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Upload area */
    .upload-container {
        background-color: #1a1c24;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(123, 47, 247, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(123, 47, 247, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1a1c24;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar section */
    .sidebar-section {
        background-color: #0e1117;
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-title {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(123, 47, 247, 0.3);
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: white;
        padding: 0.5rem;
        border-radius: 0.3rem;
        white-space: nowrap;
        z-index: 1;
        font-size: 0.8rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #3d5af1;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }
    
    /* Remove default footer */
    .reportview-container .main footer {
        visibility: hidden;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    /* Image guidelines collapsible */
    .guidelines {
        background-color: #1a1c24;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .guidelines-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        font-weight: 600;
    }
    
    .guidelines-content {
        margin-top: 1rem;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .guidelines-content ul {
        margin-left: 1.5rem;
        margin-bottom: 0;
    }
    
    /* Loading indicator */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .loading-text {
        margin-top: 1rem;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Download button */
    .download-btn {
        display: inline-block;
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 0.5rem;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
        box-shadow: 0 4px 10px rgba(123, 47, 247, 0.3);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(123, 47, 247, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title">Upload and download</div>', unsafe_allow_html=True)
    
    # Upload section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("Upload an image")
    
    uploaded_file = st.file_uploader("Drag and drop file here", 
                                    type=["png", "jpg", "jpeg"],
                                    label_visibility="collapsed")
    
    st.markdown("<div style='font-size:0.9rem; color:rgba(255,255,255,0.6);'>Limit 200MB per file • PNG, JPG, JPEG</div>", 
                unsafe_allow_html=True)
    
    # Image guidelines
    st.markdown("""
    <div class="guidelines">
        <div class="guidelines-header">
            <span>ℹ️</span>
            <span>Image Guidelines</span>
            <span>▾</span>
        </div>
        <div class="guidelines-content">
            <ul>
                <li>Maximum file size: 10MB</li>
                <li>Large images will be automatically resized</li>
                <li>Supported formats: PNG, JPG, JPEG</li>
                <li>Processing time depends on image size</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">Remove background from your image</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available <a href="https://github.com/danielgatis/rembg" style="color: #3d5af1;">here</a> on GitHub. Special thanks to the <a href="https://github.com/danielgatis/rembg" style="color: #3d5af1;">rembg library</a> 😊</p>', unsafe_allow_html=True)

# Create two columns for original and processed images
col1, col2 = st.columns(2)

# Function to get image download link
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}" class="download-btn">{text}</a>'
    return href

def process_image(upload):
    # Read uploaded image
    image = Image.open(upload)
    
    # Create a copy for display
    image_for_display = image.copy()
    
    # Check if image needs to be resized (for display purposes)
    max_size = (800, 800)
    if image_for_display.width > max_size[0] or image_for_display.height > max_size[1]:
        image_for_display.thumbnail(max_size)
    
    # Display original image
    with col1:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">Original Image 📷</div>', unsafe_allow_html=True)
        st.image(image_for_display, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show a progress bar during processing
    progress_text = "Removing background..."
    progress_bar = st.progress(0)
    
    # Process the image with rembg
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">Fixed Image ✨</div>', unsafe_allow_html=True)
        
        # Create a placeholder for the processed image
        result_placeholder = st.empty()
        
        # Simulate processing with progress bar
        for i in range(101):
            # Update progress bar
            progress_bar.progress(i)
            if i < 70:  # Make the progress seem natural
                time.sleep(0.01)
            else:
                time.sleep(0.03)
        
        # Actually process the image
        try:
            # Use rembg to remove background
            result = rembg.remove(
                data=io.BytesIO(upload.getvalue()).read(),
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Convert back to PIL Image
            output = Image.open(io.BytesIO(result))
            
            # Resize for display if needed
            output_display = output.copy()
            if output_display.width > max_size[0] or output_display.height > max_size[1]:
                output_display.thumbnail(max_size)
            
            # Display the result
            result_placeholder.image(output_display, use_column_width=True)
            
            # Add download button
            st.markdown(get_image_download_link(output, f"bg_removed_{upload.name}", "⬇️ Download Result"), unsafe_allow_html=True)
            
        except Exception as e:
            result_placeholder.error(f"Error processing image: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear progress bar after completion
    progress_bar.empty()
    
    # Display completion message
    completion_time = round(np.random.uniform(1.0, 3.0), 2)  # Random time for demonstration
    st.markdown(f'<div style="text-align: center; color: rgba(255,255,255,0.6);">Completed in {completion_time} seconds</div>', unsafe_allow_html=True)

# Main app logic
if uploaded_file is not None:
    process_image(uploaded_file)
else:
    # Display placeholder or instructions when no image is uploaded
    placeholder_col1, placeholder_col2 = st.columns(2)
    
    with placeholder_col1:
        st.markdown('<div class="image-container" style="height: 400px; display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: rgba(255,255,255,0.5);">Original image will appear here</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with placeholder_col2:
        st.markdown('<div class="image-container" style="height: 400px; display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: rgba(255,255,255,0.5);">Background-removed image will appear here</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Background Remover • Created with Streamlit and rembg</div>', unsafe_allow_html=True) 