if __name__ == '__main__':
    first_number = 1
    second_number = first_number
    second_number += 1

    print "\nInteger assignment example:"
    print "second_number =", second_number, "first_number = ", first_number

    first_list = [1]
    second_list = first_list
    second_list[0] += 1

    print "\nDefault list assignment example"
    print "second_list = ", second_list, "first_list =", first_list

    first_list[0] = 1
    second_list = first_list[:] #slice [:] is the python slice operator
                                # can b eused to make sub lists
                                #but, crucially. It also makes a copy
    second_list[0] += 1         #here, only second_list is incremented
                                #the same list
    print "\nSliced (copied list assignment example"
    print "second_list =", second_list, "first_name =", first_list, "\n"
