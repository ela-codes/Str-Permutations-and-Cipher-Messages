# Problem Set 4A
# Name: Aena Teodocio
# Collaborators:
# Time Spent: x:xx

def get_permutations(word):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    '''

    # base case
    if len(word) == 1: # base case
        return [word]

    elif len(word) == 2: # 2! of possible combinations
        perms = []
        for i in word:
            perms += [i + j for j in word if j != i]
        return perms

    else: 
        # apply combinations by dropping each first unique letter
        # do recursive calls to reduce remainig letters into pairs of two
        # re-join when done & repeat until last unique letter is reached
        # Exampe: 'ABC' 
        # drop A -> find permutations for BC -> ['BC', 'CB'] -> join A to both perms -> ['ABC', 'ACB']
        
        result = []
        for i in word:
            remaining = [other for other in word if other != i]
            result.extend([i + word for word in get_permutations(remaining)])

    return result



if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    test_cases = {'abc': ['abc', 'acb', 'bac', 'bca', 'cba', 'cab']}
    for i in test_cases:
           print('Input:', i)
           print('Expected Output:', sorted(test_cases[i]))
           print('Actual Output:', sorted(get_permutations(i)))
           print('-------------------')
