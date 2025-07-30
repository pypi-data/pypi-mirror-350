Writing Python Tests for Vajra
==================================

In Vajra, we use :code:`pytest` for implementing our tests.

We currently have 3 main test categories:

- Functional: for performance and correctness tests
- Unit
- Integration

For each of these categories, you will find a submodule under :code:`test/`.
Please add your tests to the appropriate one. You're free to create subdirectories.

For :code:`pytest` to properly detect your tests, you will need to categorize it using the :code:`@pytest.mark`
helper. For example, see this unit test

.. code-block:: python

    @pytest.mark.unit
    def test_unit_example():
        pass

You will see available marks in :code:`pyproject.toml`.

If you are mocking, use :code:`pytest-mock`. Also, be sure to check out :code:`fixtures`, :code:`@parametrize`, and
other cool :code:`pytest` features that you might need.
