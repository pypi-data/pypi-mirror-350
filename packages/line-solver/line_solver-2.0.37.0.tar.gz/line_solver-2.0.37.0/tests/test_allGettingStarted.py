import os
import shutil
import unittest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

class TestGettingStarted(unittest.TestCase):

    # Directory containing the notebooks, relative to the root of the project
    notebooks_dir = 'gettingstarted'

    def run_notebook(self, filename):
        working_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        os.chdir(working_dir)
        filepath = os.path.join(self.notebooks_dir, filename)
        print(f'Running notebook: {filename} Working directory: {working_dir}', flush=True)

        with open(filepath) as f:
            nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            try:
                ep.preprocess(nb, {'metadata': {'path': self.notebooks_dir}})
                print(f'Finished running notebook: {filename}', flush=True)
            except Exception as e:
                print(f"Notebook {filename} failed with error: {e}", flush=True)
            finally:
                # Clean up _trial_temp if it exists
                if os.path.exists("_trial_temp"):
                    shutil.rmtree("_trial_temp")

        # Check for errors in cell outputs
        for cell in nb.cells:
            if cell.cell_type == 'code':
                for output in cell.get('outputs', []):
                    if output.output_type == 'error':
                        error_name = output.get("ename", "")
                        error_value = output.get("evalue", "")
                        # traceback_text = "\n".join(output.get("traceback", []))
                        self.fail(
                            f"Notebook {filename} failed.\n"
                            f"Error Name: {error_name}\n"
                            f"Error Value: {error_value}\n"
                            #   f"Traceback:\n{traceback_text}"
                        )

    def test_getting_started_ex1(self):
        self.run_notebook("getting_started_ex1.ipynb")

    def test_getting_started_ex2(self):
        self.run_notebook("getting_started_ex2.ipynb")

    def test_getting_started_ex3(self):
        self.run_notebook("getting_started_ex3.ipynb")

    def test_getting_started_ex4(self):
        self.run_notebook("getting_started_ex4.ipynb")

    def test_getting_started_ex5(self):
        self.run_notebook("getting_started_ex5.ipynb")

    def test_getting_started_ex6(self):
        self.run_notebook("getting_started_ex6.ipynb")

    def test_getting_started_ex7(self):
        self.run_notebook("getting_started_ex7.ipynb")

    def test_getting_started_ex8(self):
        self.run_notebook("getting_started_ex8.ipynb")


if __name__ == '__main__':
    unittest.main(verbosity=2)
