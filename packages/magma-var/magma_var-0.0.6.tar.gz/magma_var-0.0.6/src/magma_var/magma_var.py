from magma_var.utils import check_directory
import os


class MagmaVar:
    def __init__(self, token: str, volcano_code: str,
                 start_date: str, end_date: str, current_dir: str = None,
                 verbose: bool = False):
        self.token = token
        self.volcano_code = volcano_code
        self.start_date = start_date
        self.end_date = end_date

        if current_dir is None:
            current_dir = os.getcwd()
        self.current_dir = current_dir

        self.output_dir, self.figures_dir, self.magma_dir = check_directory(current_dir)

        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

        self.verbose = verbose
