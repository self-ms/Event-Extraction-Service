import time

class JsonNormalizer:

    def __init__(self, orgin):
        self.orgin= orgin

    def getJson(self):

        sentences_len= len(self.orgin["sentences"])
        doc_id=self.orgin["doc_key"]
        doc_tokens= []

        sentences= []
        ner_pred= []
        rel_pred= []
        event_pred= []

        doc_len=0

        for idx in range(sentences_len):

            tokens= self.orgin["sentences"][idx]

            sentences.append({"id": f"{doc_id}_{idx}" , "tokens":tokens, "start":doc_len, "end":doc_len+len(tokens)-1})

            ner_pred.append(self.ner(self.orgin["predicted_ner"][idx]))

            rel_pred= rel_pred + self.rel(self.orgin["predicted_relations"][idx])

            event_pred = event_pred + self.event(self.orgin["predicted_events"][idx], idx)

            doc_tokens=doc_tokens + tokens

            doc_len= doc_len+len(tokens)

        return {"id":doc_id, "doc_tokens":doc_tokens, "create":time.time(), "sentences":sentences
                , "events":event_pred, "ner":ner_pred, "relations":rel_pred}

    def ner(self,ner_org):

        ner_norm=[]

        for ner in ner_org:
            start=ner[0]
            end=ner[1] + 1
            typ=ner[2]
            confidence=ner[3]
            softmax=ner[4]

            ner_norm.append({"start":start, "end":end, "type":typ, "confidence":confidence, "softmax":softmax})

        return ner_norm

    def rel(self,rel_org):

        rel_norm=[]

        for rel in rel_org:

            source_start=rel[0]
            source_end= rel[1] + 1
            destination_start= rel[2]
            destination_end= rel[3] + 1
            typ= rel[4]
            confidence=rel[5]
            softmax=rel[6]

            rel_norm.append({"source":{"start":source_start,"end":source_end}, "destination":{"start":destination_start,"end":destination_end}, "type":typ, "confidence":confidence, "softmax":softmax})

        return rel_norm

    def event(self,event_org, set_idx):
        event_norm=[]
        for event in event_org:
            trigger= self.eventTrig(event[0], set_idx)
            argument= self.eventArg(event[1:])

            event_norm.append({"trigger":trigger, "argument":argument})

        return event_norm

    def eventArg(self,arg_org):

        arg_norm=[]

        for arg in arg_org:

            start=arg[0]
            end=arg[1]+1
            role=arg[2]
            confidence=arg[3]
            softmax=arg[4]

            arg_norm.append({"start":start, "end":end, "role":role, "confidence":confidence, "softmax":softmax})

        return arg_norm

    def eventTrig(self,trig_org, set_idx):

        return {"start":trig_org[0], "end":trig_org[0]+1, "type":trig_org[1], "confidence":trig_org[2], "softmax":trig_org[3], "sentence_index":set_idx}

