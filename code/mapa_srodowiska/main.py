import OpenEXR
import Imath
import numpy as np
import os
import OpenGL.GL as gl
import OpenGL.GLUT as glut

def load_hdr_environment_map(filepath):
    """
    Load an HDR environment map from an OpenEXR file.
    
    Args:
        filepath (str): Path to the HDR file.
        
    Returns:
        np.ndarray: A NumPy array representing the HDR environment map in (H, W, 3) format.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Check file permissions
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"File is not readable: {filepath}")
    
    # Open the EXR file
    try:
        exr_file = OpenEXR.InputFile(filepath)
    except Exception as e:
        raise OSError(f"Unable to open '{filepath}' for read: {str(e)}")
    
    # Get the image dimensions
    header = exr_file.header()
    dw = header['dataWindow']
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    # Define the channel names (R, G, B)
    channels = ['R', 'G', 'B']
    
    # Read the channel data
    channel_data = {
        channel: exr_file.channel(channel, Imath.PixelType(Imath.PixelType.FLOAT))
        for channel in channels
    }
    
    # Convert channel data to NumPy arrays
    hdr_image = np.zeros((height, width, 3), dtype=np.float32)
    for i, channel in enumerate(channels):
        hdr_image[:, :, i] = np.frombuffer(channel_data[channel], dtype=np.float32).reshape(height, width)

    return hdr_image

def display_hdr_image(hdr_image):
    height, width, _ = hdr_image.shape
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glDrawPixels(width, height, gl.GL_RGB, gl.GL_FLOAT, hdr_image)
    glut.glutSwapBuffers()

def main(filepath):
    # List files in the current directory
    print("Files in the current directory:")
    for file in os.listdir("."):
        print(file)
    
    # Check file details
    print(f"\nChecking file: {filepath}")
    print(f"File exists: {os.path.exists(filepath)}")
    print(f"File is readable: {os.access(filepath, os.R_OK)}")
    print(f"File size: {os.path.getsize(filepath)} bytes")
    
    try:
        hdr_map = load_hdr_environment_map(filepath)
        print("HDR Map Loaded. Shape:", hdr_map.shape)
        
        # Initialize GLUT and create window
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(hdr_map.shape[1], hdr_map.shape[0])
        glut.glutCreateWindow(b"HDR Environment Map")
        
        # Set display callback
        glut.glutDisplayFunc(lambda: display_hdr_image(hdr_map))
        
        # Start the GLUT main loop
        glut.glutMainLoop()
    except Exception as e:
        print(e)

# Example usage
if __name__ == "__main__":
    filepath = "lilienstein_1k.exr"
    main(filepath)
