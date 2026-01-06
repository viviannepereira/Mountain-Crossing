from PIL import Image
import numpy as numpie
import re

class MoutainMapper:

    def __init__(self, filename):

        # Intialize attributes

        self.min , self.max , self.range , self.elavation_data , self.rows , self.columns = self.extract_data(filename)

        #image_matrix = make_image(elavation_data)

        #find_lowest_elavation(image_matrix, elavation_data)


    def extract_data(self, filename):

        with open(filename, 'r') as file:

            lines = file.read().splitlines()

        elavation_data = []

        for line in lines:

            new_line = line.splitlines()

            new_line[0] = new_line[0].split("   ")

            elavation_data.append(new_line[0])

        max = 0

        min = elavation_data[0][0]

        for line in lines:

            for elavation in line:

                if int(elavation) > max:

                    max = int(elavation)

                elif int(elavation) < min:

                    min = int(elavation)

        print(max)
        print(min)
        
        rows_x_col = re.findall(r"\d+x{1}\d+", filename)

        rows, columns = rows_x_col[0].split("x")




    def make_image(self, elavation_data):

        current_pixel = (0,0)




#m = MoutainMapper("Colorado_480x480.dat")
m = MoutainMapper("mini_14x26.dat")



