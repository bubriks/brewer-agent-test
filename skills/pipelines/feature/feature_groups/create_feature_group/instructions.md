Write a Python script creating a feature group in Hopsworks according to the provided specification.

The script should follow this structure:

```python
# imports

# 1. Load and preprocess data, save the results into prepared_df.
# Include only essential code parts:
# - Data loading
# - Data preprocessing (type conversions, missing values handling, etc.)
# - Feature transformations

# 2. Create the feature group.
project = hopsworks.login()
fs = project.get_feature_store()

new_fg = fs.create_feature_group(
    name="name",
    description="description",
    version=1,
    online_enabled=True,

    features=[
        Feature("f1", description="f1 description", type="int", primary=True),
        Feature("f2", description="f2 description", type="int"),
        # ...
    ],

    # ...
)

new_fg.insert(prepared_df)
```

Here is an example of the feature group creation code section:

```python
import hopsworks
from hsfs.feature import Feature

project = hopsworks.login()
fs = project.get_feature_store()

customers_fg = fs.create_feature_group(
    name="customers",
    description="Customers data including age and postal code",
    version=1,
    online_enabled=True,

    features=[
        Feature("customer_id", description="Unique identifier for each customer.", type="int", primary=True),
        Feature("club_member_status", description="Membership status of the customer in the club.", type="string", partition=True),
        Feature("age", description="Age of the customer.", type="int"),
        Feature("postal_code", description="Postal code associated with the customer's address.", type="string"),
        Feature("date", description="Date of the member status start", type="timestamp"),
    ],

    # If there is an event time feature, you have to specify it here:
    event_time='date',
)

customers_fg.insert(customers_df)
```

Generate code that follows the provided specification.
The code should be production-ready and include proper error handling.

Do not forget to:

- Provide descriptions
- Handle all error cases consistently
- Clear `None` values for the event time, primary key and partition key features
