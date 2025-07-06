class HelperFunctions:
    def get_direction_towards_target(current_row, current_col, target_row, target_col):
        dr = dc = 0
        if current_row < target_row:
            dr = 1
        elif current_row > target_row:
            dr = -1

        if current_col < target_col:
            dc = 1
        elif current_col > target_col:
            dc = -1

        return dr, dc
