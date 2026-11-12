import string
from pathlib import Path
import pandas as pd

#--------------------------------------------------------------------------------------------
# Variables
#--------------------------------------------------------------------------------------------
letters = list(string.ascii_uppercase) #because assumption is that answers are in all caps
positions=['first', 'second', 'third', 'fourth', 'fifth']
vowels = ['A', 'E', 'I', 'O', 'U']
month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
short_month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
directory = directory = Path(__file__).parent / 'data'
partial_file_name = ('*.txt')

#--------------------------------------------------------------------------------------------
# Function to find the answer file
#--------------------------------------------------------------------------------------------
def find_latest_file(dir, partial_file_name):
    files = [f for f in dir.iterdir() if f.is_file()]
    if files:
    # Get the file with the maximum modification time
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
    return latest_file

#--------------------------------------------------------------------------------------------
# Get the data from answer file
#--------------------------------------------------------------------------------------------
text_file_name = find_latest_file(directory, partial_file_name)
df= pd.read_csv(text_file_name)
all_answers = df['Answer'].to_list()

last_date_str = str(df['Year'].iloc[-1]) + '-' + str(df['Month'].iloc[-1]) + '-' + str(df['Date'].iloc[-1])

month_name_num = month_names.index(df['Month'].iloc[-1]) + 1
last_date_val = str(df['Year'].iloc[-1]) + '-' + f"{month_name_num:02}" + '-' + str(df['Date'].iloc[-1])

#--------------------------------------------------------------------------------------------
# Functions to get counts and navigate the df
#--------------------------------------------------------------------------------------------
def get_letter_counts(answers):
    letter_position_counts = [[0 for i in range(0,5)] for letter in letters]
    for word in answers:
        for i, letter in enumerate(word):
            letter_position_counts[letters.index(letter)][i] += 1
    return letter_position_counts

def get_puzzle_num(date_str):
    s = date_str.split('-')
    #print(s)
    year_val = int(s[0])
    date_val = int(s[2])
    month_val = month_names[int(s[1]) - 1]
    num = df.loc[(df['Year'] == year_val) & (df['Month'] == month_val) & (df['Date'] == date_val), 'Puzzle_Number'].values[0]
    return num

def get_answers_between_dates(start_date, end_date):
    num1 = get_puzzle_num(start_date)
    num2 = get_puzzle_num(end_date)
    custom_df = df.loc[(df['Puzzle_Number'] >= num1) & (df['Puzzle_Number'] <= num2), 'Answer']
    custom_answers = custom_df.tolist()
    return custom_answers

def get_answers_for_year(year_val):
    result_df = df.loc[(df['Year'] == year_val), 'Answer']
    answers = result_df.tolist()
    return answers

def get_all_answers():
    answers = df['Answer'].tolist()
    return answers

def get_puzzle_number(answer):
    result_df = df.loc[(df['Answer'] == answer), 'Puzzle_Number']
    puzzle_numbers = result_df.tolist()
    return puzzle_numbers

def get_dates_list(answer):
    date_df = df.loc[(df['Answer'] == answer)]
    date_str_list = []
    for row in date_df.itertuples():
        month_name_num = month_names.index(row.Month)
        date_str = str(row.Year)+f"{month_name_num:02}"+f"{row.Date:02}"
        date_str_list.append(date_str)
    return date_str_list

def get_counts_by_month_for_year(year_val, month_val):
    answers_df = df.loc[(df['Year'] == year_val) & (df['Month'] == month_val), 'Answer']
    answers = answers_df.tolist()
    letter_counts = get_letter_counts(answers)
    return letter_counts

def get_years():
    year_list = list(set(df['Year'].tolist()))
    return year_list
#============================================================================================
df_duplicates = df[df.duplicated(subset=['Answer'], keep="first")]
df_duplicates_answers_list = df_duplicates['Answer'].tolist()

df_duplicates_all = df[df.duplicated(subset=['Answer'], keep=False)]
sorted_duplicates = df_duplicates_all.sort_values(by='Answer')

#print(df_duplicates.to_string(index=False))
#print(sorted_duplicates.to_string(index=False))
#print(df_duplicates_answers_list)

'''
answers = get_all_answers()
letter_counts = get_letter_counts(answers)

index_names = [f"<button type='button' onclick=\"show_letter_graph('{letter_name}')\">{letter_name}</button>" for letter_name in letters]
column_names = [f"<button type='button' onclick=\"show_position_graph('{position_name}')\">{position_name}</button>" for position_name in positions]

counts_df = pd.DataFrame(letter_counts, index=index_names, columns=column_names)
'''
def color_max_min(val, min_val, max_val):
    if val == min_val:
        bg_color = 'gray'
    elif val == max_val:
        bg_color = 'green'
    else:
        bg_color = 'white'
    return f'background-color: {bg_color};'

def map_style_to_df(df):
    min_val_list = []
    max_val_list = []
    column_names = df.columns
    for column in column_names:
        min_val_list.append(df[column].min())
        max_val_list.append(df[column].max())

    styled_df = (
        df.style
        .map(color_max_min, subset=[column_names[0]], min_val=min_val_list[0], max_val=max_val_list[0])
        .map(color_max_min, subset=[column_names[1]], min_val=min_val_list[1], max_val=max_val_list[1])
        .map(color_max_min, subset=[column_names[2]], min_val=min_val_list[2], max_val=max_val_list[2])
        .map(color_max_min, subset=[column_names[3]], min_val=min_val_list[3], max_val=max_val_list[3])
        .map(color_max_min, subset=[column_names[4]], min_val=min_val_list[4], max_val=max_val_list[4])
    )

    html_output = styled_df.to_html(escape=False, classes='data')
    return html_output


#html_output = style_table_df.to_html(escape=False)
'''
with open('table.html', 'w') as f:
    f.write(map_style_to_df(counts_df))
'''
'''
df = pd.DataFrame({
    'Item': ['Apples', 'Bananas', 'Cherries'],
    'Profit': [120, -45, 80],
    'Stock': [50, 12, 5]
})

def highlight_low_stock(val, min_val, max_val):
    if val == min_val:
        bg_color = 'gray'
    elif val == max_val:
        bg_color = 'green'
    else:
        bg_color='white'
    return f'background-color: {bg_color};' 

styled_df = (
    df.style
    .map(highlight_low_stock, subset=['Stock'], min_val=5, max_val=50)
    .map(highlight_low_stock, subset=['Profit'], min_val=-45, max_val=120)
)

html_output = styled_df.to_html()

with open('table.html', 'w') as f:
    f.write(html_output)
'''
#.............................................................................................
'''
answers = get_all_answers()
letter_counts = get_letter_counts(answers)

counts_df = pd.DataFrame(letter_counts, index=letters, columns=positions)

print(counts_df)
max_first = counts_df['first'].max()
min_first = counts_df['first'].min()
#print(max_first)

def color_max_min(val):
    if val == max_first:
        color = 'green'
    elif val == min_first:
        color = 'gray'
    else:
        color = 'black'
    return f'color: {color}; font-weight: bold;'

# Apply only to the'Change' column and export to HTML
styled_df = counts_df.style.map(color_max_min, subset=['first'])
html_output = styled_df.to_html()
with open('table.html', 'w') as f:
    f.write(html_output)


#to get min of a row
min_val_for_A = counts_df.loc['A'].min()
print(min_val_for_A)
'''
'''
print("--------------------------------")
print("Letter with max occurrences by position:")
print("--------------------------------")
for pos in positions:
    print(pos,  counts_df[pos].idxmax())

print("--------------------------------")
print("Letter with max occurrences by position:")
print("--------------------------------")
for pos in positions:
    print(pos ,  counts_df[pos].idxmin())

print("--------------------------------")
print("Max occurrences of letter were in:")
print("--------------------------------")

max_in_row = counts_df.eq(counts_df.max(axis=1), axis=0)
print(max_in_row)

print("--------------------------------")
print("Least occurrences of letter were in:")
print("--------------------------------")

min_in_row = counts_df.eq(counts_df.min(axis=1), axis=0)

min_cols = min_in_row.apply(lambda row: row[row].index.tolist(), axis=1)
print(min_cols)
'''






