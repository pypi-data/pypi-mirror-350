from pydantic_ai import Agent


def validate_agent(agent: Agent):
    result = agent.run_sync("this is a test, just echo 'hello'")
    valid = True if 'hello' in result.data.lower() else False
    if not valid:
        raise ValueError(f'{agent} failed to create agent. Please check the client config.')
    else:
        print(f'{agent} agent created successfully.')


if __name__ == "__main__":

    from util_agent.agent_examples import create_gpt_4o_agent

    validate_agent(create_gpt_4o_agent())
