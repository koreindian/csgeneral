import math

def main():
    print(prob_dominant_child(2,2,2))
    print(prob_dominant_child(27,23,24))

# Given: three positive integers k, m, n representing a population
# containing k + m + n organisms: k individuals are homozygous
# dominant for a factor, m are heterzygous, and n are homozygous
# recessive.
# Return: The probability that two randomly selected mating organisms 
# will produce an individual possessing a dominant allele.
def prob_dominant_child(k, m, n):
    num_pairs = choose(k + m + n, 2)
    
    # Calculate expected number of homozygous recessive children
    homozygous_recessive = 0

    # With homozygous recessive parents
    homozygous_recessive += choose(n, 2)

    # With one homozygous recessive parent and one heterozygous
    homozygous_recessive += 0.50 * (m * n)

    # With two heterozygous parents
    homozygous_recessive += 0.25 * choose(m, 2)

    return 1 - homozygous_recessive / num_pairs

def choose(n, r):
    f = math.factorial
    return f(n) // (f(r) * f(n - r))


if __name__ == '__main__':
    main() 
