from typing import Optional, Tuple


def normalize_page_range(
    total_pages: int, page_start: Optional[int], page_end: Optional[int]
) -> Tuple[int, int]:
    """
    :param: page_start: from 0 to total_pages - 1
        if not set or smaller than 0, will start from 0,
        if bigger than page length, only the last page will be processed,
        else, start from the page_start as set.

    :param: page_end: from 0 to total_pages - 1
        if not set or smaller than page_start, will end to the last page,
        if bigger than page length, will end to the last page,
        else, end to the page_end as set.
    """
    if page_start is None or page_start < 0:
        page_start = 0
    elif page_start >= total_pages:
        page_start = total_pages - 1

    if page_end is None or page_end < page_start or page_end >= total_pages:
        page_end = total_pages - 1
    return page_start, page_end
