init()

## 1. Example with one evaluation


@evaluator()
def my_evaluator(a, b):
    # perform eval
    return Evaluation(pass_=True, score=0.77)


@traced()
def func_a():
    my_evaluator(1, 2)


func_a()

## Result:
# Span(func_a)
# +- Log(func_name=foo, args=(), output=None)
# +- Span(my_evaluator)
#    +- Log(log_type=evaluation, body={"a": 1, "b": 2})
#    +- Evaluation(pass=True, score=0.77)


## 2. Example with Patronus client usage

client = Client()


class MyEvaluator(StructureEvaluator):
    def evaluate(self, task_output, gold_answer, **kwargs):
        return task_output.lower().strip() == gold_answer.lower().strip()


client = Client()
client.register_evaluator("my-eval", MyEvaluator())


@traced()
def func_b():
    client.evaluate(evaluators=["my-eval"], task_output=" fOO\t", gold_answer="foo")


func_b()

## Result:
# Span(func_a)
# +- Log(func_name=foo, args=(), output=None)
# +- Span(my-eval)
#    +- Log(log_type=evaluation, body={"task_output": " fOO\t, "gold_answer": "foo"})
#    +- Evaluation(pass=True)


## 3. Ex. with evaluation bundle


@traced()
def func_c():
    client.evaluate(evaluators=["my-eval", ("judge", "patronus:fuzzy-match")], task_output=" fOO\t", gold_answer="foo")


## Result:
# Span(func_a)
# +- Log(func_name=foo, args=(), output=None)
# +- Span(Evaluation bundle)
#    +- Log(log_type=evaluation, body={"task_output": " fOO\t, "gold_answer": "foo"})
#    +- Span(my-eval)
#       +- Evaluation(pass=True)
#    +- Span(judge-small-2024-08-11:patronus:fuzzy-match)
#       +- Evaluation(pass=True)
