from ..exceptions import NullException


class ListUtils(object):
    @staticmethod
    def add_or_create(m_list, x, duplicate_allow=False):
        m_list = m_list if m_list is not None else []
        xs = [x] if not isinstance(x, list) else x
        for x in xs:
            if x is not None:
                if duplicate_allow or x not in m_list:
                    m_list.append(x)
        return m_list

    @staticmethod
    def is_empty(m_list):
        return m_list is None or not len(m_list)

    @staticmethod
    def is_empty_or_any(m_list, x, allow_none=False):
        return ListUtils.is_empty(m_list) or x in [m for m in m_list if m is not None or allow_none]

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

    @staticmethod
    def to_list(element):
        if element is None:
            raise NullException()
        return element if isinstance(element, list) else [element]

    @staticmethod
    def len_or_abs(m_list):
        if m_list is None:
            return 0
        else:
            return len(m_list)
