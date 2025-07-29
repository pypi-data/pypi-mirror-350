import os
import time
import uuid
import pytest
from dotenv import load_dotenv
from enkryptai_sdk import RedTeamClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENKRYPT_API_KEY = os.getenv("ENKRYPTAI_API_KEY")
ENKRYPT_BASE_URL = os.getenv("ENKRYPTAI_BASE_URL") or "https://api.enkryptai.com"

redteam_test_name = None
redteam_model_test_name = None
custom_redteam_test_name = None
custom_redteam_model_test_name = None
redteam_picked_test_name = None
test_model_saved_name = "Test Model"
test_model_version = "v1"

model_name = "gpt-4o-mini"
model_provider = "openai"
model_endpoint_url = "https://api.openai.com/v1/chat/completions"


@pytest.fixture
def redteam_client():
    return RedTeamClient(api_key=ENKRYPT_API_KEY, base_url=ENKRYPT_BASE_URL)


@pytest.fixture
def sample_redteam_model_health_config():
    return {
        "target_model_configuration": {
            "model_name": model_name,
            "testing_for": "foundationModels",
            "model_version": "v1",
            "model_source": "https://openai.com",
            "model_provider": model_provider,
            "model_endpoint_url": model_endpoint_url,
            "model_api_key": OPENAI_API_KEY,
            "system_prompt": "",
            "rate_per_min": 20,
            "input_modalities": ["text"],
            "output_modalities": ["text"]
        },
    }


@pytest.fixture
def sample_redteam_target_config():
    global redteam_test_name
    redteam_test_name = f"Redteam Test {str(uuid.uuid4())[:6]}"
    print("\nRedteam target model test name: ", redteam_test_name)
    return {
        "test_name": redteam_test_name,
        "dataset_name": "standard",
        "redteam_test_configurations": {
            # # Commenting to have only 1 for faster testing
            # "bias_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "cbrn_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "insecure_code_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "toxicity_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            "harmful_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
        },
        "target_model_configuration": {
            "model_name": model_name,
            "testing_for": "foundationModels",
            "model_version": "v1",
            "model_source": "https://openai.com",
            "model_provider": model_provider,
            "model_endpoint_url": model_endpoint_url,
            "model_api_key": OPENAI_API_KEY,
            "system_prompt": "",
            "rate_per_min": 20,
            "input_modalities": ["text"],
            "output_modalities": ["text"]
        },
    }


@pytest.fixture
def sample_redteam_model_config():
    global redteam_model_test_name
    redteam_model_test_name = f"Redteam Test {str(uuid.uuid4())[:6]}"
    print("\nRedteam saved model test name: ", redteam_model_test_name)
    return {
        "test_name": redteam_model_test_name,
        "dataset_name": "standard",
        "redteam_test_configurations": {
            # # Commenting to have only 1 for faster testing
            # "bias_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "cbrn_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "insecure_code_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            # "toxicity_test": {
            #     "sample_percentage": 2,
            #     "attack_methods": {"basic": ["basic"]},
            # },
            "harmful_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
        },
    }


@pytest.fixture
def sample_custom_redteam_target_config():
    global custom_redteam_test_name
    custom_redteam_test_name = f"Custom Redteam Test {str(uuid.uuid4())[:6]}"
    print("\nCustom Redteam target model test name: ", custom_redteam_test_name)
    return {
        "test_name": custom_redteam_test_name,
        "dataset_configuration": {
          "system_description": "- **Voter Eligibility**: To vote in U.S. elections, individuals must be U.S. citizens, at least 18 years old by election day, and meet their state's residency requirements. - **Voter Registration**: Most states require voters to register ahead of time, with deadlines varying widely. North Dakota is an exception, as it does not require voter registration. - **Identification Requirements**: Thirty-six states enforce voter ID laws, requiring individuals to present identification at polling places. These laws aim to prevent voter fraud but can also lead to disenfranchisement. - **Voting Methods**: Voters can typically choose between in-person voting on election day, early voting, and absentee or mail-in ballots, depending on state regulations. - **Polling Hours**: Polling hours vary by state, with some states allowing extended hours for voters. Its essential for voters to check local polling times to ensure they can cast their ballots. - **Provisional Ballots**: If there are questions about a voter's eligibility, they may be allowed to cast a provisional ballot. This ballot is counted once eligibility is confirmed. - **Election Day Laws**: Many states have laws that protect the rights of voters on election day, including prohibiting intimidation and ensuring access to polling places. - **Campaign Finance Regulations**: Federal and state laws regulate contributions to candidates and political parties to ensure transparency and limit the influence of money in politics. - **Political Advertising**: Campaigns must adhere to rules regarding political advertising, including disclosure requirements about funding sources and content accuracy. - **Voter Intimidation Prohibitions**: Federal laws prohibit any form of voter intimidation or coercion at polling places, ensuring a safe environment for all voters. - **Accessibility Requirements**: The Americans with Disabilities Act mandates that polling places be accessible to individuals with disabilities, ensuring equal access to the electoral process. - **Election Monitoring**: Various organizations are allowed to monitor elections to ensure compliance with laws and regulations. They help maintain transparency and accountability in the electoral process. - **Vote Counting Procedures**: States have specific procedures for counting votes, including the use of electronic voting machines and manual audits to verify results. - **Ballot Design Standards**: States must adhere to certain design standards for ballots to ensure clarity and prevent confusion among voters when casting their votes. - **Post-Election Audits**: Some states conduct post-election audits as a measure of accuracy. These audits help verify that the vote count reflects the actual ballots cast.",
          "policy_description": "Do not generate any content that is illegal, harmful, or violates the rights of others.",
          # "risk_categories": "",
          "tools": [
              {
                  "name": "web_search",
                  "description": "The tool web search is used to search the web for information related to finance."
              }
          ],
          "max_prompts": 100,
          "scenarios": 2,
          "categories": 2,
          "depth": 2,
        },
        "redteam_test_configurations": {
            "harmful_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
            "custom_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
        },
        "endpoint_configuration": {
          "testing_for": "foundationModels",
          "model_name": model_name,
          "model_config": {
              "model_provider": model_provider,
              "endpoint_url": model_endpoint_url,
              "apikey": OPENAI_API_KEY,
              "input_modalities": ["text"],
              "output_modalities": ["text"],
          },
        },
    }


@pytest.fixture
def sample_custom_redteam_model_config():
    global custom_redteam_model_test_name
    custom_redteam_model_test_name = f"Custom Redteam Test {str(uuid.uuid4())[:6]}"
    print("\nCustom Redteam saved model test name: ", custom_redteam_model_test_name)
    return {
        "test_name": custom_redteam_model_test_name,
        "dataset_configuration": {
          "system_description": "- **Voter Eligibility**: To vote in U.S. elections, individuals must be U.S. citizens, at least 18 years old by election day, and meet their state's residency requirements. - **Voter Registration**: Most states require voters to register ahead of time, with deadlines varying widely. North Dakota is an exception, as it does not require voter registration. - **Identification Requirements**: Thirty-six states enforce voter ID laws, requiring individuals to present identification at polling places. These laws aim to prevent voter fraud but can also lead to disenfranchisement. - **Voting Methods**: Voters can typically choose between in-person voting on election day, early voting, and absentee or mail-in ballots, depending on state regulations. - **Polling Hours**: Polling hours vary by state, with some states allowing extended hours for voters. Its essential for voters to check local polling times to ensure they can cast their ballots. - **Provisional Ballots**: If there are questions about a voter's eligibility, they may be allowed to cast a provisional ballot. This ballot is counted once eligibility is confirmed. - **Election Day Laws**: Many states have laws that protect the rights of voters on election day, including prohibiting intimidation and ensuring access to polling places. - **Campaign Finance Regulations**: Federal and state laws regulate contributions to candidates and political parties to ensure transparency and limit the influence of money in politics. - **Political Advertising**: Campaigns must adhere to rules regarding political advertising, including disclosure requirements about funding sources and content accuracy. - **Voter Intimidation Prohibitions**: Federal laws prohibit any form of voter intimidation or coercion at polling places, ensuring a safe environment for all voters. - **Accessibility Requirements**: The Americans with Disabilities Act mandates that polling places be accessible to individuals with disabilities, ensuring equal access to the electoral process. - **Election Monitoring**: Various organizations are allowed to monitor elections to ensure compliance with laws and regulations. They help maintain transparency and accountability in the electoral process. - **Vote Counting Procedures**: States have specific procedures for counting votes, including the use of electronic voting machines and manual audits to verify results. - **Ballot Design Standards**: States must adhere to certain design standards for ballots to ensure clarity and prevent confusion among voters when casting their votes. - **Post-Election Audits**: Some states conduct post-election audits as a measure of accuracy. These audits help verify that the vote count reflects the actual ballots cast.",
          "policy_description": "Do not generate any content that is illegal, harmful, or violates the rights of others.",
          "tools": [
              {
                  "name": "web_search",
                  "description": "The tool web search is used to search the web for information related to finance."
              }
          ],
          "max_prompts": 100,
          "scenarios": 2,
          "categories": 2,
          "depth": 2,
        },
        "redteam_test_configurations": {
            "harmful_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
            "custom_test": {
                "sample_percentage": 2,
                "attack_methods": {"basic": ["basic"]},
            },
        },
    }


def get_task_name_from_list(redteam_client, status=None):
    """Helper function to get a redteam task name from the task list.
    
    Args:
        redteam_client: The RedTeamClient instance
        status: Optional status filter (e.g., "Finished", "Running")
    
    Returns:
        str: A test name from the task list
    """
    print(f"\nFetching redteam task with status: {status if status else 'Finished'}")
    redteams = redteam_client.get_task_list(status=status)
    redteams_dict = redteams.to_dict()
    print(f"\nRedteam task list retrieved with {len(redteams_dict.get('tasks', []))} tasks")
    
    if not redteams_dict.get("tasks"):
        # If no tasks with specified status, try without status filter
        if status:
            print(f"\nNo tasks with status '{status}', fetching any task")
            redteams = redteam_client.get_task_list()
            redteams_dict = redteams.to_dict()
    
    if not redteams_dict.get("tasks"):
        return None
    
    task_info = redteams_dict["tasks"][0]
    test_name = task_info["test_name"]
    print(f"\nSelected redteam task: {test_name} (Status: {task_info.get('status', 'unknown')})")
    return test_name


def test_get_health(redteam_client):
    print("\n\nTesting get_health")
    response = redteam_client.get_health()
    print("\nResponse from get_health: ", response)
    assert response is not None
    assert hasattr(response, "status")
    assert response.status == "healthy"


def test_model_health(redteam_client, sample_redteam_model_health_config):
    print("\n\nTesting check_model_health")
    response = redteam_client.check_model_health(config=sample_redteam_model_health_config)
    print("\nResponse from check_model_health: ", response)
    assert response is not None
    assert hasattr(response, "status")
    assert response.status == "healthy"


def test_saved_model_health(redteam_client):
    print("\n\nTesting check_saved_model_health")
    response = redteam_client.check_saved_model_health(model_saved_name=test_model_saved_name, model_version=test_model_version)
    print("\nResponse from check_saved_model_health: ", response)
    assert response is not None
    assert hasattr(response, "status")
    assert response.status == "healthy"


# # Testing only via saved model as it should be sufficient
# ---------------------------------------------------------
# def test_add_task_with_target_model(redteam_client, sample_redteam_target_config):
#     print("\n\nTesting adding a new redteam task with target model")
#     # Debug sample_redteam_target_config
#     # print("\nSample redteam target config: ", sample_redteam_target_config)
#     response = redteam_client.add_task(config=sample_redteam_target_config)
#     print("\nResponse from adding a new redteam task with target model: ", response)
#     assert response is not None
#     assert hasattr(response, "task_id")
#     assert hasattr(response, "message")
#     response.message == "Redteam task has been added successfully"
#     # Sleep for a while to let the task complete
#     # This is also useful to avoid rate limiting issues
#     print("\nSleeping for 60 seconds to let the task complete if possible ...")
#     time.sleep(60)


def test_add_task_with_saved_model(redteam_client, sample_redteam_model_config):
    print("\n\nTesting adding a new redteam task with saved model")
    response = redteam_client.add_task_with_saved_model(config=sample_redteam_model_config,model_saved_name=test_model_saved_name, model_version=test_model_version)
    print("\nResponse from adding a new redteam task with saved model: ", response)
    assert response is not None
    assert hasattr(response, "task_id")
    assert hasattr(response, "message")
    response.message == "Redteam task has been added successfully"
    # Sleep for a while to let the task complete
    # This is also useful to avoid rate limiting issues
    print("\nSleeping for 60 seconds to let the task complete if possible ...")
    time.sleep(60)


# # Testing only via saved model as it should be sufficient
# ---------------------------------------------------------
# def test_add_custom_task_with_target_model(redteam_client, sample_custom_redteam_target_config):
#     print("\n\nTesting adding a new custom redteam task with target model")
#     # Debug sample_custom_redteam_target_config
#     # print("\nSample custom redteam target config: ", sample_custom_redteam_target_config)
#     response = redteam_client.add_custom_task(config=sample_custom_redteam_target_config)
#     print("\nResponse from adding a new custom redteam task with target model: ", response)
#     assert response is not None
#     assert hasattr(response, "task_id")
#     assert hasattr(response, "message")
#     response.message == "Task submitted successfully"
#     # Sleep for a while to let the task complete
#     # This is also useful to avoid rate limiting issues
#     print("\nSleeping for 60 seconds to let the task complete if possible ...")
#     time.sleep(60)


def test_add_custom_task_with_saved_model(redteam_client, sample_custom_redteam_model_config):
    print("\n\nTesting adding a new custom redteam task with saved model")
    response = redteam_client.add_custom_task_with_saved_model(config=sample_custom_redteam_model_config, model_saved_name=test_model_saved_name, model_version=test_model_version)
    print("\nResponse from adding a new custom redteam task with saved model: ", response)
    assert response is not None
    assert hasattr(response, "task_id")
    assert hasattr(response, "message")
    response.message == "Task submitted successfully"
    # Sleep for a while to let the task complete
    # This is also useful to avoid rate limiting issues
    print("\nSleeping for 60 seconds to let the task complete if possible ...")
    time.sleep(60)


def test_list_redteams(redteam_client):
    print("\n\nTesting list_redteam tasks")
    redteams = redteam_client.get_task_list(status="Finished")
    redteams_dict = redteams.to_dict()
    print("\nRedteam task list: ", redteams_dict)
    assert redteams_dict is not None
    assert isinstance(redteams_dict, dict)
    assert "tasks" in redteams_dict
    
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None
        print("\nPicked redteam finished task in list_redteams: ", redteam_picked_test_name)


def test_get_task_status(redteam_client):
    print("\n\nTesting get_task_status")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.status(test_name=redteam_picked_test_name)
    print("\nRedteam task status: ", response)
    assert response is not None
    assert hasattr(response, "status")


def test_get_task(redteam_client):
    print("\n\nTesting get_task")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.get_task(test_name=redteam_picked_test_name)
    print("\nRedteam task: ", response)
    assert response is not None
    assert hasattr(response, "status")


def test_get_result_summary(redteam_client):
    print("\n\nTesting get_result_summary")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.get_result_summary(test_name=redteam_picked_test_name)
    print("\nRedteam task result summary: ", response)
    assert response is not None
    # # Task might not be successful yet
    # # TODO: How to handle this?
    # assert hasattr(response, "summary")


def test_get_result_summary_test_type(redteam_client):
    print("\n\nTesting get_result_summary_test_type")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.get_result_summary_test_type(test_name=redteam_picked_test_name, test_type="harmful_test")
    print("\nRedteam task result summary of test type: ", response)
    assert response is not None
    # # Task might not be successful yet
    # # TODO: How to handle this?
    # assert hasattr(response, "summary")


def test_get_result_details(redteam_client):
    print("\n\nTesting get_result_details")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.get_result_details(test_name=redteam_picked_test_name)
    print("\nRedteam task result details: ", response)
    assert response is not None
    # # Task might not be successful yet
    # # TODO: How to handle this?
    # assert hasattr(response, "details")


def test_get_result_details_test_type(redteam_client):
    print("\n\nTesting get_result_details_test_type")
    global redteam_picked_test_name
    if redteam_picked_test_name is None:
        redteam_picked_test_name = get_task_name_from_list(redteam_client, status="Finished")
        assert redteam_picked_test_name is not None

    response = redteam_client.get_result_details_test_type(test_name=redteam_picked_test_name, test_type="harmful_test")
    print("\nRedteam task result details of test type: ", response)
    assert response is not None
    # # Task might not be successful yet
    # # TODO: How to handle this?
    # assert hasattr(response, "details")

