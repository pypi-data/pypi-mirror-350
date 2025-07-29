import pandas as pd
import re
import os


input_file = "/media/edabk/ST_500G_disk1/huongnhai/nhai/KMAP/kmap_results_test_v2.xlsx" 
df = pd.read_excel(input_file)

# Create output directory for LaTeX files
output_latex_dir = "/media/edabk/ST_500G_disk1/huongnhai/nhai/KMAP/output"
os.makedirs(output_latex_dir, exist_ok=True)


def parse_groups(groups_str):
    """Parse groups from the string in the format: GROUP1 (1, 2, 3)"""
    groups = []
    if pd.notna(groups_str):
        for line in groups_str.split('\n'):
            match = re.search(r'GROUP\d+\s*\((.*?)\)', line)
            if match:
                groups.append(match.group(1))
    return groups


def generate_kmap(vars, minterms, dontcares):
    """Generate K-map from the given minterms and don't cares"""
    minterms = [int(x) for x in minterms.split(',') if x.strip().isdigit()]
    if isinstance(dontcares, str):
        dontcares = [int(x) for x in dontcares.split(',') if x.strip().isdigit()]
    else:
        dontcares = []

    if len(vars.split(',')) == 4:  #four variable
        kmap = [[0 for _ in range(4)] for _ in range(4)]
        mapping = [
            (0, 0, 0), (0, 1, 1), (0, 2, 3), (0, 3, 2),
            (1, 0, 4), (1, 1, 5), (1, 2, 7), (1, 3, 6),
            (2, 0, 12), (2, 1, 13), (2, 2, 15), (2, 3, 14),
            (3, 0, 8), (3, 1, 9), (3, 2, 11), (3, 3, 10)
        ]
    else: #three variable
        kmap = [[0 for _ in range(4)] for _ in range(2)]
        mapping = [
            (0, 0, 0), (0, 1, 1), (0, 2, 3), (0, 3, 2),
            (1, 0, 4), (1, 1, 5), (1, 2, 7), (1, 3, 6)
        ]
    
    for row, col, val in mapping:
        if val in minterms:
            kmap[row][col] = 1
        elif val in dontcares:
            kmap[row][col] = 'x'
    
    return kmap, mapping

def kmap_to_latex(kmap, is_4var=True):

    """Convert K-map to LaTeX"""

    rows = 4 if is_4var else 2
    if rows == 4: #four variable
        latex = "\\[\\begin{array} {|c|c|c|c|c|} \\hline ab \\backslash cd & 00 & 01 & 11 & 10 \\\\ \\hline "
        for i in range(rows):
            row_label = "00" if i == 0 else "01" if i == 1 else "10" if i == 3 else "11"
            latex += f"{row_label} & {' & '.join(str(kmap[i][j]) for j in range(4))} \\\\ \\hline "
        latex += "\\end{array}\\]"
    elif rows == 2: #three variable
        latex = "\\[\\begin{array} {|c|c|c|c|c|} \\hline a \\backslash bc & 00 & 01 & 11 & 10 \\\\ \\hline "
        for i in range(rows):
            row_label = "0" if i == 0 else "1"
            latex += f"{row_label} & {' & '.join(str(kmap[i][j]) for j in range(4))} \\\\ \\hline "
        latex += "\\end{array}\\]"        
    return latex

def get_cell_positions(group, mapping):
    """Get the cell positions for a group in the format of row-col pairs"""
    cells = []
    for item in group.strip().split(','):
        value = int(item.strip())
        for row, col, val in mapping:
            if val == value:
                cells.append((row, col))
    return cells


def generate_tikz_code(kmap, group_cells_list, is_4var=True):
    """Generate TikZ code for highlighting groups in the K-map"""
    rows = 4 if is_4var else 2
    cols = 4
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'brown']
    
    tikz_begin = "\\begin{tikzpicture}[overlay, remember picture]\n"
    tikz_end = "\\end{tikzpicture}"
    
    # Create cells with TikZ nodes
    array_code = "$\\begin{array}{|c|" + "c|" * cols + "} \\hline\n"
    
    if is_4var:
        array_code += "ab \\backslash cd & 00 & 01 & 11 & 10 \\\\ \\hline\n"
        for i in range(rows):
            row_label = "00" if i == 0 else "01" if i == 1 else "11" if i == 2 else "10"
            array_code += f"{row_label} & "
            for j in range(cols):
                value = kmap[i][j]
                array_code += f"\\tikz[baseline]{{\\node (cell{i}-{j}) {{${value}$}};}}"
                if j < cols - 1:
                    array_code += " & "
            array_code += " \\\\ \\hline\n"
    else:
        array_code += "a \\backslash bc & 00 & 01 & 11 & 10 \\\\ \\hline\n"
        for i in range(rows):
            row_label = "0" if i == 0 else "1"
            array_code += f"{row_label} & "
            for j in range(cols):
                value = kmap[i][j]
                array_code += f"\\tikz[baseline]{{\\node (cell{i}-{j}) {{${value}$}};}}"
                if j < cols - 1:
                    array_code += " & "
            array_code += " \\\\ \\hline\n"
    
    array_code += "\\end{array}$"
    
    tikz_node = f"\\node (cell00) at (0,0) [inner sep=0pt] {{{array_code}}};\n"
    
    # Generate highlight rectangles for each group
    highlight_code = ""
    used_colors = []  # Theo dõi màu đã dùng để tránh trùng lặp
    
    for idx, cells in enumerate(group_cells_list):
        # Chọn màu chưa dùng hoặc quay lại từ đầu nếu hết
        color = colors[idx % len(colors)]
        if color in used_colors and idx < len(colors):
            color = colors[idx]  # Đảm bảo mỗi nhóm có màu khác nhau nếu có thể
        used_colors.append(color)
        
        if len(cells) == 1:
            # Single cell
            i, j = cells[0]
            highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
            highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-{j}.north west) \n"
            highlight_code += f"    rectangle \n"
            highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-{j}.south east);\n"
        else:
            # Xác định kích thước nhóm
            rows_in_group = sorted(set(i for i, j in cells))
            cols_in_group = sorted(set(j for i, j in cells))
            height = len(rows_in_group)
            width = len(cols_in_group)

            # Nhóm quấn quanh góc (4 ô ở 4 góc)
            if is_4var and len(cells) == 4 and (0, 0) in cells and (0, 3) in cells and (3, 0) in cells and (3, 3) in cells:
                for i, j in [(0, 0), (0, 3), (3, 0), (3, 3)]:
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-{j}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-{j}.south east);\n"
            # Kiểm tra quấn quanh ngang
            elif width == 2 and 0 in cols_in_group and 3 in cols_in_group and all(j in [0, 3] for i, j in cells):
                for i in rows_in_group:
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-0.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-0.south east);\n"
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-3.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-3.south east);\n"
            # Kiểm tra quấn quanh dọc (chỉ cho 4 biến)
            elif is_4var and height == 2 and 0 in rows_in_group and 3 in rows_in_group and all(i in [0, 3] for i, j in cells):
                for j in cols_in_group:
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell0-{j}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell0-{j}.south east);\n"
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell3-{j}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell3-{j}.south east);\n"
            # Nhóm quấn quanh toàn bộ (4x4 hoặc 2x4)
            elif (is_4var and height == 4 and width == 4) or (not is_4var and height == 2 and width == 4):
                highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell0-0.north west) \n"
                highlight_code += f"    rectangle \n"
                highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{rows-1}-{cols-1}.south east);\n"
            # Nhóm thông thường
            else:
                min_row = min(i for i, j in cells)
                max_row = max(i for i, j in cells)
                min_col = min(j for i, j in cells)
                max_col = max(j for i, j in cells)
                
                if len(cells) in [1, 2, 4, 8] and (max_row - min_row + 1) * (max_col - min_col + 1) == len(cells):
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{min_row}-{min_col}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{max_row}-{max_col}.south east);\n"
    
    return f"\\[\n{tikz_begin}\n{tikz_node}\n{highlight_code}\n{tikz_end}\n\\]"

# def generate_tikz_code(kmap, group_cells_list, is_4var=True):
    """Generate TikZ code for highlighting groups in the K-map"""
    rows = 4 if is_4var else 2
    cols = 4
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'brown']
    
    tikz_begin = "\\begin{tikzpicture}[overlay, remember picture]\n"
    tikz_end = "\\end{tikzpicture}"
    
    # Create cells with TikZ nodes
    array_code = "$\\begin{array}{|c|" + "c|" * cols + "} \\hline\n"
    
    if is_4var:
        array_code += "ab \\backslash cd & 00 & 01 & 11 & 10 \\\\ \\hline\n"
        for i in range(rows):
            row_label = "00" if i == 0 else "01" if i == 1 else "11" if i == 2 else "10"
            array_code += f"{row_label} & "
            for j in range(cols):
                value = kmap[i][j]
                array_code += f"\\tikz[baseline]{{\\node (cell{i}-{j}) {{${value}$}};}}"
                if j < cols - 1:
                    array_code += " & "
            array_code += " \\\\ \\hline\n"
    else:
        array_code += "a \\backslash bc & 00 & 01 & 11 & 10 \\\\ \\hline\n"
        for i in range(rows):
            row_label = "0" if i == 0 else "1"
            array_code += f"{row_label} & "
            for j in range(cols):
                value = kmap[i][j]
                array_code += f"\\tikz[baseline]{{\\node (cell{i}-{j}) {{${value}$}};}}"
                if j < cols - 1:
                    array_code += " & "
            array_code += " \\\\ \\hline\n"
    
    array_code += "\\end{array}$"
    
    tikz_node = f"\\node (cell00) at (0,0) [inner sep=0pt] {{{array_code}}};\n"
    
    # Generate highlight rectangles for each group
    highlight_code = ""
    for idx, cells in enumerate(group_cells_list):
        color = colors[idx % len(colors)]
        
        if len(cells) == 1:
            # Single cell
            i, j = cells[0]
            highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
            highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-{j}.north west) \n"
            highlight_code += f"    rectangle \n"
            highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-{j}.south east);\n"
        else:
            # Xác định kích thước nhóm (chiều cao và chiều rộng)
            rows_in_group = sorted(set(i for i, j in cells))
            cols_in_group = sorted(set(j for i, j in cells))
            height = len(rows_in_group)
            width = len(cols_in_group)

            # Kiểm tra quấn quanh ngang (wrap-around horizontally)
            if width == 2 and 0 in cols_in_group and 3 in cols_in_group and all(j in [0, 3] for i, j in cells):
                for i in rows_in_group:
                    # Vẽ hai hình chữ nhật: một ở cột 0, một ở cột 3
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-0.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-0.south east);\n"
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{i}-3.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{i}-3.south east);\n"
            # Kiểm tra quấn quanh dọc (wrap-around vertically, only for 4-var)
            elif is_4var and height == 2 and 0 in rows_in_group and 3 in rows_in_group and all(i in [0, 3] for i, j in cells):
                for j in cols_in_group:
                    # Vẽ hai hình chữ nhật: một ở hàng 0, một ở hàng 3
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell0-{j}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell0-{j}.south east);\n"
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell3-{j}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell3-{j}.south east);\n"
            # Kiểm tra nhóm quấn quanh toàn bộ (4x4 hoặc 2x4)
            elif (is_4var and height == 4 and width == 4) or (not is_4var and height == 2 and width == 4):
                highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell0-0.north west) \n"
                highlight_code += f"    rectangle \n"
                highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{rows-1}-{cols-1}.south east);\n"
            # Nhóm thông thường (không quấn quanh)
            else:
                min_row = min(i for i, j in cells)
                max_row = max(i for i, j in cells)
                min_col = min(j for i, j in cells)
                max_col = max(j for i, j in cells)
                
                # Kiểm tra nếu nhóm hợp lệ (kích thước là lũy thừa của 2)
                if len(cells) in [1, 2, 4, 8] and (max_row - min_row + 1) * (max_col - min_col + 1) == len(cells):
                    highlight_code += f"\\draw[{color}, thick, rounded corners=5pt, fill={color}!10, opacity=0.5] \n"
                    highlight_code += f"    ([xshift=-0.15cm, yshift=0.15cm]cell{min_row}-{min_col}.north west) \n"
                    highlight_code += f"    rectangle \n"
                    highlight_code += f"    ([xshift=0.15cm, yshift=-0.10cm]cell{max_row}-{max_col}.south east);\n"
    
    return f"\\[\n{tikz_begin}\n{tikz_node}\n{highlight_code}\n{tikz_end}\n\\]"

def kmap_to_tikz_latex(kmap, groups, mapping, is_4var=True):
    """Convert K-map to LaTeX with TikZ highlighting for groups"""
    # Process groups to get cell positions
    group_cells_list = []
    for group in groups:
        cells = get_cell_positions(group, mapping)
        group_cells_list.append(cells)
    
    # Generate TikZ code
    return generate_tikz_code(kmap, group_cells_list, is_4var)


def generate_latex(row):
    """Generate LaTeX for the given row"""
    func_match = re.search(r'f\((.*?)\) = (.*?)(?: \+ dontcares: (.*))?$', row['Function']) # f(a, b, c) = m(0, 1, 2, 3, 4, 5, 6, 7) + dontcares: 8, 9
    # re.search(r'f\((.*?)\) = (.*?) \+ dontcares: (.*)', row['Function'])
    if not func_match:
        return None, None, None

    vars = func_match.group(1)
    minterms = func_match.group(2).strip()
    dontcares = func_match.group(3).strip() if func_match.group(3) is not None else ""
    result_match = re.search(r'RESULT:\s*f\((.*?)\) = (.*)', row['Result'])
    result = result_match.group(2).strip() if result_match else ""
    groups = parse_groups(row['Groups'])

    flag_dontcare = func_match.group(3) is not None
    # print(flag_dontcare)

    data_input = f"\\textbf{{Problem}} Use the Karnaugh map method to simplify the following function: \\( f({vars}) = \\Sigma m({minterms}) + \\Sigma d({dontcares}) \\)" if flag_dontcare else f"\\textbf{{Problem}} Use the Karnaugh map method to simplify the following function: \\( f({vars}) = \\Sigma m({minterms}) \\)"

    # data_solution
    is_4var = len(vars.split(',')) == 4
    kmap, mapping = generate_kmap(vars, minterms, dontcares)
    kmap_tikz_latex = kmap_to_tikz_latex(kmap, groups, mapping, is_4var)
    kmap_latex = kmap_to_latex(kmap, is_4var)  # Định nghĩa hàm phù hợp

    
    # groups_latex = "\\[\\begin{array}{|c|c|} \\hline "
    # for i, group in enumerate(groups, 1):
    #     groups_latex += f"({group}) & {'term' + str(i)} \\\\ \\hline "
    # groups_latex += "\\end{array}\\]"
    
    data_solution = (
        "\\begin{enumerate} \n"
        "\\item Construct the K-map table. \\\\ We have " + str(len(vars.split(','))) + f" variables $({vars})$. Typically, a {'4-variable' if is_4var else '3-variable'} K-map is arranged as follows (in Gray code order): \\\\ \n"
        "Rows (based on "+('$ab$' if is_4var else '$a$')+"): \\begin{itemize} \\item " + ('00, 01, 11, 10' if is_4var else '0, 1') + " \\end{itemize} \n"
        "Columns (based on " + ('$cd$' if is_4var else '$bc$') + "): \\begin{itemize} \\item 00, 01, 11, 10 \\end{itemize} \n"
        "The cells in the K-map are numbered as minterms, as shown below: \n" +
        ('\\[\\begin{array} {|c|c|c|c|c|} \\hline ab \\backslash cd & 00 & 01 & 11 & 10 \\\\ \\hline 00 & 0 & 1 & 3 & 2 \\\\ \\hline 01 & 4 & 5 & 7 & 6 \\\\ \\hline 11 & 12 & 13 & 15 & 14 \\\\ \\hline 10 & 8 & 9 & 11 & 10 \\\\ \\hline \\end{array}\\]' if is_4var else '\\[\\begin{array} {|c|c|c|c|c|} \\hline a \\backslash bc & 00 & 01 & 11 & 10 \\\\ \\hline 0 & 0 & 1 & 3 & 2 \\\\ \\hline 1 & 4 & 5 & 7 & 6 \\\\ \\hline \\end{array}\\]') + "\n"
        f"For the function: \\begin{{itemize}} \n"
        f"\\item 1 at minterms: ${minterms}$. \n" + (f"\\item Don't-care (x) at minterms: ${dontcares}$. \n" if flag_dontcare else "") +
        "\\item 0 at all other minterms. \n"
        "\\end{itemize} \n"
        f"Now, fill the K-map with values of 1, 0" + (", or x (dont-care)" if flag_dontcare else "") + f": {kmap_latex} \n"
        "\\item Grouping (grouping 1s and leveraging don't-care cells). \\\\ \n"
        "We group in powers of 2 (1, 2, 4, 8, ...) and use the x cells if they help expand the groups. Here's one way to group (each “group” corresponds to a product term in the simplified form): \\\\\\\\" + kmap_tikz_latex + "\n"
        f"\\\\\\\\The result is: $f({vars}) = {result}$ \n"
        "\\end{enumerate}"
    )

    # data_output
    data_output = f"f({vars}) = {result}"

    return data_input, data_solution, data_output


def create_full_latex_document(data_input, data_solution, case_number):
    """Create a complete LaTeX document"""
    latex_preamble = (
        "\\documentclass{article}\n"
        "\\usepackage{amsmath, array, xcolor}\n"
        "\\usepackage{tikz}\n"
        "\\usetikzlibrary{shapes.geometric}\n"
        "\\begin{document}\n\n"
    )
    
    latex_ending = "\\end{document}"
    
    return latex_preamble + data_input + "\n\n" + data_solution + "\n\n" + latex_ending


# Process each row and generate LaTeX files
results = []
for index, row in df.iterrows():
    case_number = row['Case']
    data_input, data_solution, data_output = generate_latex(row)
    
    if data_input:
        # Add to Excel results
        results.append({
            'Case': case_number,
            'data_input': data_input,
            'data_solution': data_solution,
            'data_output': data_output
        })
        
        # Generate and save complete LaTeX document
        full_latex = create_full_latex_document(data_input, data_solution, case_number)
        latex_file_path = os.path.join(output_latex_dir, f"kmap_case_{case_number}.tex")
        
        with open(latex_file_path, 'w', encoding='utf-8') as latex_file:
            latex_file.write(full_latex)

# Save Excel file as before
output_df = pd.DataFrame(results)
output_file = "../output_kmap2000QnAkmap_tikz_v1.xlsx"
output_df.to_excel(output_file, index=False)

print(f"Excel results saved in {output_file}")
print(f"LaTeX files saved in {output_latex_dir}")