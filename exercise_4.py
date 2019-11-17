# function to find maximum of two values 
def maximum(x,y):
    if x>y:
        return x
    else:
        return y


def long_palindromic_seq(str): 
    n = len(str) 
  
    # Creating a table to store results of subproblems 
    L = [[0 for x in range(n)] for x in range(n)] 
  
    # Strings of length 1 are palindrome of length 1 
    for i in range(n): 
        L[i][i] = 1
   
    for c in range(2, n+1): 
        for i in range(n-c+1): 
            j = i+c-1
            if str[i] == str[j] and c == 2: 
                L[i][j] = 2
            elif str[i] == str[j]: 
                L[i][j] = L[i+1][j-1] + 2
            else: 
                L[i][j] = maximum(L[i][j-1], L[i+1][j]); 
  
    return L[0][n-1]

# testing the code 
seq = "DATAMININGSAPIENZA"
print("The length of the Longest palindromic sequence is " + str(long_palindromic_seq(seq)))
