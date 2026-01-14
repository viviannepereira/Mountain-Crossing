from PIL import Image
import numpy as numpy
import random

class MoutainMapper:

    def __init__(self, filename:str):

        # Intialize attributes

        min , max , range , elavation_data , rows , columns = self.extract_data(filename)

        image_matrix = self.make_image(elavation_data, min, range, rows, columns)

        self.draw_elavations(image_matrix, elavation_data, rows, columns)

        self.convert_to_jpeg(image_matrix)


    def extract_data(self, filename:str):

        """
        Docstring for extract_data
        
        :param self: MountainMapper object
        :param filename: name of file with elavation data
        :type filename: str

        Creates matrix from elavation data and exacts needed data from matrix

        returns the minimum elavation, maxmimum elavation, the range between minimum and maximum, the matrix of elavation data, max rows, and max columns.
        """

        with open(filename, 'r') as file:

            # each line in data is now a string in a list

            lines = file.read().splitlines()

        elavation_data = []

        for line in lines:

            # each line in matrix has one element in it which is a string of elavations

            new_line = line.splitlines()

            # now each line in matrix has multiple elements which are each an elavation

            new_line[0] = new_line[0].split()

            # each list is added to elavation_data to create matrix

            elavation_data.append(new_line[0])

        # find the max and min elavations in elavation_data

        min, max = self.find_min_and_max(elavation_data)

        # find the range between the max and min elavations

        range = int(max) - int(min)

        # find the max number of rows and columns

        rows, columns = len(elavation_data), len(elavation_data[0])

        return min, max, range, elavation_data, rows, columns


    def find_min_and_max(self, elavation_data:list) -> int:
        """
        Docstring for find_min_and_max
        
        :param self: MountainMapper object
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :return: Minimum and maximum elavations in elavation_data
        :rtype: int

        Finds minimum and maximum elavations in elavation_data.
        """

        max = 0

        min = int(elavation_data[0][0])

        for line in elavation_data:

            for elavation in line:

                if int(elavation) > max:

                    max = int(elavation)

                elif int(elavation) < min:

                    min = int(elavation)

        return min, max

    def make_image(self, elavation_data:list, min:int, range:int, rows:int, columns:int):

        """
        Docstring for make_image
        
        :param self: MountainMapper object
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :param min: Minimum elavation in elavation_data
        :type min: int
        :param range: Range between minimum elavation and maximum elavation
        :type range: int
        :param rows: Max rows in elavation_data and image_matrix
        :type rows: int
        :param columns: Max columns in elavation_data and image_matrix
        :type columns: 
        
        Makes a greyscale image out of elavation_data
        """

        # create numpy matrix to hold greyscale image
        
        image_matrix = numpy.zeros(shape=(rows, columns, 3), dtype=numpy.uint8)

        current_pixel = (0, 0)
        
        for line in elavation_data:
            
            for elavation in line:

                # calculate RGB greyscale value from elavation value

                shifted_value = int(elavation) - min

                percentage = shifted_value / range

                grey_value = int(255 * percentage)

                # set current pixel as new greyscale value

                image_matrix[current_pixel[0]][current_pixel[1]] = [grey_value, grey_value, grey_value]

                # check if we are currently on the last column

                if current_pixel[1] == columns - 1:

                    current_pixel = (current_pixel[0], 0)

                else:

                    current_pixel = (current_pixel[0], current_pixel[1] + 1)

            current_pixel = (current_pixel[0] + 1, current_pixel[1])

        jpeg = Image.fromarray(image_matrix, "RGB")

        jpeg.save("output/output_greyscale.jpg")

        return image_matrix
    
    def draw_elavations(self, image_matrix:list, elavation_data:list, rows:int, columns:int):

        """
        Docstring for draw_elavations
        
        :param self: MountainMapper object
        :param image_matrix: Matrix of pixels that create greyscale image with red paths
        :type image_matrix: list
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :param rows: Max rows in elavation_data and image_matrix
        :type rows: int
        :param columns: Max columns in elavation_data and image_matrix
        :type columns: 
        
        Draws all paths 
        """

        # line_number keeps track of the line we are currently on (the y-value)

        line_number = 0

        for line in elavation_data:

            # for each y-value, create a path

            self.path_drawer(line_number, rows, columns, elavation_data, image_matrix)

            line_number += 1


    def path_drawer(self, line_number:int, rows:int, columns:int, elavation_data:list, image_matrix:list):

        """
        Docstring for path_drawer
        
        :param self: MountainMapper object
        :param line_number: Current row we are on in both the elavation_data and image_matrix
        :type line_number: int
        :param rows: Max rows in elavation_data and image_matrix
        :type rows: int
        :param columns: Max columns in elavation_data and image_matrix
        :type columns: int
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :param image_matrix: Matrix of pixels that create greyscale image with red paths
        :type image_matrix: list

        Draws paths individually 
        """

        end = False

        current_pixel = (line_number, 0)

        while end == False:

            # makes current pixel red

            image_matrix[current_pixel[0]][current_pixel[1]] = [255, 0, 0]

            # calculates next pixel location

            next_location = self.next_location(current_pixel, columns, rows, elavation_data)

            if next_location == None:
                   
                end = True

            else:

                current_pixel = next_location


    def next_location(self, current_pixel:tuple, columns:int, rows:int, elavation_data:list) -> tuple:

        """
        Docstring for next_location
        
        :param self: MountainMapper object
        :param current_pixel: Pixel currently on
        :type current_pixel: tuple
        :param columns: Max columns in elavation_data and image_matrix
        :type columns: int
        :param rows: Max rows in elavation_data and image_matrix
        :type rows: int
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :return: Returns the next pixel location to travel to
        :rtype: tuple

        Finds the next possible location to travel to by using a greedy algorithm.
        """

        # find indexes of pixels, straight, up, and down from the current pixel

        straight_index = (current_pixel[0], current_pixel[1] + 1)

        up_index = (current_pixel[0] - 1, current_pixel[1] + 1)
        
        down_index = (current_pixel[0] + 1, current_pixel[1] + 1)
        
        # if a pixel ahead of current does not exist, return None

        if straight_index[1] >= columns:

            return None

        else:

            # if up pixel does not exist

            if up_index[0] < 0:

                # calculate the cost it would take to travel from the current elavation to the one straight ahead

                straight_cost = self.calculate_cost(current_pixel, straight_index, elavation_data)

                # calculate the cost it would take to travel from the current elavation to the one straight ahead and down

                down_cost = self.calculate_cost(current_pixel, down_index, elavation_data)

                # if the cost it takes to go straight is less than or equal to the cost it takes to go straight and down, return straight_index
                
                if straight_cost <= down_cost:

                    return straight_index
                
                else:

                    # otherwise, return down_index

                    return down_index
                
            # if down index does not exist, return the straight index
                
            elif down_index[0] > rows - 1:

                return straight_index
            
            else:
                # if everything exists, calculate the cost for each possible position

                straight_cost = self.calculate_cost(current_pixel, straight_index, elavation_data)

                down_cost = self.calculate_cost(current_pixel, down_index, elavation_data)

                up_cost = self.calculate_cost(current_pixel, up_index, elavation_data)

                if up_cost == down_cost:

                    # coin flip between two options

                    return random.choice([up_index, down_index])

                if straight_cost == down_cost and straight_cost == up_cost:

                    return straight_index
                
                if up_cost < straight_cost and up_cost < down_cost:

                    return up_index
                
                if straight_cost < down_cost:

                    return straight_index

                return down_index
                


    def calculate_cost(self, current_pixel:tuple, next_pixel:tuple, elavation_data:list) -> int:

        """
        Docstring for calculate_cost
        
        :param self: MountainMapper object
        :param current_pixel: Pixel we are currently on
        :type current_pixel: tuple
        :param next_pixel: Possible pixel we could travel to
        :type next_pixel: tuple
        :param elavation_data: Matrix of all possible elavations
        :type elavation_data: list
        :return: The cost of traveling to next_pixel
        :rtype: int

        Calculates the cost of travelling from the current pixel to another
        """

        return int(elavation_data[current_pixel[0]][current_pixel[1]]) - int(elavation_data[next_pixel[0]][next_pixel[1]])
            

    def convert_to_jpeg(self, image_matrix:list):
        
        """
        Docstring for convert_to_jpeg
        
        :param self: MountainMapper object
        :param image_matrix: matrix of pixels that create image
        :type image_matrix: list

        Transforms image_matrix into a JPEG image

        """
        jpeg = Image.fromarray(image_matrix, "RGB")

        jpeg.save("output/output.jpg")

        

def main():

    m = MoutainMapper("Colorado_480x480.dat")
    #m = MoutainMapper("mini.dat")

main()

