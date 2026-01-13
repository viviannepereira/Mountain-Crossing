from PIL import Image
import numpy as numpy
import random

class MoutainMapper:

    def __init__(self, filename):

        # Intialize attributes

        min , max , range , elavation_data , rows , columns = self.extract_data(filename)

        image_matrix = self.make_image(elavation_data, min, range, rows, columns)

        self.draw_elavation(image_matrix, elavation_data, rows, columns)

        self.convert_to_jpeg(image_matrix)


    def extract_data(self, filename):

        with open(filename, 'r') as file:

            # each line in data is now a string in a list

            lines = file.read().splitlines()

        elavation_data = []

        for line in lines:

            # now a list with one element in it, which was the string

            new_line = line.splitlines()

            new_line[0] = new_line[0].split()

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

    def make_image(self, elavation_data, min, range, rows, columns):
        
        image_matrix = numpy.zeros(shape=(rows, columns, 3), dtype=numpy.uint8)

        current_pixel = (0, 0)
        
        for line in elavation_data:
            
            for elavation in line:

                shifted_value = int(elavation) - min

                percentage = shifted_value / range

                grey_value = int(255 * percentage)

                image_matrix[current_pixel[0]][current_pixel[1]] = [grey_value, grey_value, grey_value]

                if current_pixel[1] == columns - 1:

                    current_pixel = (current_pixel[0], 0)

                else:

                    current_pixel = (current_pixel[0], current_pixel[1] + 1)

            current_pixel = (current_pixel[0] + 1, current_pixel[1])

        jpeg = Image.fromarray(image_matrix, "RGB")

        jpeg.save("output/output1.jpg")

        return image_matrix
    
    def draw_elavation(self, image_matrix, elavation_data, rows, columns):

        current_pixel = (0, 0)

        starting_elavation = (0, 0)

        end = False


        while end == False:

            image_matrix[current_pixel[0]][current_pixel[1]] = [255, 0, 0]

            next_location = self.next_location(current_pixel, columns, rows, elavation_data)

            if next_location == None:

                if starting_elavation[0] >= rows-1:
                   
                    end = True

                else:

                    starting_elavation = (starting_elavation[0] + 1, 0)

                    current_pixel = starting_elavation

            else:

                current_pixel = next_location

        return image_matrix


    def next_location(self, current_pixel, columns, rows, elavation_data):

        straight_index = (current_pixel[0], current_pixel[1] + 1)

        up_index = (current_pixel[0] - 1, current_pixel[1] + 1)
        
        down_index = (current_pixel[0] + 1, current_pixel[1] + 1)

        if straight_index[1] >= columns:

            return None

        else:

            if up_index[0] < 0:

                if elavation_data[straight_index[0]][straight_index[1]] <= elavation_data[down_index[0]][down_index[1]]:

                    return straight_index
                
                else:

                    return down_index
                
            elif down_index[0] > rows - 1:

                return straight_index
            
            else:

                return random.choice([up_index, down_index])

    def convert_to_jpeg(self, image_matrix):

        jpeg = Image.fromarray(image_matrix, "RGB")

        jpeg.save("output/output.png")


# turn while loop into for loop

# change next_location algorithm 

# add comments and docstrings





        



m = MoutainMapper("Colorado_480x480.dat")
#m = MoutainMapper("mini.dat")



