import pandas as pd

from mgo_ai.mgo_ml_base import MLRegistry
import h2o


class Trainer():
    def __init__(self, db, model_name, model_class, model_category,  data_table_view, exclude_features_from_cb=False, version=1, **kw):
        self.db = db
        self.data_table_view = data_table_view
        self.data = None
        self.model_name = model_name
        if isinstance(model_class, str):
            self.model_class_name = model_class
            self.model_class = getattr(h2o.estimators, model_class)
        else:
            self.model_class_name = model_class.__name__
        self.model_class = model_class
        self.model_category = model_category
        self.version = version
        self.features = None
        self.target = None
        self.exclude_features = exclude_features_from_cb

    def set_model_class(self, model_class):
        if isinstance(model_class, str):
            self.model_class_name = model_class
            self.model_class = getattr(h2o.estimators, model_class)
        else:
            self.model_class_name = model_class.__name__

    def refresh_data(self, exclude_features=None):

        self.data = pd.read_sql(f"select * from {self.data_table_view}", self.db.engine)

        return self

    def train(self,  save=True, version=None, ratios: list=[0.8], seed=42, **training_params):
        try:
            h2o.init()
            if not version:
                version = self.version
            if self.data is None:
                self.refresh_data()
            if not isinstance(self.data, h2o.H2OFrame):
                data = h2o.H2OFrame(self.data)  # H2O can usually infer types well
            else:
                data = self.data
            # Ensure the target variable is a factor (categorical)
            data[self.target] = data[self.target].asfactor()

            # Split data into training and testing sets (80/20 split)
            train, test = data.split_frame(ratios=ratios, seed=seed)
            # Initialize and train the model (Random Forest in this example)

            model_id = f"{self.model_category}_{self.model_name}_{self.model_class_name}_{version}"
            model = self.model_class(
                seed=seed,  # Random seed for reproducibility
                model_id=model_id,
                **training_params
            )
            model.train(x=self.features, y=self.target, training_frame=train)

            # Evaluate model performance on the test set
            performance = model.model_performance(test)
            print(performance)


            # Save the trained model
            model_path = h2o.save_model(model=model, path="./", force=True)
            res = MLRegistry(self.db, foreign=False).set_model(
                   model_id,
                   self.model_name,
                   self.model_category,
                   self.model_class_name,
                   self.data_table_view,
                   version,
                   self.features,
                   self.target,
                   model_path=model_path,
                   performance_metrics=performance,
                   seed=seed,
                   **training_params
            )

            print(f"Model saved to: {model_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
            h2o.cluster().shutdown()
            raise e

        return self





