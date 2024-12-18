def add_elements(first, second = 1):
    result = first + second
    return result

list_first = [1, 2, 3]
list_second = [4,5,6]

# for 이해
result_list = list()
# use one parameter
# for number_first in list_first:
#     result = add_elements(number_first)
#     result_list.append(result)
# result_list
# pass

# use two parameters
for number_first, number_second in zip(list_first, list_second):
    result = add_elements(number_first, number_second)
    result_list.append(result)
result_list
pass


# map() : callback function// looping돌때 만들어놓은 특정 function, network
#one parameter
# result_map = map(add_elements, list_first)
# result_map_list = list(result_map)
# pass

#two parameter
# result_map = map(add_elements, list_first, list_second)
# result_map_list = list(result_map)
# pass

# apply() with pandas
data = {'col_first': list_first
        , 'col_second' : list_second}

import pandas as pd
df_first = pd.DataFrame(data)
pass

#one parameter : series
# result_df = df_first['col_first'].apply(add_elements)
# pass

#over two parameter : dataframe
def add_elements_df(series_bundle):
    result = series_bundle['col_first'] + series_bundle['col_second']
    return result
    pass
#결측치 채우고 덮어씌우는 기능

df_first['add_elements'] = df_first.apply(add_elements_df, axis = 1)
pass