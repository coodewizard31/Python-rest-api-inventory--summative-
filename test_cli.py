# test_cli.py - tests for the CLI commands. Run with:  pytest -v
# We fake the keyboard (input) and fake the API (requests), so no server is needed.
import requests
from unittest.mock import patch, MagicMock
import cli


def fake_response(data, status=200):
    """Make a pretend answer from the API."""
    response = MagicMock()
    response.status_code = status
    response.json.return_value = data
    return response


ITEM = {"id": 1, "status": 1, "price": 3.99, "stock": 20,
        "product": {"product_name": "Almond Milk", "brands": "Silk", "ingredients_text": ""}}


@patch("cli.requests.get")
def test_view_all(fake_get, capsys):
    fake_get.return_value = fake_response([ITEM])
    cli.view_all()
    assert "Almond Milk" in capsys.readouterr().out


@patch("builtins.input", return_value="1")
@patch("cli.requests.get")
def test_view_one(fake_get, fake_input, capsys):
    fake_get.return_value = fake_response(ITEM)
    cli.view_one()
    assert "Almond Milk" in capsys.readouterr().out


@patch("builtins.input", return_value="99")
@patch("cli.requests.get")
def test_view_one_not_found(fake_get, fake_input, capsys):
    fake_get.return_value = fake_response({"error": "Item not found"}, 404)
    cli.view_one()
    assert "Item not found" in capsys.readouterr().out


@patch("builtins.input", side_effect=["Oat Milk", "Oatly", "2.5", "10"])
@patch("cli.requests.post")
def test_add_item(fake_post, fake_input, capsys):
    fake_post.return_value = fake_response(ITEM, 201)
    cli.add_item()
    assert "Item added!" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "5.0", ""])
@patch("cli.requests.patch")
def test_update_item(fake_patch, fake_input, capsys):
    fake_patch.return_value = fake_response(ITEM, 200)
    cli.update_item()
    assert "Item updated!" in capsys.readouterr().out


@patch("builtins.input", return_value="1")
@patch("cli.requests.delete")
def test_delete_item(fake_delete, fake_input, capsys):
    fake_delete.return_value = fake_response({"message": "Item deleted"}, 200)
    cli.delete_item()
    assert "Item deleted!" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "3017620422003", "n"])
@patch("cli.requests.get")
def test_find_on_api(fake_get, fake_input, capsys):
    fake_get.return_value = fake_response({"status": 1, "product": {"product_name": "Nutella", "brands": "Ferrero"}})
    cli.find_on_api()
    assert "Nutella" in capsys.readouterr().out


@patch("builtins.input", side_effect=["1", "0"])
@patch("cli.requests.get", side_effect=requests.exceptions.ConnectionError)
def test_menu_when_api_is_down(fake_get, fake_input, capsys):
    cli.main()   # choose 1 (view all), then 0 (quit)
    assert "could not reach the API" in capsys.readouterr().out