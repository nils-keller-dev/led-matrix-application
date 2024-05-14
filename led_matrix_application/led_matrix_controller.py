from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

class LEDMatrixController:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.brightness = 50 
        self.matrix = RGBMatrix(options=options)

    def fill(self, r, g, b):
        self.matrix.Fill(r, g, b)