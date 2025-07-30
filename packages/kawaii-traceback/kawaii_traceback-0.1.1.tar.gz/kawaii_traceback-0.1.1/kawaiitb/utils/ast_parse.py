import astroid


def is_point_before(line: int, col: int, start_line: int, start_col: int):
    return (
            (line < start_line) or
            (line == start_line and col < start_col)
    )


def is_point_after(line: int, col: int, end_line: int, end_col: int):
    return (
            (line > end_line) or
            (line == end_line and col > end_col)
    )


def is_point_inside(line: int, col: int, start_line: int, end_line: int, start_col: int, end_col: int):
    if start_line == line == end_line:
        return start_col <= col <= end_col
    return (
            (line == start_line and col >= start_col) or
            (line == end_line and col <= end_col) or
            (start_line < line < end_line)
    )


def is_completely_inside(node: astroid.nodes.NodeNG, start_line: int, end_line: int, start_col: int, end_col: int):
    if any((
        not hasattr(node, 'lineno') or node.lineno is None,
        not hasattr(node, 'col_offset') or node.col_offset is None,
        not hasattr(node, 'end_lineno') or node.end_lineno is None,
        not hasattr(node, 'end_col_offset') or node.end_col_offset is None,
    )): return False
    return (
            is_point_inside(node.lineno, node.col_offset, start_line, end_line, start_col, end_col) and
            is_point_inside(node.end_lineno, node.end_col_offset, start_line, end_line, start_col, end_col)
    )


def is_partially_inside(node: astroid.nodes.NodeNG, start_line: int, end_line: int, start_col: int, end_col: int):
    if any((
        not hasattr(node, 'lineno') or node.lineno is None,
        not hasattr(node, 'col_offset') or node.col_offset is None,
        not hasattr(node, 'end_lineno') or node.end_lineno is None,
        not hasattr(node, 'end_col_offset') or node.end_col_offset is None,
    )): return False
    return (
            is_point_before(node.lineno, node.col_offset, end_line, end_col) or
            is_point_after(node.end_lineno, node.end_col_offset, start_line, start_col)
    )


def astroid_walk_inside(node: astroid.nodes.NodeNG, start_line: int, end_line: int, start_col: int, end_col: int):
    if is_completely_inside(node, start_line, end_line, start_col, end_col):
        yield node
    for child in node.get_children():  # 这里不能检查部分包含，因为部分大节点可能缺结束位，无法判断是否包含
        if isinstance(child, astroid.nodes.NodeNG) and \
                is_partially_inside(child, start_line, end_line, start_col, end_col):
            yield from astroid_walk_inside(child, start_line, end_line, start_col, end_col)


