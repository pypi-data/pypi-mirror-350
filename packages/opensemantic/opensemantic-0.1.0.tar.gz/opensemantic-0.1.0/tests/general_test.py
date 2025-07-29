from opensemantic import OswBaseModel


def test_opensemantic():

    # Create an instance of OswBaseModel
    model = OswBaseModel()

    # Check if the instance is created successfully
    assert isinstance(
        model, OswBaseModel
    ), "Failed to create an instance of OswBaseModel"


if __name__ == "__main__":
    test_opensemantic()
    print("All tests passed!")
