def index_of_element_at(elements, x):
    #TODO Binary Search
    for i in range(len(elements)):
        if (x >= elements[i].x_start) & (x < elements[i].x_end):
            return i
    return None
