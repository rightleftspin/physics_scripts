import numpy as np

# "Empty, up, right, left, down"

states = ["e", "u", "r", "l", "d"]

def check_mat(mat, col, row):
    col_works = np.dot(mat, np.ones(len(col))) == col 
    row_works = np.dot(np.transpose(mat), np.ones(len(row))) == row 

    return(col_works and row_works)

def update_around(mat, current_spot):
    # Check boundries 

column_sum = [4, 2, 2, 15, 4, 5, 4, 12, 8, 4, 7, 2, 2, 2, 4, 4, 1]
row_sum = [1, 1, 6, 1, 11, 1, 5, 7, 1, 6, 1, 1, 9, 3, 5, 2, 2, 2, 2 ,5, 2, 8]

sol_mat = np.zeros((len(row_sum), len(column_sum)))

sol_mat[0, 15] = 1
sol_mat[1, 15] = 1
sol_mat[2, 15] = 1
sol_mat[2, 14] = 1





