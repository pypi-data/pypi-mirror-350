from patronus.evals import RemoteEvaluator
from patronus.experiments import run_experiment

dataset = [
    {
        "task_output": "A charming two-story farmhouse perches atop a rolling green hillside, surrounded by mature oak trees and flowering wildflowers. The white clapboard exterior gleams in the late afternoon sunlight, while smoke curls gently from the brick chimney. A winding gravel driveway leads up to the wraparound porch, where a wooden rocking chair offers a perfect vantage point to take in the sweeping valley views below.",
        "task_attachments": [
            {
                "media_type": "image/jpeg",
                "url": "https://helpx-prod.scene7.com/is/image/HelpxProd/upload-content-to-adobe-stock_1408x792-1?$pjpeg$&jpegSize=300&wid=1408",
                "usage_type": "evaluated_model_output"
            }
        ],

    }
]


caption_hallucination = RemoteEvaluator("judge-image", "patronus:caption-hallucination")
caption_describes_primary_object = RemoteEvaluator("judge-image", "patronus:caption-describes-primary-object")
caption_describes_non_primary_objects = RemoteEvaluator("judge-image",
                                                                "patronus:caption-describes-non-primary-objects")
caption_mentions_primary_object_location = RemoteEvaluator("judge-image",
                                                                   "patronus:caption-mentions-primary-object-location")
caption_hallucination_strict = RemoteEvaluator("judge-image", "patronus:caption-hallucination-strict")

results = run_experiment(
    project_name="Multimodal Experiments",
    experiment_name="GPT-4o Image Captioning",
    dataset=dataset,
    evaluators=[caption_hallucination],
    tags={"dataset_key": "8233883", "model_key": "gpt-4o",
          "system_prompt": "This is an image for which you need to generate a caption."}
)