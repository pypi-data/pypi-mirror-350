def repeat_cons_n(s: str, numRows: int, delimiter: str, epoch: int, separator: str)->str:
    
    # Primary intializations
    inc_matrix_col = 1
    count = 0
    remaining = []
    
    last_col = 0
    
    cols = len(s)
    
    matrix = [['' for _ in range (cols)] for _ in range (numRows)]
    
    # Creating numRows columnary filling
    for j in range (0, cols, cols + numRows):
        for i in range(numRows):
            for k in s:
                if count < numRows:
                    matrix[i][j] += k
                else:
                    for m in range (k+1, k+3):
                        remaining.append(s[k])
                    k = numRows + 2
    
    
    #Arranging the patterns
        # I]
    if numRows % 2 == 1:
        for c in range (len(s)):
            c_new = c
            for d in range(0, len(remaining)):
                while(c_new == 1 or c_new == c + numRows - 1 ):
                    matrix[numRows//2][c_new] = remaining[d]
                c_new += 1
                c = c_new
    
    
        # II]
    result = ""
    
    q = numRows - 1
    
    if numRows % 2 == 0:
        for d in range(0, len(remaining)):
            for c in range (len(s)):
                c_new = c
                while(c_new == 1 or c_new == c + numRows - 1):
                    matrix[q][c_new] = remaining[d]
                    q -= 1
                
                q = numRows - 1
    
    
    # Creating string
    for x in range(numRows):
        for y in range(len(s)):
            result += matrix[x][y]
        result += delimiter
    result += separator
            
    
    # print(matrix)
    
    # string s will be printed numRows times, n times
    print(result * epoch)


# Call the function
# repeat_cons_n("Hello World", 2, "->>", 9, "")





