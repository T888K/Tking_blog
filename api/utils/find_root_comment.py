def find_root_comment(comment):
    if comment.parent_comment:
        return find_root_comment(comment.parent_comment)
    return comment
