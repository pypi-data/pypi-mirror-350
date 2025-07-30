# test_library.py

def run_asak_test():
    print("Attempting to import 'asak' class from 'asakpy' package...")
    try:
        from asakpy.asakpy import asak  # Correct import: from package_name import ClassName

        print("Import successful!")

        # Define a dummy configuration to instantiate the 'asak' class
        # This config must match the expected structure in your __init__.py
        dummy_config = {
            "providers": {
                "test_provider_alpha": {
                    "base_url": "https://api.dummy-alpha.com/v1",
                    "key": "fake_key_alpha_12345"
                }
            },
            "models": [
                {
                    "provider": "test_provider_alpha",
                    "model": "alpha-model-001",
                    "rate_limit": {"rpm": 10, "rpd": 1000} # Requests Per Minute, Requests Per Day
                },
                {
                    "provider": "test_provider_alpha",
                    "model": "alpha-model-002",
                    "rate_limit": {"rpm": 5, "rpd": 500}
                }
            ]
        }

        print("\nAttempting to instantiate the 'asak' class with the dummy config...")
        asak_client = asak(config=dummy_config)
        print("'asak' class instantiated successfully.")

        print("\nVerifying recorder initialization:")
        initial_records = asak_client.recorder.get()
        print(f"Initial records from recorder: {initial_records}")
        if len(initial_records) == len(dummy_config["models"]):
            print(f"Recorder correctly initialized for {len(initial_records)} models. ✅")
        else:
            print(f"Error: Recorder expected {len(dummy_config['models'])} model records, but found {len(initial_records)}. ❌")

        print("\nTesting 'get_model' functionality (mode='index'):")
        # Define a simple filter that always returns True for testing
        def always_true_filter(index, model_details):
            return True

        selected_model_info = asak_client.get_model(mode='index', filter=always_true_filter)
        print(f"Selected model details (index mode): {selected_model_info}")

        expected_model_name = dummy_config["models"][0]["model"]
        if selected_model_info.get('model') == expected_model_name:
            print(f"Correct model ('{expected_model_name}') selected by index mode. ✅")
        else:
            print(f"Error: Incorrect model selected. Expected '{expected_model_name}', got '{selected_model_info.get('model')}'. ❌")

        # Check if the recorder logged the 'get_model' call
        records_after_selection = asak_client.recorder.get()
        if len(records_after_selection[0]['m']) == 1 and len(records_after_selection[0]['d']) == 1:
            print("Recorder correctly logged the 'get_model' call for the first model. ✅")
        else:
            print(f"Error: Recorder did not log 'get_model' call as expected. Records for model 0: {records_after_selection[0]}. ❌")

        print("\nAll tests completed.")

    except ModuleNotFoundError:
        print("\nCritical Error: `ModuleNotFoundError`. The 'asakpy' package could not be found. ❌")
        print("Please ensure you have followed these steps carefully:")
        print("  1. Your project structure should be: `your_project_root/asakpy/__init__.py`")
        print("  2. You must run `pip install -e .` from `your_project_root/`.")
        print("  3. Ensure you are using the Python environment where 'asakpy' was installed.")
    except ImportError as e_imp:
        print(f"\nImportError: Could import 'asakpy' but failed to import 'asak' from it. Details: {e_imp} ❌")
        print("This might indicate an issue with `__all__` in `asakpy/__init__.py` or an internal package structure problem.")
    except ValueError as e_val:
        print(f"\nValueError during 'asak' operation: {e_val} ❌")
        print("This could be due to an incorrect configuration or an issue within the class logic (e.g., rate limits, model availability).")
    except Exception as e_gen:
        print(f"\nAn unexpected error occurred: {e_gen} ❌")

if __name__ == "__main__":
    run_asak_test()