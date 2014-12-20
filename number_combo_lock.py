#The recursive method below was originally written by GitHub user Mariatta, and has been slightly adapted for use.
#The original code can be found here: https://github.com/Mariatta/permutation
#The recursive permutation method is much faster than the iterative method but is limited to 999 calls.

def number_combo_lock_recursive(items_to_permute):
    all_permutations = []  # contains a list of permutations found
    def permute(items_to_permute):
        """
        Recursive method to collect permutations
        :param items_to_permute: A list of items to permute
        """
        if not isinstance(items_to_permute, list):
            items_to_permute = [items_to_permute]
        if not items_to_permute in all_permutations:
            all_permutations.append(items_to_permute)
        if len(items_to_permute) > 1:
            for i in xrange(0, len(items_to_permute)):
                # iterate through each items, and shift it to the back of the list
                # eg if we have ABCD
                # first shift A to the back, eg BCD A
                # second shift B to the back, eg ACD B
                # third shift C to the back, eg ABD C
                # then permute each newly found combination
                # eg call permute on BCDA, ACDB, ABDC
                item_to_shift = items_to_permute[i]
                head = []
                tail = []
                if i != 0:
                    head = items_to_permute[0:i]
                if i != len(items_to_permute):
                    tail = items_to_permute[i + 1:]
                new_combo = head + tail + [item_to_shift]
                if not new_combo in all_permutations:
                    all_permutations.append(new_combo)
                    permute(new_combo)

    def main():
        permute(range(items_to_permute))  #unfortunately Python is limited to 999 calls.
        for combo in all_permutations:
            print combo
        print "%s permutations found " % len(all_permutations)

    if __name__ == "__main__":
        main()

num = number_combo_lock_recursive(6)
print num

#Since the recursive method above is limited by Python to 999 calls, for larger sets of numbers we will need to use
#an iterative method. The function below is an adaptation of Tom Switzer's code,
#which can be found here: https://github.com/tixxit/permute

def number_combo_lock_iterative(lst, k):
    # Copyright (c) 2009, Tom Switzer <thomas.switzer@gmail.com>
    #
    # Permission to use, copy, modify, and/or distribute this software for any
    # purpose with or without fee is hereby granted, provided that the above
    # copyright notice and this permission notice appear in all copies.
    #
    # THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    # WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    # MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    # ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    # WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    # ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    # OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

    """
    The permute module defines iterators that run over all the permutations or
    combinations of lists.
    """

    def _invert(lst, l, r):
        for i in range((r - l + 1) / 2):
            lst[l + i], lst[r - i] = lst[r - i], lst[l + i]

    def _binary_search(lst, val, l=0, r=-1, cmp=cmp, reverse=False):
        r = r > l and r or len(lst)
        sgn = reverse and -1 or 1
        while l < r:
            c = (l + r) / 2
            if lst[c] == val:
                return c
            l, r = (sgn * cmp(lst[c], val)) < 0 and (c + 1, r) or (l, c)
        return l

    def permutations(lst):
        """
        Returns an iterator whose .next() method returns all possible
        permutations of lst in lexicographical order.

        A permutation is a bijective mapping p: {0,1,..,n-1}->{0,1,..,n-1}. If
        n is the length of lst, then a permutation of lst is a list whose
        i-th element is the p(i)-th element in lst; that is,
        [lst[p(0)], lst[p(1)], .., lst[p(n-1)]]. The iterator returned by this
        function will iterate through all possible (n!) mappings
        p: {0,1,..,n-1}->{0,1,..,n-1}. It starts with the mapping p(i) = i, and
        proceeds in lexicographical order for p(0), p(1), .., p(n-1), ending with
        the permutation p(i) = n - i - 1.

        All permutations of [2, 4, 5]:

         #   >>> print [x for x in permutations([2,4,5])]
            [[2, 4, 5], [2, 5, 4], [4, 2, 5], [4, 5, 2], [5, 2, 4], [5, 4, 2]]

        It is good to remember that the order of the permutations is in
        lexicographical order of the indices of lst and not the values.

        #>>> print [x for x in permutations([2,3,1])]
        [[2, 3, 1], [2, 1, 3], [3, 2, 1], [3, 1, 2], [1, 2, 3], [1, 3, 2]]

        We can confirm that this returns len(lst)! items:

            #>>> print len([x for x in permutations(range(8))])
            40320
            #>>> def fac(n): return reduce(lambda y, x: y * x, range(1, n + 1))
            #>>> print fac(8)
            40320

        @param lst: An indexable object
        """
        p, t = range(len(lst)), type(lst)
        while True:
            yield t(lst[i] for i in p)
            flip = len(p) - 2
            while flip >= 0 and p[flip] > p[flip + 1]:
                flip -= 1
            if flip < 0:  # Is p in reverse-sorted order?
                return
            else:
                next = _binary_search(p, p[flip], l=flip + 1, reverse=True) - 1
                p[flip], p[next] = p[next], p[flip]
                _invert(p, flip + 1, len(p) - 1)

    def combinations(lst, k):
        """
        Returns an iterator whose .next() method returns all possible sets of size
        C{k} of C{lst}.

        This should be thought of in the sense of the choose method; how
        many ways can C{k} items be chosen from C{lst}, where the order of those
        items does not matter. As an example:

        Print all combinations of sets of size 2 from [0, 1, 2, 3]

           # >>> print [x for x in combinations(range(4), 2)]
            [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]

        Assure that the number of items generated is C{len(lst)} choose C{k}

            #>>> print len([x for x in combinations(range(11), 4)])
            330
            #>>> def fac(n): return reduce(lambda y, x: y * x, range(1, n + 1))
            #>>> print fac(11) / (fac(4) * fac(11 - 4))
            330

        @param lst: An indexable object
        @param k  : Size of the combinations
        """
        indices, tail, t = range(k), len(lst) - k, type(lst)
        while indices[0] <= tail:
            yield t(lst[i] for i in indices)
            for i in xrange(k - 1, -1, -1):
                indices[i] += 1
                for j in xrange(i + 1, k):
                    indices[j] = indices[j - 1] + 1
                if indices[i] <= tail + i:
                    break

    def permutations_of_combinations(lst, k):
        """Returns all permutations of k-combinations of lst."""
        for cmb in combinations(lst, k):
            for perm in permutations(cmb):
                yield perm

    num = [x for x in permutations_of_combinations(range(lst), k)]
    return num

num =  number_combo_lock_iterative(10, 8)
print num

#We may want to display every combination of digits (i.e. every unique number) as an integer.
#The function I wrote below takes the array of numbers outputted in the iterative process and converts them
#to integers. NOTE: The recursive method has not been updated to take advantage of this translation function.

def translate(numList, loopprint):
    num = numList
    numtrans = []
    for i in range(len(num)):
        num[i] = map(str, num[i])
        num[i] = ''.join(num[i])
        num[i] = int(num[i])
        if loopprint == 1:
            print num[i]
        numtrans.append(num[i])
    return numtrans

trans = translate(num, 1)
print trans
