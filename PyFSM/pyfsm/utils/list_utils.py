

class ListUtils(object):
    @staticmethod
    def add_or_create(m_list, x):
        m_list = m_list if m_list is not None else []
        if x not in m_list:
            m_list.append(x)
        return m_list

    @staticmethod
    def is_empty(m_list):
        return m_list is None or not len(m_list)

    @staticmethod
    def is_empty_or_any(m_list, x):
        return ListUtils.is_empty(m_list) or x in m_list

    @staticmethod
    def is_empty_or_any_expr(m_list, expr):
        if ListUtils.is_empty(m_list):
            return True
        for item in m_list:
            if expr(item):
                return True
        return False

    @staticmethod
    def get_or_else(m_list, el=None):
        if el is None:
            el = []
        return m_list if m_list is not None else el
