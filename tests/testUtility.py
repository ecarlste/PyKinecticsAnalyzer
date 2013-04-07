__author__ = 'Erik S Carlsten'


class TestUtility:
    def assertAlmostEqual_mat4(self, first, second, places=7):
        difference = second - first
        difference_list = difference.toList()

        total_difference = 0
        for item in difference_list:
            total_difference += abs(item)

        total_difference = round(total_difference, places)

        assert total_difference == 0, "first != second: using places=%d" % places