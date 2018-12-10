import math


class PaginationState:
    def __init__(self, total_items, items_per_page=20):
        self._sensitivities = None
        self._current_page = 1
        self._total_items = total_items
        self._items_per_page = items_per_page

        self._n_pages = self._calculate_n_pages()
        self._assign_sensitivities()

    def _assign_sensitivities(self):
        # Single page
        if self._total_items <= self._items_per_page:
            self._sensitivities = (False, False, False, False)
        # First page
        elif self._current_page == 1:
            self._sensitivities = (False, False, True, True)
        # Last page
        elif self._current_page == self._n_pages:
            self._sensitivities = (True, True, False, False)
        # Middle page
        else:
            self._sensitivities = (True, True, True, True)

    def _get_shown_range(self):
        first = (self._current_page - 1) * self._items_per_page + 1
        last = min(self._total_items, first + self._items_per_page - 1)

        return first, last

    def _calculate_n_pages(self):
        return math.ceil(self._total_items / self._items_per_page)

    def goto_next_page(self):
        if self._current_page < self._n_pages:
            self._current_page += 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_previous_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_first_page(self):
        if self._current_page != 1:
            self._current_page = 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_last_page(self):
        if self._current_page != self._n_pages:
            self._current_page = self._n_pages
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    @property
    def total_items(self):
        return self._total_items

    @total_items.setter
    def total_items(self, value):
        self._total_items = value