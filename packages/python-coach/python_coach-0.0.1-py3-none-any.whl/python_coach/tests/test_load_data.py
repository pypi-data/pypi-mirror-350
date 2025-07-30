from datacontext.dc import DataContext


def test_load_data() -> None:
    context = DataContext()
    data = context.get_quiz_json("Ivan@gmail.com", "pwd")
    assert data is not None


def test_transforn_data() -> None:
    context = DataContext()
    data = context.get_quiz_json("Ivan@gmail.com", "pwd")
    state = context.create_state(data)
    assert state is not None
