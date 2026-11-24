from app.memory.session_manager import (
    session_manager
)


def test_session_created():

    session = (
        session_manager.get(
            "test_session"
        )
    )

    assert (
        session.session_id
        ==
        "test_session"
    )