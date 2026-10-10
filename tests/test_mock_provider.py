from app.providers.mock import MockProvider


def test_mock_provider_returns_deterministic_response():
    provider = MockProvider()
    response = provider.generate("What is 2 + 2?", system_prompt="Answer briefly.")

    assert response.output == "4"
    assert response.model_id == "mock-model-v1"
    assert response.provider == "mock"
    assert response.usage is not None
