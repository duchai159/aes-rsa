import random

def get_prime(bits):
    """
        Sinh ngẫu nhiên số nguyên tố, kích thước bits
    """
    while True:
        prime_candidate = __get_low_level_prime(bits)
        if __miller_rabin_test(prime_candidate, k=20):
            return prime_candidate

def get_small_primes(number):
    """
        Sử dụng sàn Eratosthenes
        Tìm danh sách các số nguyên tố <= number
        Get small primes using Sieve of Eratosthenes algorithm. 
        Return a list with primes smaller than or equal to number. It is also given that n is a small number.
    """
    # list of primes up to number
    list_of_primes = []       

    # Create a boolean array "prime[0..n]" and initialize  all entries it as true:
    prime = [True for i in range(number+1)]
    # first prime
    p = 2
    
    # algorithm:
    while p * p <= number:
        if prime[p] == True:
            # Update all multiples of p
            for i in range(p * p, number+1, p):
                prime[i] = False
        p+=1
    
    # return list of primes
    for i in range(number):
        if prime[i] == True:
            list_of_primes.append(i)        

    # Bỏ 2 số đầu tiên (là 0 và 1)
    return list_of_primes[2:]

# get all primes up to 1000
list_of_primes = get_small_primes(1000)

def __get_low_level_prime(bits=1024):
    """
        The prime candidate is divided by the pre-generated primes to check for divisibility.
        Division with first primes to check for divisibility. If the Prime candidate is divisible 
        by any of the generated primes prior, the test fails and we take a new prime.
        This is repeated as long as a value which is coprime to all the primes in our generated
        primes list is found.
    """

    while True:
        # Obtain a random number
        prime_candidate = __random_number(bits=bits) 
        divisor_found = False
        for divisor in list_of_primes: 
            if prime_candidate % divisor == 0 and divisor  ** 2 <= prime_candidate:
                divisor_found= True
                break
        
        # If no divisor found, return value
        if not divisor_found:
            return prime_candidate   

# return number of bit size n private function:
def __random_number(bits):
    """Generate number from 2^{bits-1} to 2^bits"""
    return(random.randrange(2**(bits-1), 2**bits-1))

def __miller_rabin_test(n, k=10):
    """Miller Rabin test for k iterations"""
    for i in range(k):
        a = random.randrange(2, n - 1)
        if not __single_test(n, a):
            return False
    return True

def __single_test(n, a):
    """One iteration of miller rabin test"""
    exp = n - 1
    while not exp & 1:
        exp >>= 1
            
    if pow(a, exp, n) == 1:
        return True
            
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1
            
    return False
    