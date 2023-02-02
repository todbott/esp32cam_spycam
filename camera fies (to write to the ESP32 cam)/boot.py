import binascii
import camera
import time
import network
import uos
import machine
import urequests_two as urequests


class CameraController:

    def __init__(self) -> None:


        # Here is the LAN thing
        self.sta = network.WLAN(network.STA_IF)

        # And the flash for the camera
        self.led = machine.Pin(4, machine.Pin.OUT)

        # And the image counter for saving images
        self.imageCounter = 0

        # And the camera
        self.camera = None

        # Finally, initialize the SD card, in case we want to save images
        uos.mount(machine.SDCard(), "/sd")



    def __initCamera(self):

        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

        ## Other settings:
        # flip up side down
        camera.flip(1)
        # left / right
        camera.mirror(1)

        # framesize
        camera.framesize(camera.FRAME_SVGA)
        # The options are the following:
        # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
        # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
        # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
        # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
        # FRAME_P_FHD FRAME_QSXGA
        # Check this link for more information: https://bit.ly/2YOzizz

        # special effects
        camera.speffect(camera.EFFECT_NONE)
        # The options are the following:
        # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

        # white balance
        camera.whitebalance(camera.WB_HOME)
        # The options are the following:
        # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

        # saturation
        camera.saturation(2)
        # -2,2 (default 0). -2 grayscale 

        # brightness
        camera.brightness(0)
        # -2,2 (default 0). 2 brightness

        # contrast
        camera.contrast(0)
        #-2,2 (default 0). 2 highcontrast

        # quality
        camera.quality(10)
        # 10-63 lower number means higher quality

        # Assign the camera instance to self.camera
        self.camera = camera



    def __connectToWiFi(self):
        self.sta.active(True)
        self.sta.connect("IODATA-cdbc80-2G", "8186896622346")

        while self.sta.isconnected() == False:
            time.sleep(2)



    def takePhotoAndSend(self):

        for x in range(0, 60):
  
            url = "https://us-central1-hotaru-kanri.cloudfunctions.net/room-stats"
            data = {'light': str(binascii.b2a_base64(self.camera.capture()))[2:-3]}
            headers = {}
            headers['Content-Type'] = 'application/json'

            r = urequests.post(url, json=data, headers=headers)
            print(r.status_code)
            r.close()   
            
            time.sleep(30)



    def takePhotoAndSave(self):

        # Turn on the flash
        self.led.on()

        # Take a picture and save it
        with open(f"/sd/{self.imageCounter}_.jpeg", "wb") as im:
            im.write(self.camera.capture())

        # Turn the flash off
        self.led.off()

        # Increase the image counter
        self.imageCounter += 1
        

cc = CameraController()
cc.__initCamera()
cc.__connectToWiFi()
cc.takePhotoAndSend()