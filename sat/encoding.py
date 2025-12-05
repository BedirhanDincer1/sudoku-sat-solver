# sat/encoding.py

def var_id(i, j, n):
    """
    SAT solver için (i, j, n) üçlüsünü tek bir tamsayı ID'ye çevirir.
    Örn: p(i,j,n) -> 100*i + 10*j + n
    """
    return 100 * i + 10 * j + n


def add_cell_constraints(clauses):
    """
    Her hücre (i,j) için:
    1) En az bir sayı olmalı
    2) En fazla bir sayı olmalı
    """

    # --- 1) EN AZ BİR SAYI ---
    for i in range(1, 10):
        for j in range(1, 10):
            clause = []
            for n in range(1, 10):
                clause.append(var_id(i, j, n))
            clauses.append(clause)

    # --- 2) EN FAZLA BİR SAYI ---
    for i in range(1, 10):
        for j in range(1, 10):
            for n1 in range(1, 10):
                for n2 in range(n1 + 1, 10):
                    # n1 ve n2 aynı anda olamaz
                    clauses.append([
                        -var_id(i, j, n1),
                        -var_id(i, j, n2)
                    ])



def add_row_constraints(clauses):
    """
    Her satırda her sayı:
    1) En az bir kere bulunmalı
    2) En fazla bir kere bulunmalı
    """

    # --- 1) EN AZ BİR KEZ ---
    for i in range(1, 10):          # satırlar
        for n in range(1, 10):      # sayı 1-9
            clause = []
            for j in range(1, 10):  # sütunlar
                clause.append(var_id(i, j, n))
            clauses.append(clause)

    # --- 2) EN FAZLA BİR KEZ ---
    for i in range(1, 10):          # satırlar
        for n in range(1, 10):      # sayı
            for j1 in range(1, 10):
                for j2 in range(j1 + 1, 10):
                    clauses.append([
                        -var_id(i, j1, n),
                        -var_id(i, j2, n)
                    ])


def add_column_constraints(clauses):
    """
    Her sütunda her sayı:
    1) En az bir kez bulunmalı
    2) En fazla bir kez bulunmalı
    """

    # --- 1) EN AZ BİR KEZ ---
    for j in range(1, 10):          # sütunlar
        for n in range(1, 10):      # sayılar
            clause = []
            for i in range(1, 10):  # satırlar
                clause.append(var_id(i, j, n))
            clauses.append(clause)

    # --- 2) EN FAZLA BİR KEZ ---
    for j in range(1, 10):          # sütunlar
        for n in range(1, 10):      # sayılar
            for i1 in range(1, 10):
                for i2 in range(i1 + 1, 10):
                    clauses.append([
                        -var_id(i1, j, n),
                        -var_id(i2, j, n)
                    ])


def add_block_constraints(clauses):
    """
    Her 3x3 blokta her sayı:
    1) En az bir kez bulunmalı
    2) En fazla bir kez bulunmalı
    """

    # 3x3 bloklar 0,1,2 indexleriyle gezilir
    for br in range(3):          # block row
        for bc in range(3):      # block col

            # --- 1) EN AZ BİR KEZ ---
            for n in range(1, 10):     # sayı 1-9
                clause = []

                # blok içindeki tüm hücreleri gez
                for i in range(1 + br*3, 1 + br*3 + 3):   # satırlar
                    for j in range(1 + bc*3, 1 + bc*3 + 3):  # sütunlar
                        clause.append(var_id(i, j, n))

                clauses.append(clause)

            # --- 2) EN FAZLA BİR KEZ ---
            for n in range(1, 10):

                # bloktaki hücreleri liste halinde topla
                cells = []
                for i in range(1 + br*3, 1 + br*3 + 3):
                    for j in range(1 + bc*3, 1 + bc*3 + 3):
                        cells.append((i, j))

                # Tüm hücre çiftleri
                for idx1 in range(len(cells)):
                    for idx2 in range(idx1 + 1, len(cells)):
                        i1, j1 = cells[idx1]
                        i2, j2 = cells[idx2]

                        clauses.append([
                            -var_id(i1, j1, n),
                            -var_id(i2, j2, n)
                        ])


def add_fixed_cells(grid, clauses):
    """
    OCR'dan gelen grid'deki başlangıç sayıları CNF'e ekler.
    Örn: grid[i][j] = 5 ise, p(i,j,5) True olmak zorunda.
    """
    for i in range(1, 10):          # Satırlar 1-9
        for j in range(1, 10):      # Sütunlar 1-9
            value = grid[i-1][j-1]  # grid 0-indexli olduğu için i-1,j-1

            if value != 0:          # Eğer hücre doluysa
                clauses.append([ var_id(i, j, value) ])



def build_cnf_from_grid(grid):
    """
    Dışarıdan kullanılacak ana fonksiyon.
    OCR'dan gelen 9x9 grid'i alır,
    tüm sudoku kurallarını CNF'e çevirir ve clauses listesini döndürür.
    """
    clauses = []

    # 1) Sudoku'nun genel kurallarını ekle
    add_cell_constraints(clauses)
    add_row_constraints(clauses)
    add_column_constraints(clauses)
    add_block_constraints(clauses)

    # 2) Sudoku'nun başlangıç verilerini (grid) ekle
    add_fixed_cells(grid, clauses)

    return clauses
