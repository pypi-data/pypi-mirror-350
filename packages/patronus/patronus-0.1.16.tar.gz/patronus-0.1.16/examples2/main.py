import patronus

cli = patronus.Client()


task_output = "print('Hello World')"


def sync_calls():
    # Sync version, simplified API, no error handling
    cli.evaluate(
        "judge",
        "patronus:is-code",
        evaluated_model_output=task_output,
    )

    # Option with error handling
    cli.api.evaluate_one_sync(
        patronus.api_types.EvaluateRequest(
            evaluators=[patronus.api_types.EvaluateEvaluator(evaluator="judge", criteria="patronus:is-code")],
            evaluated_model_output=task_output,
        )
    )
    # Option **without** error handling
    cli.api.evaluate_sync(
        patronus.api_types.EvaluateRequest(
            evaluators=[patronus.api_types.EvaluateEvaluator(evaluator="judge", criteria="patronus:is-code")],
            evaluated_model_output=task_output,
        )
    )


async def async_calls():
    is_code_eval = cli.remote_evaluator("judge", "patronus:is-code")
    # Option with error handling and retries
    await is_code_eval.evaluate(evaluated_model_output=task_output)

    # Option with error handling
    cli.api.evaluate_one_sync(
        patronus.api_types.EvaluateRequest(
            evaluators=[patronus.api_types.EvaluateEvaluator(evaluator="judge", criteria="patronus:is-code")],
            evaluated_model_output=task_output,
        )
    )
    # Option **without** error handling
    cli.api.evaluate_sync(
        patronus.api_types.EvaluateRequest(
            evaluators=[patronus.api_types.EvaluateEvaluator(evaluator="judge", criteria="patronus:is-code")],
            evaluated_model_output=task_output,
        )
    )
