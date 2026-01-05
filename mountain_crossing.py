from PIL import Image
import numpy as numpie

class MoutainMapper:

    def __init__(self, filename):

        self.min , self.max , self.range , self.elavation_data , self.rows , self.columns = self.extract_data(filename)

        #image_matrix = make_image(elavation_data)

        #find_lowest_elavation(image_matrix, elavation_data)


    def extract_data(self, filename):

        with open(filename, 'r') as file:

            lines = file.read().splitlines()

        max = 0

        min = -1

        print(lines)
        #for line in lines:

    def make_image(self, elavation_data):

        current_pixel = (0,0)




#m = MoutainMapper("Colorado_480x480.dat")
m = MoutainMapper("mini.dat")



