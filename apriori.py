from math import ceil
from itertools import combinations
from collections import defaultdict

MIN_SUPPORT_PERCENT = 0.035

# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A dictionary of transactions and a set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    for line in input_file:
        lines = line.split('\t')
        transactions[lines[0]] = lines[1:-1]
    #getting all distinct items
    for i in transactions.values():
        for j in i:
            itemset.add(j)
    return transactions, itemset


# This function calculates support of the itemset from transactions
# param transactions: All transactions in a dictionary
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def support(transactions, itemset):
    support_count = 0
    tuple1 = tuple(itemset)

    #counting occurrence of items
    for j in transactions.values():
        list1 = set(j)
        if list1.issuperset(tuple1):
            support_count +=1
    return support_count


# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):

    # Record seen_itemsets to prevent duplicates
    seen_itemsets = set()
    joined_itemsets = set()
    comb = list()

    ##2 is special case
    if itemset_size == 2:
        comb = combinations(frequent_itemsets[1], 2)
        joined_itemsets = set(comb)

    else:
        comb = list(frequent_itemsets[itemset_size-1])
        for i in range(0, len(comb) -1):
            for j in range(1, len(comb)):
                temp1 = set(comb[i])
                temp2 = set(comb[j])
                k = temp1.union(temp2)
                if  len(k) == itemset_size:
                    if k not in seen_itemsets:
                        joined_itemsets.add(frozenset(k))
                        seen_itemsets.add(frozenset(k))

    return joined_itemsets


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    apriori_pruned_itemsets = set()

    bad = False
    if itemset_size > 2 :
            for i in selected_itemsets:
                comb = set(list(combinations(i, itemset_size-1)))
                for j in comb:
                    if len(frequent_itemsets[itemset_size-1].intersection(j)) > 0:
                        bad = True
                        break
                if bad == False:
                    apriori_pruned_itemsets.add(i)
                bad = False
    else:
        #Two never gets pruned
        apriori_pruned_itemsets.add(tuple(selected_itemsets))

    return apriori_pruned_itemsets


# This function generates candidate itemsets of size (itemset_size) by selective joining and apriori pruning
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: candidate itemsets formed by selective joining and apriori pruning
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets


# This function generates a table of itemsets with all frequent items from transactions based on a given minimum support
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent itemsets of different sizes
def generate_all_frequent_itemsets(transactions, items, min_support):
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = list()
    frequent_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()

    item_counts = defaultdict(int)
    for i in transactions.values():
        for j in i:
            item_counts[j] += 1
    temp_list = list()
    for i in item_counts:
        if item_counts[i] >= min_support:
            temp_list.append(i)
    frequent_itemsets[itemset_size] = temp_list

    itemset_size += 1

    #generating the frequent itemsets for >= 2
    while frequent_itemsets[itemset_size-1]:
        frequent_itemsets[itemset_size] = list()
        count = defaultdict(int)
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size)
        pruned_itemset = set()
        for i in candidate_itemsets:
            if itemset_size == 2:
                for k in i:
                    count = support(transactions, k)
                    if count >= min_support:
                        pruned_itemset.add(tuple(k))
                    frequent_itemsets[itemset_size] = pruned_itemset
            else:
                count = support(transactions, i)
                if count >= min_support:
                    pruned_itemset.add(tuple(i))
                frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    size = len(frequent_itemsets_table)
    for i in range (2, size):
        for _ in frequent_itemsets_table[i]:
            file.write("{")
            count = support(transactions, _)
            size = len(_)
            count1= 0
            for j in _:
                file.write(str(j))
                count1 += 1
                if count1 != size:
                    file.write(", ")
            file.write("}")
            file.write(" " + str(format((count/len(transactions))*100, '.2f')) + "% support" + "\n")
    file.close()

# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'result.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)

if __name__ == '__main__':
    main()
