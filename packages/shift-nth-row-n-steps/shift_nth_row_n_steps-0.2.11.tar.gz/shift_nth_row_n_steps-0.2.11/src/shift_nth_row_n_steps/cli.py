import ivy
import typer
from cm_time import timer
from rich import print

from ._main import (
    shift_nth_row_n_steps,
    shift_nth_row_n_steps_for_loop_assign,
    shift_nth_row_n_steps_for_loop_concat,
)

app = typer.Typer()


@app.command()
def benchmark(
    backend: str = typer.Option("numpy"),
    device: str = typer.Option("cpu"),
    dtype: str = typer.Option("float32"),
    n_end: int = typer.Option(10),
) -> None:
    """
    Benchmark the two implementations of the function.

    Parameters
    ----------
    backend : str, optional
        The backend to use, by default typer.Option("numpy")
    device : str, optional
        The device to use, by default typer.Option("cpu")
    dtype : str, optional
        The dtype to use, by default typer.Option("float32")
    n_end : int, optional
        The maximum power of 2 to use, by default typer.Option(10)

    """
    if device == "gpu":
        device = "gpu:0"
    elif device == "tpu":
        device = "tpu:0"
    ivy.set_backend(backend)
    ivy.set_default_device(device)
    ivy.set_default_float_dtype(ivy.FloatDtype(dtype))
    for i in range(n_end):
        n = 2**i
        input = ivy.random.random_uniform(shape=(n, n))
        with timer() as t1:
            shift_nth_row_n_steps(input)
        with timer() as t2:
            shift_nth_row_n_steps_for_loop_concat(input)
        with timer() as t3:
            shift_nth_row_n_steps_for_loop_assign(input)
        print(
            f"{n}: propsed: {t1.elapsed:g}, "
            f"for loop (concat): {t2.elapsed:g}, "
            f"for loop (assign): {t3.elapsed:g}"
        )
