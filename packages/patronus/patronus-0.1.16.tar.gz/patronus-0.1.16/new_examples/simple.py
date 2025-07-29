import textwrap

from patronus.evals import RemoteEvaluator
from patronus.experiments import run_experiment

dataset = [
    {
        "task_input": "What are the symptoms of diabetes?",
        "task_context": textwrap.dedent("""\
            Common symptoms of diabetes include:
            - Increased thirst and urination
            - Fatigue
            - Blurred vision
            - Unexplained weight loss
            - Slow-healing sores
            - Frequent infections

            Type 1 diabetes symptoms often develop quickly,
            while Type 2 diabetes symptoms may develop gradually or be mild.
            """),
        "gold_answer": textwrap.dedent("""
            Common diabetes symptoms include increased thirst and urination,
            fatigue, blurred vision, unexplained weight loss, slow-healing sores,
            and frequent infections. Type 1 symptoms develop quickly, while 
            Type 2 may develop gradually.
            """)
    },
    {
        "task_input": "What planets are in our solar system?",
        "task_context": textwrap.dedent("""\
            Our solar system contains eight planets:
            - Mercury: closest to the Sun
            - Venus: second planet from the Sun
            - Earth: our home planet
            - Mars: fourth planet from the Sun
            - Jupiter: largest planet
            - Saturn: known for its rings
            - Uranus: ice giant with tilted rotation
            - Neptune: farthest planet from the Sun

            Pluto was reclassified as a dwarf planet in 2006.
            """),
        "gold_answer": textwrap.dedent("""\
            Our solar system has eight planets: Mercury, Venus,
            Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.
            Pluto was reclassified as a dwarf planet in 2006.
            """)
    }
]


def mock_llm_response(row, **kwargs):
    if "diabetes" in row.task_input:
        return textwrap.dedent("""
            Diabetes typically presents with increased thirst and urination,
            fatigue, blurred vision, unexplained weight loss, slow-healing
            wounds, and frequent infections.
            While Type 1 diabetes symptoms tend to appear rapidly,
            Type 2 diabetes may develop more gradually with milder symptoms.
            """)
    elif "planets" in row.task_input:
        return textwrap.dedent("""
            Our solar system consists of eight planets: Mercury, Venus, Earth,
            Mars, Jupiter, Saturn, Uranus, and Neptune. Mercury has virtually
            no atmosphere, while Venus has a thick, toxic atmosphere.
            Earth is the only known planet with life, and Mars has polar ice
            caps. Jupiter has a prominent Great Red Spot, Saturn has beautiful
            rings, Uranus rotates on its side,
            and Neptune experiences the strongest winds in the solar system.
            """)
    else:
        return None


# If you're running the experiment in Jupyter Notebooks please await it (`await run_experiment(...)`)
run_experiment(
    dataset=dataset,
    task=mock_llm_response,
    evaluators=[
        RemoteEvaluator("lynx", "patronus:hallucination"),
        RemoteEvaluator("judge", "patronus:is-concise"),
    ],
    experiment_name="quickstart"
    # This is the default and can be omitted
    # api_key=os.environ.get("PATRONUS_API_KEY"),
)
