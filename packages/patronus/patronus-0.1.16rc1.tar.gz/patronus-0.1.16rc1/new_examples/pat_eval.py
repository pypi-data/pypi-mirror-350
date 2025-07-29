from patronus import init
from patronus import RemoteEvaluator

init()

check_hallucinates = RemoteEvaluator("lynx", "patronus:hallucination")

resp = check_hallucinates.evaluate(
    task_input="What is the car insurance policy?",
    task_context=(
        """
        To qualify for our car insurance policy, you need a way to show competence 
        in driving which can be accomplished through a valid driver's license. 
        You must have multiple years of experience and cannot be graduating from driving school before or on 2028.
        """
    ),
    task_output="To even qualify for our car insurance policy, you need to have a valid driver's license that expires later than 2028."
)
print(resp.model_dump_json(indent=4))