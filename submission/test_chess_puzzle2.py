import pytest
from chess_puzzle import *

@pytest.mark.parametrize("input_str, expected_result", [
        ("a26", (1,26)),
        ("z1", (26,1)),
        ("a1", (1,1)),
        ("z26", (26,26)),
        ("e7", (5,7)),
        ("e2",(5,2))
    ]
)
def test_location2index(input_str, expected_result):
    assert location2index(input_str) == expected_result

@pytest.mark.parametrize("input_ords, expected_result", [
        ((1,26), "a26"),
        ((26,1), "z1"),
        ((1,1), "a1"),
        ((26,26), "z26"),
        ((5,7), "e7"),
        ((5,2), "e2")
    ]
)
def test_index2location(input_ords, expected_result):
    assert index2location(input_ords[0], input_ords[1]) == expected_result

b2_wb1 = Bishop(1,1,True)
b2_wb2 = Bishop(26,26,True)
b2_wk1 = King(2,1,True)
b2_bb1 = Bishop(7,8,False)
b2_bb2 = Bishop(25,25,False)
b2_bk1 = King(5,9,False)
b2_wb2a = Bishop(25,25,True)
B2 = (26, [b2_wb1, b2_bb1, b2_wb2, b2_bb2, b2_wk1, b2_bk1])
B2A = (26, [b2_wb2a, b2_wb1, b2_wk1, b2_bb1, b2_bk1])

b3_wk1 = King(4,5,True)
b3_wk1a = King(4,4,True)
b3_wb1 = Bishop(1,5,True)
b3_wb2 = Bishop(2,4,True)
b3_wb3 = Bishop(3,3,True)
b3_wb4 = Bishop(4,2,True)
b3_wb5 = Bishop(5,1,True)
b3_wb6 = Bishop(2,5,True)
b3_wb7 = Bishop(3,4,True)
b3_wb8 = Bishop(4,3,True)
b3_wb9 = Bishop(5,2,True)
b3_bk1 = King(2,1,False)
B3 = (5, [b3_wk1, b3_wb1, b3_wb2, b3_wb3, b3_wb4, b3_wb5, b3_wb6, b3_wb7, b3_wb8, b3_wb9, b3_bk1])
B3A = (5, [b3_wk1a, b3_wb1, b3_wb2, b3_wb3, b3_wb4, b3_wb5, b3_wb6, b3_wb7, b3_wb8, b3_wb9, b3_bk1])

b4_wk1 = King(4,2,True)
b4_wb1 = Bishop(3,1,True)
b4_wb2 = Bishop(3,2,True)
b4_wb3 = Bishop(4,4,True)
b4_wb3a = Bishop(5,5,True)
b4_bk1 = King(1,2,False)
B4 = (5, [b4_wk1, b4_wb1, b4_wb2, b4_wb3, b4_bk1])
B4A = (5, [b4_wk1, b4_wb1, b4_wb2, b4_wb3a, b4_bk1])

b5_wb1 = Bishop(2,5,True)
b5_wb2 = Bishop(4,4,True)
b5_wb2a = Bishop(3,3,True)
b5_wb3 = Bishop(3,1,True)
b5_wb4 = Bishop(5,5,True)
b5_wb5 = Bishop(4,1,True)
b5_wk1 = King(3,5,True)
b5_wk1a = King(2,5,True)
b5_bb1 = Bishop(3,3,False)
b5_bb2 = Bishop(5,3,False)
b5_bb3 = Bishop(1,2,False)
b5_bk1 = King(2,3,False)
B5 = (5, [b5_wb1, b5_bb1, b5_wb2, b5_bb2, b5_wb3, b5_wk1, b5_bk1])
B5A = (5, [b5_wk1a, b5_wb4, b5_bk1, b5_bb2, b5_bb3, b5_wb3, b5_wb5])
B5B = (5, [b5_wb1, b5_wb2a, b5_bb2, b5_wb3, b5_wk1, b5_bk1])

@pytest.mark.parametrize("filename, board, size, expected_result", [
    ("submission/board_examp.txt", B5, 5, True),
    ("submission/test_files/board_b2.txt", B2, 26, True),
    ("submission/test_files/board_b2.txt", B3, 26, False),
    ("submission/test_files/board_checkmate.txt", B3, 5, True),
    ("submission/test_files/board_stalemate.txt", B4, 5, True),
    ("submission/test_files/board_stalemate.txt", B2, 5, False)
    ]
)
def test_read_board(filename, board, size, expected_result):
    B = read_board(filename)
    assert B[0] == size

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in board[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found == expected_result

    for piece1 in board[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found == expected_result

@pytest.mark.parametrize("filename, expected_result", [
    ("submission/board_examp.txt", True),
    ("submission/test_files/board_b2.txt", True),
    ("submission/test_files/board_checkmate.txt", True),
    ("submission/test_files/board_stalemate.txt", True),
    ("submission/invalid_file_2kings.txt", False),
    ("submission/invalid_file_size.txt", False),
    ("submission/invalid_file_outofbound.txt", False),
    ("submission/invalid_file_extradata.txt", False) 
    ]
)
def test_read_board2(filename, expected_result):
    try:
        B = read_board(filename)
        if B is not None:
            assert True == expected_result
    except Exception:
        assert expected_result is False

@pytest.mark.parametrize("input_ord, board, expected_result", [
    ((9,9), B2, False),
    ((25,25), B2, True),
    ((2,2), B3, False),
    ((2,1), B3, True),
    ((3,2), B4, True),
    ((5,5), B4, False),
    ((2,2), B5, False)
    ]
)
def test_is_piece_at(input_ord, board, expected_result):
    assert is_piece_at(input_ord[0], input_ord[1], board) == expected_result

@pytest.mark.parametrize("input_ord, board, expected_result", [
    ((5,9), B2, b2_bk1),
    ((5,1), B3, b3_wb5),
    ((4,5), B3, b3_wk1),
    ((3,1), B4, b4_wb1),
    ((1,2), B4, b4_bk1),
    ((3,3), B5, b5_bb1)
    ]
)
def test_piece_at(input_ord, board, expected_result):
    assert piece_at(input_ord[0], input_ord[1], board) == expected_result

@pytest.mark.parametrize("piece, input_ord, board, expected_result", [
    (b2_wb2, (25,25), B2, True),
    (b3_wk1, (5,5), B3, True),
    (b3_wb3, (5,5), B3, True),
    (b3_wb3, (1,5), B3, False),
    (b4_wk1, (5,2), B4, True),
    (b4_wk1, (4,2), B4, False),
    (b5_wb2, (5,5), B5, True)
    ]
)
def test_can_reach(piece, input_ord, board, expected_result):
    assert piece.can_reach(input_ord[0], input_ord[1], board) == expected_result

@pytest.mark.parametrize("piece, input_ord, board, expected_result", [
    (b2_wb2, (25,25), B2, True),
    (b2_wb2, (24,25), B2, False),
    (b2_bk1, (5,10), B2, True),
    (b2_bk1, (5,25), B2, False),
    (b3_wk1, (5,5), B3, True),
    (b3_wb3, (5,5), B3, True),
    (b3_wb3, (1,5), B3, False),
    (b4_wb3, (3,3), B4, True),
    (b4_wb3, (1,5), B4, False),
    (b5_wb2, (5,5), B5, False)
    ]
)
def test_can_move_to(piece, input_ord, board, expected_result):
    assert piece.can_move_to(input_ord[0], input_ord[1], board) == expected_result

@pytest.mark.parametrize("side, board, expected_result", [
    (True, B2, False),
    (False, B2, False),
    (False, B3, True),
    (True, B3, False),
    (True, B4, False),
    (False, B4, False),
    (False, B5A, True)
    ]
)
def test_is_check(side, board, expected_result):
    assert is_check(side, board) == expected_result

@pytest.mark.parametrize("side, board, expected_result", [
    (True, B2A, False),
    (False, B2A, False),
    (False, B3, True),
    (True, B3, False),
    (True, B4, False),
    (False, B4, False),
    (False, B5A, True)
    ]
)
def test_is_checkmate(side, board, expected_result):
    assert is_checkmate(side, board) == expected_result

@pytest.mark.parametrize("side, board, expected_result", [
    (True, B2, False),
    (False, B2, False),
    (False, B3, False),
    (True, B3, False),
    (True, B4, False),
    (False, B4, True),
    (True, B5, False)
    ]
)
def test_is_stalemate(side, board, expected_result):
    assert is_stalemate(side, board) == expected_result

@pytest.mark.parametrize("piece, move, board, board2, size, expected_result", [
    (b2_wb2, (25,25), B2, B2A, 26, True),
    (b3_wk1, (4,4), B3, B3A, 5, True),
    (b3_wk1, (4,4), B3, B4, 5, False),
    (b4_wb3, (5,5), B4, B4A, 5, True),
    (b5_wb2, (3,3), B5, B5B, 5, True)
    ]
)
def test_move_to(piece, move, board, board2, size, expected_result):
    Actual_B = piece.move_to(move[0], move[1], board)

    #check if actual board has same contents as expected 
    assert Actual_B[0] == size

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in board2[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found == expected_result


    for piece in board2[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found == expected_result
