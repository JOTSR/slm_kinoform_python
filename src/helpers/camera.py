from pypylon import pylon
from PIL import Image, ImageTk
import cv2
import time

imagecool = None

def capture_frames(app):
        info = pylon.DeviceInfo()
        info.SetDeviceClass("BaslerUsb")
        app.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        app.camera.Open()
        app.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        
        try:
            while app.camera_running and app.camera.IsGrabbing():
                currentTime = time.perf_counter_ns()
                grabResult = app.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                
                fpsLimit = currentTime - app.timestamp > 1e9 / app.fps
                
                if grabResult.GrabSucceeded() and fpsLimit:
                    imagecool = grabResult.Array
                    image = cv2.cvtColor(imagecool, cv2.COLOR_BGR2RGB)
                    app.photo.put(image)
                    app.timestamp = time.perf_counter_ns()
                    image_update(app)
                    
                else:
                    time.sleep(1e-2)
                grabResult.Release()
        finally:
            app.camera.StopGrabbing()
            app.camera.Close()
            app.camera = None

def image_update(app):
        try:
            camImage = app.photo.get_nowait()
            camImage = Image.fromarray(camImage)  
            camImage_tk = ImageTk.PhotoImage(camImage)  
            app.camera_canvas.create_image(360, 270, image=camImage_tk)
            app.camera_canvas.image = camImage_tk  
        except:
            pass

def update_exposure(app, value):
    if app.camera == None:
        return
    try:
        app.camera.ExposureTime.SetValue(2 ** value)
    except:
        pass
