Usage Sample
''''''''''''

.. code:: python

        import torch
        from sklearn.model_selection import train_test_split
        from nlpx.tokenize import Tokenizer
        from nlpx.model.classifier import TextCNNClassifier
        from nlpx.model.wrapper import ClassifyModelWrapper
        from nlpx.dataset import TokenDataset, PaddingTokenCollator

        if __name__ == '__main__':
            classes = ['class1', 'class2', 'class3'...]
            texts = [[str],]
            labels = [0, 0, 1, 2, 1...]
            tokenizer = Tokenizer.from_texts(texts, min_freq=5)
            sent = 'I love you'
            tokens = tokenizer.encode(sent, max_length=6)
            # [101, 66, 88, 99, 102, 0]
            sent = tokenizer.decode(tokens)
            # ['<BOS>', 'I', 'love', 'you', '<EOS>', '<PAD>']

            tokens = tokenizer.batch_encode(texts, padding=False)
            X_train, X_test, y_train, y_test = train_test_split(tokens, labels, test_size=0.2)
            train_set = TokenDataset(X_train, y_train)
            val_set = TokenDataset(X_test, y_test)

            model = TextCNNClassifier(embed_dim=128, vocab_size=tokenizer.vocab_size, num_classes=len(classes))
            model_wrapper = ClassifyModelWrapper(model, classes=classes)
            model_wrapper.train(train_set, val_set, show_progress=True, collate_fn=PaddingTokenCollator(tokenizer.pad))

            result = model_wrapper.evaluate(val_set, collate_fn=PaddingTokenCollator(tokenizer.pad))
            # 0.953125

            test_inputs = torch.tensor(test_tokens, dtype=torch.long)
            result = model_wrapper.predict(test_inputs)
            # [0, 1]

            result = model_wrapper.predict_classes(test_inputs)
            # ['class1', 'class2']

            result = model_wrapper.predict_proba(test_inputs)
            # ([0, 1], array([0.99439645, 0.99190724], dtype=float32))

            result = model_wrapper.predict_classes_proba(test_inputs)
            # (['class1', 'class2'], array([0.99439645, 0.99190724], dtype=float32))
