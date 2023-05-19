from app01.models import Comment


def find_root_sub_comment(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        # 找到所有的根评论的子评论
        sub_comment_list.append(sub_comment)
        find_root_sub_comment(sub_comment, sub_comment_list)

def sub_comment_list(nid):
    # 找到所有的评论
    comment_query = Comment.objects.filter(article_id=nid).order_by('-create_time')
    # 存储评论的表
    comment_list = []

    for comment in comment_query:
        # 如果没有父类，就代表它是根评论
        if not comment.parent_comment:
            # 递归找到所有的子评论
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue

    return comment_list
