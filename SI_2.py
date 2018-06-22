__author__ = "Paweł Bernecki"

import CSP


def main():
    """
    task:
        0 - N queens
        1 - Latin square
        
    size:


    algorithm:
        0 - forward checking
        1 - backtracking 
        
    """
    size = int(input("Specify the desired size of the board: "))
    csp = CSP.CSP(task=1, size=size)
    results = csp.start(algorithm=1)
    # for r in results:
    #    print(r)
    print("Solutions found: ", len(results[0]), "Number of iterations: ", results[1])
    


if __name__ == '__main__':
    main()

