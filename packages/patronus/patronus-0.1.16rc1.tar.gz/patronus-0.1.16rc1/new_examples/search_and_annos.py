import math

import time

import itertools

import logging

import patronus
from patronus import get_api_client
from patronus.api import api_types
from patronus.datasets import Row
from patronus.evals import evaluator, RemoteEvaluator
from patronus.experiments import FuncEvaluatorAdapter, TaskResult, run_experiment

patronus_root_logger = logging.getLogger("patronus")
patronus_root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)-8s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)
patronus_root_logger.addHandler(console_handler)

patronus.init()

log = patronus.get_logger()

api_client = get_api_client()

ANNO_CRITERIA_NAME = "is-correct"

log.info("Listing annotation criteria...")
anno_ls = api_client.list_annotation_criteria_sync().annotation_criteria

anno_exists = False
anno = None
for anno in anno_ls:
    if anno.name == ANNO_CRITERIA_NAME:
        anno_exists = True
        anno = anno

if anno_exists:
    log.info(f"Annotation criteria {ANNO_CRITERIA_NAME!r} exists")
else:
    log.info(f"Annotation criteria does not {ANNO_CRITERIA_NAME!r} exists. Creating...")
    project = api_client.create_project_sync(api_types.CreateProjectRequest(name="Global"))
    anno = api_client.create_annotation_criteria_sync(api_types.CreateAnnotationCriteriaRequest(
        project_id=project.id,
        name=ANNO_CRITERIA_NAME,
        description=None,
        annotation_type=api_types.AnnotationType.binary,
        categories=None,
    )).annotation_criteria

log.info(f"Annotation Criteria ID: {anno.id}")


def my_task(row: Row, **kwargs):
    return f"{row.task_input} World"


# Reference remote Judge Patronus Evaluator with is-concise criteria.
# This evaluator runs remotely on Patronus infrastructure.
is_concise = RemoteEvaluator("judge", "patronus:is-concise")


@evaluator()
def exact_match(row: Row, task_result: TaskResult, **kwargs):
    log.info(f"{task_result.output=}  :: {row.task_output=}")
    return task_result.output == row.task_output


result = run_experiment(
    project_name="Tutorial Project",
    dataset=[
        {
            "task_input": "Hello",
            "gold_answer": "Hello World",
        },
        {
            "task_input": "Bon",
            "gold_answer": "Bon Dia",
        },
    ],
    task=my_task,
    evaluators=[is_concise, FuncEvaluatorAdapter(exact_match)],
)

exp_id = result.experiment.id

log.info("Searching logs...")

logs = []
for c in itertools.count():
    search_logs_resp = api_client.search_logs_sync(
        api_types.SearchLogsRequest(filters=[
            api_types.SearchLogsFilter(
                field="log_attributes['pat.experiment.id']",
                op="eq",
                value=exp_id
            ),
            api_types.SearchLogsFilter(
                field="log_attributes['pat.log.type']",
                op="eq",
                value="eval"
            ),
        ])
    )
    logs = search_logs_resp.logs
    log.info(f"Found {len(search_logs_resp.logs)} logs")
    if len(search_logs_resp.logs) > 0 or c > 10:
        break

    sleep_for = math.pow(c+1, 2)
    time.sleep(sleep_for)
    print(f"Waiting for {sleep_for}s")

log_ids = set()
logs2 = []

for lg in logs:
    if lg.log_attributes["pat.log.id"] not in log_ids:
        log_ids.add(lg.log_attributes["pat.log.id"])
        logs2.append(lg)

log.info(f"deduped logs: {len(logs2)}")

for log in logs2:
    print(f"Log: {log.body}")

    ans = None
    while True:
        user_input = input(">>> Is this correct (yes/no)? ")
        user_input = user_input.strip().lower()
        if user_input == "yes":
            ans = True
        elif user_input == "no":
            ans = False

        if ans is not None:
            break
        else:
            print("Invalid answer.")

        resp = api_client.annotate(api_types.AnnotateRequest(
            annotation_criteria_id=anno.id,
            log_id=log.log_attributes["pat.log.id"],
            value_pass=ans,
        ))
        print(resp)
        print("Annotation given")
