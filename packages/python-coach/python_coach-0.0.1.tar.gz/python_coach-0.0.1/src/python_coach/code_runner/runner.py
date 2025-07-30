# pylint: disable=W0122

from types import CodeType
from copy import copy
import textwrap
from typing import Any, Callable, Iterator
from code_runner.result_case import ResultCase, RunResult


class CodeRunner:

    class SolutionFuncError(Exception):
        pass

    def __init__(self, function_name: str = "solution") -> None:
        self._printed_lines: list[str] = []
        self._function_name = function_name

    def run_code(self,
                 cases: list[dict[str, Any]],
                 code: str) -> RunResult:
        cleaned_code = textwrap.dedent(code)
        try:
            compiled_code = CodeRunner._try_compile(cleaned_code)
            function_to_run = self._try_get_solution_func(compiled_code)
        except (SyntaxError, NameError) as synt_err:
            return RunResult.create_error_result([str(synt_err)])
        except CodeRunner.SolutionFuncError as func_err:
            return RunResult.create_error_result([str(func_err)])

        result_cases = list(self._run_test_cases(cases, function_to_run))
        distinct_errors = list(
            set(c.exception for c in result_cases if c.exception is not None))

        return RunResult(
            all_cases=result_cases,
            printed_lines=self._printed_lines,
            errors=distinct_errors)

    def _try_get_solution_func(self,
                               compiled_code: CodeType | None) -> Callable[..., Any]:
        if compiled_code is None:
            raise ValueError("No code to run")
        loc: dict[str, object] = {}
        exec_globals = copy(globals())
        exec_globals.update({
            'print': self._my_print
        })
        exec(compiled_code, exec_globals, loc)
        if self._function_name not in loc:
            raise CodeRunner.SolutionFuncError(
                f"No function {self._function_name} in code. You may have accidentally deleted it.")
        function_to_run = loc[self._function_name]
        if not callable(function_to_run):
            raise CodeRunner.SolutionFuncError(
                f"Function {self._function_name} not recognized")
        return function_to_run

    @staticmethod
    def _try_compile(code: str) -> CodeType:
        compile_result = compile(code, '<string>', "exec")
        return compile_result

    def _my_print(self, *args: Any):
        for arg in args:
            self._printed_lines.append(arg)

    def _run_test_cases(self,
                        cases: list[dict[str, Any]],
                        func: Callable[..., Any]) -> Iterator[ResultCase]:
        for c in cases:
            params = dict((k, v) for k, v in c.items() if k != 'expected')
            exp = c['expected']
            try:
                actual = func(**params)
                result_case = ResultCase(
                    func_params=params,
                    expected=exp,
                    actual=actual,
                    passed=str(exp) == str(actual)
                )
                yield result_case
            except Exception as ex:
                yield ResultCase(
                    func_params=params,
                    expected=exp,
                    actual=None,
                    passed=False,
                    exception=str(ex)
                )
