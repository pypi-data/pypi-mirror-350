class DefaultFormatter:
    @staticmethod
    def format(data, h2o_model):
        drop_cols = ['declined', 'mid_id', 'order_id', 'parent_processor', 'project', 'time_stamp']
        data = data.drop(columns=drop_cols, errors='ignore')  # errors='ignore' prevents error if column doesn't exist
        lag_cols = [col for col in data.columns if "approval" in col.lower()]
        data[lag_cols] = (data[lag_cols] * 100).round(0).astype(int)
        if h2o_model:
            features = h2o_model.features
            target = h2o_model.targets
        else:
            features = list(set(data.columns) - set(['approved']))
            target = 'approved'
        return data, features, target


class V2Formatter:
    @staticmethod
    def format(data, h2o_model):
        lag_cols = ['order_total']
        data[lag_cols] = (data[lag_cols] * 100).round(0).astype(int)
        if h2o_model:
            features = h2o_model.features
            target = h2o_model.targets
        else:
            features = list(set(['cc_type', 'order_total', 'campaign_class', 'processor', 'iin']) - set(['approved']))
            target = 'approved'
        return data, features, target


class V3Formatter:
    @staticmethod
    def format(data, h2o_model):
        drop_cols = ['declined', 'mid_id', 'order_id', 'parent_processor', 'project', 'time_stamp']
        data = data.drop(columns=drop_cols, errors='ignore')  # errors='ignore' prevents error if column doesn't exist
        lag_cols = [col for col in data.columns if "approval" in col.lower()] + ['order_total']
        data[lag_cols] = (data[lag_cols] * 100).round(0).astype(int)
        if h2o_model:
            features = h2o_model.features
            target = h2o_model.targets
        else:
            features = list(set(data.columns) - set(['approved']))
            target = 'approved'
        return data, features, target


VERSIONS = {
    1: DefaultFormatter,
    2: V2Formatter,
    3: V3Formatter
}