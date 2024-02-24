from typing import List
import numpy as np
import warnings

from overrides import overrides
import numpy
import json

from allennlp.common.util import JsonDict
from allennlp.nn import util
from allennlp.data import Batch
from allennlp.data import DatasetReader
from allennlp.models import Model
from allennlp.predictors.predictor import Predictor

from news_handler.mongo_utils.query_utils import QueryUtils
from news_handler.mongo_utils.mongo_builder import MongoBuilder
from .postprocess import JsonNormalizer

@Predictor.register("dygie")
class DyGIEPredictor(Predictor):
    """
    Predictor for DyGIE model.

    If model was trained on coref, prediction is done on a whole document at
    once. This risks overflowing memory on large documents.
    If the model was trained without coref, prediction is done by sentence.
    """
    def __init__(self, model: Model, dataset_reader: DatasetReader) -> None:
        mongo_builder = MongoBuilder()

        ern_collection = \
            mongo_builder.get_mongodb_collection(collection_name="ERN")

        self.ERN_DB = QueryUtils(ern_collection)

        super().__init__(model, dataset_reader)

    def predict(self, document):
        return self.predict_json({"document": document})


    def predict_tokenized(self, tokenized_document: List[str]) -> JsonDict:
        instance = self._words_list_to_instance(tokenized_document)
        return self.predict_instance(instance)

    @overrides
    def dump_line(self, outputs):
        # Need to override to tell Python how to deal with Numpy ints.
        return json.dumps(outputs, default=int) + "\n"

    # TODO(dwadden) Can this be implemented in `forward_on_instance`  instead?
    @overrides
    def predict_instance(self, instance):
        """
        An instance is an entire document, represented as a list of sentences.
        """
        model = self._model
        cuda_device = model._get_prediction_device()

        # Try to predict this batch.
        try:
            dataset = Batch([instance])
            dataset.index_instances(model.vocab)
            model_input = util.move_to_device(dataset.as_tensor_dict(), cuda_device)
            # print("model_input: ",model_input['metadata'])
            prediction = model.make_output_human_readable(model(**model_input)).to_json()

            # pred_json = {'id':prediction['doc_key'], 'sentences':prediction['sentences'], 'ner':prediction['predicted_ner']
            #             ,'relations':prediction['predicted_relations'], 'events':prediction['predicted_events']}
            post_proces_json=JsonNormalizer(prediction)
            pred_json=post_proces_json.getJson()
            self.ERN_DB.insert(pred_json)

            print("doc inserted DB")

        # If we run out of GPU memory, warn user and indicate that this document failed.
        # This way, prediction doesn't grind to a halt every time we run out of GPU.
        except RuntimeError as err:
            # doc_key, dataset, sentences, message
            metadata = instance["metadata"].metadata
            doc_key = metadata.doc_key
            msg = (f"Encountered a RunTimeError on document {doc_key}. Skipping this example."
                   f" Error message:\n{err.args[0]}.")
            warnings.warn(msg)
            prediction = metadata.to_json()
            prediction["_FAILED_PREDICTION"] = True

        return prediction


