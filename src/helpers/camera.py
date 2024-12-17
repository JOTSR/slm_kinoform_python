from pypylon import pylon
from PIL import Image , ImageTk
import cv2

def capture_frames(app):
        
        info = pylon.DeviceInfo()
        info.SetDeviceClass("BaslerUsb")
        app.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        app.camera.Open()
        app.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        try:
            while app.camera_running and app.camera.IsGrabbing():
                grabResult = app.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    image = grabResult.Array
                
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    image_tk = ImageTk.PhotoImage(image)
                  
                    # app.image_label.configure(image=image_tk)
                    # app.image_label.image = image_tk
                grabResult.Release()
        finally:
            app.camera.StopGrabbing()
            app.camera.Close()
            app.camera = None
