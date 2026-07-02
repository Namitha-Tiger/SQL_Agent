from src.memory import MemoryManager


def test_add_interaction():

    state = {
        "question": "Total customers",
        "sql": "SELECT COUNT(*) FROM customers",
        "answer": "120 customers",
        "history": [],
    }

    history = MemoryManager.add_interaction(state)

    assert len(history) == 1

    assert history[0]["question"] == "Total customers"
    

def test_format_history():

    history = [
        {
            "question": "Total customers",
            "sql": "SELECT COUNT(*)",
            "answer": "100",
        }
    ]

    text = MemoryManager.format_history(history)

    assert "Total customers" in text

    assert "SELECT COUNT(*)" in text
    
def test_empty_history():

    text = MemoryManager.format_history([])

    assert text == "No previous conversation."