import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=7, position='pos'):
        """
        current_page：当前页码
        all_count：数据库总条数
        base_url：原始url
        query_params：保留原搜索条件
        per_page：一页显示多少条数据
        pager_page_count：最多显示多少个页码
        """

        self.all_count = all_count
        self.per_page = per_page
        self.position = position

        # 计算一共有多少个页码
        # 取余
        # div, p = divmod(all_count, per_page)
        # if p != 0:
        #     div += 1
        # self.current_page = div

        # 进位
        self.current_count = math.ceil(all_count / per_page)

        # 只能时满足条件的正数
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params
        self.pager_page_count = pager_page_count

        # print(self.current_page, self.current_count)
        # 分页的中值
        self.half_pager_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 如果可以分页的页码小于最大显示页码，就然最大显示页码变成可分页页码
            self.pager_page_count = self.current_count

    def pager_html(self):
        # 计算页码的起始和结束 分类讨论 （正常情况）
        start = self.current_page - self.half_pager_count
        end = self.current_page + self.half_pager_count
        if self.current_page <= self.half_pager_count:
            # 在左侧显示（比如第一页如果显示的页码没有超过中值）
            start = 1
            # 右侧显示当前最大的值
            end = self.pager_page_count
        if self.current_page + self.half_pager_count >= self.current_count:
            # 在右侧显示（最后一页的那种情况）
            start = self.current_count - self.pager_page_count + 1
            end = self.current_count

        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">上一页</a></li>')

        # 数字部分
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="actives"><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            page_list.append(li)

        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">下一页</a></li>')

        if len(page_list) == 1:
            # 不显示分页器
            page_list = []
        return ''.join(page_list)

    @property
    def query_encode(self):
        return self.query_params.urlencode()

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page


if __name__ == '__main__':
    pager = Pagination(
        current_page=20,
        all_count=100,
        base_url='/article',
        query_params={'tag': 'python'},
        per_page=5,
        pager_page_count=7
    )
    # print(pager.start, pager.end)
    print(pager.pager_html())
