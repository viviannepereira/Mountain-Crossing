from PIL import Image
import numpy as numpy

class MoutainMapper:

    def __init__(self, filename):

        # Intialize attributes

        min , max , range , elavation_data , rows , columns = self.extract_data(filename)

        image_matrix = self.make_image(elavation_data, min, max, range, rows, columns)

        #find_lowest_elavation(image_matrix, elavation_data)


    def extract_data(self, filename):

        with open(filename, 'r') as file:

            lines = file.read().splitlines()

        elavation_data = []

        for line in lines:

            new_line = line.splitlines()

            new_line[0] = new_line[0].split("   ")

            elavation_data.append(new_line[0])

        min, max = self.find_min_and_max(elavation_data)

        range = int(max) - int(min)

        rows, columns = len(elavation_data), len(elavation_data[0])

        return min, max, range, elavation_data, rows, columns


    def find_min_and_max(self, elavation_data):

        max = 0

        min = int(elavation_data[0][0])

        for line in elavation_data:

            for elavation in line:

                if int(elavation) > max:

                    max = int(elavation)

                elif int(elavation) < min:

                    min = int(elavation)

        return min, max

    def make_image(self, elavation_data, min, max, range, rows, columns):
        
        image_matrix = numpy.zeros(shape=(rows, columns), dtype=object)

        current_pixel = (0, 0)
        
        for line in elavation_data:
            
            
            for elavation in line: 

                shifted_value = int(elavation) - min

                percentage = shifted_value / range

                grey_value = 255 * percentage

                print(image_matrix)

                image_matrix[current_pixel[0], current_pixel[1]] = (grey_value, grey_value, grey_value)

                if current_pixel[0] >= rows:

                    current_pixel = (0, current_pixel[1])

                current_pixel = (current_pixel[0] + 1, current_pixel[1])

            current_pixel = (current_pixel[0], current_pixel[1] + 1)

        print(image_matrix)



        



#m = MoutainMapper("Colorado_480x480.dat")
m = MoutainMapper("mini.dat")



